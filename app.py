import streamlit as st
import time
from streamlit_gsheets import GSheetsConnection
import json
import toml

class app():
    def __init__(self):

        #페이지 설정
        st.set_page_config(page_title="SWAK_EscapeReservation")

        #헤더 설정
        st.header("수학동아리 :blue[방탈출] 예약")
        self.reservation_, current_reservation = st.tabs(["예약하기", "예약 상황 확인하기"]) 
        #변수 설정
        self.dates = [f"5월 {i}일" for i in range(27,32)]
        self.slots = ["아침","점심"]
        self.studentNumber = [f"{i}명" for i in range(4,6)]
        self.data = None
        self.load_data()
        self.save()
        for i in range(1,6):
            if f"Student{i}" not in st.session_state:
                st.session_state[f'Student{i}'] = ""
        with open("./.streamlit/secrets.toml", "r",encoding="utf-8") as f:
            self.secrets = toml.load(f)

    #파일 불러오기
    def load_data(self):
        with open("./data.json",encoding="utf-8") as f:
            self.data = json.load(f)        

    def save(self):
        with open("./data.json","w",encoding="utf-8") as f:
            json.dump(self.data,f,ensure_ascii=False,indent=4)
        

    def reservation(self):
    #예약 폼 설정
        with self.reservation_:
            st.subheader("1. :blue[날짜, 시간, 학생 수]를 선택합니다")
            st.subheader("2. 학생의 :blue[학번과 이름]을 입력합니다")
            st.subheader("3. :red[예약하기] 버튼을 눌러 예약합니다")
            with st.form("예약하기"):
                #컨테이너 설정
                with st.container():
                    date = st.selectbox("날짜를 선택하세요",self.dates)
                    slot = st.selectbox("시간을 선택하세요",self.slots)
                    studentNum = st.selectbox("학생 수를 선택하세요",self.studentNumber)
                    self.load_data()
                    for i in range(1,6):
                        st.session_state[f'Student{i}'] = st.text_input(f"{i}번 학생의 학번과 이름을 입력하세요")
                    reservation_submitted = st.form_submit_button("예약하기")
                    
                if reservation_submitted:
                    is_error = False
                    #학생 이름을 모두 입력했는지 검사
                    for i in range(1,int(studentNum[0]) + 1):
                        if st.session_state[f'Student{i}'] is None or st.session_state[f'Student{i}'] == "":
                            st.error("등록 후 학생 이름을 모두 입력해 주세요.")
                            is_error = True
                            break
                        else: 
                            continue
                    try:
                        if is_error == False and self.data["날짜"][slot][self.data["날짜"][slot].index(date)] is not None:
                            #저장을 위한 변수 생성
                            studentsData = []
                            students = [st.session_state[f'Student{i}'] for i in range(1,int(studentNum[0]) + 1)]
                            try:
                                for i in range(0,int(studentNum[0])):
                                    studentsData.append({str(students[i][:5]) : students[i][5:]})
                            except:
                                st.error("학번과 이름을 모두 입력해 주세요.")
                                is_error = True

                            #학생중 이미 다른 날짜에 예약했는지 검사
                            if is_error == False:
                                for student in studentsData:
                                    for i in self.data["신청"]["아침"]:
                                        if student in i["students"]:
                                            st.error(f"{student.values()}님이 이미 예약했습니다")
                                            is_error = True
                                    for i in self.data["신청"]["점심"]:
                                        if student in i["students"]:
                                            st.error(f"{str(student.values())[13:-3]}님이 이미 예약했습니다")
                                            is_error = True
                                #저장
                                if is_error == False:
                                    self.data["날짜"][slot].remove(date)
                                    data = {"date" : date, 
                                            "studentNum" : studentNum, 
                                            "students" : studentsData}
                                    self.data["신청"][slot].append(data)
                                    st.success("예약이 완료되었습니다.",icon="✅")
                                    self.save() 
                                    conn = st.connection("gsheets", type=GSheetsConnection)
                                    sheet_data = {"Data" : data}
                                    conn.update(worksheet="시트1", data=sheet_data)
                    except:
                        st.error("이미 예약된 날짜입니다.")

app = app()                
app.reservation()