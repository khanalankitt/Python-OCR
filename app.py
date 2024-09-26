# import os
# import re
# from pdf2image import convert_from_path
# import easyocr

# # Paths
# pdf_path = "result.pdf"
# poppler_path = r"C:\poppler\bin"  # Specify the path to the Poppler binaries
# output_dir = './images'
# final_result_file = "final.txt"
# extracted_text_file = "extracted.txt"  # File for saving all extracted text

# # Create output directory if it doesn't exist
# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)

# # Convert PDF to images
# images = convert_from_path(pdf_path, poppler_path=poppler_path)

# # Initialize EasyOCR Reader
# reader = easyocr.Reader(['en'])  # Specify the language(s)

# # Dictionary to hold counts for each campus
# campus_counts = {}
# current_campus = ""

# # Regular expression patterns
# campus_pattern = re.compile(r"^\d+\.\s?(.*)")  
# symbol_pattern = re.compile(r"\b79\d{6}\b")  # Pattern for symbol numbers starting with "79"

# # Open file to write extracted text
# with open(extracted_text_file, 'w') as extracted_file:
#     # Process each image
#     for i, image in enumerate(images):
#         # Save the image
#         image_path = os.path.join(output_dir, f'page-{i + 1}.png')
#         image.save(image_path, 'PNG')
#         print(f'Saved image: {image_path}')

#         # Perform OCR
#         results = reader.readtext(image_path)

#         # Process each extracted result
#         for (bbox, text, prob) in results:
#             print(f"Extracted Text: {text}")  # Debugging output

#             # Write extracted text to file
#             extracted_file.write(f"{text}\n")

#             # Check if the text is a campus name (starting with a number followed by a dot, with or without a space)
#             campus_match = campus_pattern.match(text)
#             if campus_match:
#                 # New campus found, reset symbol collection
#                 current_campus = campus_match.group(1).strip()
#                 print(f"Detected new campus: {current_campus}")
#                 if current_campus not in campus_counts:
#                     campus_counts[current_campus] = 0  # Initialize count for the campus
#                 continue

#             # If we're reading symbols, look for symbol numbers in the text
#             symbol_numbers = symbol_pattern.findall(text)
#             if symbol_numbers and current_campus:
#                 count = len(symbol_numbers)
#                 campus_counts[current_campus] += count  # Add to the count for the current campus
#                 print(f"Found {count} symbol numbers for campus: {current_campus}")

# # Write the final result to the file
# with open(final_result_file, 'w') as f:
#     for campus, count in campus_counts.items():
#         f.write(f'{campus}: {count}\n')

# print(campus_counts)

# print(f'Counts saved to {final_result_file}')
# print(f'All extracted text saved to {extracted_text_file}')


import os
from pdf2image import convert_from_path
import easyocr
import difflib
import re


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
current_campus = ""  # Tracks the current campus being processed

# List of college names (known list of campuses)
college_names = [
    "Patan Multiple Campus", "Amrit Campus", "Bhaktapur Multiple Campus", "Padmakanya Multiple Campus",
    "St. Xavier's College", "Kathford International College of Engineering and Management", "New Summit College",
    "Prime College", "St. Lawrence College", "College of Applied Business and Technology", "Kathmandu BernHardt College",
    "Deerwalk Institute of Technology", "Vedas College", "Texas International College", "Ambition College",
    "National College of Computer Studies", "Orchid International College", "Sagarmatha College of Science & Technology",
    "Nagarjuna College of Information Technology", "Academia International College", "Himalaya College of Engineering",
    "Asian School of Management and Technology", "Madan Bhandari Memorial College", "Nepalaya College",
    "Asian College of Higher Studies", "Trinity International College", "Samriddhi College", "Swastik College",
    "Kathmandu College of Technology", "NIST", "Siddhanath Science Campus", 
    "Ramswaru Ramsagar Multiple Campus", "Mechi Multiple Campus", "Shreeyantra College", 
    "Central Campus of Technology", "Birendra Memorial College", "Godawari College", 
    "Mahendra Morang Adarsh Multiple Campus", "Birat Kshitiz College", "Nihareeka College", 
    "Birat Multiple College", "AIMS College", "Himalaya Darshan College", "National Infotech", 
    "Hetauda City College", "Birendra Multiple Campus", "Chitwan College of Technology", 
    "Lumbini ICT Campus", "Prithvi Narayan Campus", "Mount Annapurna Campus", "Soch College of IT", 
    "Butwal Multiple Campus", "Lumbini City College", "Nepathya College", "Bhairahawa Multiple Campus", 
    "Mahendra Multiple Campus, Nepalgunj", "Banke Bageshwori Campus, Nepalgunj", "Nepalgunj Campus", 
    "Mahendra Multiple Campus, Dang", "Ambikeshwari Campus"
]

# Regular expression to find symbol numbers that start with "79" and are 7 digits long
symbol_pattern = re.compile(r"\b79\d{6}\b")

# Open file to write extracted text for review
with open(extracted_text_file, 'w') as extracted_file:
    # Process each image
    for i, image in enumerate(images):
        # Save the image for potential debugging/visual review
        image_path = os.path.join(output_dir, f'page-{i + 1}.png')
        image.save(image_path, 'PNG')
        print(f'Saved image: {image_path}')

        # Perform OCR on the image
        results = reader.readtext(image_path)

        # Process each extracted text line
        for (bbox, text, prob) in results:
            print(f"Extracted Text: {text}")  # Debugging output to see OCR results
            extracted_file.write(f"{text}\n")  # Write extracted text to a file for further review

            # Attempt to find a matching campus from the list of known campuses
            closest_match = difflib.get_close_matches(text, college_names, n=1, cutoff=0.6)

            if closest_match:
                current_campus = closest_match[0]
                print(f"Detected campus (best match): {current_campus}")
                if current_campus not in campus_counts:
                    campus_counts[current_campus] = 0  # Initialize count for the new campus
            else:
                # Continue counting symbols for the previously detected campus
                print(f"No campus match found for: {text}")

            # Search for symbol numbers in the extracted text
            symbol_numbers = symbol_pattern.findall(text)
            if symbol_numbers and current_campus:
                count = len(symbol_numbers)
                campus_counts[current_campus] += count  # Increment count for the current campus
                print(f"Found {count} symbol numbers for campus: {current_campus}")
                print(f"Updated count for {current_campus}: {campus_counts[current_campus]}")

# Ensure that campus counts are properly populated before writing to the final file
if campus_counts:
    # Write the final campus counts to the result file
    with open(final_result_file, 'w') as f:
        for campus, count in campus_counts.items():
            f.write(f'{campus}: {count}\n')
            print(f'Writing {campus}: {count} to final result file')
else:
    print("No campuses found to write to the file.")

# Summary
print(f'Counts saved to {final_result_file}')
print(f'All extracted text saved to {extracted_text_file}')
