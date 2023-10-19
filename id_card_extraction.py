import pytesseract
import easyocr
from glob import glob
import re
import cv2
import os
from mtcnn import MTCNN

import matplotlib.pyplot as plt
from skimage import measure, morphology
from skimage.color import label2rgb
from skimage.measure import regionprops
import numpy as np
import os

fields = ["s.m", "date_of_issue", "date_of_expiry", "unique_identifier", "id_number"] 



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
    return image


def thick_font(image):
    # Dilation and Erosion
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,2), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return image

# regex 
# recognise date 
def date_matches_three(date):
    pattern = '\d{2}\.\d{2}\.\d{4}'
    return re.findall(pattern, date)

# remove non alphanumeric characcter
def remove_non_alphanumeric(string):
    # Use regular expression to remove non-alphanumeric characters
    cleaned_string = re.sub(r'\W+', ' ', string)
    return cleaned_string

# extract word between two strings
def extract_words_between_strings(text, start_string, end_string):
    pattern = r"(?<=\b{}\b).*?(?=\b{}\b)".format(re.escape(start_string), re.escape(end_string))
    extracted_words = re.findall(pattern, text)
    return extracted_words


def extract_words_between_start_and_first_numeric(text, start_string):
    pattern = r"(?<=\b{}\b).*?(?=\b\d)".format(re.escape(start_string))
    extracted_words = re.findall(pattern, text)
    return extracted_words


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
    
    def signature_extraction(self):
        # get the image path
        img = cv2.imread(self.img, 0)

        # crop the image with opencv
        y = 250
        x = 400
        h = 550
        w = 700
        crop_img = img[x:w, y:h]
        
        # apply thresholding to partition the background and foreground of grayscale
        img = cv2.threshold(crop_img, 127, 255, cv2.THRESH_BINARY)[1]
        
        """
        Now that the image is ready, connected component analysis must be applied to 
        detect the connected regions in the image. This helps in identifying the 
        signature area, as signature characters are coupled together. skimage provides
        a function to do this
        """

        # connected component analysis by scikit-learn framework
        # identify blobs whose size is greater than the image pixel average
        blobs = img > img.mean()

        # measure the size of each blob
        blobs_labels = measure.label(blobs, background=1)
        
        # the blob labels are converted to RGB and are overlaid on the original image
        # for better visualization
        image_label_overlay = label2rgb(blobs_labels, image=img)

        """

        A blob is a set of pixel values that generally distinguishes an object from
        its background. In this case, the text and signature are blobs on a background
        of white pixels.
        
        """
        
        """
        Generally, a signature will be bigger than other text areas in a document, 
        so you need to do some measurements. Using component analysis, find the biggest
        component among the blobs
        """

        # initialize the variables to get the biggest component
        the_biggest_component = 0
        total_area = 0
        counter = 0
        average = 0.0
        
        # iterate over each blob and get the highest size component
        for region in regionprops(blobs_labels):
            # if blob size is greater than 10 then add it to the total area
            if (region.area > 10):
                total_area = total_area + region.area
                counter = counter + 1

            # take regions with large enough areas and filter the highest component
            if (region.area >= 250):
                if (region.area > the_biggest_component):
                    the_biggest_component = region.area

        # calculate the average of the blob regions
        
        if counter != 0:
            average = (total_area/counter)
            print("the_biggest_component: " + str(the_biggest_component))
            print("average: " + str(average))
        else:
            average = 1
        
        # Now let's filter out some outliers that might get confused
        # with the signature blob

        # the parameters are used to remove outliers of small size connected pixels
        constant_parameter_1 = 84
        constant_parameter_2 = 250
        constant_parameter_3 = 100

        # the parameter is used to remove outliers of large size connected pixels
        constant_parameter_4 = 18

        # experimental-based ratio calculation, modify it for your cases
        a4_small_size_outlier_constant = (
            (average/constant_parameter_1)*constant_parameter_2)+constant_parameter_3
        print("a4_small_size_outlier_constant: " + str(a4_small_size_outlier_constant))


        # experimental-based ratio calculation, modify it for your cases
        a4_big_size_outlier_constant = a4_small_size_outlier_constant*constant_parameter_4
        print("a4_big_size_outlier_constant: " + str(a4_big_size_outlier_constant))


        # remove the connected pixels that are smaller than threshold a4_small_size_outlier_constant
        pre_version = morphology.remove_small_objects(
            blobs_labels, a4_small_size_outlier_constant)
        # remove the connected pixels that are bigger than threshold a4_big_size_outlier_constant
        component_sizes = np.bincount(pre_version.ravel())
        too_small = component_sizes > (a4_big_size_outlier_constant)
        too_small_mask = too_small[pre_version]
        pre_version[too_small_mask] = 0
        # save the pre-version, which is the image with color labels after connected component analysis
        plt.imsave('pre_version.png', pre_version)


        # read the pre-version
        img = cv2.imread('pre_version.png', 0)
        # ensure a binary image with Otsu’s method
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

        # Creating a directory to save the signatures
        save_dir = f'{os.path.dirname(os.path.abspath(__file__))}/signatures'
        os.makedirs(save_dir, exist_ok=True)

        cv2.imwrite(f'{save_dir}/signature.jpg', img)
        # cv2.imwrite("./images/output.png", img)


    def text_detection(self):
        
        img = cv2.imread(self.img)
        # 1 - Convert the image to gray scale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        
        # 2 - Performing OTSU threshold
        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        
        # Specify structure shape and kernel size.
        # Kernel size increases or decreases the area
        # of the rectangle to be detected.
        # A smaller value like (10, 10) will detect
        # each word instead of a sentence.
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (12, 12))
        
        
        # Applying dilation on the threshold image
        dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)


        # Finding contours
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                        cv2.CHAIN_APPROX_NONE)


        # Creating a copy of image
        im2 = img.copy()
        
        # A text file is created and flushed
        file = open("recognized.txt", "w+")
        file.write("")
        file.close()
        

        # Looping through the identified contours
        # Then rectangular part is cropped and passed on
        # to pytesseract for extracting text from it
        # Extracted text is then written into the text file
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            
            # Drawing a rectangle on copied image
            rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Cropping the text block for giving input to OCR
            cropped = im2[y:y + h, x:x + w]
            
            # Open the file in append mode
            file = open("recognized.txt", "a")
            
            # Apply OCR on the cropped image
            text = pytesseract.image_to_string(cropped) # , config='--psm 1'
            
            # Appending the text into file
            file.write(text)
            file.write("\n")
            
            # Close the file
            file.close
        
        with open('./recognized.txt', 'r') as file:
            info = file.read().rstrip('\n')
            info = remove_non_alphanumeric(info)
        print(info)
        print(date_matches_three(info))
        extracted_infos = extract_words_between_strings(info, "REPUBLIC OF CA", "1808")
        print(extracted_infos)
        extracted_infos_two = extract_words_between_start_and_first_numeric(info, "REPUBLIC OF CA")
        print(extracted_infos_two)
        
image_back = TextExtract('../../id card dataset/Aadhaar/id_back.jpg')
image_front = TextExtract('../../id card dataset/Aadhaar/id.jpg')
image_front.text_detection()
image_front.signature_extraction()
TextExtract('./signatures/signature.jpg')

