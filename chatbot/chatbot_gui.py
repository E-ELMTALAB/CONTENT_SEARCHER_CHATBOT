import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('ChatBot UI')
        self.setGeometry(100, 100, 400, 500)

        # Create the central widget and main layout
        central_widget = QWidget(self)
        main_layout = QVBoxLayout(central_widget)

        # Text display area
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        main_layout.addWidget(self.text_display)

        # Input area
        self.input_text = QTextEdit()
        main_layout.addWidget(self.input_text)

        # Send button
        send_button = QPushButton('Send', self)
        send_button.clicked.connect(self.on_send_button_clicked)
        main_layout.addWidget(send_button)

        # Set the central widget and show the main window
        self.setCentralWidget(central_widget)
        self.show()

    def on_send_button_clicked(self):
        user_input = self.input_text.toPlainText()
        if user_input.strip():
            self.display_user_message(user_input)
            response = get_chatbot_response(user_input)
            self.display_chatbot_message(response)
            self.input_text.clear()

    def display_user_message(self, message):
        self.text_display.append("You: " + message)

    def display_chatbot_message(self, message):
        self.text_display.append(message)


def get_chatbot_response(user_input):
    # Replace this with your actual chatbot logic
    response = "ChatBot: Hello, I am a simple chatbot. You said: " + user_input
    return response


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChatWindow()
    sys.exit(app.exec_())
