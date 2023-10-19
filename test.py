import cv2
import numpy as np
import pytesseract

# Load the image using OpenCV
image = cv2.imread('../../id card dataset/Aadhaar/id.jpg')

# Step 1: Image resizing
resized_image = cv2.resize(image, None, fx=0.5, fy=0.5)

# Step 2: Image denoising
denoised_image = cv2.medianBlur(resized_image, 5)

# Step 3: Image enhancement
#enhanced_image = cv2.equalizeHist(denoised_image)

# Step 4: Binarization
gray_image = cv2.cvtColor(denoised_image, cv2.COLOR_BGR2GRAY)
_, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

# Step 5: Text region detection
edges = cv2.Canny(binary_image, 30, 150)
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
text_regions = []
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    if w > 50 and h > 50:
        text_regions.append((x, y, w, h))

# Step 6: Text region normalization
normalized_text_regions = []
for (x, y, w, h) in text_regions:
    roi = binary_image[y:y+h, x:x+w]
    normalized_roi = cv2.resize(roi, (200, 50))
    normalized_text_regions.append(normalized_roi)

# Step 7: Face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# Step 8: Face region normalization
normalized_faces = []
for (x, y, w, h) in faces:
    roi = resized_image[y:y+h, x:x+w]
    normalized_roi = cv2.resize(roi, (200, 200))
    normalized_faces.append(normalized_roi)

# Perform OCR on text regions
for region in normalized_text_regions:
    text = pytesseract.image_to_string(region)
    print("Extracted Text:", text)

# Display the normalized faces
for face in normalized_faces:
    cv2.imshow("Face", face)
    cv2.waitKey(0)

cv2.destroyAllWindows()
