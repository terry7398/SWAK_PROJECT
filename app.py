import streamlit as st
from streamlit_gsheets import GSheetsConnection
import json
import toml
from streamlit.web.server.websocket_headers import _get_websocket_headers

class app():
    #초기화
    def __init__(self):
        #페이지 설정
        st.set_page_config(page_title="SWAK_EscapeReservation",layout='wide')
        
        #헤더 설정
        st.header("난우중학교 :blue[솩] 동아리")
        st.header(":lock: :blue[솩  이스케이프 3기] 예약",divider="rainbow")

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
        self.admin = None
        self.loadIP()
        self.loadData()
        for i in range(1,6):
            if f"Student{i}" not in st.session_state:
                st.session_state[f'Student{i}'] = ""
        with open("./.streamlit/secrets.toml", "r",encoding="utf-8") as f:
            self.secrets = toml.load(f) 
    #파일 불러오기
    def loadData(self):
        with open("./data.json",encoding="utf-8") as f:
            self.data = json.load(f)      
    def loadIP(self):
        with open("./ip.json",encoding="utf-8") as f:
            self.ip = json.load(f)
    def loadDataFromGoogleSP(self):
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(
            ttl="1s",
            worksheet="시트1",
            usecols=[0],
            nrows=2,
        )
        self.data["날짜"] = eval(df["Data"][0])
        self.data["신청"] = eval(df["Data"][1])
        self.saveData()
        df = conn.read(
            ttl="1s",
            worksheet="시트2",
            usecols=[0],
            nrows=1,
        )
        self.ip["headers"] = eval(df["Data"][0])
        self.saveIP()
        st.success("성공적으로 불러왔습니다",icon="✅")
    @staticmethod
    def getHeader():
        headers = _get_websocket_headers()
        if headers is None:
            return {}
        return headers    
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
    def saveIP(self):
        with open("./ip.json","w",encoding="utf-8") as f:
            json.dump(self.ip,f,ensure_ascii=False,indent=4)
    #구글 스프레드시트 저장
    def saveDataToGoogleSP(self):
        conn = st.connection("gsheets", type=GSheetsConnection)
        sheet_data = {"Data" : self.data}
        conn.update(worksheet="시트1", data=sheet_data)
        conn = st.connection("gsheets", type=GSheetsConnection)
        sheet_data = {"Data" : self.ip}
        conn.update(worksheet="시트2", data=sheet_data)  
    #비밀번호 검사
    def checkPassword(self,n,method):
        # n : key number
        # method : 1 = confirm, 2 = delete
        if method == 1:
            with st.popover("Confirm"):
                st.write(":red[모든 예약 내용이 저장됩니다 지워야 할 예약 내용이 있다면 지운 다음 저장해 주세요]")
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
            self.saveDataToGoogleSP()
    #삭제 허락                  
    def deleteReservation(self,n,p,slot,date):
        if self.checkPassword(n,p):
            if slot == 1:
                for i in range(len(self.data["신청"]["아침"])):
                    if self.data["신청"]["아침"][i]["date"] == date:
                        del self.data["신청"]["아침"][i]
                        self.data["날짜"]["아침"].append(date)
                        self.saveData()
                        self.saveDataToGoogleSP()
            elif slot == 2:
                for i in range(len(self.data["신청"]["점심"])):
                    if self.data["신청"]["점심"][i]["date"] == date:
                        del self.data["신청"]["점심"][i]
                        self.data["날짜"]["점심"].append(date)
                        self.saveData()
                        self.saveDataToGoogleSP()
    #학생중 이미 다른 날짜에 예약했는지 검사
    def uniqueReservationCheck(self):
        for student in self.studentsData:
            for i in self.data["신청"]["아침"]:
                if student in i["students"]:
                    st.error(f"이미 예약한 학생이 있습니다")
                    return False
            for i in self.data["신청"]["점심"]:
                if student in i["students"]:
                    st.error(f"이미 예약한 학생이 있습니다")
                    return False
        return True
    #학생 이름을 모두 입력했는지 검사
    def correctNameCheck(self):
        try:
            for i in range(1,int(self.studentNum[0]) + 1):
                if st.session_state[f'Student{i}'] is None or st.session_state[f'Student{i}'] == "":
                    st.error("학생 이름을 모두 입력해 주세요.")
                    return False
                else: 
                    continue
            if self.data["날짜"][self.slot][self.data["날짜"][self.slot].index(self.date)] is not None:   
                try:
                    if self.CheckStudentId(self.students):
                        for i in range(0,int(self.studentNum[0])):
                            if len(self.students[i]) < 7 or len(self.students[i]) > 9:
                                st.error("이름을 올바르게 입력해 주세요")
                                return False
                    else:
                        st.error("학번과 이름을 모두 입력해 주세요.")
                        return False
                    for i in range(0,int(self.studentNum[0])):
                        self.studentsData.append({self.students[i][:5] : self.students[i][5:]})
                        self.studentsId.append(self.students[i][:5])
                    return True
                except:
                    st.error("학번과 이름을 모두 입력해 주세요.")
                    return False
        except:
            st.error("예약에 실패했습니다. 이미 예약된 날짜인지 확인해 주세요.")
            return False
    #같은 예약에 같은 학번이 있는지 검사    
    def uniqueIDCheck(self):
        if len(self.studentsId) != len(set(self.studentsId)):
            st.error("중복된 학번이 있습니다.")
            return False
        return True
    #전화번호를 정확히 입력했는지 검사
    def telephoneNumberCheck(self):
        if len(st.session_state["Telephone"]) != 13:
            st.error("전화번호를 정확히 입력해 주세요")
            return False
        if st.session_state["Telephone"][3] != "-" or st.session_state["Telephone"][8] != "-":
            st.error("전화번호를 정확히 입력해 주세요")
            return False
        
        #EsterEgg - 1
        esterEggNumber = ["010-1234-5678","010-8765-4321"]
        for i in range(1,10):
            esterEggNumber.append("010-"+str(i)+str(i)+str(i)+str(i)+"-"+str(i)+str(i)+str(i)+str(i))
        if st.session_state["Telephone"] in esterEggNumber:
            st.success("EsterEgg - 1")
            return False
        
        return True
    #사용된 전화번호인지 검사
    def uniqueTelephoneNumberCheck(self):
        for i in self.data["신청"]["아침"]:
            if st.session_state["Telephone"] in i["telephone"]:
                st.error(f"전화번호가 이미 사용되었습니다")
                return False
        for i in self.data["신청"]["점심"]:
            if st.session_state["Telephone"] in i["telephone"]:
                st.error(f"전화번호가 이미 사용되었습니다")
                return False
        return True
    #예약 최종 저장
    def saveReservation(self):
        header = dict(self.getHeader())
        ip = header["X-Forwarded-For"]
        if ip in self.ip["ip"]:
            st.error("이미 예약했습니다 다른 학생이 예약해 주세요")
            return False
        if ip == None:
            st.error("에러발생 다시 시도해 주세요")
            return False
        self.data["날짜"][self.slot].remove(self.date)
        data = {"date" : self.date,
                "studentNum" : self.studentNum,
                "students" : self.studentsData,
                "telephone" : st.session_state["Telephone"]}
        self.data["신청"][self.slot].append(data)
        self.ip["ip"].append(ip)
        st.success("예약이 완료되었습니다.",icon="✅")
        self.saveData()
        self.saveIP()       
    #예약 상황 확인하기
    def currentReservation(self):
        self.loadData()
        try:
            self.admin = st.query_params["admin"]
        except:
            pass
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
                                    if self.admin == self.secrets["Password"]["admin"]:
                                        st.write(f"대표학생 전화번호 : "+i["telephone"])
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
                                    if self.admin == self.secrets["Password"]["admin"]:
                                        st.write(f"대표학생 전화번호 : "+i["telephone"])
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
        with st.popover("Load"):
            ps = st.text_input("비밀번호를 입력하세요",key=f"LoadPasswordInput",type="password")
            if st.button("Load",key=f"Load"):
                if ps == self.secrets["Password"]["loadPassword"]:
                    self.loadDataFromGoogleSP()
                else:
                    st.error("비밀번호가 틀렸습니다.")       
    #예약하기
    def reservation(self):
    #예약 폼 설정
        with self.reservation_:
            with st.container(height=200):
                st.write("1. :blue[날짜, 시간, 학생 수]를 선택합니다")
                st.write("2. 대표학생의 :blue[전화번호]를 입력합니다")
                st.write("4. 학생의 :blue[학번과 이름]을 입력합니다")
                st.write("3. :red[예약하기] 버튼을 눌러 예약합니다")
            with st.form("예약하기"):
                #컨테이너 설정
                with st.container():
                    self.studentsData = []
                    self.studentsId = []
                    st.selectbox("방탈출 이름",["난우교도소 : 진실의 서막","EsterEgg-2"],disabled=True)
                    self.date = st.selectbox("날짜를 선택해 주세요",self.dates)
                    self.slot = st.selectbox("시간을 선택해 주세요",self.slots)
                    self.studentNum = st.selectbox("학생 수를 선택해 주세요",self.studentNumber)
                    self.loadData()
                    st.write("대표 학생의 전화번호를 입력해 주세요")
                    st.session_state['Telephone'] = st.text_input(f"(ex:010-1234-5678)",max_chars=13)
                    st.write(":red[학생 수에 맞게 학번과 이름을 입력해 주세요]")
                    st.write("(ex:10101홍길동)")
                    st.session_state[f'Student{1}'] = st.text_input(f":red[대표] 학생의 학번과 이름을 입력해 주세요",max_chars=9)
                    for i in range(2,5):
                        st.session_state[f'Student{i}'] = st.text_input(f"{i}번 학생의 학번과 이름을 입력해 주세요",max_chars=9)
                    st.write(":red[4명이라면 5번 학생 입력란은 비워놓으셔도 됩니다]")
                    st.session_state[f'Student{5}'] = st.text_input(f"{5}번 학생의 학번과 이름을 입력해 주세요",max_chars=9)
                    self.students = [st.session_state[f'Student{i}'] for i in range(1,int(self.studentNum[0]) + 1)]
                    reservation_submitted = st.form_submit_button("예약하기")
                    
                if reservation_submitted:
                    if self.correctNameCheck():
                        if self.uniqueReservationCheck(): 
                            if self.uniqueIDCheck():
                                if self.telephoneNumberCheck():
                                    if self.uniqueTelephoneNumberCheck():
                                        self.saveReservation()

app = app()                

app.reservation()
app.currentReservation()