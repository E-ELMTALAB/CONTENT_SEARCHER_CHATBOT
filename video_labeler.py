import os
import cv2
import numpy as np
import pandas as pd
import tensorflow as tf
from transformers import AutoImageProcessor, TFResNetForImageClassification

class Object_Based_Labeler():

    def __init__(self):
        self.flag = 0
        self.iteration = 0
        self.skip_frames = 60
        self.image_processor = AutoImageProcessor.from_pretrained("microsoft/resnet-50")
        self.model = TFResNetForImageClassification.from_pretrained("microsoft/resnet-50")

    def detect_objects(self , frame):

        inputs = self.image_processor(frame, return_tensors="tf")
        logits = self.model(**inputs).logits

        # model predicts one of the 1000 ImageNet classes
        predicted_label = int(tf.math.argmax(logits, axis=-1))
        label = self.model.config.id2label[predicted_label]
        label = "-".join(label.split(","))

        return label 

    def make_csv(self , info_dict):

        # making the dataframe and making a csv file from it 
        df = pd.DataFrame(info_dict)
        df.to_csv("video_info.csv" , index = False)

    def process_videos(self , folder_path):

        # making the dict for the dataframe
        info_dict = {
                    "file_path" : [] ,
                        "id" : [] ,
                        "containing_objects" : [] ,
                        "containing_actions" : []
                    }
        
        # go through all of the videos in the folder
        for file in folder_path:
            video_path = os.path.join(VIDEO_DIR , file)

            
            # filling the appropriate attributes
            info_dict["file_path"].append(video_path)
            info_dict["id"].append(os.path.basename(video_path))
            info_dict["containing_actions"].append("None")

            # opening the video file
            cap = cv2.VideoCapture(video_path)
            labels = []

            # Read and display each frame until the video ends
            while True:
                # Read the next frame
                ret, frame = cap.read()
                if not ret:
                    break
                
                # if flag is true , go on and detect the objects
                if self.flag :
                    # process and label the frame
                    label = self.detect_objects(frame)
                    labels.append(label)

                # controlling the amout of frames to skip for detection
                if not self.flag:
                    self.iteration += 1
                    if (self.iteration == self.skip_frames):
                        self.flag = 1
                        self.iteration = 0

                cv2.waitKey(1)

            # appending the labels detected from the video
            info_dict["containing_objects"].append("-".join(list(set(labels))))

        self.make_csv(info_dict)


if __name__ == "__main__":

    # the path of the video
    VIDEO_DIR = r"videos"
    labeler = Object_Based_Labeler() 
    labeler.process_videos(VIDEO_DIR)