import cv2
import pytesseract
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Specify the path to the Tesseract executable if it's not in your PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Path to the input image
input_image_path = 'images/input_image.png'
# Path to save the output image
output_image_path = 'images/output_image.png'

# Load the input image using OpenCV
image = cv2.imread(input_image_path)

# Convert the image to RGB (OpenCV loads images in BGR format)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Perform OCR using Tesseract
ocr_result = pytesseract.image_to_data(image_rgb, output_type=pytesseract.Output.DICT)

# Load the image using PIL for drawing
pil_image = Image.fromarray(image_rgb)
draw = ImageDraw.Draw(pil_image)

# Define the font for drawing text
font = ImageFont.load_default()

# Iterate over the OCR results and draw the bounding boxes and text
for i in range(len(ocr_result['text'])):
    if int(ocr_result['conf'][i]) > 0:  # Only consider results with confidence > 0
        x = ocr_result['left'][i]
        y = ocr_result['top'][i]
        w = ocr_result['width'][i]
        h = ocr_result['height'][i]
        text = ocr_result['text'][i]

        # Draw the bounding box
        draw.rectangle([(x, y), (x + w, y + h)], outline='red', width=2)
        # Draw the text
        draw.text((x, y - 10), text, fill='red', font=font)

# Save the output image
pil_image.save(output_image_path)

print(f"Output image saved to {output_image_path}")
