import os
import re
from pdf2image import convert_from_path
import easyocr

# Paths
pdf_path = "result.pdf"
poppler_path = r"C:\poppler\bin"  # Specify the path to the Poppler binaries
output_dir = './images'
final_result_file = "final.txt"
extracted_text_file = "extracted.txt"  # File for saving all extracted text

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Convert PDF to images
images = convert_from_path(pdf_path, poppler_path=poppler_path)

# Initialize EasyOCR Reader
reader = easyocr.Reader(['en'])  # Specify the language(s)

# Dictionary to hold counts for each campus
campus_counts = {}
current_campus = ""

# Regular expression patterns
campus_pattern = re.compile(r"^\d+\.\s?(.*)")  
symbol_pattern = re.compile(r"\b79\d{6}\b")  # Pattern for symbol numbers starting with "79"

# Open file to write extracted text
with open(extracted_text_file, 'w') as extracted_file:
    # Process each image
    for i, image in enumerate(images):
        # Save the image
        image_path = os.path.join(output_dir, f'page-{i + 1}.png')
        image.save(image_path, 'PNG')
        print(f'Saved image: {image_path}')

        # Perform OCR
        results = reader.readtext(image_path)

        # Process each extracted result
        for (bbox, text, prob) in results:
            print(f"Extracted Text: {text}")  # Debugging output

            # Write extracted text to file
            extracted_file.write(f"{text}\n")

            # Check if the text is a campus name (starting with a number followed by a dot, with or without a space)
            campus_match = campus_pattern.match(text)
            if campus_match:
                # New campus found, reset symbol collection
                current_campus = campus_match.group(1).strip()
                print(f"Detected new campus: {current_campus}")
                if current_campus not in campus_counts:
                    campus_counts[current_campus] = 0  # Initialize count for the campus
                continue

            # If we're reading symbols, look for symbol numbers in the text
            symbol_numbers = symbol_pattern.findall(text)
            if symbol_numbers and current_campus:
                count = len(symbol_numbers)
                campus_counts[current_campus] += count  # Add to the count for the current campus
                print(f"Found {count} symbol numbers for campus: {current_campus}")

# Write the final result to the file
with open(final_result_file, 'w') as f:
    for campus, count in campus_counts.items():
        f.write(f'{campus}: {count}\n')
print(campus_counts)
print(f'Counts saved to {final_result_file}')
print(f'All extracted text saved to {extracted_text_file}')
