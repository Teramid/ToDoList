from itertools import count
import typing
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as Qt
from PyQt6 import uic
import sqlite3
from random import randint
import sys


# Create database or connect to on
connData = sqlite3.connect("ToDoList.db")

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
    autostart BOOLEAN,
    minimize BOOLEAN,
    color_mode BOOLEAN)
    """
)

# Download last settigns
cData.execute("SELECT * FROM settings")
settingsData = cData.fetchone()
if settingsData is None:
    cData.execute(
        "INSERT INTO settings(opacity, minimize, color_mode, autostart) VALUES(100, TRUE, FALSE, FALSE)"
    )
    cData.execute("SELECT * FROM settings")
    settingsData = cData.fetchone()


opacitySettings = settingsData[0]
autostartSettings = settingsData[1]
minimizeSettings = settingsData[2]
colorSettings = settingsData[3]

# commit changes
connData.commit()

# close connection
connData.close()


class UI(qtw.QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load the ui file
        uic.loadUi("ToDoList.ui", self)

        # Define the buttons
        self.leave_pushButton = self.findChild(qtw.QPushButton, "leave_pushButton")
        self.refreshtask_pushButton = self.findChild(
            qtw.QPushButton, "refreshtask_pushButton"
        )
        self.addtask_pushButton = self.findChild(qtw.QPushButton, "addtask_pushButton")
        self.deletetask_pushButton = self.findChild(
            qtw.QPushButton, "deletetask_pushButton"
        )
        self.finishtask_pushButton = self.findChild(
            qtw.QPushButton, "finishtask_pushButton"
        )
        self.defaultcalendar_pushButton = self.findChild(
            qtw.QPushButton, "defaultcalendar_pushButton"
        )
        self.uncompletedtask_pushButton = self.findChild(
            qtw.QPushButton, "uncompletedtask_pushButton"
        )
        self.deletetask_pushButton_2 = self.findChild(
            qtw.QPushButton, "deletetask_pushButton_2"
        )

        # Define checkboxes
        # Tasks tab checkboxes
        self.deadlineDate_CheckBox = self.findChild(
            qtw.QCheckBox, "deadlineDate_CheckBox"
        )
        self.deadlineTime_CheckBox = self.findChild(
            qtw.QCheckBox, "deadlineTime_CheckBox"
        )
        self.autoStart_checkBox = self.findChild(qtw.QCheckBox, "autoStart_checkBox")
        # Settings tab checkboxes
        self.exit_checkBox = self.findChild(qtw.QCheckBox, "exit_checkBox")
        self.minimize_checkBox = self.findChild(qtw.QCheckBox, "minimize_checkBox")
        self.darkMode_checkBox = self.findChild(qtw.QCheckBox, "darkMode_checkBox")
        self.lightMode_checkBox = self.findChild(qtw.QCheckBox, "lightMode_checkBox")

        # Define the tab, table, combo
        self.tabWidget = self.findChild(qtw.QTabWidget, "tabWidget")
        self.tasks_tableWidget = self.findChild(qtw.QTableWidget, "tasks_tableWidget")
        self.calendar_tableWidget = self.findChild(
            qtw.QTableWidget, "calendar_tableWidget"
        )
        self.completed_tableWidget = self.findChild(
            qtw.QTableWidget, "completed_tableWidget"
        )
        self.timesort_comboBox = self.findChild(qtw.QComboBox, "timesort_comboBox")
        self.selectdate_label = self.findChild(qtw.QLabel, "selectdate_label")
        self.opacityPercent_label = self.findChild(qtw.QLabel, "opacityPercent_label")

        # table function
        # self.tasks_tableWidget.itemChanged.connect(self.refreshtask_pushButton_down)

        # Define textEdit
        self.addtask_lineEdit = self.findChild(qtw.QLineEdit, "addtask_lineEdit")

        # Define stuff
        self.deadline_dateEdit = self.findChild(qtw.QDateEdit, "deadline_dateEdit")
        self.deadline_timeEdit = self.findChild(qtw.QTimeEdit, "deadline_timeEdit")
        self.calendarWidget = self.findChild(qtw.QCalendarWidget, "calendarWidget")
        self.opacity_horizontalSlider = self.findChild(
            qtw.QSlider, "opacity_horizontalSlider"
        )

        # settime
        self.deadline_dateEdit.setDate(Qt.QDate.currentDate())
        self.deadline_timeEdit.setTime(Qt.QTime.currentTime())
        self.deadline_dateEdit.setMinimumDate(Qt.QDate.currentDate())

        # Click Button
        self.leave_pushButton.clicked.connect(self.leave_pushButton_down)
        self.refreshtask_pushButton.clicked.connect(self.refreshtask_pushButton_down)
        self.addtask_pushButton.clicked.connect(self.addtask_pushButton_down)
        self.deletetask_pushButton.clicked.connect(self.deletetask_pushButton_down)
        self.finishtask_pushButton.clicked.connect(self.finishtask_pushButton_down)
        self.defaultcalendar_pushButton.clicked.connect(
            self.defaultcalendar_pushButton_down
        )
        self.uncompletedtask_pushButton.clicked.connect(
            self.uncompletedtask_pushButton_down
        )
        self.deletetask_pushButton_2.clicked.connect(self.deletetask_pushButton_2_down)

        # Calendar button
        self.calendarWidget.selectionChanged.connect(self.selectdate_calendarWidget)

        # Update checkbox
        self.deadlineDate_CheckBox.toggled.connect(self.checked)
        self.deadlineTime_CheckBox.toggled.connect(self.checked)

        # Slider
        self.opacity_horizontalSlider.valueChanged.connect(
            self.opacity_horizontalSlider_change
        )
        # Slider properties
        self.opacity_horizontalSlider.setMinimum(1)
        self.opacity_horizontalSlider.setMaximum(100)
        self.opacity_horizontalSlider.setValue(opacitySettings)
        self.opacityPercent_label.setText(f"{self.opacity_horizontalSlider.value()}%")

        # Checkboxes state
        self.autoStart_checkBox.setChecked(autostartSettings)
        self.autoStart_checkBox.toggled.connect(self.autostart_checked)
        if minimizeSettings == True:
            self.minimize_checkBox.setChecked(True)
            self.exit_checkBox.setChecked(False)
        else:
            self.minimize_checkBox.setChecked(False)
            self.exit_checkBox.setChecked(True)
        self.minimize_checkBox.toggled.connect(self.minimizeExit_checked)
        self.exit_checkBox.toggled.connect(self.minimizeExit_checked)

        # Set column size
        # tasktable
        self.tasks_tableWidget.setColumnWidth(0, 170)
        self.tasks_tableWidget.setColumnWidth(1, 80)
        self.tasks_tableWidget.setColumnWidth(2, 90)
        # calendar table
        self.calendar_tableWidget.setColumnWidth(0, 245)
        self.calendar_tableWidget.setColumnWidth(1, 90)
        # completed table
        self.completed_tableWidget.setColumnWidth(0, 170)
        self.completed_tableWidget.setColumnWidth(1, 80)
        self.completed_tableWidget.setColumnWidth(2, 90)
        # Hidden column
        self.tasks_tableWidget.setColumnHidden(3, True)
        self.completed_tableWidget.setColumnHidden(3, True)

        # Download data
        self.download_database()

        # Window attribute
        self.setWindowFlags(Qt.Qt.WindowType.FramelessWindowHint)
        # self.setAttribute(Qt.Qt.WidgetAttribute.WA_TranslucentBackground)

        # show the app
        self.show()

    # Additional functions
    # Move window
    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
        self.dragPos = event.globalPosition().toPoint()
        event.accept()

    def timeleft_func(self, currentDate, currentTime, selectTime, selectDate):
        current_date_time = Qt.QDateTime(currentDate, currentTime)
        selected_date_time = Qt.QDateTime(selectDate, selectTime)
        timeLeft = current_date_time.daysTo(selected_date_time)

        if current_date_time.secsTo(selected_date_time) > 0:
            if current_date_time.secsTo(selected_date_time) < 86400:
                timeLeft = int(current_date_time.secsTo(selected_date_time) / 3600)
                timeLeft_text = (
                    f"{timeLeft} hours" if timeLeft > 1 else f"{timeLeft} hour"
                )
                if timeLeft < 1:
                    timeLeft = int(
                        (current_date_time.secsTo(selected_date_time) % 3600) / 60
                    )
                    timeLeft_text = (
                        f"{timeLeft} minutes" if timeLeft > 1 else f"{timeLeft} minute"
                    )
            else:
                timeLeft_text = (
                    f"{timeLeft} days" if timeLeft > 1 else f"{timeLeft} day"
                )

            timeLeft_text = qtw.QTableWidgetItem(timeLeft_text)
        else:
            timeLeft_text = qtw.QTableWidgetItem("Time has passed")
        return timeLeft_text

    # Slider Opacity
    def opacity_horizontalSlider_change(self, value):
        self.opacityPercent_label.setText(f"{value}%")
        opacityValue = value / 100
        self.setWindowOpacity(opacityValue)
        # connect to database
        connData = sqlite3.connect("ToDoList.db")

        # Cursor
        cData = connData.cursor()

        cData.execute("UPDATE settings SET opacity=?", (value,))
        dataRecords = cData.fetchall()
        # commit changes
        connData.commit()

        # close connection
        connData.close()

    # Download all data from the database
    def download_database(self):
        currentDate = Qt.QDate.currentDate()
        currentTime = Qt.QTime.currentTime()
        # connect to database
        connData = sqlite3.connect("ToDoList.db")

        # Cursor
        cData = connData.cursor()

        cData.execute(
            "SELECT * FROM todolist ORDER BY date_task ASC, time_task ASC, id_task, completed_task"
        )
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
                    itemDate = record[1].split(".")
                    itemTime = record[2].split(":")
                    itemDate = Qt.QDate(
                        int(itemDate[2]), int(itemDate[1]), int(itemDate[0])
                    )
                    itemTime = Qt.QTime(int(itemTime[0]), int(itemTime[1]))
                    self.tasks_tableWidget.setRowCount(row_count + 1)
                    itemTime = qtw.QTableWidgetItem(
                        self.timeleft_func(currentDate, currentTime, itemTime, itemDate)
                    )
                    itemDate = qtw.QTableWidgetItem(record[1])
                self.tasks_tableWidget.setRowCount(row_count + 1)
                self.tasks_tableWidget.setItem(
                    row_count, 0, qtw.QTableWidgetItem(record[0])
                )
                self.tasks_tableWidget.setItem(
                    row_count, 1, qtw.QTableWidgetItem(itemTime)
                )
                self.tasks_tableWidget.setItem(
                    row_count, 2, qtw.QTableWidgetItem(itemDate)
                )
                self.tasks_tableWidget.setItem(
                    row_count, 3, qtw.QTableWidgetItem(str(record[3]))
                )

            else:
                row_count = self.completed_tableWidget.rowCount()
                self.completed_tableWidget.setRowCount(row_count + 1)
                self.completed_tableWidget.setItem(
                    row_count, 0, qtw.QTableWidgetItem(record[0])
                )
                self.completed_tableWidget.setItem(
                    row_count, 1, qtw.QTableWidgetItem(record[1])
                )
                self.completed_tableWidget.setItem(
                    row_count, 2, qtw.QTableWidgetItem(record[2])
                )
                self.completed_tableWidget.setItem(
                    row_count, 3, qtw.QTableWidgetItem(str(record[3]))
                )

    # Button function
    def leave_pushButton_down(self):
        qtw.QApplication.exit()

    def refreshtask_pushButton_down(self):
        self.tasks_tableWidget.clearContents()
        self.tasks_tableWidget.setRowCount(0)
        self.completed_tableWidget.clearContents()
        self.completed_tableWidget.setRowCount(0)
        self.download_database()

    def selectdate_calendarWidget(self):
        dateSelect = self.calendarWidget.selectedDate()
        # Create database or connect to on
        connData = sqlite3.connect("ToDoList.db")

        # Cursor
        cData = connData.cursor()

        cData.execute(
            "SELECT * FROM todolist WHERE date_task=? ORDER BY time_task ASC",
            (dateSelect.toString("dd.MM.yyyy"),),
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
            self.calendar_tableWidget.setItem(
                row_count, 0, qtw.QTableWidgetItem(record[0])
            )
            self.calendar_tableWidget.setItem(
                row_count, 1, qtw.QTableWidgetItem(record[2])
            )

    def defaultcalendar_pushButton_down(self):
        today = Qt.QDate.currentDate()
        self.calendarWidget.setSelectedDate(today)
        self.calendarWidget.setCurrentPage(today.year(), today.month())

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
            connData = sqlite3.connect("ToDoList.db")
            # Cursor
            cData = connData.cursor()
            items[3] = int(items[3])
            # Add task to database
            cData.execute(
                "UPDATE todolist SET completed_task = 0 WHERE id_task= ?",
                (items[3],),
            )

            # commit changes
            connData.commit()

            # close connection
            connData.close()
            self.refreshtask_pushButton_down()

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
            connData = sqlite3.connect("ToDoList.db")
            # Cursor
            cData = connData.cursor()
            items[3] = int(items[3])
            # Add task to database
            cData.execute(
                "UPDATE todolist SET completed_task = 1 WHERE id_task= ?",
                (items[3],),
            )

            # commit changes
            connData.commit()

            # close connection
            connData.close()
            self.refreshtask_pushButton_down()

    def addtask_pushButton_down(self):
        # grab name, date and time task
        nameTask = qtw.QTableWidgetItem(self.addtask_lineEdit.text())
        currentDate = Qt.QDate.currentDate()
        currentTime = Qt.QTime.currentTime()
        if self.addtask_lineEdit.text():
            if self.deadlineDate_CheckBox.isChecked() == True:
                dateTask = qtw.QTableWidgetItem(self.deadline_dateEdit.text())

            elif (
                self.deadlineDate_CheckBox.isChecked() == False
                and self.deadlineTime_CheckBox.isChecked() == True
            ):
                dateTask = qtw.QTableWidgetItem(
                    Qt.QDate.currentDate().toString("dd.MM.yyyy")
                )

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

            elif (
                self.deadlineTime_CheckBox.isChecked() == False
                and self.deadlineDate_CheckBox.isChecked() == True
            ):
                selectTime = Qt.QTime(23, 59)
                timeLeft_text = self.timeleft_func(
                    currentDate, currentTime, selectTime, self.deadline_dateEdit.date()
                )
                selectTime = selectTime.toString("hh:mm")

            else:
                selectTime = "-"
                timeLeft_text = qtw.QTableWidgetItem("-")

            # Create database or connect to on
            connData = sqlite3.connect("ToDoList.db")

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
            self.tasks_tableWidget.setItem(
                row_count, 3, qtw.QTableWidgetItem(str(randomNumber))
            )
            self.addtask_lineEdit.setText("")
            self.deadline_dateEdit.setDate(Qt.QDate.currentDate())
            self.deadline_timeEdit.setTime(Qt.QTime.currentTime())
            self.refreshtask_pushButton_down()
        else:
            pass

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
            connData = sqlite3.connect("ToDoList.db")

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
            connData = sqlite3.connect("ToDoList.db")

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

    # checkbox fucntion

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

    def autostart_checked(self):
        # connect to db
        connData = sqlite3.connect("ToDoList.db")

        # Cursor
        cData = connData.cursor()

        if self.autoStart_checkBox.isChecked() == True:
            cData.execute("UPDATE settings SET autostart = TRUE")

            """ADD autostart function"""

        else:
            cData.execute("UPDATE settings SET autostart = FALSE")
        # commit changes
        connData.commit()

        # close connection
        connData.close()

    def minimizeExit_checked(self):
        # minimize checkbox
        if self.minimize_checkBox.isChecked() == True:
            self.exit_checkBox.setChecked(False)

        # exit checkbox
        if self.exit_checkBox.isChecked() == True:
            self.minimize_checkBox.setChecked(False)


# Init the app
app = qtw.QApplication(sys.argv)
UIWindow = UI()
app.exec()
