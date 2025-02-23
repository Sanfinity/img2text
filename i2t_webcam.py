import cv2
import pytesseract
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Specify the path to the Tesseract executable if it's not in your PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Define the font for drawing text
font = ImageFont.load_default()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to RGB (OpenCV captures in BGR format)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Perform OCR using Tesseract
    ocr_result = pytesseract.image_to_data(frame_rgb, output_type=pytesseract.Output.DICT)

    # Load the frame into PIL for drawing
    pil_image = Image.fromarray(frame_rgb)
    draw = ImageDraw.Draw(pil_image)

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

    # Convert the PIL image back to OpenCV format
    frame_with_text = np.array(pil_image)

    # Convert RGB to BGR
    frame_with_text = cv2.cvtColor(frame_with_text, cv2.COLOR_RGB2BGR)

    # Display the resulting frame
    cv2.imshow('Live OCR', frame_with_text)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
