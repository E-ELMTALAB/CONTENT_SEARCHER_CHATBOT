import cv2
import numpy 
import os

VIDEO_DIR = r"C:\python\NLP\content_searcher\videos"
files = os.listdir(VIDEO_DIR)

for file in os.listdir(VIDEO_DIR):
    video_path = os.path.join(VIDEO_DIR , file)

    # opening the video file
    cap = cv2.VideoCapture(video_path)
    # Read and display each frame until the video ends
    while True:
        # Read the next frame
        ret, frame = cap.read()

        # Check if the frame was read successfully
        if not ret:
            break

        # Display the frame
        cv2.imshow('Video Player', frame)

        # Check for the 'q' key to quit the video playback
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    