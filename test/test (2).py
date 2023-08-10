import cv2
import numpy as np

# Load two images
play_image = cv2.imread(r"C:\Users\Morvarid\Downloads\play-button-icon-Graphics-1-6-580x386.jpg")
overlay_image = cv2.imread(r'C:\Users\Morvarid\Pictures\Saved Pictures\avatar1243759155 (1).jpg')
overlay_image = cv2.resize(overlay_image , (600 , 600))
play_image = cv2.resize(play_image , (600 , 600))
play_image = cv2.bitwise_not(play_image)


# Check if images are loaded successfully
if play_image is None or overlay_image is None:
    print("Error loading images.")
else:
    # Make sure both images have the same dimensions
    if play_image.shape != overlay_image.shape:
        print("Images have different dimensions. They cannot be added.")
    else:

        play_height , play_width , play_channel = play_image.shape
        overlay_height , overlay_width , overlay_channel = overlay_image.shape

        


        # Add the two images together
        combined_image = cv2.add(image1, image2)

        # Display or save the combined image
        cv2.imshow('Combined Images', combined_image)
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