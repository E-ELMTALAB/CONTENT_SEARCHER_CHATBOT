from collections import defaultdict

import spacy
from time import time

# objects = []

# start = time()
# nlp = spacy.load("en_core_web_md")
# end = time()
# print("took : " + str((end - start)))
#
# text = "there are many puppies of dogs in a fenced in area"
# text = text.replace("__" , " ")
# start = time()
# # doc = nlp(text)
# #
# # for token in doc:
# #     if token.pos_ == "NOUN":
# #         objects.append(token.text)
#
# def process_request(request):
#     doc = nlp(request)
#     # Extract the part-of-speech tags and tokens
#     pos_list = [token.pos_ for token in doc]
#     token_list = [token.lemma_ for token in doc]
#
#     actions_list = []
#     action_list = []
#     object_list = []
#     flag = 0
#
#     for i in range(len(pos_list)):
#         curr_pos = pos_list[i]
#         curr_token = token_list[i]
#
#         if (curr_pos == "NOUN") and not flag:
#             print(curr_token)
#             object_list.append(curr_token)
#         if (curr_pos == "VERB") and not flag:
#             print(curr_token)
#             action_list.append(curr_token)
#             flag = 1
#         if flag:
#             if curr_pos == "NOUN":
#                 action_list.append(curr_token)
#                 actions_list.append("_".join(action_list))
#                 action_list.clear()
#                 object_list.append(curr_token)
#                 flag = 0
#
#     return list(set(object_list)), list(set(actions_list))
#
# objects , actions = process_request(text)
# end = time()
#
# print("time took " + str((end - start)))
#
# print(objects)
# print("\n")
# print(actions)
s = time()
alt_obj_list = []
alt_thing_list = []
# sorted_frames = {}
sorted_frames = defaultdict(int)
score = 0
obj_list = "be_puppy@be_puppy@@be_sheep___walk_grass___play_grass@be_sheep___stand_field@be_puppy___play_grass@be_puppy___play_grass@play_plant___be_dog@be_dog___stand_wood@be_puppy@be_puppy@be_lot@stand_bucket___be_dog@stand_grass___be_dog@be_dog___walk_grass@be_dog___lay_grass@be_dog___run_grass@walk_grass@be_dog___play_sidewalk@lay_blanket___be_dog@lay_rug___be_dog@stand_dirt___be_puppy@stand_dirt___be_puppy@be_puppy___play_grass@be_puppy___play_dirt@stand_sidewalk___be_dog@be_dog@be_dog@lay_ground___be_dog@play_dog___be_dog@sit_ground___be_dog@eat_food___be_dog@be_dog@lay_ground___be_dog"
things_list = "dog_fenced_puppy_area@dog_puppy@dog_cage_ground_blanket@sheep_grass_dog@sheep_field_grass_building@dog_grass_puppy@dog_grass_puppy@plant_dog_dirt@dog_wood@cage_puppy_floor@dog_cage_puppy@lot_puppy_basket@dog_bucket@frisbee_dog_grass@dog_grass@dog_grass@dog_grass@dog_grass_house@dog_sidewalk@dog_blanket@rug_dog@dirt_puppy@dog_dirt_puppy_area@dog_grass_puppy@dog_dirt_puppy@dog_sidewalk@dog_puppy_sidewalk@dog_sidewalk@dog_ground_puppy@dog@dog_ground@dog_food@dog@dog_ground"
requests = ["walk_grass" , "play_grass"]
things_request = ["dog" , "grass"]

new_obj_list = obj_list.split("@")
for obj_items in new_obj_list:
    alt_obj_list.append(obj_items.split("___"))

new_thing_list = things_list.split("@")
for thing_items in new_thing_list:
    alt_thing_list.append(thing_items.split("_"))

for request in requests:
    for i , objs_list in enumerate(alt_obj_list):
        if request in objs_list:
            num = objs_list.count(request)
            sorted_frames[str(i)] += num

for request in things_request:
    for i , things_list in enumerate(alt_thing_list):
        if request in things_list:
            num = things_list.count(request)
            sorted_frames[str(i)] += num
sorted_frames = sorted(sorted_frames.items(), key=lambda x: x[1], reverse=True)
highest_score_frame = sorted_frames[0][0]


# highest_score_frame = list(sorted_frames.keys())[0]
print("the highest score frame : " + str(highest_score_frame))
print("score : " + str(sorted_frames[0][1]))

e = time()
print("time took : " + str((e - s)))
print(alt_obj_list)
