import streamlit as st
import time
from streamlit_gsheets import GSheetsConnection
import json
import toml
from streamlit import runtime
from streamlit.runtime.scriptrunner import get_script_run_ctx

class app():
    def __init__(self):

        #페이지 설정
        st.set_page_config(page_title="SWAK_EscapeReservation")

        #헤더 설정
        st.header("수학동아리 :blue[방탈출] 예약")

        #새로고침 버튼
        if st.button("새로고침"):
            st.rerun()

        #탭 설정
        self.reservation_, self.current_reservation = st.tabs(["예약하기", "예약 상황 확인하기"]) 

        #변수 설정
        self.dates = [f"5월 {i}일" for i in range(27,32)]
        self.slots = ["아침","점심"]
        self.studentNumber = [f"{i}명" for i in range(4,6)]
        self.data = None
        self.ip = None
        self.load_ip()
        self.load_data()
        for i in range(1,6):
            if f"Student{i}" not in st.session_state:
                st.session_state[f'Student{i}'] = ""
        with open("./.streamlit/secrets.toml", "r",encoding="utf-8") as f:
            self.secrets = toml.load(f)

    #파일 불러오기
    def load_data(self):
        with open("./data.json",encoding="utf-8") as f:
            self.data = json.load(f)      
    def load_ip(self):
        with open("./ip.json",encoding="utf-8") as f:
            self.ip = json.load(f)

    #ip추출
    @staticmethod
    def getRemoteIp() -> str:
        try:
            ctx = get_script_run_ctx()
            if ctx is None:
                return None

            session_info = runtime.get_instance().get_client(ctx.session_id)
            if session_info is None:
                return None
        except:
            return None
        return session_info

    #학번 검사
    @staticmethod
    def CheckStudentId(students):
        try:
            Num = [str(i) for i in range(10)]
            is_error = False
            for student in students:
                if is_error == False:
                    for i in student[:5]:
                        if i not in Num:
                            st.error("학번과 이름을 모두 입력해 주세요.")
                            is_error = True
                            break
            if is_error == False:
                return True
            else:
                return False
        except:
            return False

    #로컬 파일 저장
    def saveData(self):
        with open("./data.json","w",encoding="utf-8") as f:
            json.dump(self.data,f,ensure_ascii=False,indent=4)
    def saveIpData(self):
        with open("./ip.json","w",encoding="utf-8") as f:
            json.dump(self.ip,f,ensure_ascii=False,indent=4)
        self.saveInfoToGoogleSP()

    #구글 스프레드시트 저장
    def saveGoogleSP(self):
        conn = st.connection("gsheets", type=GSheetsConnection)
        sheet_data = {"Data" : self.data}
        conn.update(worksheet="시트1", data=sheet_data)
    def saveInfoToGoogleSP(self):
        conn = st.connection("gsheets", type=GSheetsConnection)
        sheet_data = {"Data" : self.ip}
        conn.update(worksheet="시트2", data=sheet_data)
        
    #비밀번호 검사
    def checkPassword(self,n,method):
        # n : key number
        # method : 1 = confirm, 2 = delete
        if method == 1:
            with st.popover("Confirm"):
                ps = st.text_input("비밀번호를 입력하세요",key=f"passwordInput{n}",type="password")
                if st.button("Confirm",key=f"confirm{n}"):
                    if ps == self.secrets["Password"]["confirmPassword"]:
                        st.success("성공적으로 저장되었습니다",icon="✅")
                        return True
                    else:
                        st.error("비밀번호가 틀렸습니다.")
                        return False
        elif method == 2:
            with st.popover("Delete"):     
                ps = st.text_input("비밀번호를 입력하세요",key=f"passwordInput{n}",type="password")
                if st.button("Delete",key=f"confirm{n}"):
                    if ps == self.secrets["Password"]["confirmPassword"]:
                        st.success("성공적으로 삭제되었습니다",icon="✅")
                        return True
                    else:
                        st.error("비밀번호가 틀렸습니다.")
                        return False

    #예약 허락
    def confirmReservation(self,n,p):
        if self.checkPassword(n,p):
            self.saveGoogleSP()

    #삭제 허락                  
    def deleteReservation(self,n,p,slot,date):
        if self.checkPassword(n,p):
            if slot == 1:
                for i in range(len(self.data["신청"]["아침"])):
                    if self.data["신청"]["아침"][i]["date"] == date:
                        del self.data["신청"]["아침"][i]
                        self.data["날짜"]["아침"].append(date)
                        self.saveData()
                        self.saveGoogleSP()
            elif slot == 2:
                for i in range(len(self.data["신청"]["점심"])):
                    if self.data["신청"]["점심"][i]["date"] == date:
                        del self.data["신청"]["점심"][i]
                        self.data["날짜"]["점심"].append(date)
                        self.saveData()
                        self.saveGoogleSP()

    #예약 상황 확인하기
    def currentReservation(self):
        self.load_data()
        with self.current_reservation:
            with st.container():
                st.subheader(":blue[아침] (7시 53분~)")
                l = 1
                o = 100
                for i in range(5):
                    is_reservated = False
                    date = self.data["일정"]["아침"][i]
                    for k in self.data["신청"]["아침"]:
                        if k["date"] == date:
                            is_reservated = True
                    if is_reservated:
                        with st.expander(self.data["일정"]["아침"][i] + "   :red[예약됨]"):
                            date = self.data["일정"]["아침"][i]
                            
                            for i in self.data["신청"]["아침"]:
                                if i["date"] == date:
                                    st.write("학생 수 : "+i["studentNum"])
                                    studentId = []
                                    for key in i["students"]:
                                        num = [int(ke) for ke in key.keys()]
                                        studentId.append(int(num[0]))
                                    index = 0
                                    for k in studentId:
                                        st.write(k ," : " + i["students"][index][str(k)])
                                        index += 1
                                    self.confirmReservation(l,1)
                                    self.deleteReservation(o,2,1,date)
                                    l += 1
                                    o += 1

                    else:
                        with st.expander(self.data["일정"]["아침"][i] + " :blue[예약가능]"):
                            st.write("")

            with st.container():
                st.subheader(":blue[점심] (12시 37분~)")
                l = 1000
                o = 10000
                for i in range(5):
                    is_reservated = False
                    date = self.data["일정"]["점심"][i]
                    for k in self.data["신청"]["점심"]:
                        if k["date"] == date:
                            is_reservated = True
                    if is_reservated:
                        with st.expander(self.data["일정"]["점심"][i] + "   :red[예약됨]"):
                            date = self.data["일정"]["점심"][i]
                            for i in self.data["신청"]["점심"]:  
                                if i["date"] == date:
                                    st.write("학생 수 : "+i["studentNum"])
                                    studentId = []
                                    for key in i["students"]:
                                        num = [int(ke) for ke in key.keys()]
                                        studentId.append(int(num[0]))
                                    index = 0
                                    for k in studentId:
                                        st.write(k ," : " + i["students"][index][str(k)])
                                        index += 1
                                    self.confirmReservation(l,1)
                                    self.deleteReservation(o,2,2,date)
                                    l += 1
                                    o += 1
                    else:
                        with st.expander(self.data["일정"]["점심"][i] + " :blue[예약가능]"):
                            st.write("")        

    #예약하기
    def reservation(self):
    #예약 폼 설정
        with self.reservation_:
            with st.container(height=150):
                st.write("1. :blue[날짜, 시간, 학생 수]를 선택합니다")
                st.write("2. 학생의 :blue[학번과 이름]을 입력합니다")
                st.write("3. :red[예약하기] 버튼을 눌러 예약합니다")
            with st.form("예약하기"):
                #컨테이너 설정
                with st.container():
                    date = st.selectbox("날짜를 선택하세요",self.dates)
                    slot = st.selectbox("시간을 선택하세요",self.slots)
                    studentNum = st.selectbox("학생 수를 선택하세요",self.studentNumber)
                    self.load_data()
                    st.write(":red[학생 수에 맞게 학번과 이름을 입력해 주세요]")
                    st.session_state[f'Student{1}'] = st.text_input(f"{1}번 학생의 학번과 이름을 입력하세요 (ex:10101홍길동)",max_chars=9)
                    for i in range(2,6):
                        st.session_state[f'Student{i}'] = st.text_input(f"{i}번 학생의 학번과 이름을 입력하세요",max_chars=9)
                    reservation_submitted = st.form_submit_button("예약하기")
                    
                if reservation_submitted:
                    is_error = False
                    #학생 이름을 모두 입력했는지 검사
                    for i in range(1,int(studentNum[0]) + 1):
                        if st.session_state[f'Student{i}'] is None or st.session_state[f'Student{i}'] == "":
                            st.error("학생 이름을 모두 입력해 주세요.")
                            is_error = True
                            break
                        else: 
                            continue
                    try:
                        if is_error == False and self.data["날짜"][slot][self.data["날짜"][slot].index(date)] is not None:
                            #저장을 위한 변수 생성
                            studentsData = []
                            studentsId = []
                            students = [st.session_state[f'Student{i}'] for i in range(1,int(studentNum[0]) + 1)]
                            try:
                                if self.CheckStudentId(students):
                                    for i in range(0,int(studentNum[0])):
                                        if len(students[i]) < 7 or len(students[i]) > 9:
                                            is_error = True
                                            st.error("이름을 올바르게 입력해 주세요")
                                            break
                                else:
                                    is_error = True
                                    st.error("학번과 이름을 모두 입력해 주세요.")
                                if is_error == False:
                                    for i in range(0,int(studentNum[0])):
                                        studentsData.append({students[i][:5] : students[i][5:]})
                                        studentsId.append(students[i][:5])

                            except:
                                st.error("학번과 이름을 모두 입력해 주세요.")
                                is_error = True

                            #학생중 이미 다른 날짜에 예약했는지 검사
                            if is_error == False:
                                for student in studentsData:
                                    for i in self.data["신청"]["아침"]:
                                        if student in i["students"]:
                                            duplicatedStudent = student.values()
                                            st.error(f"{duplicatedStudent}님이 이미 예약했습니다")
                                            is_error = True
                                    for i in self.data["신청"]["점심"]:
                                        if student in i["students"]:
                                            duplicatedStudent = student.values()
                                            st.error(f"{duplicatedStudent}님이 이미 예약했습니다")
                                            is_error = True
                                if is_error == False:
                                    if len(studentsId) != len(set(studentsId)):
                                        st.error("중복된 학번이 있습니다.")
                                        is_error = True
                                        
                                    #저장
                                    if is_error == False:
                                        ip = str(self.getRemoteIp())
                                        if ip in self.ip["ip"] and ip != None:
                                            is_error = True
                                            st.error("이미 예약했습니다 다른 학생이 예약해 주세요")
                                        if ip == None:
                                            is_error = True
                                            st.error("에러발생 다시 시도해 주세요")
                                        if is_error == False:
                                            self.data["날짜"][slot].remove(date)
                                            data = {"date" : date,
                                                "studentNum" : studentNum,
                                                "students" : studentsData}  
                                            self.data["신청"][slot].append(data)
                                            self.ip["ip"].append(ip)
                                            st.success("예약이 완료되었습니다.",icon="✅")
                                            self.saveData()
                                            self.saveIpData()
                    except:
                         st.error("예약에 실패했습니다. 이미 예약된 날짜인지 확인해 주세요")

app = app()                
app.reservation()
app.currentReservation()