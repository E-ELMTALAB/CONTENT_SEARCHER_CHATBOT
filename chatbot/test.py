import cv2

table = [['data\\ges\\activa-6g-right-front-three-quarter.webp', 'activa-6g-right-front-three-quarter.webp', 'road_motorcycle_side', 'park_side'], ['data\\ges\\free-images-social.png', 'free-images-social.png', 'bottle_laptop_cup_chair_group_people_table_handbag_person', 'sit_table'], ['data\\ges\\images1.jpg', 'images1.jpg', 'field_woman_dress_tv_person', 'stand_field'], ['data\\ges\\images2.jpg', 'images2.jpg', 'cow_giraffe_field_top', 'stand_top'], ['data\\ges\\images3.jpg', 'images3.jpg', 'baby_basket_plant_lot_person', 'lay_basket_fill_lot'], ['data\\ges\\images4.jpg', 'images4.jpg', 'table_person_laptop', 'use_laptop'], ['data\\ges\\images5.jpg', 'images5.jpg', 'top_person_hill_man', 'stand_top'], ['data\\images\\images6.jpg', 'images6.jpg', 'woman_dining table_picture_camera_person_clock', 'take_picture_hold_camera'], ['data\\ges\\orangutan_1600x1000_279157.jpg', 'orangutan_1600x1000_279157.jpg', 'elephant_bear_face', 'nan']]

request_objects = ["woman" , "person" , "camera"]
request_actions = ["holding_camera" , "take_picture"]

def find_occurrence(request_objects , request_actions):

    sorted_items = {}
    for item in table:
        score = 0
        objects = item[2]
        action = item[3]
        file_path = item[0]

        object_list = objects.split("_")
        action_list = action.split("_")

        # calculating the highest score
        highest_score = len(object_list) + (len(action_list) // 2)

        for obj_request in request_objects:
            if obj_request in object_list:
                score += 1

        for act_request in request_actions:
            if act_request in action :
                score += 1

        sorted_items[file_path] = score

    sorted_items = sorted(sorted_items.items(), key=lambda x: x[1], reverse=True)
    image_path = sorted_items[0][0]
    image_path = image_path.replace("\\" , "/")
    image_path = r"C:\\python\\NLP\\content_searcher\\" + image_path
    image_path = image_path.replace("\\\\", "/")
    image = cv2.imread(image_path)

    return image

cv2.imshow("image" , find_occurance(request_objects , request_actions))
cv2.waitKey(0)
# print(sorted_items)
if __name__ == "__main__":
    pass
    # import os
    #
    # print("Current working directory:", os.getcwd())
    # image = cv2.imread(r"C:\python\NLP\content_searcher\data\images\images6.jpg")
    # cv2.imshow("image" , image)
    # cv2.waitKey(0)