import cv2
import matplotlib.pyplot as plt
from glob import glob
import pytesseract as pt
import re
import os
import easyocr
from mtcnn import MTCNN
import json
from PIL import Image
from urllib import request
import numpy as np
import urllib
import inspect

from utils import show_image, crop_image_roi, load_from_url, text_extract, numeric_handler, remove_non_alphanumeric, create_json
from classes import RegionFront, RegionBack

img_path = './images/id.jpg'

# load the image
img = cv2.imread(img_path, 0)

# display the image
show_image(img)

# extract informations on the front of the ID card
# dictionary where the infos are stored
front_infos = {}

for r in RegionFront.CCCD.ROIS:
    crop_img = crop_image_roi(img, RegionFront.CCCD.ROIS[r][0])

    # apply thresholding to partition the background and foreground of grayscale
    match r:

        case "surname":
            img_final = cv2.threshold(crop_img, 160, 255, cv2.THRESH_BINARY)[1]

        case "given_names":
            img_final = cv2.threshold(crop_img, 150, 255, cv2.THRESH_BINARY)[1]

        case "birth_date":
            img_final = cv2.threshold(crop_img, 165, 255, cv2.THRESH_BINARY)[1]

        case "birth_place":
            img_final = cv2.threshold(crop_img, 165, 255, cv2.THRESH_BINARY)[1]

        case "sex" | "height":
            img_final = cv2.threshold(crop_img, 160, 255, cv2.THRESH_BINARY)[1]

        case "occupation":
            img_final = cv2.threshold(crop_img, 165, 255, cv2.THRESH_BINARY)[1]
        case "signature":
            img_final = cv2.threshold(
                crop_img, 127, 255, cv2.THRESH_BINARY)[1]
        case _:
            img_final = cv2.threshold(
                crop_img, 127, 255, cv2.THRESH_BINARY)[1]

    # img_final = cv2.threshold(crop_img, 160, 255, cv2.THRESH_BINARY)[1]
    # extract the text
    if r != "signature":
        front_infos[r] = remove_non_alphanumeric(
            pt.image_to_string(img_final, config='--oem 1 --psm 6'))

    else:
        # Creating a directory to save the signatures
        save_dir = f'{os.path.dirname(os.path.abspath(__file__))}/signatures'
        os.makedirs(save_dir, exist_ok=True)

        # cv2.imwrite(f'{save_dir}/signature'+ re.sub(r'\s', '', front_infos["surname"])+'jpg', img_final)
        cv2.imwrite(f'{save_dir}/{front_infos["surname"].strip().lower()}_signature.jpg', img_final)

        # save the directory of the cropped image of the signature
        front_infos[r] = f'{save_dir}/{front_infos["surname"].strip().lower()}_signature.jpg'

print(front_infos)



# load the back of the image
img_back_path = './images/id_back.jpg'

# load the image
img_back = cv2.imread(img_back_path, 0)

# display the image
show_image(img_back)

# dictionary where the infos are stored
back_infos = {}

for r in RegionBack.CCCD.ROIS:
    crop_img = crop_image_roi(img_back, RegionBack.CCCD.ROIS[r][0])

    # apply thresholding to partition the background and foreground of grayscale
    match r:

        case "father":
            img_final = cv2.threshold(crop_img, 85, 255, cv2.THRESH_BINARY)[1]

        case "mother":
            img_final = cv2.threshold(crop_img, 85, 255, cv2.THRESH_BINARY)[1]

        case "address":
            img_final = cv2.threshold(crop_img, 85, 255, cv2.THRESH_BINARY)[1]

        case "identification_post":
            img_final = cv2.threshold(crop_img, 100, 255, cv2.THRESH_BINARY)[1]

        case "signature":
            img_final = cv2.threshold(crop_img, 100, 255, cv2.THRESH_BINARY)[1]
        case _:
            img_final = cv2.threshold(crop_img, 127, 255, cv2.THRESH_BINARY)[1]

    # img_final = cv2.threshold(crop_img, 160, 255, cv2.THRESH_BINARY)[1]
    # extract the text
    if r != "signature":
        back_infos[r] = remove_non_alphanumeric(
            pt.image_to_string(img_final, config='--oem 1 --psm 6'))

    else:
        # Creating a directory to save the signatures
        save_dir = f'{os.path.dirname(os.path.abspath(__file__))}/signatures'
        os.makedirs(save_dir, exist_ok=True)

        # cv2.imwrite(f'{save_dir}/signature'+ re.sub(r'\s', '', front_infos["surname"])+'jpg', img_final)
        cv2.imwrite(f'{save_dir}/signature_authority.jpg', img_final)
        # cv2.imwrite("./images/output.png", img)
    # show_image(img_final)
print(back_infos)


# extract numeric informations

# on the back
results = numeric_handler(img_back)
numeric_values_back = {"s.m": results[0], "date_issue": results[1],
                       "date_expiry": results[2], "unique_identifier": results[3], "id": results[4]}
print(numeric_values_back)

# on the front
results = numeric_handler(img)
numeric_values_front = {"s.m": results[0], "date_issue": results[1],
                        "date_expiry": results[2], "unique_identifier": results[3], "id": results[4]}
print(results)

# create a json file from front infos
front_infos = {**front_infos, **numeric_values_front}
create_json(front_infos)

# create a json file from front infos
back_infos = {**back_infos, **numeric_values_back}
create_json(back_infos)
