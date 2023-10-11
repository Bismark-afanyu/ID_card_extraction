import pytesseract
import easyocr
from glob import glob
import re
import cv2
import os 
from mtcnn import MTCNN
import numpy as np

from matplotlib import pyplot as plt

# imgs = glob('/home/aja/Documents/ML/dataset/text_extraction/test/*')
# image = imgs[1]
image = "C:/Users/BANTA/Desktop/ML projects/dataSets/Aadhaar/106.jpg"


class TextExtract:
    """
    Class reponsible for extraction and handling of information from an image
    """

    def __init__(self, image):
        self.img = image  # image to be processed
        self.num = {}  # numeric values extracted
        self.info = {}  # non-numeric values extracted
        self.extract(fields)  # method for extraction



    def quality_check(image):

        THRESH = 100

        blur = cv2.Laplacian(image, cv2.CV_64F).var()

        if blur >= THRESH:
            print("Image is clear, continuing...")
            return True
        else: 
            print("Blurry image, stopping preprocessing")
            return False
        

    def binarization(image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        return gray_image

    def noise_removal(image):
        kernel = np.ones((1, 1), np.uint8)
        image = cv2.dilate(image, kernel, iterations=1)
        kernel = np.ones((1,1), np.uint8)
        image = cv2.erode(image, kernel, iterations=1)
        image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        image = cv2.medianBlur(image, 3)
        return (image)


    def thick_font(image):
        # Dilation and Erosion

        image = cv2.bitwise_not(image)
        kernel = np.ones((2,2), np.uint8)
        image = cv2.dilate(image, kernel, iterations=1)
        image = cv2.bitwise_not(image)
        return (image)
   

    def numeric_handler(self):  # sourcery skip: raise-specific-error
        """ 
        method responsible for handling numeric values found on the image.

        Uses easyocr library to extract values and find every numeric value on the image.
        
        output:
            - returns a list of numeric values that was found on the image
        """
        numeric = []
        # dealing with numbers
        num_reader = easyocr.Reader(['en', 'fr'])
        nums = num_reader.readtext(self.img)
        spec = [',', '.']  # list of special characters identified
        # nums output is represented as [(bbox, text, prob),...]
        nums = [value[1] for value in nums]
        for text in nums:
            if text.isnumeric():
                numeric.append(text)
            else:
                try:
                    # for every special character identified in our list of special letters
                    numeric.extend(text.replace(spc, '.') for spc in spec if spc in text)
                except:
                    # handling extraction error
                    raise Exception('An error occured while extracting numeric values')
        return numeric

    def info_handler(self):
        char = pytesseract.image_to_string(image)
        # still to be implemented

    def extract(self, fields):
        nums = self.numeric_handler()

        print("Numeric values:")
        if nums:
            for i, num in enumerate(nums):
                if i < len(fields):
                    field = fields[i]
                    self.num[f"{field}"] = num
                    print(self.num)
        else:
            print("No numeric values found.") # for testing purpose only, remove when not need anymore

    def detect_faces(self):
        img_data = cv2.imread(image)
        # Creating an instance of the MTCNN detector
        detector = MTCNN()

        # Detecting the faces in the image
        faces = detector.detect_faces(img_data)

        # Creating a directory to save the cropped faces
        save_dir = f'{os.path.dirname(os.path.abspath(__file__))}/cropped_faces'
        os.makedirs(save_dir, exist_ok=True)

        # Croping and saving the detected faces
        for i, face in enumerate(faces):
            x, y, w, h = face['box']
            cropped_face = img_data[y:y+h, x:x+w]
            cv2.imwrite(f'{save_dir}/face_{i}.jpg', cropped_face)
            self.image = str(save_dir) + "/face_" + str(i) + ".jpg"
            print (self.image) # for testing purpose only, remove when not need anymore

            # Drawing bounding boxes around the detected faces
            cv2.rectangle(img_data, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Print the cropped face
            print(f'Cropped Face {i}:') # for testing purpose only, remove when not need anymore
            print(cropped_face) # for testing purpose only, remove when not need anymore
        return img_data

fields = ["s.m", "date_of_issue", "date_of_expiry", "unique_identifier", "id_number"]  

text = TextExtract(image)
text.extract(fields)
text.detect_faces()
 