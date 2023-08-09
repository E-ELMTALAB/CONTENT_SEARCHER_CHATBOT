import os
import cv2
import torch
import numpy as np
import pandas as pd
from tqdm import tqdm
import tensorflow as tf
from transformers import pipeline
from transformers import DetrImageProcessor, DetrForObjectDetection
from transformers import AutoImageProcessor, TFResNetForImageClassification
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer

class Object_Based_Labeler():

    def __init__(self):
        self.flag = 0
        self.iteration = 0
        self.skip_frames = 120
        self.processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-101")
        self.detection_model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-101")
        self.caption_model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.caption_model.to(self.device)

    def detect_caption(self , frame):
        pixel_values = self.feature_extractor(images=frame, return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(self.device)

        output_ids = self.caption_model.generate(pixel_values, **{"max_length": 24, "num_beams": 4})
        preds = self.tokenizer.batch_decode(output_ids, skip_special_tokens=True)
        caption = [pred.strip() for pred in preds]

        return caption
        
    def detect_objects(self , frame):

        height , width , _ = frame.shape
        inputs = self.processor(images=frame, return_tensors="pt")
        outputs = self.detection_model(**inputs)

        target_sizes = torch.tensor([(height , width)])
        results = self.processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

        labels = []
        number_of_detections = results["labels"].numpy()
        # mean_confidence = np.mean(np.array(results["scores"].tolist()))
        if len(number_of_detections) > 0:
            for label in results["labels"]:
                labels.append(self.detection_model.config.id2label[label.item()])
                label = "-".join(list(set(labels)))

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
                        "containing_captions" : []
                    }
        
        # go through all of the videos in the folder
        for file in os.listdir(folder_path):
          if file.endswith("mp4"):
            video_path = os.path.join(VIDEO_DIR , file)
            print(video_path)
            
            # filling the appropriate attributes
            info_dict["file_path"].append(video_path)
            info_dict["id"].append(os.path.basename(video_path))
            # info_dict["containing_actions"].append("None")

            # opening the video file
            cap = cv2.VideoCapture(video_path)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            labels = []
            captions = []

            progress_bar = tqdm(total=frame_count)
            # Read and display each frame until the video ends
            for frame_index in range(0, frame_count, self.skip_frames + 1):

                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
                progress_bar.update(1)

                # if flag is true , go on and detect the objects
                ret, frame = cap.read()
                if not ret:
                    break
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                cv2.imshow("frame", frame)
                cv2.waitKey(1)

                # process and label the frame
                label = self.detect_objects(frame)

                if label != "None":
                    caption = self.detect_caption(frame)
                    captions.append(caption)
                    labels.append(label)
                    labels = list(set(labels))
                    print(labels)

            # print(captions)
            unique_caption_list = []
            seen = set()
            captions = np.ravel(captions)

            for sublist in captions:
                element = sublist
                if element not in seen:
                    seen.add(element)
                    unique_caption_list.append(sublist)
            # appending the labels detected from the video
            info_dict["containing_objects"].append("-".join(list(set(labels))))
            info_dict["containing_captions"].append("__".join(unique_caption_list))

        self.make_csv(info_dict)


if __name__ == "__main__":

    # the path of the video
    VIDEO_DIR = "data/videos"
    labeler = Object_Based_Labeler() 
    labeler.process_videos(VIDEO_DIR)