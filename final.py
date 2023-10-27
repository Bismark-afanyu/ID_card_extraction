import cv2
import matplotlib.pyplot as plt
from glob import glob
import pytesseract as pt
import re
import os
import easyocr
from mtcnn import MTCNN

"""
Page segmentation modes:
  0    Orientation and script detection (OSD) only.
  1    Automatic page segmentation with OSD.
  2    Automatic page segmentation, but no OSD, or OCR.
  3    Fully automatic page segmentation, but no OSD. (Default)
  4    Assume a single column of text of variable sizes.
  5    Assume a single uniform block of vertically aligned text.
  6    Assume a single uniform block of text.
  7    Treat the image as a single text line.
  8    Treat the image as a single word.
  9    Treat the image as a single word in a circle.
 10    Treat the image as a single character.
 11    Sparse text. Find as much text as possible in no particular order.
 12    Sparse text with OSD.
 13    Raw line. Treat the image as a single text line,
       bypassing hacks that are Tesseract-specific.
OCR Engine modes: (see https://github.com/tesseract-ocr/tesseract/wiki#linux)
  0    Legacy engine only.
  1    Neural nets LSTM engine only.
  2    Legacy + LSTM engines.
  3    Default, based on what is available.

"""


# remove non alphanumeric characcter
def remove_non_alphanumeric(string):
    # substitute non-alphanumeric characters with space
    cleaned_string = re.sub(r'\W+', ' ', string)
    return cleaned_string


img_path = './id.jpg'
# get the image path
img = cv2.imread(img_path, 0)


def show_image(image):
    plt.imshow(image, cmap="gray")
    plt.title('Image')
    plt.axis('off')
    plt.show()


show_image(img)


# crop the image with opencv for occupation on the front.
y = 250
x = 450
h = 600
w = 480

crop_img_occupation = img[x:w, y:h]
# apply thresholding to partition the background and foreground of grayscale
img_occupation = cv2.threshold(
    crop_img_occupation, 165, 255, cv2.THRESH_BINARY)[1]
text_occupation = remove_non_alphanumeric(pt.image_to_string(img_occupation))
# show_image(img_occupation)


# We have all the the coordinates for the all the informations on the front of the
# ID card.

"""
1 - get an image 
2 - get the contours of elements for front then back
3 - knowing that we are going from the bottom to the top and
    from the right to the left, extract the corresponding infos.
"""


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


# print(get_contours(img_path))


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


# text_extract(get_contours(img_path)[1], img_path)


# create a class with the regions of interest


# custom class to declare region of interest of the front of the ID card
class RegionFront():
    class CCCD(object):
        # coordinates are of the form (y, x , h , w )
        ROIS = {
            "surname": [(250, 140, 600, 200)],  # done
            "given_names": [
                (250, 220, 600, 250),
            ],  # done
            "birth_date": [(250, 300, 600, 330)],  # done
            "birth_place": [(250, 350, 600, 380)],  # done
            "sex": [(250, 400, 600, 430)],  # done
            "height":  [(250, 400, 600, 430)],  # done
            "occupation": [(250, 450, 600, 480)],  # done
            "signature": [(250, 450, 550, 700)],
        }

# Create a custom function to cropped image base on religion of interest


def cropImageRoi(image, roi):
    roi_cropped = image[
        int(roi[1]): int(roi[3]), int(roi[0]): int(roi[2])
    ]

    return roi_cropped


# dictionary where the infos are stored
front_infos = {}

for r in RegionFront.CCCD.ROIS:
    crop_img = cropImageRoi(img, RegionFront.CCCD.ROIS[r][0])

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
        cv2.imwrite(f'{save_dir}/signature.jpg', img_final)
        # cv2.imwrite("./images/output.png", img)
    # show_image(img_final)
print(front_infos)

# extract face

# def detect_faces(img_path):
#     # img_data = cv2.imread(img_path)
#     images = glob(img_path)
#     # Load the image
#     img_data = cv2.imread(images[0])
#     # Creating an instance of the MTCNN detector
#     detector = MTCNN()

#     # Detecting the faces in the image
#     faces = detector.detect_faces(img_data)

#     # Creating a directory to save the cropped faces
#     save_dir = f'{os.path.dirname(os.path.abspath(__file__))}/cropped_faces'
#     os.makedirs(save_dir, exist_ok=True)

#     # Croping and saving the detected faces
#     for i, face in enumerate(faces):
#         x, y, w, h = face['box']
#         cropped_face = img_data[y:y+h, x:x+w]
#         cv2.imwrite(f'{save_dir}/face_{i}.jpg', cropped_face)
#         image = str(save_dir) + "/face_" + str(i) + ".jpg"
#         print (image) # for testing purpose only, remove when not need anymore

#         # Drawing bounding boxes around the detected faces
#         cv2.rectangle(img_data, (x, y), (x+w, y+h), (0, 255, 0), 2)

#         # Print the cropped face
#         print(f'Cropped Face {i}:') # for testing purpose only, remove when not need anymore
#         print(cropped_face) # for testing purpose only, remove when not need anymore
#     return img_data
# face = detect_faces(img_path)
# show_image(face)
class RegionBack():
    class CCCD(object):
        # coordinates are of the form (y, x , h , w )
        ROIS = {
            "father": [(40, 50, 200, 100)],  # done
            "mother": [
                (40, 100, 200, 200),
            ],  # done
            "address": [(40, 250, 200, 350)],  # done
            "identification_post": [(650, 240, 850, 270)],  # done
            "signature": [(250, 200, 550, 400)],
        }


img_back = cv2.imread('./id_back.jpg', 0)
show_image(img_back)

# dictionary where the infos are stored
back_infos = {}

for r in RegionBack.CCCD.ROIS:
    crop_img = cropImageRoi(img_back, RegionBack.CCCD.ROIS[r][0])

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

print("*"*150)
print("\n **extract numerical information with better accuracy** \n")


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


results = numeric_handler(img_back)
numeric_values_back = {"s.m": results[0], "date_issue": results[1],
                  "date_expiry": results[2], "unique_identifier": results[3], "id": results[4]}
print(numeric_values_back)

results = numeric_handler(img)
numeric_values_front = {"s.m": results[0], "date_issue": results[1],
                  "date_expiry": results[2], "unique_identifier": results[3], "id": results[4]}
print(results)
