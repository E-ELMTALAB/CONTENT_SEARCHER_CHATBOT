import os
import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm
import tensorflow as tf
from transformers import pipeline
from transformers import DetrImageProcessor, DetrForObjectDetection
from transformers import AutoImageProcessor, TFResNetForImageClassification

class Object_Based_Labeler():

    def __init__(self):
        self.flag = 0
        self.iteration = 0
        self.skip_frames = 60
        self.processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-101")
        self.detection_model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-101")
        self.image_to_text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")

    def detect_objects(self , frame):

        inputs = self.image_processor(frame, return_tensors="tf")
        logits = self.model(**inputs).logits
        scores = tf.nn.softmax(logits).numpy()

        # model predicts one of the 1000 ImageNet classes
        predicted_index = int(tf.math.argmax(logits, axis=-1))
        prediction_score = scores[0][predicted_index]
        if (prediction_score) >= 0.7 :
          label = self.model.config.id2label[predicted_index]
          label = "-".join(label.split(","))

        else:
          label = "None"

        return label 

    def make_csv(self , info_dict):

        # making the dataframe and making a csv file from it 
        print("i made the csv !")
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
        for file in os.listdir(folder_path):
          if file.endswith("mp4"):
            video_path = os.path.join(VIDEO_DIR , file)
            print(video_path)
            
            # filling the appropriate attributes
            info_dict["file_path"].append(video_path)
            info_dict["id"].append(os.path.basename(video_path))
            info_dict["containing_actions"].append("None")

            # opening the video file
            cap = cv2.VideoCapture(video_path)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            labels = []
            i = 0

            progress_bar = tqdm(total=frame_count)
            # Read and display each frame until the video ends
            for i in range (frame_count):
                progress_bar.update(1)
                
                # if flag is true , go on and detect the objects
                if self.flag :
                    ret, frame = cap.read()
                    if not ret:
                      break

                    # process and label the frame
                    label = self.detect_objects(frame)
                    if label != "None":
                      labels.append(label)
                    self.flag = 0

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
    VIDEO_DIR = "/content/videos"
    labeler = Object_Based_Labeler() 
    labeler.process_videos(VIDEO_DIR)