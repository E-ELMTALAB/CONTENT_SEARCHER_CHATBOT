import pygame
from pymediainfo import MediaInfo
from ffpyplayer.player import MediaPlayer
from os.path import exists, basename, splitext
from os import strerror
from errno import ENOENT
import numpy as np
import cv2
import io
from PIL import Image

class Video:
    def __init__(self, path):
        self.path = path
        self.frame = cv2.imread(r"C:\Users\Morvarid\Downloads\play-button-icon-Graphics-1-6-580x386.jpg")

        if exists(self.path):
            cap = cv2.VideoCapture(self.path)
            self.video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.video = MediaPlayer(self.path)
            info = self.get_file_data()

            self.duration = info["duration"]
            self.frames = 0
            self.frame_delay = 1 / info["frame rate"]
            self.size = info["original size"]
            self.image = pygame.Surface((0, 0))

            self.active = True
        else:
            raise FileNotFoundError(ENOENT, strerror(ENOENT), self.path)

    def get_file_data(self):
        info = MediaInfo.parse(self.path).video_tracks[0]
        return {"path": self.path,
                "name": splitext(basename(self.path))[0],
                "frame rate": float(info.frame_rate),
                "frame count": info.frame_count,
                "duration": info.duration / 1000,
                "original size": (info.width, info.height),
                "original aspect ratio": info.other_display_aspect_ratio[0]}

    def get_playback_data(self):
        return {"active": self.active,
                "time": self.video.get_pts(),
                "volume": self.video.get_volume(),
                "paused": self.video.get_pause(),
                "size": self.size}

    def restart(self):
        self.video.seek(0, relative=False, accurate=False)
        self.frames = 0
        self.active = True

    def close(self):
        self.video.close_player()
        self.active = False

    def set_size(self, size):
        self.video.set_size(size[0], size[1])
        self.size = size

    def set_volume(self, volume):
        self.video.set_volume(volume)

    def seek(self, seek_time, accurate=False):
        vid_time = self.video.get_pts()
        if vid_time + seek_time < self.duration and self.active:
            self.video.seek(seek_time)
            if seek_time < 0:
                while (vid_time + seek_time < self.frames * self.frame_delay):
                    self.frames -= 1

    def toggle_pause(self):
        self.video.toggle_pause()

    def update(self):
        updated = False
        while self.video.get_pts() > self.frames * self.frame_delay:
            frame, val = self.video.get_frame()
            # print(frame)
            self.frames += 1
            updated = True
        if updated:
            if val == "eof":
                self.active = False
            elif frame != None:
                self.image = pygame.image.frombuffer(frame[0].to_bytearray()[0], frame[0].get_size(), "RGB")
                # Convert the frame to a NumPy array
                frame_array = frame[0].to_bytearray()[0]

                frame_np = np.frombuffer(frame_array, dtype=np.uint8)
                # print("frmae shape " + str(frame_np.shape))
                # print(self.video_height)
                # print(self.video_width)
                print(str(self.video.get_pts()))
                frame_height = int((900 * self.video_height) / self.video_width)
                frame_width = 900
                frame_np = frame_np.reshape( frame_height,frame_width , 3)  # Assuming RGB format
                self.frame = frame_np

                # print(self.frame)
                # print("fuck you bitch")

                # print(frame_np)
                # image = np.array(Image.open(io.BytesIO(image_bytes)))

                # Display the frame using OpenCV (optional)
                # cv2.imshow('Video Frame', frame_np)
                # cv2.waitKey(1)
                # print(len(frame_array))
        return updated

    def draw(self, surf, pos, force_draw=True):
        if self.active:
            if self.update() or force_draw:
                pass
                # surf.blit(self.image, pos)