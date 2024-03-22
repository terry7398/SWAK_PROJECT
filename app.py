import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import gspread
import gspread 
import time

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

st.header("수학동아리 :blue[방탈출] 문제")

df = conn.read(
        worksheet="시트1",
        ttl="30s",
        usecols=[0,1,2,3],
        nrows=100
    )

i = 0
with st.expander("문제  ⤵"):
    for row in df.itertuples():
        if pd.isnull(row.ProblemName):
            break
        if st.button(f"{row.ProblemName}"):
            with st.container():
                data_ = {"문제내용": row.ProblemContent,"답 형식":row.AnswerType}
                data = pd.Series(data_)
                st.write(data)
        i+=1

if "ProblemName" not in st.session_state:
    st.session_state['ProblemName'] = ""
if "AnswerType" not in st.session_state:
    st.session_state['AnswerType'] = ""
if "Example" not in st.session_state:
    st.session_state['Example'] = ""
if "ProblemContent" not in st.session_state:
    st.session_state['ProblemContent'] = ""

with st.expander("문제 추가하기"):
    with st.form("AddProblem"):
        with st.container():
            st.session_state['ProblemName'] = st.text_input("문제 이름",key="name",value="")
            st.session_state['ProblemContent'] = st.text_input("문제 내용",key="content",value="")
            st.session_state['AnswerType'] = st.text_input("답 형식",key="type",value="")
            st.session_state['Example'] = st.text_input("예시",key="ex",value="")
            submitted = st.form_submit_button("문제 추가하기")

            if submitted:
                with st.spinner("Loading..."):
                    time.sleep(1)
                if st.session_state['AnswerType'] == "" or st.session_state['ProblemName'] == "" or st.session_state['ProblemContent'] == "":
                    st.error("문제를 입력해 주세요")
                else:
                    data_= {"ProblemName" : st.session_state['ProblemName'],
                            "ProblemContent" : st.session_state['ProblemContent'], 
                            "AnswerType" : st.session_state['AnswerType'],
                            "Example" : st.session_state['Example']}
                    data = pd.Series(data_)
                    df.loc[i,:] = data
                    conn.update(worksheet="시트1",data=df)
                    st.success("성공적으로 추가되었습니다",icon="✅")


