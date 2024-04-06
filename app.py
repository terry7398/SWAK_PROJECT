import streamlit as st
import pandas as pd
import time
import json
import toml
from streamlit_gsheets import GSheetsConnection

st.header("수학동아리 :blue[방탈출]")

with open("./data.json","r",encoding="utf-8") as f:
    a_Data = json.load(f)


if st.button("Refresh"):
    st.rerun()

problem, story, comment,Resource,development = st.tabs(["Problem", "Story","Comment","Resource","Development"])

def load_ChatData():
    with open("./chat_data.json", encoding="utf-8") as f:
        chatData = json.load(f)
    return chatData

def save(choice, data_ = a_Data):
    if choice == 1:
        with open("./data.json","w",encoding="UTF-8") as f:
            json.dump(data_,f,ensure_ascii=False, indent=4)
    elif choice == 2:
        with open("./chat_data.json","w", encoding="utf-8") as f:
            json.dump(data_,f,ensure_ascii=False, indent=4)

import os

# 파일 업로드 함수
def save_uploaded_file(directory, file):
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(os.path.join(directory, file.name), 'wb') as f:
        f.write(file.getbuffer())
    return st.success('파일 업로드 성공')

chat_load = False
    
with story:
    chat_load = False
    if "StoryText" not in st.session_state:
        st.session_state['StoryText'] = ""
    story_text = a_Data['Story']
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
                    a_Data["Story"] = st.session_state['StoryText']
                    save(1)
                    st.success("성공적으로 수정되었습니다",icon="✅")
                    st.rerun()
                    
with problem:
    chat_load = False
    i = 0
    with st.expander("문제  ⤵"):
        for row in a_Data["Problem"].keys():
            if st.button(f"{row}"):
                with st.container():
                    try: 
                        data_ = {"문제 내용": a_Data["Problem"][row]["ProblemContent"],"답 형식":a_Data["Problem"][row]["AnswerType"],"예시":a_Data["Problem"][row]["Example"]}
                        data__ = pd.Series(data_)
                        st.write(data__)
                    except:
                        data_ = {"문제 내용": a_Data["Problem"][row]["ProblemContent"],"답 형식":a_Data["Problem"][row]["AnswerType"]}
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
                        a_Data["Problem"][st.session_state['ProblemName']] = {
                                "ProblemContent" : st.session_state['ProblemContent'], 
                                    "AnswerType" : st.session_state['AnswerType'],
                                    "Example" : st.session_state['Example']
                            }
                        save(1)
                        st.success("성공적으로 추가되었습니다",icon="✅")
                        st.rerun()

    with st.expander("데이터 다운로드"):
        with open("./data.json",encoding="utf-8") as f:
            st.download_button(
                    label="Download JSON Data File",
                    data=f,
                    file_name="data.json",
            )
        with open("./chat_data.json",encoding="utf-8") as f:
            st.download_button(
                label="Download JSON Chat Data File",
                data=f,
                file_name="chat_data.json",
            )
        
            

with comment:
    chat_data = load_ChatData()
    messages = st.container(height=500)
    if chat_load == False:
        for i in chat_data["chat"]:
            messages.chat_message("user").write(i)
        chat_load = True
    if chat := st.chat_input("메시지를 입력하세요"):
        if chat[0] == "!":
            try:
                chat_data["chat"].remove(chat[1:])
                save(2,data_=chat_data)
                st.rerun()
            except Exception as e:
                st.error(f"{chat}이 리스트에서 삭제할 수 없습니다\n\n Error:{e}")
        else:
            chat_data["chat"].append(chat)
            messages.chat_message("user").write(chat)
            save(2,data_=chat_data)     
with Resource:
    with st.expander("이미지 업로드"):
        img_file = st.file_uploader('이미지를 업로드 하세요.', type=['png', 'jpg'])
    
    if img_file is not None:
        save_uploaded_file("source",img_file)
    with st.expander("이미지"):
        file_names = os.listdir("./source")
        for filename in file_names:
            st.write(filename[:-4])
            st.image("./source/"+filename)

with development:
    if "Password" not in st.session_state:
        st.session_state['Password'] = ""

    with open("./.streamlit/secrets.toml", "r",encoding="utf-8") as f:
        secrets = toml.load(f)

    st.session_state['Password'] = st.text_input("password",value="")
    if st.button("Google Spreadsheet save"):
        if st.session_state['Password'] == secrets['Development']['Password']:
            with st.spinner("Loading..."):
                time.sleep(1)
            with open("./data.json","r",encoding="utf-8") as f:
                a_DataRaw = f.read()
            with open("./chat_data.json", encoding="utf-8") as f:
                ChatDataRaw = f.read()    
            conn = st.connection("gsheets", type=GSheetsConnection)
            sheet_data = {"Chatdata" : ChatDataRaw, "AData" : a_DataRaw}
            conn.update(worksheet="시트2", data=sheet_data)
            st.success("성공적으로 저장되었습니다",icon="✅")
