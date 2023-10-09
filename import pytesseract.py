import pytesseract
import easyocr
import cv2
from glob import glob
import re
import os 
from mtcnn import MTCNN

#imgs = glob('C:/Users/BANTA/Desktop/ML projects/dataSets/Aadhaar/*')
image =   "C:/Users/BANTA/Desktop/ML projects/dataSets/Aadhaar/106.jpg"   #imgs[0]


class TextExtract:
    """
    Class reponsible for extraction and handling of information from an image
    """

    def __init__(self, image):
        self.img = image  # image to be processed
        self.num = {}  # numeric values extracted
        self.info = {}  # non-numeric values extracted
        #self.extract()  # method for extraction

    # def numeric_handler(self):  # sourcery skip: raise-specific-error
    #     """ 
    #     method responsible for handling numeric values found on the image.

    #     Uses easyocr library to extract values and find every numeric value on the image.
        
    #     output:
    #         - returns a list of numeric values that was found on the image
    #     """
    #     numeric = []
    #     # dealing with numbers
    #     num_reader = easyocr.Reader(['en', 'fr'])
    #     nums = num_reader.readtext(self.img)
    #     spec = [',', '.']  # list of special characters identified
    #     # nums output is represented as [(bbox, text, prob),...]
    #     nums = [value[1] for value in nums]
    #     for text in nums:
    #         if text.isnumeric():
    #             numeric.append(text)
    #         else:
    #             try:
    #                 # for every special character identified in our list of special letters
    #                 numeric.extend(text for spc in spec if spc in text)
    #             except:
    #                 # handling extraction error
    #                 raise Exception('An error occured while extracting numeric values')
    #     return numeric
    
    
    def numeric_handler(self):
        numeric = {}
        num_reader = easyocr.Reader(['en', 'fr'])
        nums = num_reader.readtext(self.img)

        for i in range(1, len(nums)):
            bbox, text, prob = nums[i]
            if text.isnumeric():
                field = self.get_field_name(nums, i)
                if field:
                    if field in numeric:
                        numeric[field].append(text)
                    else:
                        numeric[field] = [text]

        return numeric

    def get_field_name(self, nums, idx):
        for j in range(idx-1, -1, -1):
            bbox, text, prob = nums[j]
            if text.strip().endswith(':'):
                return text.strip()[:-1]

        return None

    def extract(self):
        nums = self.numeric_handler()

        print("Numeric values:")
        if nums:
            for field, values in nums.items():
                print(f"{field}: {', '.join(values)}")
        else:
            print("No numeric values found.")
        
    def info_handler(self):
        char = pytesseract.image_to_string(image)

    #def extract(self):
        nums = self.numeric_handler()
        print(nums) # for testing purpose only, remove when not need anymore

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


text = TextExtract(image)
text.extract()
text.detect_faces()

