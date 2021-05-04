from PyQt5 import uic, QtCore
import os
import sys
import threading
from PyQt5 import uic, QtCore ,QtWidgets
from PyQt5.QtGui import QPalette , QColor,QFont,QIcon ,QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QProgressBar , QFileDialog  ,QPushButton, QWidget ,QTableWidget,QTableWidgetItem ,QAbstractItemView
from PyQt5.QtCore import QThread
import multiprocessing
from PIL import Image, ImageEnhance
from subprocess import Popen
import pandas as pd
import xlwt 
from xlwt import Workbook 
import xlsxwriter
import subprocess
import operator
PlayerName="                          "

class SingUpWindow(QWidget):
    def __init__(self, parent=None):
        super(SingUpWindow, self).__init__(parent)
        self.Signup_B = QPushButton("Sign up", self)

        self.Username_Lable = QtWidgets.QLabel("Username",self)
        self.Password_Lable = QtWidgets.QLabel("Password",self)
        self.Email_Lable = QtWidgets.QLabel("Email",self)
        self.Check_Lable = QtWidgets.QLabel("                                                                       ",self)

        self.LineEdit_UserName = QtWidgets.QLineEdit(self)
        self.LineEdit_Password = QtWidgets.QLineEdit(self)
        self.LineEdit_Email = QtWidgets.QLineEdit(self)
        self.Signup_B.resize(200, 50)
    

        self.LineEdit_UserName.resize(200, 50) 
        self.LineEdit_Password.resize(200, 50)
        self.LineEdit_Email.resize(200, 50)

        self.Email_Lable.move(100, 275)

        self.Check_Lable.move(230, 150)

        self.Username_Lable.move(100, 185)
        self.Password_Lable.move(100, 235)

        self.LineEdit_UserName.move(200, 175)
        self.LineEdit_Password.move(200, 225)
        self.LineEdit_Email.move(200, 275)
        self.Signup_B.move(200, 325)

        self.Username_Lable.setFont(QFont('SansSerif', 15))
        self.Password_Lable.setFont(QFont('SansSerif', 15))
        self.Email_Lable.setFont(QFont('SansSerif', 15))
        self.LineEdit_UserName.setFont(QFont('SansSerif', 15))
        self.LineEdit_Password.setFont(QFont('SansSerif', 15))
        self.LineEdit_Email.setFont(QFont('SansSerif', 15))

        ##########
  


class loadtable(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(loadtable, self).__init__(parent)

        self.setColumnCount(3)
        self.setRowCount(20)
        self.setFont(QFont("Helvetica", 10, QFont.Normal, italic=False))   
        headertitle = ("Rank","Usernames","Scores")
        self.setHorizontalHeaderLabels(headertitle)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setHighlightSections(False)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.setColumnWidth(1, 130)





class UIWindow(QWidget):
    def __init__(self, parent=None):
        super(UIWindow, self).__init__(parent)
        # mainwindow.setWindowIcon(QtGui.QIcon('PhotoIcon.png'))
        table = loadtable()
        file_name =  "Scores.xlsx"
        df = pd.read_excel(file_name)
        Users= df.set_index('Usernames').T.to_dict('records')
        temp_dict=Users[0]
        sorted_x = sorted(temp_dict.items(), key=operator.itemgetter(1))
        j=0
        for i in reversed(range(len(sorted_x))):
            table.setItem(j , 0 , QTableWidgetItem("#"+str(j+1)))
            table.setItem(j , 1 , QTableWidgetItem(sorted_x[i][0]))
            table.setItem(j , 2 , QTableWidgetItem(str(sorted_x[i][1])))
            j=j+1
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        button_layout = QtWidgets.QVBoxLayout()
        button_layout2 = QtWidgets.QVBoxLayout()
        self.Play_Button = QPushButton('PLay', self)
        self.Back_Button= QPushButton('Save and exit ', self)
        button_layout.addWidget(self.Play_Button, alignment=QtCore.Qt.AlignBottom)
        button_layout2.addWidget(self.Back_Button, alignment=QtCore.Qt.AlignBottom)
        tablehbox = QtWidgets.QHBoxLayout()
        tablehbox.setContentsMargins(10,10,10,10)
        tablehbox.addWidget(table)
        grid = QtWidgets.QGridLayout(self)
        grid.addLayout(button_layout, 0, 1)
        grid.addLayout(button_layout2, 0, 2)
        grid.addLayout(tablehbox, 0, 0) 
        #self.Play_Button.resize(200, 50)
        #self.Play_Button.move(200, 225)

        


class UIToolTab(QWidget):
    def __init__(self, parent=None):
        super(UIToolTab, self).__init__(parent)
        self.Login_Button = QPushButton("Login", self)
        self.Signup_Button = QPushButton("Sign up", self)

        self.label_username = QtWidgets.QLabel("Username",self)
        self.label_password = QtWidgets.QLabel("Password",self)
        self.UserName_LineEdit = QtWidgets.QLineEdit(self)
        self.Password_LineEdit = QtWidgets.QLineEdit(self)
        self.Lable_Check = QtWidgets.QLabel("                                                                       ",self)

        self.Signup_Button.resize(200, 50)
        self.Login_Button.resize(200, 50)  
        self.UserName_LineEdit.resize(200, 50)
        self.Password_LineEdit.resize(200, 50) 

        


        self.Lable_Check.move(200, 150)
        self.label_username.move(100, 185)
        self.label_password.move(100, 235)
        self.label_username.setFont(QFont('SansSerif', 15))
        self.label_password.setFont(QFont('SansSerif', 15))

        self.UserName_LineEdit.setFont(QFont('SansSerif', 15))
        self.Password_LineEdit.setFont(QFont('SansSerif', 15))

        self.UserName_LineEdit.move(200, 175)
        self.Password_LineEdit.move(200, 225)
        self.Login_Button.move(200, 275)
        self.Signup_Button.move(200, 325)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        #self.setGeometry(50, 50, 600, 600)
        self.setFixedSize(600, 600)
        self.startUIToolTab()
        self.setWindowIcon(QIcon('../Assets/v.png'))

    def startUIToolTab(self):
        self.ToolTab = UIToolTab(self)
        self.setWindowTitle("Login")
        self.setCentralWidget(self.ToolTab)
        self.ToolTab.Login_Button.clicked.connect(self.Check_userpass)
        self.ToolTab.Signup_Button.clicked.connect(self.StartSingUpWindow)
        self.show()
    def Check_userpass(self):
        if(os.path.exists("Usernames.xlsx")):
            df = pd.read_excel("Usernames.xlsx") 
            Users= df.set_index('Usernames').T.to_dict('records')
            My_dict=Users[0]
            if (self.ToolTab.UserName_LineEdit.text()) in My_dict.keys() :
                if( str(My_dict[self.ToolTab.UserName_LineEdit.text()]) == self.ToolTab.Password_LineEdit.text()):
                    self.startUIWindow()
                    self.Current_Player_name=self.ToolTab.UserName_LineEdit.text()
                    global PlayerName
                    PlayerName=self.Current_Player_name
            else :
                self.ToolTab.Lable_Check.setText("Your Username or password is not correct")
        else :
            self.ToolTab.Lable_Check.setText("Your Username or password is not correct")
    def startUIWindow(self):
        self.Window = UIWindow(self)
        self.setWindowTitle("GameStore")
        self.setCentralWidget(self.Window)
        self.Window.Play_Button.clicked.connect(self.Play_Game)
        self.Window.Back_Button.clicked.connect(self.GOHome)

        self.show()
    def GOHome(self):
        
        if(os.path.exists('tempScore.txt')):
            SaveScore()
            #sys.exit(0)
        self.startUIToolTab()

    def StartSingUpWindow(self):
        self.SWindow = SingUpWindow(self)
        self.setWindowTitle("Sing Up")
        self.setCentralWidget(self.SWindow)
        self.SWindow.Signup_B.clicked.connect(self.Sing_UP)
        self.show()
    def Sing_UP(self):
        if(os.path.exists("Usernames.xlsx")):
            file_name =  "Usernames.xlsx"
            df = pd.read_excel(file_name)
            Users= df.set_index('Usernames').T.to_dict('records')
            My_dict=Users[0]
            if (self.SWindow.LineEdit_UserName.text()) in My_dict.keys() :
                self.SWindow.Check_Lable.setText("This Username already exists")
            elif(self.SWindow.LineEdit_Password.text()=="" or self.SWindow.LineEdit_UserName.text()=="" ):
                self.SWindow.Check_Lable.setText("You should fill all the fields")
            else:
                My_dict[self.SWindow.LineEdit_UserName.text()]=self.SWindow.LineEdit_Password.text()
                workbook  = xlsxwriter.Workbook('Temp.xlsx')
                worksheet = workbook.add_worksheet()
                worksheet.write(0, 0, 'Usernames') 
                worksheet.write(0, 1, 'Passwords') 
                i=1
                for x, y in My_dict.items():

                    
                    worksheet.write(i, 0, x) 
                    worksheet.write(i, 1, y) 
                    i=i+1
                workbook.close()
                os.remove("Usernames.xlsx") 
                os.rename('Temp.xlsx', "Usernames.xlsx")
                if(os.path.isfile("Scores.xlsx")):
                    file_name =  "Scores.xlsx"
                    df = pd.read_excel(file_name)
                    Users= df.set_index('Usernames').T.to_dict('records')
                    temp_dict=Users[0]
                    workbook  = xlsxwriter.Workbook('Temp.xlsx')
                    worksheet = workbook.add_worksheet()
                    worksheet.write(0, 0, 'Usernames') 
                    worksheet.write(0, 1, 'Scores') 
                    i=1
                    for x, y in temp_dict.items():

                        
                        worksheet.write(i, 0, x) 
                        worksheet.write(i, 1, y) 
                        i=i+1
                    worksheet.write(i, 0, self.SWindow.LineEdit_UserName.text()) 
                    worksheet.write(i, 1, str(0)) 
                    workbook.close()
                    os.remove("Scores.xlsx") 
                    os.rename('Temp.xlsx', "Scores.xlsx")
                    self.startUIToolTab()
                else :
                    workbook  = xlsxwriter.Workbook('Scores.xlsx')
                    worksheet = workbook.add_worksheet()
                    worksheet.write(0, 0, 'Usernames') 
                    worksheet.write(0, 1, 'Scores') 
                    i=1
                    for x, y in My_dict.items():
                        worksheet.write(i, 0, x) 
                        worksheet.write(i, 1, 0) 
                        i=i+1
                    worksheet.write(i, 0, self.SWindow.LineEdit_UserName.text()) 
                    worksheet.write(i, 1, str(0)) 
                    workbook.close()
                    self.startUIToolTab()
        else: 
            file_name =  "Usernames.xlsx"
            if(self.SWindow.LineEdit_Password.text()=="" or self.SWindow.LineEdit_UserName.text()=="" ):
                self.SWindow.Check_Lable.setText("you should fill all the fields")
            else:
                workbook  = xlsxwriter.Workbook('Usernames.xlsx')
                worksheet = workbook.add_worksheet()
                worksheet.write(0, 0, 'Usernames') 
                worksheet.write(0, 1, 'Passwords') 
                worksheet.write(1, 0, self.SWindow.LineEdit_UserName.text()) 
                worksheet.write(1, 1, self.SWindow.LineEdit_Password.text()) 
                workbook.close()
                if(os.path.isfile("Scores.xlsx")):
                    file_name =  "Scores.xlsx"
                    df = pd.read_excel(file_name)
                    Users= df.set_index('Usernames').T.to_dict('records')
                    temp_dict=Users[0]
                    workbook  = xlsxwriter.Workbook('Temp.xlsx')
                    worksheet = workbook.add_worksheet()
                    worksheet.write(0, 0, 'Usernames') 
                    worksheet.write(0, 1, 'Scores') 
                    i=1
                    for x, y in temp_dict.items():

                        
                        worksheet.write(i, 0, x) 
                        worksheet.write(i, 1, y) 
                        i=i+1
                    worksheet.write(i, 0, self.SWindow.LineEdit_UserName.text()) 
                    worksheet.write(i, 1, str(0)) 
                    workbook.close()
                    os.remove("Scores.xlsx") 
                    os.rename('Temp.xlsx', "Scores.xlsx")
                    self.startUIToolTab()
                else :
                    workbook  = xlsxwriter.Workbook('Scores.xlsx')
                    worksheet = workbook.add_worksheet()
                    worksheet.write(0, 0, 'Usernames') 
                    worksheet.write(0, 1, 'Scores') 
                    worksheet.write(1, 0, self.SWindow.LineEdit_UserName.text()) 
                    worksheet.write(1, 1, str(0)) 
                    workbook.close()      
                    self.startUIToolTab()
    def SnakeGame(slef):
        os.system("python main.py")
    def MotionDetector(self):
        os.system("python Motion.py")
    def VoiceDetector(self):
        os.system("python Voice.py")

    def Play_Game(self):
        #self.t1=threading.Thread(target=self.MotionDetector)
        #self.t1.demon=True
        #self.t1.start()
        self.t2=threading.Thread(target=self.VoiceDetector)
        self.t2.demon=True
        self.t2.start()
        self.t3=threading.Thread(target=self.SnakeGame)
        self.t3.demon=True
        self.t3.start()

def SaveScore():
    if(os.path.exists('tempScore.txt')):
        f = open("tempScore.txt", "r")
        Score= f.read()
        f.close()
        os.remove("tempScore.txt")
        if(os.path.isfile("Scores.xlsx")):
            file_name =  "Scores.xlsx"
            df = pd.read_excel(file_name)
            Users= df.set_index('Usernames').T.to_dict('records')
            temp_dict=Users[0]
            if(int(temp_dict[PlayerName]) < int(Score) ):
                temp_dict[PlayerName]=Score
                workbook  = xlsxwriter.Workbook('Temp.xlsx')
                worksheet = workbook.add_worksheet()
                worksheet.write(0, 0, 'Usernames') 
                worksheet.write(0, 1, 'Scores') 
                i=1
                for x, y in temp_dict.items():
                    worksheet.write(i, 0, x) 
                    worksheet.write(i, 1, y) 
                    i=i+1
                workbook.close()
                os.remove("Scores.xlsx") 
                os.rename('Temp.xlsx', "Scores.xlsx")
                sys.exit()

app=QApplication (sys.argv)
app.setStyle("Fusion")
palette = QPalette()
palette.setColor(QPalette.Window, QColor(53, 53, 53))
palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
palette.setColor(QPalette.Base, QColor(25, 25, 25))
palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
palette.setColor(QPalette.Text, QColor(255, 255, 255))
palette.setColor(QPalette.Button, QColor(53, 53, 53))
palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
palette.setColor(QPalette.Link, QColor(42, 130, 218))
palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
app.setPalette(palette)


w=MainWindow()

w.show()
sys.exit(app.exec_())

