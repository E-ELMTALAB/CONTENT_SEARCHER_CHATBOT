import sys
from PyQt5.QtWidgets import QApplication, QMainWindow , QLabel , QPushButton  , QHBoxLayout  , QSizePolicy , QFrame 
from PyQt5.QtCore import Qt , QSize , QRect , QTimer
from PyQt5.QtGui import QFont , QPixmap
from ui import Ui_MainWindow
from chatbot_backend import Chatbot

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the user interface
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.chatbot = Chatbot()
        self.wellcome()

        # sending the request in the chat by clicking or pressing the return
        self.ui.pushButton.clicked.connect(self.add_user_request)
        self.ui.lineEdit.returnPressed.connect(self.add_user_request)

    # used for the first chat of the bot
    def wellcome(self):
        wellcome_text = "Hi there! I'm the image search assistant. ask me to find images or ask me to help you with the commands..."
        self.send_response(wellcome_text)

    # used for giving examples when needed
    def give_examples(self):
        example_list = ["find me a picture of a woman holding a camera" , "can you give me an image of an elephant in the forest" , "give me a picture of a bunch of kids playing in the field"]
        self.send_response("you can say things like ...")
        for example in example_list:
            self.send_response(example)

    # sending use request and also printing it in the chat
    def add_user_request(self):
        text = self.ui.lineEdit.text()
        self.ui.lineEdit.clear()
        window = QFrame()
        window.setStyleSheet("background-color:white;")
        hbox_layout = QHBoxLayout()
        new_label = QLabel(text, self)
        new_label.setStyleSheet("border: 2px solid #6133a1;\n")
        font = QFont()
        font.setPointSize(12)  # Change the font size to 16 points
        new_label.setFont(font)
        new_label.adjustSize()
        new_label.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)  # Set the size policy
        # Set the maximum width for the label (adjust this value to your desired threshold)
        new_label.setMaximumWidth(500)
        new_label.setWordWrap(True)  # Enable text wrapping
        new_label.setMinimumHeight(50)
        hbox_layout.addWidget(new_label)
        hbox_layout.setAlignment(Qt.AlignRight)
        self.ui.vbox_layout.addLayout(hbox_layout)
        QTimer.singleShot(20, lambda: self.scrollToBottom(self.ui.scrollArea))

        #send request for the chatbot server
        received_text , responses_info = self.chatbot.async_send_message(text)
        if responses_info["intent"]["name"] == "request_for_picture":
            value = responses_info["entities"][0]["value"]
            objects, actions = self.chatbot.process_request(value)
            image , image_path = self.chatbot.actions.find_request(request_objects=objects, request_actions=actions)
            self.send_image(image_path)
        else:
            self.send_response(received_text)

        if received_text == "give_examples":
            self.give_examples()

    # responding in the chat
    def send_response(self , text):
        window = QFrame()
        window.setStyleSheet("background-color:white;")
        hbox_layout = QHBoxLayout()
        self.new_label = QLabel(text, self)
        self.new_label.setStyleSheet("border: 2px solid #3498db;\n")
        font = QFont()
        font.setPointSize(12)  # Change the font size to 16 points
        self.new_label.setFont(font)
        self.new_label.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)  # Set the size policy
        # Set the maximum width for the label (adjust this value to your desired threshold)
        self.new_label.setMaximumWidth(500)
        self.new_label.setWordWrap(True)  # Enable text wrapping
        self.new_label.setMinimumHeight(50)
        hbox_layout.addWidget(self.new_label)
        hbox_layout.setAlignment(Qt.AlignLeft)
        window.setLayout(hbox_layout)
        self.ui.vbox_layout.addWidget(window)
        QTimer.singleShot(20, lambda: self.scrollToBottom(self.ui.scrollArea))

    # function for sending images in the chat
    def send_image(self , image_path):
        text = self.ui.lineEdit.text()
        window = QFrame()
        window.setStyleSheet("background-color:white;")
        hbox_layout = QHBoxLayout()
        self.new_label = QLabel(text, self)
        self.new_label.setStyleSheet("border: 2px solid #3498db;\n")
        self.new_label.setFixedWidth(500)
        font = QFont()
        font.setPointSize(12)
        self.new_label.setFont(font)
        self.new_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)  # Set the size policy
        self.new_label.setWordWrap(True)  # Enable text wrapping
        height = self.set_image(image_path)
        hbox_layout.addWidget(self.new_label)
        hbox_layout.setAlignment(Qt.AlignLeft)
        window.setLayout(hbox_layout)
        self.ui.vbox_layout.addWidget(window)
        QTimer.singleShot(20, lambda: self.scrollToBottom(self.ui.scrollArea)) # used for scrolling to the buttom of the chat

    # used for setting the image on the label
    def set_image(self, image_path):
        # Load the image using QPixmap
        pixmap = QPixmap(image_path)
        # Set the width of the image to 500 and calculate the proportional height
        width = 500
        height = int(pixmap.height() * width / pixmap.width())
        pixmap = pixmap.scaled(width, height)
        # Set the pixmap to the label
        self.new_label.setPixmap(pixmap)
        self.new_label.setMaximumHeight(pixmap.height())
        return height


    def scrollToBottom(self, scroll_area):
        # Scroll the scroll area to the bottom
        v_scroll_bar = scroll_area.verticalScrollBar()
        v_scroll_bar.setValue(v_scroll_bar.maximum())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
