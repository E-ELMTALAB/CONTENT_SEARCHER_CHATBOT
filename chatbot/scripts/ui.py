# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designergiwDLH.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                          QMetaObject, QObject, QPoint, QRect,
                          QSize, QTime, QUrl, Qt, pyqtSignal)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt5.QtWidgets import (QApplication, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QScrollArea, QSizePolicy, QStatusBar,
    QWidget , QLabel , QVBoxLayout)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1093, 874)
        MainWindow.setStyleSheet(u"background-color:rgb(83, 101, 116)")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(20, 30, 1041, 711))
        self.scrollArea.setStyleSheet(u"background-color: white; border-radius:10px;")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1039, 709))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        # Set the scroll area properties
        self.scrollArea.verticalScrollBar().setStyleSheet('''
            QScrollBar:vertical {
                border: 1px solid #808080;
                background: #f0f0f0;
                width: 15px;
            }

            QScrollBar::handle:vertical {
                background: #c0c0c0;
                min-height: 20px;
            }

            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }
        ''')
        # self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.scrollToBottom(self.scrollArea)

        self.vbox_layout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.vbox_layout.setAlignment(Qt.AlignTop) 
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(20, 770, 1061, 61))
        self.widget.setStyleSheet(u"")
        self.lineEdit = QLineEdit(self.widget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setPlaceholderText("Chat with the bot...")
        self.lineEdit.setGeometry(QRect(0, 0, 981, 61))
        font = QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setKerning(False)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet(u"        QLineEdit {\n"
"			background-color:white;\n"
"            border: 2px solid #3498db;\n"
"            border-radius: 10px;\n"
"            padding: 8px;\n"
"            font-size: 20px;\n"
"        }\n"
"        QLineEdit:focus {\n"
"            border: 2px solid #2980b9;\n"
"        }")
        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(990, 0, 61, 61))
        self.pushButton.setStyleSheet(u"background-color:rgb(22, 172, 140);\n"
"border: none;\n"
"border-radius: 7px;")
        icon = QIcon()
        icon.addFile(u"C:/Users/Morvarid/Downloads/373675-200.png", QSize(), QIcon.Active, QIcon.On)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QSize(30, 50))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1093, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.labels = {}
        self.vertical_position = 0
        # Generate a bunch of buttons and add them to the scroll area
        # button_width = 100
        # button_height = 50
        # button_margin = 10
        # num_buttons = 100  # You can adjust the number of buttons as per your requirement

        # for i in range(num_buttons):
        #     button = QPushButton(self.scrollAreaWidgetContents)
        #     button.setObjectName(f"button_{i}")
        #     button.setText(f"Button {i+1}")
        #     button.setGeometry(QRect((i % 5) * (button_width + button_margin),
        #                              (i // 5) * (button_height + button_margin),
        #                              button_width, button_height))
        #     button.setStyleSheet(u"background-color:rgb(255, 255, 255);\n"
        #                          "border: 1px solid black;")

        # # Calculate the required height of the scroll area based on the number of buttons
        # total_rows = (num_buttons + 4) // 5  # 5 buttons per row
        # scroll_area_height = total_rows * (button_height + button_margin) + button_margin
        # self.scrollAreaWidgetContents.setMinimumSize(QSize(899, scroll_area_height))
        # self.scrollAreaWidgetContents.setMaximumSize(QSize(899, scroll_area_height))


        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        # self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"request an image here ...", None))
        self.pushButton.setText("")
    # retranslateUi

    def create_label(self, text):
        label = QLabel(self.scrollAreaWidgetContents)
        label.setObjectName(f"label_{len(self.labels)}")
        label.setText(text)
        label.setStyleSheet(u"background-color:rgb(255, 255, 255);\n"
                            "border: 1px solid black;")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        label.setWordWrap(True)
        label.adjustSize()

        # Add the label to the labels dictionary
        self.labels[label.objectName()] = label

        # Position the label in the scroll area
        label.setGeometry(10, len(self.labels) * 60, label.sizeHint().width(), 50)

        # Update the minimum size of the scroll area
        scroll_area_height = len(self.labels) * 60 + 50
        self.scrollAreaWidgetContents.setMinimumSize(QSize(899, scroll_area_height))
        self.scrollAreaWidgetContents.setMaximumSize(QSize(899, scroll_area_height))

        self.scrollArea.setWidgetResizable(True)

    def on_lineEdit_returnPressed(self):
        text = self.lineEdit.text()
        if text.strip():
            self.create_label(text)
            self.lineEdit.clear()

    # def scrollToBottom(self, scroll_area):
    #     # Scroll the scroll area to the bottom
    #     v_scroll_bar = scroll_area.verticalScrollBar()
    #     v_scroll_bar.setValue(v_scroll_bar.maximum())
class ClickableLabel(QLabel):
    clicked = pyqtSignal()  # Custom signal

    def __init__(self, text):
        super().__init__(text)

    def mousePressEvent(self, event):
        self.clicked.emit()  # Emit the custom signal when clicked


