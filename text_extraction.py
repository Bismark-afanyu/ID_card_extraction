import pytesseract
import easyocr
from glob import glob
import csv

imgs = glob('/home/aja/Documents/ML/dataset/text_extraction/test/*')
image = imgs[1]


class TextExtract:
    """
    Class reponsible for extraction and handling of information from an image
    """

    def __init__(self, image):
        self.img = image  # image to be processed
        self.num = {}  # numeric values extracted
        self.string = {}  # non-numeric values extracted
        self.extract()  # method for extraction

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

    def extract(self):
        # still to be implemented
        nums = self.numeric_handler()
        # self.toCSV()
        print("\n",nums, "\n") # for testing purpose only, remove when not need anymore
    
    def toCSV(self):
        """This method saves a csv file called id_cards that containes every information collected.

        Args:
            path (String): Containes the path to the directory for the id_cards to be saved
        """
        info = self.string.update(self.num) # concatinating all the informations we have together
        with open("id_cards.csv", 'a', newline='') as csvfile:
            fieldnames = ["given_name", "surname", "sex", "height", "father", "mother","place_of_birth", "occupation","date_of_birth","unique_identifier", "date_of_issue", "date_of_expiry", "id_number", "face", "signature", "sm", "address", "identification_post"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader() # set the headers
            writer.writerow(info) # fill in the information

    def toJSON(self):  # sourcery skip: raise-specific-error
        """This method produces a json format that can be used for cloud operations.

        Returns:
            Dict : dictionary containing all the information extracted from the id card
        """
        try:
            return self.string.update(self.num)
        except:
            raise Exception("An error occured during concatination of information.")




text = TextExtract(image)
