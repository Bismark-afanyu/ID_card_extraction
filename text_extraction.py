import pytesseract
import easyocr
from glob import glob
import re
import cv2
import os 
from mtcnn import MTCNN

# imgs = glob('/home/aja/Documents/ML/dataset/text_extraction/test/*')
# image = imgs[1]
image = "C:/Users/BANTA/Desktop/ML projects/dataSets/Aadhaar/105.jpg"


class TextExtract:
    """
    Class reponsible for extraction and handling of information from an image
    """

    def __init__(self, image):
        self.img = image  # image to be processed
        self.num = {}  # numeric values extracted
        self.info = {}  # non-numeric values extracted
        self.extract(fields)  # method for extraction

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
                    self.num = (f"{field}: {num}")
        else:
            print("No numeric values found.") # for testing purpose only, remove when not need anymore

    def detect_faces(self):
        img_data = cv2.imread(image)
        # Creating an instance of the MTCNN detector
        detector = MTCNN()

        # Detecting the faces in the image
        faces = detector.detect_faces(img_data)

        # Creating a directory to save the cropped faces
        save_dir = os.path.dirname(os.path.abspath(__file__)) + '/cropped_faces'
        os.makedirs(save_dir, exist_ok=True)

        # Croping and saving the detected faces
        for i, face in enumerate(faces):
            x, y, w, h = face['box']
            cropped_face = img_data[y:y+h, x:x+w]
            cv2.imwrite(f'{save_dir}/face_{i}.jpg', cropped_face)

            # Drawing bounding boxes around the detected faces
            cv2.rectangle(img_data, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Print the cropped face
            print(f'Cropped Face {i}:') # for testing purpose only, remove when not need anymore
            print(cropped_face) # for testing purpose only, remove when not need anymore
        return img_data

fields = ["S.P./S.M", "DATE OF ISSUE", "DATE OF EXPIRY", "UNIQUE IDENTIFIER", "ID NUMBER"]  

text = TextExtract(image)
text.extract(fields)
text.detect_faces()
