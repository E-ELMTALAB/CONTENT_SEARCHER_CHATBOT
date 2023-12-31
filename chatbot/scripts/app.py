import sys

import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow , QLabel , QPushButton  , QHBoxLayout  , QSizePolicy , QFrame 
from PyQt5.QtCore import Qt , QSize , QRect , QTimer
from PyQt5.QtGui import QFont, QPixmap, QImage, QIcon, QPainter
from ui import Ui_MainWindow
from ui import ClickableLabel
from chatbot_backend import Chatbot
import pygame
# from pyvidplayer_test import
from test5 import Video_Player_Window

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.video_path = "None"
        self.thumb_nail = None
        self.second = 0

        # Initialize the user interface
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.chatbot = Chatbot()
        self.wellcome()

        # sending the request in the chat by clicking or pressing the return
        self.ui.pushButton.clicked.connect(self.add_user_request)
        self.ui.lineEdit.returnPressed.connect(self.add_user_request)
    #
    # def intro(self, video_path , second):
    #
    #     vid = Video(video_path)
    #     vid.set_size((900, 900))
    #
    #     # Initialize Pygame
    #     pygame.init()
    #
    #     # Set the screen dimensions (width, height)
    #     screen_width = 800
    #     screen_height = 600
    #
    #     # Create the Pygame screen
    #     SCREEN = pygame.display.set_mode((screen_width, screen_height))
    #
    #     print(vid.get_file_data())
    #     # second = ((frame * 120) // 25) - 5
    #     print("the frame : " + str(second))
    #     vid.seek(second)
    #     while True:
    #         vid.draw(SCREEN, (0, 0))
    #         pygame.display.update()
    #         for event in pygame.event.get():
    #             if event.type == pygame.MOUSEBUTTONDOWN:
    #                 vid.close()

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

        self.receive_process_response(text)

    def receive_process_response(self , text):
        #send request for the chatbot server
        received_text , responses_info = self.chatbot.async_send_message(text)
        if responses_info["intent"]["name"] == "request_for_picture":
            value = responses_info["entities"][0]["value"]
            objects, actions = self.chatbot.process_request(value)
            image , image_path = self.chatbot.actions.find_image_request(request_objects=objects, request_actions=actions)
            self.send_image(image_path)

        elif responses_info["intent"]["name"] == "request_for_video":
            value = responses_info["entities"][0]["value"]
            objects, actions = self.chatbot.process_request(value)
            self.video_path , self.second , self.frame_index = self.chatbot.actions.find_video_request(request_objects=objects,request_actions=actions)
            if self.second != 0:
                self.waiting_for_answer = 1
                # received_text , responses_infor = self.chatbot.async_send_message("found_good_match")
                self.send_response("I have found a good match .Would you like me to take you to the exact scene where your request happens ?")

        elif (responses_info["intent"]["name"] == "affirm") and self.waiting_for_answer:
            cap = cv2.VideoCapture(self.video_path)
            cap.set(cv2.CAP_PROP_POS_FRAMES, self.frame_index)
            _ , frame = cap.read()
            height, width, channel = frame.shape
            bytes_per_line = width * channel
            frame = self.overlay_button(frame)
            self.thumb_nail = QImage(frame.data , width , height , bytes_per_line , QImage.Format_BGR888)
            self.send_video_label()
            # self.play_video()

        elif (responses_info["intent"]["name"] == "deny") and self.waiting_for_answer:
            self.frame_index = 0
            self.second = 0
            cap = cv2.VideoCapture(self.video_path)
            cap.set(cv2.CAP_PROP_POS_FRAMES, self.frame_index)
            _ , frame = cap.read()
            height, width, channel = frame.shape
            bytes_per_line = width * channel
            frame = self.overlay_button(frame)
            self.thumb_nail = QImage(frame.data , width , height , bytes_per_line , QImage.Format_BGR888)
            self.send_video_label()
            # self.play_video()

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

    def send_video_label(self):
        text = self.ui.lineEdit.text()
        window = QFrame()
        window.setStyleSheet("background-color:white;")
        hbox_layout = QHBoxLayout()
        # self.new_label = QLabel(text, self)
        self.clickableLabel = ClickableLabel("Click Me!")
        self.clickableLabel.setStyleSheet("border: 2px solid #3498db;\n")
        self.clickableLabel.setFixedWidth(500)
        font = QFont()
        font.setPointSize(12)
        self.clickableLabel.setFont(font)
        self.clickableLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)  # Set the size policy
        self.clickableLabel.setWordWrap(True)  # Enable text wrapping
        self.set_thumb_nail(self.thumb_nail)
        self.clickableLabel.clicked.connect(self.play_video)  # Connect the custom signal
        hbox_layout.addWidget(self.clickableLabel)
        hbox_layout.setAlignment(Qt.AlignLeft)
        window.setLayout(hbox_layout)
        self.ui.vbox_layout.addWidget(window)
        QTimer.singleShot(20, lambda: self.scrollToBottom(self.ui.scrollArea)) # used for scrolling to the buttom of the chat


    # # responding in the chat
    # def send_video_label(self , text):
    #     window = QFrame()
    #     window.setStyleSheet("background-color:white;")
    #     hbox_layout = QHBoxLayout()
    #     self.video_label = QPushButton(self)
    #     pixmap = QPixmap.fromImage(self.thumb_nail)
    #     width = 500
    #     height = int(pixmap.height() * width / pixmap.width())
    #     # pixmap = pixmap.scaled(width, height)
    #     icon = QIcon(pixmap)
    #     self.video_label.setIconSize(QSize(height, width))
    #     self.video_label.setIcon(icon)
    #     self.video_label.setStyleSheet("border: 2px solid #3498db;\n")
    #     self.video_label.clicked.connect(self.play_video)
    #     font = QFont()
    #     # font.setPointSize(12)  # Change the font size to 16 points
    #     # self.video_label.setFont(font)
    #     self.video_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)  # Set the size policy
    #     # # Set the maximum width for the label (adjust this value to your desired threshold)
    #     self.video_label.setMaximumWidth(500)
    #     # self.video_label.setMinimumWidth(500)
    #     # self.video_label.setWordWrap(True)  # Enable text wrapping
    #     self.video_label.setMinimumHeight(50)
    #     hbox_layout.addWidget(self.video_label)
    #     hbox_layout.setAlignment(Qt.AlignLeft)
    #     window.setLayout(hbox_layout)
    #     self.ui.vbox_layout.addWidget(window)
    #     QTimer.singleShot(20, lambda: self.scrollToBottom(self.ui.scrollArea))

    def play_video(self):
        # self.intro(self.video_path , self.second)
        self.player = Video_Player_Window()
        self.player.intro(self.video_path , self.second)

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

    def overlay_button(self, overlay_image):

        play_image = cv2.imread(r"C:\Users\Morvarid\Downloads\play-button-icon-Graphics-1-6-580x386.jpg")
        play_image = cv2.bitwise_not(play_image)
        play_image = cv2.resize(play_image, (200, 160))
        play_height, play_width, play_channel = play_image.shape
        overlay_height, overlay_width, overlay_channel = overlay_image.shape
        b1 = (overlay_height // 2)
        s1 = (play_height // 2)
        b2 = (overlay_width // 2)
        s2 = (play_width // 2)
        center = (b1, b2)
        top_left_corner = (b1 - s1, b2 - s2)
        top_right_corner = (b1 + s1, b2 - s2)
        bottom_left_corner = (b1 - s1, b2 + s2)
        bottom_right_corner = (b1 + s1, b2 + s2)

        # overlay_image = cv2.circle(overlay_image , center , 5 , (255 , 0 , 0) , -1)
        #
        # overlay_image = cv2.circle(overlay_image , top_left_corner ,5 , (255 , 255 , 0) , -1)
        # overlay_image = cv2.circle(overlay_image , top_right_corner ,5 , (255 , 255 , 0) , -1)
        # overlay_image = cv2.circle(overlay_image , bottom_left_corner ,5 , (255 , 255 , 0) , -1)
        # overlay_image = cv2.circle(overlay_image , bottom_right_corner ,5 , (255 , 255 , 0) , -1)

        cropped = overlay_image[top_left_corner[0]: bottom_right_corner[0], top_right_corner[1]: bottom_right_corner[1]]

        # Add the two images together
        combined_image = cv2.add(cropped, play_image)

        overlay_image[top_left_corner[0]: bottom_right_corner[0],
        top_right_corner[1]: bottom_right_corner[1]] = combined_image

        return overlay_image

        # Display or save the combined image
        # cv2.imshow("cropped", cropped)
        # cv2.imshow('Combined Images', overlay_image)
        # cv2.imshow("combined", combined_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def set_thumb_nail(self , thumb_nail):
        # Load the image using QPixmap
        pixmap = QPixmap.fromImage(thumb_nail)
        # Set the width of the image to 500 and calculate the proportional height
        width = 500
        height = int(pixmap.height() * width / pixmap.width())
        pixmap = pixmap.scaled(width, height)

        # Load the background and overlay images as QPixmaps
        # background = QPixmap(background_path)
        # overlay = QPixmap(r"C:\Users\Morvarid\Downloads\play-button-icon-Graphics-1-6-580x386.jpg")
        # overlay = overlay.scaled(110 , 90)
        #
        # # Calculate the center position for the overlay image
        # center_x = (pixmap.width() - overlay.width()) // 2
        # center_y = (pixmap.height() - overlay.height()) // 2
        #
        # # Create a painter to draw the overlay on top of the background at the center position
        # painter = QPainter(pixmap)
        # painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        # # Set the overlay image's alpha channel to control transparency
        # overlay_with_alpha = overlay.copy()
        #
        # painter.setOpacity(40 * 0.01)
        # painter.drawPixmap(center_x, center_y, overlay)
        # # painter.drawPixmap(center_x, center_y, overlay)
        # painter.end()
        # Set the pixmap to the label
        self.clickableLabel.setPixmap(pixmap)
        self.clickableLabel.setMaximumHeight(pixmap.height())


    def scrollToBottom(self, scroll_area):
        # Scroll the scroll area to the bottom
        v_scroll_bar = scroll_area.verticalScrollBar()
        v_scroll_bar.setValue(v_scroll_bar.maximum())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
