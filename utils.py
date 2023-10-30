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
import json
import inspect


# display the image
def show_image(image):
    plt.imshow(image, cmap="gray")
    plt.title('Image')
    plt.axis('off')
    plt.show()
    

# remove non alphanumeric character in a string
def remove_non_alphanumeric(string):
    # substitute non-alphanumeric characters with space
    cleaned_string = re.sub(r'\W+', ' ', string)
    return cleaned_string

# load an image from url
def load_from_url(url):
    # Download the image using urllib
    request.urlretrieve(url, "image.png")
    # Open the downloaded image in PIL
    my_img = Image.open("image.png")
    return my_img

# get the countours of stand out elements on an image and return the list of coodinates
# of these elements
def get_contours(img_path):
    images = glob(img_path)
    # Load the image
    image = cv2.imread(images[0])

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # performing OTSU threshold
    ret, thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    # setting the size of of rectangle of elements we are getting contours
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

    # applying dilation on the threshold image
    dilation = cv2.dilate(thresh, rect_kernel, iterations=1)

    # copy of image
    img = image.copy()

    # finding contours
    contours, hierarchy = cv2.findContours(
        dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # the list of contours coodinates
    list_coordinates = []

    for contour in contours:
        list_coordinates.append(cv2.boundingRect(contour))
    return list_coordinates


# extract text with OCR + Pytesseract from an image and some coodinates
def text_extract(coordinates, img_path):
    # read the image
    images = glob(img_path)
    # Load the image
    image = cv2.imread(images[0])
    # copy of image
    img = image.copy()
    # get the coordinates
    x, y, w, h = coordinates
    # crop the image
    rect = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cropped = img[y:y + h, x:x+w]
    # extract the text and remove non alphanumerical character at the same time
    text = remove_non_alphanumeric(pt.image_to_string(cropped))
    # print(text)
    # plot the image
    plt.imshow(cropped)
    plt.show()
    
    
# crop an  image base on region of interest
def crop_image_roi(image, roi):
    roi_cropped = image[
        int(roi[1]): int(roi[3]), int(roi[0]): int(roi[2])
    ]

    return roi_cropped

# handle numeric values on the ID card with a good accuracy
def numeric_handler(image):  # sourcery skip: raise-specific-error
    """ 
    method responsible for handling numeric values found on the image.

    Uses easyocr library to extract values and find every numeric value on the image.

    output:
        - returns a list of numeric values that was found on the image
    """
    numeric = []

    # dealing with numbers
    num_reader = easyocr.Reader(['en', 'fr'], gpu=True)
    nums = num_reader.readtext(image)
    spec = [',', '.']  # list of special characters identified

    # nums output is represented as [(bbox, text, prob),...]
    nums = [value[1] for value in nums]
    for text in nums:
        if text.isnumeric():
            numeric.append(text)
        else:
            try:
                # for every special character identified in our list of special letters
                numeric.extend(text.replace(spc, '.')
                               for spc in spec if spc in text)
            except:
                # handling extraction error
                raise Exception(
                    'An error occured while extracting numeric values')
    return numeric


# return a json file drom a dictionary

def create_json(dictionary):
    # Convert dictionary to JSON
    json_data = json.dumps(dictionary, indent=4)

    
    # Create a file from the name of the dictionary
    # Get the name of the variable
    var_name = [name for name, obj in inspect.currentframe().f_back.f_locals.items() if obj is dictionary][0]

    # Create a file with the same name
    file_name = var_name + ".json"
    
    # Write JSON data to a file
    with open(file_name, "w") as file:
        file.write(json_data)


