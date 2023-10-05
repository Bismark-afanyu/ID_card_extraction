import pytesseract
import easyocr
from glob import glob
import re

imgs = glob('/home/aja/Documents/ML/dataset/text_extraction/test/*')
image = imgs[0]


class TextExtract:
    """
    Class reponsible for extraction and handling of information from an image
    """

    def __init__(self, image):
        self.img = image  # image to be processed
        self.num = {}  # numeric values extracted
        self.info = {}  # non-numeric values extracted
        self.extract()  # method for extraction

    def numeric_handler(self):
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
                    numeric.extend(text for spc in spec if spc in text)
                except:
                    # handling extraction error
                    raise Exception('An error occured while extracting numeric values')
        return numeric

    def info_handler(self):
        char = pytesseract.image_to_string(image)

    def extract(self):
        nums = self.numeric_handler()
        print(nums) # for testing purpose only, remove when not need anymore


text = TextExtract(image)
