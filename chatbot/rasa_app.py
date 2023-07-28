import asyncio
import contextlib
import logging
import cv2
import spacy
import os, sys
import warnings
from rasa.core.agent import Agent
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import io
import logging
import subprocess
from HiddenPrints import HiddenPrints
from utils import print_colored_text
from actions import Actions


class Chatbot():

    def __init__(self):
        # load the model
        # model_path = r"models/20230721-174025-numerous-drawbridge.tar.gz"
        # self.tracker = Tracker()
        model_path = r"C:\python\NLP\content_searcher\chatbot\models\20230723-211647-brown-experience.tar.gz"
        self.agent = Agent.load(model_path)
        self.nlp = spacy.load("en_core_web_md")
        self.actions = Actions()
        # os.system("cls")
        # print_colored_text("chatbot loaded" , "green")
        # print("chatbot loaded")
        # print("\n")
    def process_request(self , request):

        doc = self.nlp(request)
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

        return object_list, actions_list

    async def send_message(self , text):
        responses_info = await self.agent.parse_message(text)
        responses = await self.agent.handle_text(text)
        # try:
        # print(responses_info)
        try:
            print("in the try block")
            output = responses[0]["text"]
            print(output)
        except:
            pass
        score = responses_info["intent"]["confidence"]

        if score < 0.95:
            # print_colored_text("I don't know what you are talking about")
            # print_colored_text(str(score))
            ouput = "None"

        # else:
        #     print_colored_text(output)
        #     intent = responses_info["intent"]["name"]
        #     if responses_info["intent"]["name"] == "request_for_picture":
        #         value = responses_info["entities"][0]["value"]
        #         objects, actions = self.process_request(value)
        #         image = self.actions.find_request(request_objects=objects, request_actions=actions)

        return output , responses_info


    # Example interaction
    async def interact(self):

        while True:
            user_input = input(">> ")

            if user_input == "/stop":
                break

            elif user_input == "cls":
                os.system("cls")

            else:
                # with HiddenPrints():
                responses_info = await self.agent.parse_message(user_input)
                responses = await self.agent.handle_text(user_input)
                    # try:
                print(responses_info)
                try:
                    output = responses[0]["text"]
                except:
                    pass
                score = responses_info["intent"]["confidence"]

                if score < 0.95 :
                    print_colored_text("I don't know what you are talking about")
                    print_colored_text(str(score))

                else :
                    print_colored_text(output)
                    intent = responses_info["intent"]["name"]
                    if responses_info["intent"]["name"] == "request_for_picture":
                        value = responses_info["entities"][0]["value"]
                        objects , actions = self.process_request(value)
                        image = self.actions.find_request(request_objects=objects , request_actions=actions)
                        cv2.imshow("image" , image)
                        cv2.waitKey(0)


    def start_interaction(self):
        asyncio.run(self.interact())

    def async_send_message(self , text):
        respond_text , response_info = asyncio.run(self.send_message(text))
        return respond_text , response_info

if __name__ == "__main__":

    MODEL_DIR = r"C:\python\NLP\content_searcher\chatbot\models\20230723-211647-brown-experience.tar.gz"
    chatbot = Chatbot()
    chatbot.start_interaction()
    # Run the interaction loop
    # asyncio.run(interact())
