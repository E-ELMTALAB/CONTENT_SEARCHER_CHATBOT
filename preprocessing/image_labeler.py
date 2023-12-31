import os
import cv2
import torch
import spacy
import pandas as pd
from transformers import DetrImageProcessor, DetrForObjectDetection
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer


class Image_Labeler():

    def __init__(self):
        self.nlp = spacy.load("en_core_web_md")
        self.processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-101")
        self.detection_model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-101")
        self.caption_model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.caption_model.to(self.device)

    def detect_caption(self, image):
        pixel_values = self.feature_extractor(images=image, return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(self.device)
        output_ids = self.caption_model.generate(pixel_values, **{"max_length": 24, "num_beams": 4})
        preds = self.tokenizer.batch_decode(output_ids, skip_special_tokens=True)
        caption = [pred.strip() for pred in preds]
        return caption[0]

    def process_caption(self , caption):
        doc = self.nlp(caption)
        pos_list = [token.pos_ for token in doc] # Extract the part-of-speech tags and tokens
        token_list = [token.lemma_ for token in doc]

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
                    object_list.append(curr_token)
                    flag = 0
        if action_list :
            action_list = "_".join(action_list)
        else :
            action_list = "None"

        return object_list, action_list

    def detect_objects(self, image):

        height, width, _ = image.shape
        inputs = self.processor(images=image, return_tensors="pt")
        outputs = self.detection_model(**inputs)
        target_sizes = torch.tensor([(height, width)])
        results = self.processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

        labels = []
        number_of_detections = results["labels"].numpy()

        if len(number_of_detections) > 0:
            for label in results["labels"]:
                labels.append(self.detection_model.config.id2label[label.item()])
            return labels

        else:
            return "None"

    def make_csv(self, info_dict): # making the dataimage and making a csv file from it
        df = pd.DataFrame(info_dict)
        df.to_csv("image_info.csv", index=False)
        print("i made the csv !")

    def process_videos(self, folder_path):

        # making the dict for the dataimage
        info_dict = {
            "file_path": [],
            "id": [],
            "containing_objects": [],
            "containing_captions": []
        }

        # go through all of the videos in the folder
        for file in os.listdir(folder_path):
            if file.endswith((".jpg", ".jpeg", ".webp", ".png")):
                image_path = os.path.join(folder_path, file)

                # filling the appropriate attributes
                info_dict["file_path"].append(image_path)
                info_dict["id"].append(os.path.basename(image_path))

                image = cv2.imread(image_path)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # process and label the image
                label = self.detect_objects(image)
                objects = []
                actions = "None"
                if label != "None":
                    caption = self.detect_caption(image)
                    objects , actions = self.process_caption(caption)

                    # appending the labels detected from the video
                    label.extend(objects)
                    label = "_".join(list(set(label)))
            info_dict["containing_objects"].append(label)
            info_dict["containing_captions"].append(actions)

        print(len(info_dict["containing_objects"]))
        print(len(info_dict["containing_captions"]))
        print(len(info_dict["file_path"]))
        print(len(info_dict["id"]))
        self.make_csv(info_dict)


if __name__ == "__main__":
    # the path of the video
    IMAGE_DIR = "data/images"
    labeler = Image_Labeler()
    labeler.process_videos(IMAGE_DIR)

