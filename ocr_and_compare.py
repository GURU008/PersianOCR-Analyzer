import cv2
import pytesseract
import os
import difflib

# Ensure pytesseract can find the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Directory paths
input_dir = r"C:\Users\HP\Desktop\OCR_Project\images"
output_dir = r"C:\Users\HP\Desktop\OCR_Project\output"

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# List of image files in the input directory
image_files = [f for f in os.listdir(input_dir) if f.endswith('.png')]

if not image_files:
    print(f"No PNG images found in the directory '{input_dir}'.")
    exit(1)

# Function to preprocess the image
def preprocess_image(image_path):
    # Read the image
    image = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive thresholding to get a binary image
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2
    )
    
    return binary

# Loop through each image file
for image_file in image_files:
    # Construct full file path
    image_path = os.path.join(input_dir, image_file)
    
    # Preprocess the image
    preprocessed_image = preprocess_image(image_path)
    
    # Perform OCR using Tesseract with Persian language
    custom_config = r'--oem 3 --psm 6 -l fas'
    text = pytesseract.image_to_string(preprocessed_image, config=custom_config)
    
    # Construct the output file path
    output_file_path = os.path.join(output_dir, os.path.splitext(image_file)[0] + ".txt")
    
    # Write the extracted text to a file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"Text from {image_file} has been written to {output_file_path}")

print("OCR processing completed.")

# Function to compare OCR output with reference text
def compare_texts(ocr_text, reference_text):
    diff = difflib.unified_diff(
        ocr_text.splitlines(), 
        reference_text.splitlines(),
        lineterm='',
    )
    return '\n'.join(diff)

# Example usage - Replace these paths with your actual files
# Check if files exist before opening them
ocr_output = os.path.join(output_dir, '1.txt')  # Replace with actual OCR output file path
reference_output = r"path_to_reference_text.txt"  # Replace with actual reference text file path

if os.path.exists(ocr_output) and os.path.exists(reference_output):
    with open(ocr_output, 'r', encoding='utf-8') as f1, open(reference_output, 'r', encoding='utf-8') as f2:
        ocr_text = f1.read()
        reference_text = f2.read()

    diff_result = compare_texts(ocr_text, reference_text)
    print(diff_result)
else:
    print("One or more files do not exist.")
