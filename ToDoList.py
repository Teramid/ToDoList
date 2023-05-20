from itertools import count
import typing
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as Qt
from PyQt6 import uic
import sqlite3
import sys


# Create database or connect to on
connData = sqlite3.connect('ToDoList.db')

# Cursor
cData = connData.cursor()

# Create table
cData.execute("""CREATE TABLE if not exists todolist(
    name_task TEXT,
    date_task TEXT,
    time_task TEXT)
    """)
cData.execute("""CREATE TABLE if not exists todolist_completed(
    name_task TEXT,
    completed_task TEXT,
    lefttime_task TEXT)
    """)
#commit changes
connData.commit()

#close connection
connData.close()




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
        self.defaultcalendar_pushButton = self.findChild(qtw.QPushButton, "defaultcalendar_pushButton")

        # Define checkboxes
        self.deadlineDate_CheckBox = self.findChild(qtw.QCheckBox, "deadlineDate_CheckBox")
        self.deadlineTime_CheckBox = self.findChild(qtw.QCheckBox, "deadlineTime_CheckBox")
        
        #Define the tab, table, combo
        self.tabWidget = self.findChild(qtw.QTabWidget, "tabWidget")
        self.tasks_tableWidget = self.findChild(qtw.QTableWidget, "tasks_tableWidget")
        self.calendar_tableWidget = self.findChild(qtw.QTableWidget, "calendar_tableWidget")
        self.completed_tableWidget = self.findChild(qtw.QTableWidget, "completed_tableWidget")
        self.timesort_comboBox = self.findChild(qtw.QComboBox, "timesort_comboBox")
        self.selectdate_label = self.findChild(qtw.QLabel, "selectdate_label")
        
        
        #table function
        #self.tasks_tableWidget.itemChanged.connect(self.refreshtask_pushButton_down)
        
        #Define textEdit
        self.addtask_lineEdit = self.findChild(qtw.QLineEdit, "addtask_lineEdit")
        
        # Define stuff
        self.deadline_dateEdit = self.findChild(qtw.QDateEdit, "deadline_dateEdit")
        self.deadline_timeEdit = self.findChild(qtw.QTimeEdit, "deadline_timeEdit")
        self.calendarWidget = self.findChild(qtw.QCalendarWidget, "calendarWidget")
        
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
        self.defaultcalendar_pushButton.clicked.connect(self.defaultcalendar_pushButton_down)

        #Calendar button
        self.calendarWidget.selectionChanged.connect(self.selectdate_calendarWidget)
        
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
        
        #Download data
        self.download_database()
        
        #show the app
        self.show()
    
    # Additional functions
    def timeleft(self, currentDate, currentTime, selectTime, selectDate):
        current_date_time = Qt.QDateTime(currentDate, currentTime)
        selected_date_time = Qt.QDateTime(selectDate,selectTime)
        timeLeft = current_date_time.daysTo(selected_date_time)
        if current_date_time.secsTo(selected_date_time) > 0:
            if current_date_time.secsTo(selected_date_time) < 86400:
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
    
    
    #Download all data from the database
    def download_database(self):
        currentDate = Qt.QDate.currentDate()
        currentTime = Qt.QTime.currentTime()
        # Create database or connect to on
        connData = sqlite3.connect('ToDoList.db')

        # Cursor
        cData = connData.cursor()
        
        cData.execute("SELECT * FROM todolist ORDER BY date_task ASC, time_task ASC")
        dataRecords = cData.fetchall()
        cData.execute("SELECT * FROM todolist_completed")
        dataRecordsCompleted = cData.fetchall()
        #commit changes
        connData.commit()

        #close connection
        connData.close()
        for record in dataRecords:
            row_count = self.tasks_tableWidget.rowCount()
            if record[2] == '-' or record[1] == '-':
                itemDate = qtw.QTableWidgetItem('-')
                itemTime = qtw.QTableWidgetItem('-')
            else:
                itemDate = record[1].split('.')
                itemTime = record[2].split(':')
                itemDate = Qt.QDate(int(itemDate[2]),int(itemDate[1]),int(itemDate[0]))
                itemTime = Qt.QTime(int(itemTime[0]),int(itemTime[1]))
                self.tasks_tableWidget.setRowCount(row_count + 1)
                itemTime =qtw.QTableWidgetItem(self.timeleft(currentDate, currentTime, itemTime, itemDate))
                itemDate = qtw.QTableWidgetItem(record[1])
            self.tasks_tableWidget.setRowCount(row_count + 1)
            self.tasks_tableWidget.setItem(row_count,0,qtw.QTableWidgetItem(record[0]))
            self.tasks_tableWidget.setItem(row_count,1,qtw.QTableWidgetItem(itemTime))
            self.tasks_tableWidget.setItem(row_count,2,qtw.QTableWidgetItem(itemDate))
        
        
        for record in dataRecordsCompleted:
            row_count = self.completed_tableWidget.rowCount()
            self.completed_tableWidget.setRowCount(row_count + 1)
            self.completed_tableWidget.setItem(row_count,0,qtw.QTableWidgetItem(record[0]))
            self.completed_tableWidget.setItem(row_count,1,qtw.QTableWidgetItem(record[1]))
            self.completed_tableWidget.setItem(row_count,2,qtw.QTableWidgetItem(record[2]))
        
        
    #save last changed to database
    def save_data(self, newTask):
        pass
    
    
                
    # Button function
    def leave_pushButton_down(self):
        qtw.QApplication.exit()
        
    def refreshtask_pushButton_down(self):
        self.tasks_tableWidget.clearContents()
        self.tasks_tableWidget.setRowCount(0)
        self.download_database()
        
    
    def selectdate_calendarWidget(self):
        dateSelect = self.calendarWidget.selectedDate()
        self.selectdate_label.setText(dateSelect.toString())
        
    def defaultcalendar_pushButton_down(self):
        today = Qt.QDate.currentDate()
        self.calendarWidget.setSelectedDate(today)
        self.calendarWidget.setCurrentPage(today.year(),today.month())
        
    def save_pushButton_down(self):
        pass

        
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
        currentDate = Qt.QDate.currentDate()
        currentTime = Qt.QTime.currentTime()
        if self.addtask_lineEdit.text():
            if self.deadlineDate_CheckBox.isChecked() == True: 
                dateTask = qtw.QTableWidgetItem(self.deadline_dateEdit.text())
                
            elif self.deadlineDate_CheckBox.isChecked() == False and self.deadlineTime_CheckBox.isChecked() == True: 
                dateTask = qtw.QTableWidgetItem(Qt.QDate.currentDate().toString("dd.MM.yyyy"))  
                 
            else: 
                dateTask = qtw.QTableWidgetItem('-')
                
            if self.deadlineTime_CheckBox.isChecked() == True:
                # Time left to deadline
                selectTime = self.deadline_timeEdit.time()
                timeLeft_text = self.timeleft(currentDate, currentTime,self.deadline_timeEdit.time(), self.deadline_dateEdit.date())
                selectTime = selectTime.toString("hh:mm")
                
            elif self.deadlineTime_CheckBox.isChecked() == False and self.deadlineDate_CheckBox.isChecked() == True:
                selectTime = Qt.QTime(23,59)
                timeLeft_text = self.timeleft(currentDate, currentTime, selectTime, self.deadline_dateEdit.date())
                selectTime = selectTime.toString("hh:mm")
                
            else:
                selectTime = "-"
                timeLeft_text = qtw.QTableWidgetItem("-")
            
            # Create database or connect to on
            connData = sqlite3.connect('ToDoList.db')

            # Cursor
            cData = connData.cursor()
            
            # Add task to database
            cData.execute("INSERT INTO todolist (name_task, date_task, time_task) VALUES (?, ?, ?)",
                (self.addtask_lineEdit.text(), dateTask.text(), selectTime))
            
            #commit changes
            connData.commit()

            #close connection
            connData.close()
            
            row_count = self.tasks_tableWidget.rowCount()
            self.tasks_tableWidget.setRowCount(row_count + 1)
            self.tasks_tableWidget.setItem(row_count,0,nameTask)
            self.tasks_tableWidget.setItem(row_count,1,timeLeft_text)
            self.tasks_tableWidget.setItem(row_count,2,dateTask)
            self.addtask_lineEdit.setText('')
            self.deadline_dateEdit.setDate(Qt.QDate.currentDate())
            self.deadline_timeEdit.setTime(Qt.QTime.currentTime())
            self.refreshtask_pushButton_down()
        else:
            pass
        
        
    def deletetask_pushButton_down(self):
        #select row click by mouse
        clicked = self.tasks_tableWidget.currentRow()
        
        if clicked > -1:
            items =[]
            for column in range(self.tasks_tableWidget.columnCount()):
                item = self.tasks_tableWidget.item(clicked, column)
                if item is not None:
                    items.append(item.text())
                else:
                    items.append("")
            # Create database or connect to on
            connData = sqlite3.connect('ToDoList.db')

            # Cursor
            cData = connData.cursor()
            
            # Remove task from db
            cData.execute("DELETE FROM todolist WHERE name_task= ? AND date_task= ?",
                        (items[0], items[2])
                        )
            
            #commit changes
            connData.commit()

            #close connection
            connData.close()
        #remove selected row
        self.tasks_tableWidget.removeRow(clicked)
        
    # checkbox fucntion
    
    def checked(self):
        #Date edit checkbox
        if self.deadlineDate_CheckBox.isChecked() == True:
            self.deadline_dateEdit.setEnabled(True)
        else:
            self.deadline_dateEdit.setEnabled(False)
        
        #Time edit checkbox
        if self.deadlineTime_CheckBox.isChecked() == True:
            self.deadline_timeEdit.setEnabled(True)
        else:
            self.deadline_timeEdit.setEnabled(False)
   
# Init the app     
app = qtw.QApplication(sys.argv)
UIWindow = UI()
app.exec()