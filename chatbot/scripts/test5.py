import pygame
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, \
    QSlider, QStyle, QSizePolicy, QFileDialog, QAction
import sys
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette, QImage, QPixmap
from PyQt5.QtCore import Qt, QUrl
from pyvidplayer_test import Video



class Video_Player_Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt5 Media Player")
        self.setGeometry(350, 100, 300, 300)
        self.setWindowIcon(QIcon('player.png'))
        # self.vid = Video(r"C:\python\NLP\content_searcher\data\videos\Schwarm von Golden Retriever Welpen.mp4")

        p =self.palette()
        p.setColor(QPalette.Window , Qt.black)
        self.setPalette(p)
        self.run = True

        self.init_ui()


        self.show()


    def init_ui(self):

        # create media player object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)


        #create videowidget object

        videowidget = QVideoWidget()
        self.video_label = QLabel("im the video player")
        self.video_label.setStyleSheet("background-color:blue;")
        print("label width : " + str(self.video_label.width()))


        #create open button
        openBtn = QPushButton('Open Video')
        openBtn.clicked.connect(self.open_file)



        #create button for playing
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(True)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))


        #create slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.sliderMoved.connect(self.set_position)
        self.slider.sliderReleased.connect(self.slider_value_changed)



        #create label
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)


        #create hbox layout
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0,0,0,0)

        #set widgets to the hbox layout
        hboxLayout.addWidget(openBtn)
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.slider)



        #create vbox layout
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(self.video_label)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)


        self.setLayout(vboxLayout)

        self.mediaPlayer.setVideoOutput(videowidget)


        #media player signals

        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    def closeEvent(self, event):
        # reply = QMessageBox.question(self, 'Quit?',
        #                              'Are you sure you want to quit?',
        #                              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        #
        # if reply == QMessageBox.Yes:
        #     if not type(event) == bool:
        #         event.accept()
        #     else:
        #         sys.exit()
        # else:
        #     if not type(event) == bool:
        #         event.ignore()
        self.run = False
        print("the video player closed")
        self.vid.close()

    def intro(self , video_path , second):

        # self.vid.start()
        self.vid = Video(video_path)
        self.vid.set_size((900, (900*self.vid.video_height)/ self.vid.video_width))
        self.playBtn.clicked.connect(self.vid.toggle_pause)

        # slider properties
        duration = self.vid.get_file_data()["duration"]
        self.slider.setRange(0, int(duration))


        # Initialize Pygame
        pygame.init()

        # Set the screen dimensions (width, height)
        screen_width = 800
        screen_height = 600

        # Create the Pygame screen
        # SCREEN = pygame.display.set_mode((screen_width, screen_height))
        SCREEN = None

        print(self.vid.get_file_data())
        self.vid.seek(second)
        while self.run:
            self.vid.draw(SCREEN, (0, 0))
            video_seconds = int(self.vid.get_playback_data()["time"])
            self.slider.setValue(video_seconds)
            # self.vid.update()
            # if self.vid.frame:
            # print(self.vid.frame)

                # print("im alive you bastards")
            height, width, channel = self.vid.frame.shape

            # print(height)
            bytes_per_line = width * channel
            image = QImage(self.vid.frame.data , width , height , bytes_per_line , QImage.Format_RGB888)
            # Load the image using QPixmap
            pixmap = QPixmap.fromImage(image)
            # Set the width of the image to 500 and calculate the proportional height
            # width = 640
            # height = int(pixmap.height() * width / pixmap.width())
            pixmap = pixmap.scaled(width, height)

            self.video_label.setPixmap(pixmap)


            # pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.vid.close()



    def slider_value_changed(self):
        self.vid.seek(self.slider.value())
        print(self.slider.value())

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.intro(filename , 0)
            self.playBtn.setEnabled(True)


    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        else:
            self.mediaPlayer.play()


    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)

            )

        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)

            )

    def position_changed(self, position):
        self.slider.setValue(position)


    def duration_changed(self, duration):
        self.slider.setRange(0, duration)


    def set_position(self, position):
        self.mediaPlayer.setPosition(position)


    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())



if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Video_Player_Window()
    sys.exit(app.exec_())