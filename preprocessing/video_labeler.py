import os
import cv2
import torch
import spacy
import numpy as np
import pandas as pd
from tqdm import tqdm
import tensorflow as tf
from transformers import pipeline
from transformers import DetrImageProcessor, DetrForObjectDetection
from transformers import AutoImageProcessor, TFResNetForImageClassification
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
from transformers import BlipProcessor, BlipForConditionalGeneration


class Object_Based_Labeler():

    def __init__(self):
        self.flag = 0
        self.iteration = 120
        self.skip_frames = 120
        self.nlp = spacy.load("en_core_web_md")
        self.processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-101")
        self.detection_model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-101")
        # self.caption_model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        # self.feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        # self.tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        # self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # self.caption_model.to(self.device)
        self.caption_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
        self.caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to(
            "cuda")

    def detect_caption(self, frame):
        # unconditional image captioning
        inputs = self.caption_processor(frame, return_tensors="pt").to("cuda")
        out = self.caption_model.generate(**inputs)
        caption = self.caption_processor.decode(out[0], skip_special_tokens=True)
        return caption

    # def detect_caption(self, image):
    #     pixel_values = self.feature_extractor(images=image, return_tensors="pt").pixel_values
    #     pixel_values = pixel_values.to(self.device)
    #     output_ids = self.caption_model.generate(pixel_values, **{"max_length": 24, "num_beams": 4})
    #     preds = self.tokenizer.batch_decode(output_ids, skip_special_tokens=True)
    #     caption = [pred.strip() for pred in preds]
    #     return caption[0]
    def specify_objects(self , text):
        objects = []
        text = text.replace("__", " ")
        doc = self.nlp(text)

        for token in doc:
            if token.pos_ == "NOUN":
                objects.append(token.text)

        return objects

    def process_request(self , captions):
        text = captions.replace("__" , " ")
        doc = self.nlp(text)
        # Extract the part-of-speech tags and tokens
        pos_list = [token.pos_ for token in doc]
        token_list = [token.lemma_ for token in doc]

        actions_list = []
        action_list = []
        object_list = []
        flag = 0

        for i in range(len(pos_list)):
            curr_pos = pos_list[i]
            curr_token = token_list[i]

            if (curr_pos == "NOUN") and not flag:
                print(curr_token)
                object_list.append(curr_token)
            if (curr_pos == "VERB") and not flag:
                print(curr_token)
                action_list.append(curr_token)
                flag = 1
            if flag:
                if curr_pos == "NOUN":
                    action_list.append(curr_token)
                    actions_list.append("_".join(action_list))
                    action_list.clear()
                    object_list.append(curr_token)
                    flag = 0

        return list(set(object_list)), list(set(actions_list))


    def detect_objects(self, frame):

        height, width, _ = frame.shape
        inputs = self.processor(images=frame, return_tensors="pt")
        outputs = self.detection_model(**inputs)

        target_sizes = torch.tensor([(height, width)])
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

    def make_csv(self, info_dict):

        # making the dataframe and making a csv file from it
        print("i made the csv !")
        df = pd.DataFrame(info_dict)
        df.to_csv("video_info.csv", index=False)

    def process_videos(self, folder_path):

        # making the dict for the dataframe
        info_dict = {
            "file_path": [],
            "id": [],
            "All_Objects": [],
            "All_Captions": [],
            "Containing_Objects": [],
            "Containing_Captions": []
        }

        # go through all of the videos in the folder
        for file in os.listdir(folder_path):
            if file.endswith("mp4"):
                video_path = os.path.join(VIDEO_DIR, file)
                print(video_path)

                # filling the appropriate attributes
                info_dict["file_path"].append(video_path)
                info_dict["id"].append(os.path.basename(video_path))
                # info_dict["containing_actions"].append("None")

                # opening the video file
                cap = cv2.VideoCapture(video_path)
                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                # labels = []
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
                    # cv2.imshow("frame", frame)
                    # cv2.waitKey(1)

                    # process and label the frame
                    # label = self.detect_objects(frame)

                    # if label != "None":
                    caption = self.detect_caption(frame)
                    print(caption)
                    captions.append(caption)
                    # labels.append(label)
                    # labels = list(set(labels))
                    # print(labels)

                    labels , actions = self.process_request(caption)
                    info_dict["Containing_Objects"].append("_".join(labels))
                    info_dict["Containing_Captions"].append("__".join(actions))

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
                labels , actions = self.process_request("__".join(unique_caption_list))
                info_dict["All_Objects"].append("-".join(labels))
                info_dict["All_Captions"].append("__".join(actions))

        self.make_csv(info_dict)


if __name__ == "__main__":
    # the path of the video
    VIDEO_DIR = r"C:\python\NLP\content_searcher\data\videos"
    labeler = Object_Based_Labeler()
    labeler.process_videos(VIDEO_DIR)