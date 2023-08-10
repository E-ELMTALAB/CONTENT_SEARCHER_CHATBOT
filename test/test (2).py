import cv2
import numpy as np

# Load two images
play_image = cv2.imread(r"C:\Users\Morvarid\Downloads\play-button-icon-Graphics-1-6-580x386.jpg")
overlay_image = cv2.imread(r'C:\Users\Morvarid\Pictures\Saved Pictures\avatar1243759155 (1).jpg')
play_image = cv2.bitwise_not(play_image)
play_image = cv2.resize(play_image , (200 , 160))
play_height , play_width , play_channel = play_image.shape
overlay_height , overlay_width , overlay_channel = overlay_image.shape
b1 = (overlay_height//2)
s1 = (play_height//2)
b2 = (overlay_width//2)
s2 = (play_width//2)
center = (b1, b2)
top_left_corner = (b1 - s1, b2 - s2)
top_right_corner = (b1 + s1, b2 - s2)
bottom_left_corner = (b1 - s1, b2 + s2)
bottom_right_corner = (b1 + s1 , b2 + s2)

# overlay_image = cv2.circle(overlay_image , center , 5 , (255 , 0 , 0) , -1)
#
# overlay_image = cv2.circle(overlay_image , top_left_corner ,5 , (255 , 255 , 0) , -1)
# overlay_image = cv2.circle(overlay_image , top_right_corner ,5 , (255 , 255 , 0) , -1)
# overlay_image = cv2.circle(overlay_image , bottom_left_corner ,5 , (255 , 255 , 0) , -1)
# overlay_image = cv2.circle(overlay_image , bottom_right_corner ,5 , (255 , 255 , 0) , -1)

cropped = overlay_image[top_left_corner[0] : bottom_right_corner[0], top_right_corner[1] : bottom_right_corner[1]]


# Add the two images together
combined_image = cv2.add(cropped, play_image)

overlay_image[top_left_corner[0]: bottom_right_corner[0], top_right_corner[1]: bottom_right_corner[1]] = combined_image

# Display or save the combined image
cv2.imshow("cropped" , cropped)
cv2.imshow('Combined Images', overlay_image)
cv2.imshow("combined" , combined_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save the combined image
# cv2.imwrite('combined_image.jpg', combined_image)


# print(sorted_items)
if __name__ == "__main__":
    pass
    # import os
    #
    # print("Current working directory:", os.getcwd())
    # image = cv2.imread(r"C:\python\NLP\content_searcher\data\images\images6.jpg")
    # cv2.imshow("image" , image)
    # cv2.waitKey(0)