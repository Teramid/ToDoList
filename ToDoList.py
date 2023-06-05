import os
import sqlite3
import sys
from random import randint

import PyQt6.QtCore as Qt
import PyQt6.QtWidgets as qtw
from PyQt6 import uic
from PyQt6.QtGui import QAction, QIcon


# File path
current_file = __file__
current_path = os.path.abspath(current_file)
current_path = current_path.split("\\")
current_path = "/".join(x for x in current_path[0 : len(current_path) - 1])
print(current_path)
databaseFile = f"{current_path}/ToDoList.db"
trayIconPng = f"{current_path}/Icons/clipboard-text.png"


# Create database or connect to on
connData = sqlite3.connect(databaseFile)

# Cursor
cData = connData.cursor()

# Create table
cData.execute(
    """CREATE TABLE if not exists todolist(
    name_task TEXT,
    date_task TEXT,
    time_task TEXT,
    id_task INT,
    completed_task BOOLEAN,
    finishDate_task TEXT,
    timeLeft_task TEXT)
    """
)
cData.execute(
    """CREATE TABLE if not exists settings(
    opacity INT,
    minimize BOOLEAN,
    color_mode BOOLEAN)
    """
)

# Download last settigns
cData.execute("SELECT * FROM settings")
settingsData = cData.fetchone()
if settingsData is None:
    cData.execute("INSERT INTO settings(opacity, minimize, color_mode) VALUES(100, TRUE, FALSE)")
    cData.execute("SELECT * FROM settings")
    settingsData = cData.fetchone()


opacitySettings = settingsData[0]
minimizeSettings = settingsData[1]
colorSettings = settingsData[2]


if colorSettings:
    uiFile = f"{current_path}/ToDoList.ui"
else:
    uiFile = f"{current_path}/ToDoList_dark.ui"
uiFile = os.path.abspath(uiFile)
# commit changes
connData.commit()

# close connection
connData.close()


class UI(qtw.QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load the ui file
        uic.loadUi(uiFile, self)

        # ___________________________________________________________________________#
        # Window
        self.move_frame = self.findChild(qtw.QFrame, "move_frame")
        self.tabWidget = self.findChild(qtw.QTabWidget, "tabWidget")

        # Move window by click frame
        if self.move_frame:
            self.move_frame.mousePressEvent = self.frameMousePressEvent
            self.move_frame.mouseMoveEvent = self.frameMouseMoveEvent

        # Define the buttons
        self.leave_pushButton = self.findChild(qtw.QPushButton, "leave_pushButton")
        self.refreshtask_pushButton = self.findChild(qtw.QPushButton, "refreshtask_pushButton")

        # Function assignment
        self.leave_pushButton.clicked.connect(self.leave_pushButton_down)
        self.refreshtask_pushButton.clicked.connect(self.refreshtask_pushButton_down)

        # Window attribute
        self.setWindowFlags(Qt.Qt.WindowType.FramelessWindowHint)

        # ___________________________________________________________________________#
        # Task tab

        # Define the buttons
        self.addtask_pushButton = self.findChild(qtw.QPushButton, "addtask_pushButton")
        self.deletetask_pushButton = self.findChild(qtw.QPushButton, "deletetask_pushButton")
        self.finishtask_pushButton = self.findChild(qtw.QPushButton, "finishtask_pushButton")

        # Assignment of button functions
        self.addtask_pushButton.clicked.connect(self.addtask_pushButton_down)
        self.deletetask_pushButton.clicked.connect(self.deletetask_pushButton_down)
        self.finishtask_pushButton.clicked.connect(self.finishtask_pushButton_down)

        # Define the checkboxes
        self.deadlineDate_CheckBox = self.findChild(qtw.QCheckBox, "deadlineDate_CheckBox")
        self.deadlineTime_CheckBox = self.findChild(qtw.QCheckBox, "deadlineTime_CheckBox")

        # Assignment of checkbox functions
        self.deadlineDate_CheckBox.toggled.connect(self.checked)
        self.deadlineTime_CheckBox.toggled.connect(self.checked)

        # Define the text/time/date Edit
        self.addtask_lineEdit = self.findChild(qtw.QLineEdit, "addtask_lineEdit")
        self.deadline_dateEdit = self.findChild(qtw.QDateEdit, "deadline_dateEdit")
        self.deadline_timeEdit = self.findChild(qtw.QTimeEdit, "deadline_timeEdit")

        # Set default time/date
        self.deadline_dateEdit.setDate(Qt.QDate.currentDate())
        self.deadline_timeEdit.setTime(Qt.QTime.currentTime())
        self.deadline_dateEdit.setMinimumDate(Qt.QDate.currentDate())

        # Define filtering combobox
        self.timesort_comboBox = self.findChild(qtw.QComboBox, "timesort_comboBox")

        # Assignment of combobox functions
        self.timesort_comboBox.activated.connect(self.timesort)
        # Define tasks table
        self.tasks_tableWidget = self.findChild(qtw.QTableWidget, "tasks_tableWidget")

        # Size column tasks table
        self.tasks_tableWidget.setColumnWidth(0, 153)
        self.tasks_tableWidget.setColumnWidth(1, 80)
        self.tasks_tableWidget.setColumnWidth(2, 90)

        # Hide ID column
        self.tasks_tableWidget.setColumnHidden(3, True)

        # ___________________________________________________________________________#
        # Completed tab

        # Define the buttons
        self.uncompletedtask_pushButton = self.findChild(qtw.QPushButton, "uncompletedtask_pushButton")
        self.deletetask_pushButton_2 = self.findChild(qtw.QPushButton, "deletetask_pushButton_2")
        # Assignment of button functions
        self.uncompletedtask_pushButton.clicked.connect(self.uncompletedtask_pushButton_down)
        self.deletetask_pushButton_2.clicked.connect(self.deletetask_pushButton_2_down)

        # Define tasks table
        self.completed_tableWidget = self.findChild(qtw.QTableWidget, "completed_tableWidget")

        # Size column tasks table
        self.completed_tableWidget.setColumnWidth(0, 153)
        self.completed_tableWidget.setColumnWidth(1, 80)
        self.completed_tableWidget.setColumnWidth(2, 90)

        # Hide ID column
        self.completed_tableWidget.setColumnHidden(3, True)

        # ___________________________________________________________________________#
        # Calendar tab

        # Define the buttons
        self.defaultcalendar_pushButton = self.findChild(qtw.QPushButton, "defaultcalendar_pushButton")

        # Assignment of button functions
        self.defaultcalendar_pushButton.clicked.connect(self.defaultcalendar_pushButton_down)

        # Define the calendarWidget
        self.calendarWidget = self.findChild(qtw.QCalendarWidget, "calendarWidget")

        # Assignment of calendar functions
        self.calendarWidget.selectionChanged.connect(self.selectdate_calendarWidget)

        # Define the table of tasks selected day
        self.calendar_tableWidget = self.findChild(qtw.QTableWidget, "calendar_tableWidget")

        # Size column calendar table
        self.calendar_tableWidget.setColumnWidth(0, 233)
        self.calendar_tableWidget.setColumnWidth(1, 90)

        # Define label to select date
        self.selectdate_label = self.findChild(qtw.QLabel, "selectdate_label")

        # ___________________________________________________________________________#
        # Settings tab

        # Define opacity sldier and label
        self.opacity_horizontalSlider = self.findChild(qtw.QSlider, "opacity_horizontalSlider")
        self.opacityPercent_label = self.findChild(qtw.QLabel, "opacityPercent_label")
        # Assignment of opacity functions
        self.opacity_horizontalSlider.valueChanged.connect(self.opacity_horizontalSlider_change)
        self.opacity_horizontalSlider.setMinimum(10)
        self.opacity_horizontalSlider.setMaximum(100)
        self.opacity_horizontalSlider.setValue(opacitySettings)
        self.opacityPercent_label.setText(f"{self.opacity_horizontalSlider.value()}%")

        # Define radio buttons
        # Minimize/exit button
        self.exit_radioButton = self.findChild(qtw.QRadioButton, "exit_radioButton")
        self.minimize_radioButton = self.findChild(qtw.QRadioButton, "minimize_radioButton")
        # Assignment of Minimize/Exit functions
        if minimizeSettings:
            self.minimize_radioButton.setChecked(True)
        else:
            self.exit_radioButton.setChecked(True)
        self.minimize_radioButton.toggled.connect(lambda: self.minimizeExit_state(self.minimize_radioButton))
        self.exit_radioButton.toggled.connect(lambda: self.minimizeExit_state(self.exit_radioButton))

        # Dark/Light mode
        self.darkMode_radioButton = self.findChild(qtw.QRadioButton, "darkMode_radioButton")
        self.lightMode_radioButton = self.findChild(qtw.QRadioButton, "lightMode_radioButton")
        self.colorMode_label = self.findChild(qtw.QLabel, "colorMode_label")
        self.colorMode_label.hide()
        # Assignment of Dark/Light functions
        if colorSettings:
            self.lightMode_radioButton.setChecked(True)
        else:
            self.darkMode_radioButton.setChecked(True)
        self.lightMode_radioButton.toggled.connect(lambda: self.colorMode_state(self.lightMode_radioButton))
        self.darkMode_radioButton.toggled.connect(lambda: self.colorMode_state(self.darkMode_radioButton))

        # ___________________________________________________________________________#

        # Download data
        self.download_database()
        # show the app
        self.show()

    # ___________________________________________________________________________#

    # Move window
    def frameMousePressEvent(self, event):
        if event.button() == Qt.Qt.MouseButton.LeftButton:
            self.dragPos = event.globalPosition().toPoint()

    def frameMouseMoveEvent(self, event):
        if hasattr(self, "dragPos") and event.buttons() & Qt.Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()

    def timeleft_func(self, currentDate, currentTime, selectTime, selectDate):
        current_date_time = Qt.QDateTime(currentDate, currentTime)
        selected_date_time = Qt.QDateTime(selectDate, selectTime)
        timeLeft = current_date_time.daysTo(selected_date_time)
        if current_date_time.secsTo(selected_date_time) > 0:
            if current_date_time.secsTo(selected_date_time) < 86400:
                timeLeft = int(current_date_time.secsTo(selected_date_time) / 3600)
                timeLeft_text = f"{timeLeft} hours" if timeLeft > 1 else f"{timeLeft} hour"
                if timeLeft < 1:
                    timeLeft = int((current_date_time.secsTo(selected_date_time) % 3600) / 60)
                    timeLeft_text = f"{timeLeft} minutes" if timeLeft > 1 else f"{timeLeft} minute"
            else:
                timeLeft_text = f"{timeLeft} days" if timeLeft > 1 else f"{timeLeft} day"

            timeLeft_text = qtw.QTableWidgetItem(timeLeft_text)
        else:
            timeLeft_text = qtw.QTableWidgetItem("Delayed")
        return timeLeft_text

    # Download all data from the database
    def download_database(self):
        # Cell format
        cellOption = Qt.Qt.AlignmentFlag.AlignLeft | Qt.Qt.AlignmentFlag.AlignCenter
        sort = self.timesort_comboBox.currentIndex()
        currentDate = Qt.QDate.currentDate()
        currentTime = Qt.QTime.currentTime()
        selectTime = ["-", "Delayed"]
        if sort == 0:
            selectTime.append(currentDate.toString("yyyy-MM-dd"))
        elif sort == 1:
            for i in range(7):
                selectTime.append(currentDate.addDays(i).toString("yyyy-MM-dd"))
        elif sort == 2:
            for i in range(14):
                selectTime.append(currentDate.addDays(i).toString("yyyy-MM-dd"))
        elif sort == 3:
            selectTime = []
        elif sort == 4:
            selectTime = ["Delayed"]
        # connect to database
        connData = sqlite3.connect(databaseFile)

        # Cursor
        cData = connData.cursor()
        cData.execute("SELECT * FROM todolist ORDER BY date(date_task) ASC, TIME(time_task)")
        dataRecords = cData.fetchall()

        # commit changes
        connData.commit()

        # close connection
        connData.close()

        for record in dataRecords:
            if record[4] == 0:
                row_count = self.tasks_tableWidget.rowCount()
                if record[2] == "-" or record[1] == "-":
                    itemDate = qtw.QTableWidgetItem("-")
                    itemTime = qtw.QTableWidgetItem("-")
                else:
                    itemDate = Qt.QDate.fromString(record[1], "yyyy-MM-dd")
                    itemTime = Qt.QTime.fromString(record[2], "hh:mm")
                    itemTime = qtw.QTableWidgetItem(self.timeleft_func(currentDate, currentTime, itemTime, itemDate))
                    itemDate = qtw.QTableWidgetItem(record[1])
                if itemDate.text() in selectTime or itemTime.text() in selectTime or sort == 3:
                    self.tasks_tableWidget.setRowCount(row_count + 1)
                    self.tasks_tableWidget.setItem(row_count, 0, qtw.QTableWidgetItem(record[0]))
                    itemTime.setTextAlignment(cellOption)
                    itemDate.setTextAlignment(cellOption)
                    self.tasks_tableWidget.setItem(row_count, 1, itemTime)
                    self.tasks_tableWidget.setItem(row_count, 2, itemDate)
                    self.tasks_tableWidget.setItem(row_count, 3, qtw.QTableWidgetItem(str(record[3])))

            else:
                row_count = self.completed_tableWidget.rowCount()
                self.completed_tableWidget.setRowCount(row_count + 1)
                self.completed_tableWidget.setItem(row_count, 0, qtw.QTableWidgetItem(record[0]))
                itemTime = qtw.QTableWidgetItem(record[6])
                itemDate = qtw.QTableWidgetItem(record[5])
                itemTime.setTextAlignment(cellOption)
                itemDate.setTextAlignment(cellOption)
                self.completed_tableWidget.setItem(row_count, 1, itemTime)
                self.completed_tableWidget.setItem(row_count, 2, itemDate)
                self.completed_tableWidget.setItem(row_count, 3, qtw.QTableWidgetItem(str(record[3])))

    # Button function

    # Close/Minimize app
    def leave_pushButton_down(self):
        if self.minimize_radioButton.isChecked():
            self.hide()
        else:
            qtw.QApplication.quit()

    # Refresh the data in the lists
    def refreshtask_pushButton_down(self):
        self.tasks_tableWidget.clearContents()
        self.tasks_tableWidget.setRowCount(0)
        self.completed_tableWidget.clearContents()
        self.completed_tableWidget.setRowCount(0)
        # Resize columns
        self.completed_tableWidget.setColumnWidth(0, 153)
        self.completed_tableWidget.setColumnWidth(1, 80)
        self.completed_tableWidget.setColumnWidth(2, 90)
        self.tasks_tableWidget.setColumnWidth(0, 153)
        self.tasks_tableWidget.setColumnWidth(1, 80)
        self.tasks_tableWidget.setColumnWidth(2, 90)
        self.calendar_tableWidget.setColumnWidth(0, 233)
        self.calendar_tableWidget.setColumnWidth(1, 90)
        # Redownload
        self.download_database()

    # ___________________________________________________________________________#

    # Tab todolist functions
    # Add task to the list
    def addtask_pushButton_down(self):
        # grab name, date and time task
        nameTask = qtw.QTableWidgetItem(self.addtask_lineEdit.text())
        currentDate = Qt.QDate.currentDate()
        currentTime = Qt.QTime.currentTime()
        if self.addtask_lineEdit.text():
            if self.deadlineDate_CheckBox.isChecked() == True:
                dateTask = qtw.QTableWidgetItem(self.deadline_dateEdit.text())

            elif self.deadlineDate_CheckBox.isChecked() == False and self.deadlineTime_CheckBox.isChecked() == True:
                dateTask = qtw.QTableWidgetItem(Qt.QDate.currentDate().toString("yyyy-MM-dd"))

            else:
                dateTask = qtw.QTableWidgetItem("-")

            if self.deadlineTime_CheckBox.isChecked() == True:
                # Time left to deadline
                selectTime = self.deadline_timeEdit.time()

                timeLeft_text = self.timeleft_func(
                    currentDate,
                    currentTime,
                    self.deadline_timeEdit.time(),
                    self.deadline_dateEdit.date(),
                )
                selectTime = selectTime.toString("hh:mm")

            elif self.deadlineTime_CheckBox.isChecked() == False and self.deadlineDate_CheckBox.isChecked() == True:
                selectTime = Qt.QTime(23, 59)
                timeLeft_text = self.timeleft_func(currentDate, currentTime, selectTime, self.deadline_dateEdit.date())
                selectTime = selectTime.toString("hh:mm")

            else:
                selectTime = "-"
                timeLeft_text = qtw.QTableWidgetItem("-")

            # Create database or connect to on
            connData = sqlite3.connect(databaseFile)

            # Cursor
            cData = connData.cursor()
            cData.execute("SELECT id_task FROM todolist")
            busyNumber = cData.fetchall()

            randomNumber = 1
            while randomNumber in busyNumber or randomNumber == 1:
                randomNumber = randint(1, 1000)
            # Add task to database
            cData.execute(
                "INSERT INTO todolist (name_task, date_task, time_task, id_task, completed_task) VALUES (?, ?, ?, ?, 0)",
                (
                    self.addtask_lineEdit.text(),
                    dateTask.text(),
                    selectTime,
                    randomNumber,
                ),
            )

            # commit changes
            connData.commit()

            # close connection
            connData.close()

            row_count = self.tasks_tableWidget.rowCount()
            self.tasks_tableWidget.setRowCount(row_count + 1)
            self.tasks_tableWidget.setItem(row_count, 0, nameTask)
            self.tasks_tableWidget.setItem(row_count, 1, timeLeft_text)
            self.tasks_tableWidget.setItem(row_count, 2, dateTask)
            self.tasks_tableWidget.setItem(row_count, 3, qtw.QTableWidgetItem(str(randomNumber)))
            self.addtask_lineEdit.setText("")
            self.deadline_dateEdit.setDate(Qt.QDate.currentDate())
            self.deadline_timeEdit.setTime(Qt.QTime.currentTime())
            self.refreshtask_pushButton_down()
        else:
            pass

    # Date and time selection fields
    def checked(self):
        # Date edit checkbox
        if self.deadlineDate_CheckBox.isChecked() == True:
            self.deadline_dateEdit.setEnabled(True)
        else:
            self.deadline_dateEdit.setEnabled(False)

        # Time edit checkbox
        if self.deadlineTime_CheckBox.isChecked() == True:
            self.deadline_timeEdit.setEnabled(True)
        else:
            self.deadline_timeEdit.setEnabled(False)

    # Delete task from the list
    def deletetask_pushButton_down(self):
        # select row click by mouse
        clicked = self.tasks_tableWidget.currentRow()

        if clicked > -1:
            items = []
            for column in range(self.tasks_tableWidget.columnCount()):
                item = self.tasks_tableWidget.item(clicked, column)
                if item is not None:
                    items.append(item.text())
                else:
                    items.append("")
            # Create database or connect to on
            connData = sqlite3.connect(databaseFile)

            # Cursor
            cData = connData.cursor()

            # Remove task from db
            cData.execute(
                "DELETE FROM todolist WHERE id_task= ?",
                (items[3],),
            )

            # commit changes
            connData.commit()

            # close connection
            connData.close()
        # remove selected row
        self.tasks_tableWidget.removeRow(clicked)

    # Finish task and move to completed tasks list
    def finishtask_pushButton_down(self):
        # Grab completed task from list
        clickedRow = self.tasks_tableWidget.currentRow()
        if clickedRow > -1:
            items = []
            for column in range(self.tasks_tableWidget.columnCount()):
                item = self.tasks_tableWidget.item(clickedRow, column)
                if item is not None:
                    items.append(item.text())
                else:
                    items.append("")

            # Create database or connect to on
            connData = sqlite3.connect(databaseFile)
            # Cursor
            cData = connData.cursor()
            items[3] = int(items[3])
            currentDate = Qt.QDate.currentDate().toString("yyyy-MM-dd")
            # Add task to database
            cData.execute(
                "UPDATE todolist SET completed_task = 1, finishDate_task = ?, timeLeft_task = ? WHERE id_task = ?",
                (
                    currentDate,
                    items[1],
                    items[3],
                ),
            )

            # commit changes
            connData.commit()

            # close connection
            connData.close()
            self.refreshtask_pushButton_down()

    # Filter list by time
    def timesort(self, index):
        self.tasks_tableWidget.clearContents()
        self.tasks_tableWidget.setRowCount(0)
        self.completed_tableWidget.clearContents()
        self.completed_tableWidget.setRowCount(0)
        self.download_database()

    # ___________________________________________________________________________#

    # Completed tab functions
    # Back select task to todolist
    def uncompletedtask_pushButton_down(self):
        # Grab completed task from list
        clickedRow = self.completed_tableWidget.currentRow()
        if clickedRow > -1:
            items = []
            for column in range(self.completed_tableWidget.columnCount()):
                item = self.completed_tableWidget.item(clickedRow, column)
                if item is not None:
                    items.append(item.text())
                else:
                    items.append("")

            # Create database or connect to on
            connData = sqlite3.connect(databaseFile)
            # Cursor
            cData = connData.cursor()
            items[3] = int(items[3])
            # Add task to database
            cData.execute(
                "UPDATE todolist SET completed_task = 0, finishDate_task = '-' , timeLeft_task = '-' WHERE id_task = ?",
                (items[3],),
            )

            # commit changes
            connData.commit()

            # close connection
            connData.close()
            self.refreshtask_pushButton_down()

    # Delete task from completed list
    def deletetask_pushButton_2_down(self):
        clicked = self.completed_tableWidget.currentRow()

        if clicked > -1:
            items = []
            for column in range(self.completed_tableWidget.columnCount()):
                item = self.completed_tableWidget.item(clicked, column)
                if item is not None:
                    items.append(item.text())
                else:
                    items.append("")
            # Create database or connect to on
            connData = sqlite3.connect(databaseFile)

            # Cursor
            cData = connData.cursor()

            # Remove task from db
            cData.execute(
                "DELETE FROM todolist WHERE id_task= ?",
                (items[3],),
            )

            # commit changes
            connData.commit()

            # close connection
            connData.close()
        # remove selected row
        self.completed_tableWidget.removeRow(clicked)

    # ___________________________________________________________________________#

    # Calendar tab functions
    # Select a date on the calendar
    def selectdate_calendarWidget(self):
        dateSelect = self.calendarWidget.selectedDate()
        # Create database or connect to on
        connData = sqlite3.connect(databaseFile)

        # Cursor
        cData = connData.cursor()

        cData.execute(
            "SELECT * FROM todolist WHERE date_task=? ORDER BY time_task ASC",
            (dateSelect.toString("yyyy-MM-dd"),),
        )
        dataRecords = cData.fetchall()
        # commit changes
        connData.commit()
        # close connection
        connData.close()
        self.calendar_tableWidget.clearContents()
        self.calendar_tableWidget.setRowCount(0)
        self.selectdate_label.setText(dateSelect.toString())
        for record in dataRecords:
            row_count = self.calendar_tableWidget.rowCount()
            self.calendar_tableWidget.setRowCount(row_count + 1)
            self.calendar_tableWidget.setItem(row_count, 0, qtw.QTableWidgetItem(record[0]))
            self.calendar_tableWidget.setItem(row_count, 1, qtw.QTableWidgetItem(record[2]))

    # Return to current date
    def defaultcalendar_pushButton_down(self):
        today = Qt.QDate.currentDate()
        self.calendarWidget.setSelectedDate(today)
        self.calendarWidget.setCurrentPage(today.year(), today.month())

    # ___________________________________________________________________________#

    # Settings tab functions
    # Slider Opacity
    def opacity_horizontalSlider_change(self, value):
        self.opacityPercent_label.setText(f"{value}%")
        opacityValue = value / 100
        self.setWindowOpacity(opacityValue)
        # connect to database
        connData = sqlite3.connect(databaseFile)

        # Cursor
        cData = connData.cursor()

        cData.execute("UPDATE settings SET opacity=?", (value,))
        dataRecords = cData.fetchall()
        # commit changes
        connData.commit()

        # close connection
        connData.close()

    # Exit button setting
    def minimizeExit_state(self, bName):
        if bName.isChecked():
            # connect to database
            connData = sqlite3.connect(databaseFile)

            # Cursor
            cData = connData.cursor()

            if bName.text() == "Minimize":
                cData.execute("UPDATE settings SET minimize=TRUE")
                self.minimize_radioButton.setChecked(True)
            else:
                cData.execute("UPDATE settings SET minimize=FALSE")
                self.exit_radioButton.setChecked(True)

            # commit changes
            connData.commit()

            # close connection
            connData.close()

    # Color mode setting
    def colorMode_state(self, bName):
        if bName.isChecked():
            # connect to database
            connData = sqlite3.connect(databaseFile)

            # Cursor
            cData = connData.cursor()

            if bName == self.lightMode_radioButton:
                cData.execute("UPDATE settings SET color_mode=TRUE")
                uiFile = "ToDoList.ui"
                uiFile = os.path.abspath(uiFile)
                self.colorMode_label.show()

            else:
                cData.execute("UPDATE settings SET color_mode=FALSE")
                uiFile = "ToDoList_dark.ui"
                uiFile = os.path.abspath(uiFile)
                self.colorMode_label.show()

            # commit changes
            connData.commit()

            # close connection
            connData.close()


# Init the app
app = qtw.QApplication(sys.argv)
UIWindow = UI()

# Create tray icon

trayIcon = qtw.QSystemTrayIcon(QIcon(trayIconPng), parent=app)
app.setQuitOnLastWindowClosed(False)

trayIcon_menu = qtw.QMenu()
showApp = QAction("Restore")
exitApp = QAction("Exit")
trayIcon_menu.addAction(showApp)
trayIcon_menu.addAction(exitApp)
trayIcon.setContextMenu(trayIcon_menu)
showApp.triggered.connect(UIWindow.showNormal)
exitApp.triggered.connect(app.quit)
trayIcon.show()


sys.exit(app.exec())
