import typing
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTabWidget, QLineEdit, QTimeEdit, QCheckBox, QComboBox, QTableWidget,QWidget,QDateEdit
from PyQt5 import QtCore, uic
import sys

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        
        # Load the ui file
        uic.loadUi("ToDoList.ui",self)
        
        #Define the buttons
        self.leave_pushButton = self.findChild(QPushButton, "leave_pushButton")
        self.refreshtask_pushButton = self.findChild(QPushButton, "refreshtask_pushButton")
        self.save_pushButton = self.findChild(QPushButton, "save_pushButton")
        self.addtask_pushButton = self.findChild(QPushButton, "addtask_pushButton")
        self.deletetask_pushButton = self.findChild(QPushButton, "deletetask_pushButton")
        
        # Define checkboxes
        self.deadlineDate_CheckBox = self.findChild(QCheckBox, "deadlineDate_CheckBox")
        self.deadlineTime_CheckBox = self.findChild(QCheckBox, "deadlineTime_CheckBox")
        
        #Define the tab, table, combo
        self.tabWidget = self.findChild(QTabWidget, "tabWidget")
        self.tasks_tableWidget = self.findChild(QTableWidget, "tasks_tableWidget")
        self.completed_tableWidget = self.findChild(QTableWidget, "completed_tableWidget")
        self.timesort_comboBox = self.findChild(QComboBox, "timesort_comboBox")
        
        #Define textEdit
        self.addtask_lineEdit = self.findChild(QLineEdit, "addtask_lineEdit")
        
        # Define stuff
        self.deadline_dateEdit = self.findChild(QDateEdit, "deadline_dateEdit")
        self.deadline_timeEdit = self.findChild(QTimeEdit, "deadline_timeEdit")
        
        # Click Button
        self.leave_pushButton.clicked.connect(self.leave_pushButton_down)
        self.refreshtask_pushButton.clicked.connect(self.refreshtask_pushButton_down)
        self.save_pushButton.clicked.connect(self.save_pushButton_down)
        self.addtask_pushButton.clicked.connect(self.addtask_pushButton_down)
        self.deletetask_pushButton.clicked.connect(self.deletetask_pushButton_down)

        #show the app
        self.show()
   
    def leave_pushButton_down(self):
        print("1")
    def refreshtask_pushButton_down(self):
        print("2")
    def save_pushButton_down(self):
        print("3")
    def addtask_pushButton_down(self):
        print("4")
    def deletetask_pushButton_down(self):
        print("5")
   
# Init the app     
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()