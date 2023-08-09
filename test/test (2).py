import cv2

obj_list = "dog_fenced_puppy_area@dog_puppy@dog_cage_ground_blanket@sheep_grass@sheep_field_grass_building@dog_grass_puppy@dog_grass_puppy@plant_dog_dirt@dog_wood@cage_puppy_floor@dog_cage_puppy@lot_puppy_basket@dog_bucket@frisbee_dog_grass@dog_grass@dog_grass@dog_grass@dog_grass_house@dog_sidewalk@dog_blanket@rug_dog@dirt_puppy@dog_dirt_puppy_area@dog_grass_puppy@dog_dirt_puppy@dog_sidewalk@dog_puppy_sidewalk@dog_sidewalk@dog_ground_puppy@dog@dog_ground@dog_food@dog@dog_ground"

splited_list = obj_list.split("@")

print(splited_list[2])


# print(sorted_items)
if __name__ == "__main__":
    pass
    # import os
    #
    # print("Current working directory:", os.getcwd())
    # image = cv2.imread(r"C:\python\NLP\content_searcher\data\images\images6.jpg")
    # cv2.imshow("image" , image)
    # cv2.waitKey(0)