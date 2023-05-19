import typing
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as Qt
from PyQt6 import uic
import sys

class UI(qtw.QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        
        # Load the ui file
        uic.loadUi("ToDoList.ui",self)
        
        #Define the buttons
        self.leave_pushButton = self.findChild(qtw.QPushButton, "leave_pushButton")
        self.refreshtask_pushButton = self.findChild(qtw.QPushButton, "refreshtask_pushButton")
        self.save_pushButton = self.findChild(qtw.QPushButton, "save_pushButton")
        self.addtask_pushButton = self.findChild(qtw.QPushButton, "addtask_pushButton")
        self.deletetask_pushButton = self.findChild(qtw.QPushButton, "deletetask_pushButton")
        self.finishtask_pushButton = self.findChild(qtw.QPushButton, "finishtask_pushButton")
        
        # Define checkboxes
        self.deadlineDate_CheckBox = self.findChild(qtw.QCheckBox, "deadlineDate_CheckBox")
        self.deadlineTime_CheckBox = self.findChild(qtw.QCheckBox, "deadlineTime_CheckBox")
        
        #Define the tab, table, combo
        self.tabWidget = self.findChild(qtw.QTabWidget, "tabWidget")
        self.tasks_tableWidget = self.findChild(qtw.QTableWidget, "tasks_tableWidget")
        self.calendar_tableWidget = self.findChild(qtw.QTableWidget, "calendar_tableWidget")
        self.completed_tableWidget = self.findChild(qtw.QTableWidget, "completed_tableWidget")
        self.timesort_comboBox = self.findChild(qtw.QComboBox, "timesort_comboBox")
        
        #Define textEdit
        self.addtask_lineEdit = self.findChild(qtw.QLineEdit, "addtask_lineEdit")
        
        # Define stuff
        self.deadline_dateEdit = self.findChild(qtw.QDateEdit, "deadline_dateEdit")
        self.deadline_timeEdit = self.findChild(qtw.QTimeEdit, "deadline_timeEdit")
        
        #settime
        self.deadline_dateEdit.setDate(Qt.QDate.currentDate())
        self.deadline_timeEdit.setTime(Qt.QTime.currentTime())
        self.deadline_dateEdit.setMinimumDate(Qt.QDate.currentDate())
        
        # Click Button
        self.leave_pushButton.clicked.connect(self.leave_pushButton_down)
        self.refreshtask_pushButton.clicked.connect(self.refreshtask_pushButton_down)
        self.save_pushButton.clicked.connect(self.save_pushButton_down)
        self.addtask_pushButton.clicked.connect(self.addtask_pushButton_down)
        self.deletetask_pushButton.clicked.connect(self.deletetask_pushButton_down)
        self.finishtask_pushButton.clicked.connect(self.finishtask_pushButton_down)
        
        # Update checkbox
        self.deadlineDate_CheckBox.toggled.connect(lambda:self.checked())
        self.deadlineTime_CheckBox.toggled.connect(lambda:self.checked())
        
        #Set column size
            #tasktable
        self.tasks_tableWidget.setColumnWidth(0, 170)
        self.tasks_tableWidget.setColumnWidth(1, 80)
        self.tasks_tableWidget.setColumnWidth(2, 90)
            #calendar table
        self.calendar_tableWidget.setColumnWidth(0, 200)
        self.calendar_tableWidget.setColumnWidth(1, 140)
            #completed table
        self.completed_tableWidget.setColumnWidth(0, 170)
        self.completed_tableWidget.setColumnWidth(1, 80)
        self.completed_tableWidget.setColumnWidth(2, 90)
        #show the app
        self.show()
    
    # Additional functions
    def timeleft(self, currentDate, currentTime):
        current_date_time = Qt.QDateTime(currentDate, currentTime)
        selected_date_time = Qt.QDateTime(self.deadline_dateEdit.date(),self.deadline_timeEdit.time())
        timeLeft = current_date_time.daysTo(selected_date_time)
        if current_date_time.secsTo(selected_date_time) > 0:
            if timeLeft < 1:
                timeLeft = int(current_date_time.secsTo(selected_date_time)/3600)
                timeLeft_text = f"{timeLeft} hours" if timeLeft>1 else f"{timeLeft} hour"
                if timeLeft<1:
                    timeLeft = int((current_date_time.secsTo(selected_date_time)%3600)/60)
                    timeLeft_text = f"{timeLeft} minutes" if timeLeft>1 else f"{timeLeft} minute"
            else:
                timeLeft_text = f"{timeLeft} days"  if timeLeft>1 else f"{timeLeft} day"
            
            timeLeft_text = qtw.QTableWidgetItem(timeLeft_text)
        else:
            timeLeft_text = qtw.QTableWidgetItem("Time has passed")
        return timeLeft_text
                
    # Button function
    def leave_pushButton_down(self):
        qtw.QApplication.exit()
        
    def refreshtask_pushButton_down(self):
        print("2")
        
    def save_pushButton_down(self):
        print("3")
        
    def finishtask_pushButton_down(self):
        # Grab completed task from list
        clickedRow = self.tasks_tableWidget.currentRow()
        if clickedRow > -1:
            items =[]
            for column in range(self.tasks_tableWidget.columnCount()):
                item = self.tasks_tableWidget.item(clickedRow, column)
                if item is not None:
                    items.append(item.text())
                else:
                    items.append("")
            items[2] = Qt.QDate.currentDate().toString("dd.MM.yyyy")     
            # Remove the task
            self.tasks_tableWidget.removeRow(clickedRow)
            
            # Add task to completed list
            row_count = self.completed_tableWidget.rowCount()
            self.completed_tableWidget.setRowCount(row_count + 1)
            
            for column, item in enumerate(items):
                self.completed_tableWidget.setItem(row_count, column, qtw.QTableWidgetItem(item))
        else:
            pass
    def addtask_pushButton_down(self):
        #grab name, date and time task
        nameTask = qtw.QTableWidgetItem(self.addtask_lineEdit.text())
        if self.addtask_lineEdit.text():
            dateTask = qtw.QTableWidgetItem(self.deadline_dateEdit.text()) if self.deadlineDate_CheckBox.isChecked() == True else qtw.QTableWidgetItem('-')
            if self.deadlineTime_CheckBox.isChecked() == True:
                # Time left to deadline
                currentDate = Qt.QDate.currentDate()
                currentTime = Qt.QTime.currentTime()
                timeLeft_text = self.timeleft(currentDate, currentTime)
            else:
                timeLeft_text = qtw.QTableWidgetItem("-")
            
            
            row_count = self.tasks_tableWidget.rowCount()
            self.tasks_tableWidget.setRowCount(row_count + 1)
            self.tasks_tableWidget.setItem(row_count,0,nameTask)
            self.tasks_tableWidget.setItem(row_count,1,timeLeft_text)
            self.tasks_tableWidget.setItem(row_count,2,dateTask)
            self.addtask_lineEdit.setText('')
            self.deadline_dateEdit.setDate(Qt.QDate.currentDate())
            self.deadline_timeEdit.setTime(Qt.QTime.currentTime())
        else:
            pass
        
        
    def deletetask_pushButton_down(self):
        #select row click by mouse
        clicked = self.tasks_tableWidget.currentRow()
        #remove selected row
        self.tasks_tableWidget.removeRow(clicked)
        
    # checkbox fucntion
    
    def checked(self):
        #Date edit checkbox
        if self.deadlineDate_CheckBox.isChecked() == True:
            self.deadline_dateEdit.setDate(Qt.QDate.currentDate())
            self.deadline_dateEdit.setEnabled(True)
        else:
            self.deadline_dateEdit.setEnabled(False)
        
        #Time edit checkbox
        if self.deadlineTime_CheckBox.isChecked() == True:
            self.deadline_timeEdit.setTime(Qt.QTime.currentTime())
            self.deadline_timeEdit.setEnabled(True)
        else:
            self.deadline_timeEdit.setEnabled(False)
   
# Init the app     
app = qtw.QApplication(sys.argv)
UIWindow = UI()
app.exec()