import streamlit as st
import pandas as pd
import time
import json


st.header("수학동아리 :blue[방탈출]")

with open("./data.json","r",encoding="utf8") as f:
    data = json.load(f)

problem, story = st.tabs(["Problem", "Story"])

def save(): 
    with open("./data.json","w",encoding="UTF-8") as f:
        json.dump(data,f,ensure_ascii=False, indent=4)
    
with story:
    if "StoryText" not in st.session_state:
        st.session_state['StoryText'] = ""
    story_text = data["Story"]
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
                    data["Story"] = st.session_state['StoryText']
                    save()
                    st.success("성공적으로 수정되었습니다",icon="✅")
                    
with problem:
    i = 0
    with st.expander("문제  ⤵"):
        for row in data["Problem"].keys():
            if st.button(f"{row}"):
                with st.container():
                    try: 
                        data_ = {"문제 내용": data["Problem"][row]["ProblemContent"],"답 형식":data["Problem"][row]["AnswerType"],"예시":data["Problem"][row]["Example"]}
                        data__ = pd.Series(data_)
                        st.write(data__)
                    except:
                        data_ = {"문제 내용": data["Problem"][row]["ProblemContent"],"답 형식":data["Problem"][row]["AnswerType"]}
                        data__ = pd.Series(data_)
                        st.write(data__)
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
                        data["Problem"][st.session_state['ProblemName']] = {
                                "ProblemContent" : st.session_state['ProblemContent'], 
                                    "AnswerType" : st.session_state['AnswerType'],
                                    "Example" : st.session_state['Example']
                            }
                        save()
                        st.success("성공적으로 추가되었습니다",icon="✅")