import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import gspread 
import time
from streamlit_extras.stoggle import stoggle

# Create a connection object.
conn = st.connection("gsheets", GSheetsConnection)

st.header("수학동아리 :blue[방탈출]")

df = conn.read(
        worksheet="시트1",
        ttl="30m",
        usecols=[0,1,2,3,4],
        nrows=100
    )

problem, story = st.tabs(["Problem", "Story"])

with story:
    if "StoryText" not in st.session_state:
        st.session_state['StoryText'] = ""
    for row in df.itertuples():
        story_text = row.Story
        break
    with st.expander("스토리 내용"):
        st.write(story_text)
    with st.expander("스토리 수정하기"):
        with st.form("스토리 수정하기"):
            with st.container():
                st.session_state['StoryText'] = st.text_area("스토리",key="story",value="")
                Story_submitted = st.form_submit_button("스토리 수정하기")

            if Story_submitted:
                with st.spinner("Loading..."):
                    time.sleep(1)
                if st.session_state['StoryText'] == "":
                    st.error("스토리를 입력해 주세요")
                else:
                    df.itertuples().Story[0] = st.session_state['StoryText']
                    conn.update(worksheet="시트1",data=df)
                    st.success("성공적으로 수정되었습니다",icon="✅")
                    
with problem:
    i = 0
    with st.expander("문제  ⤵"):
        for row in df.itertuples():
            if pd.isnull(row.ProblemName):
                break
            if st.button(f"{row.ProblemName}"):
                with st.container():
                    if pd.isnull(row.Example):
                        data_ = {"문제 내용": row.ProblemContent,"답 형식":row.AnswerType}
                        data = pd.Series(data_)
                        st.write(data)
                    else:
                        data_ = {"문제 내용": row.ProblemContent,"답 형식":row.AnswerType,"예시":row.Example}
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
                Problem_submitted = st.form_submit_button("문제 추가하기")

                if Problem_submitted:
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
