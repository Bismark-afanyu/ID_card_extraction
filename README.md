### ID_card_extraction
the extraction of information from ID cards 

## Libraries 

- opencv
- pytesseract
- easyocr
- re
- os
- mtcnn
- Pillow
- request
- inspect
- urllib
- json
- glob
- matplolib

## utils.py
- display an image : show_image(image)
- remove non alphanumeric character in a string : remove_non_alphanumeric(string)
- load an image from url : load_from_url(url)
- get the countours of stand out elements on an image and return the list of coodinates of these elements : get_contours(img_path)
- extract text with OCR + Pytesseract from an image and some coodinates : text_extract(coordinates, img_path)
- crop an  image base on region of interest : crop_image_roi(image, roi)
- handle numeric values on the ID card with a good accuracy : numeric_handler(image)
- return a json file drom a dictionary : create_json(dictionary)
- extract faces : detect_faces(image)

## classes.py
- RegionFront() : specify the regions of interest of the front of the ID Card
- RegionBack() : : specify the regions of interest of the back of the ID Card

## program.py
- load the image (locally or from url)
- depending on the key of the Region classes dictionnary, extract the informations (text, images, paths)
- 
