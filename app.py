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

# Dictionary to hold counts for each campus (for passed students)
campus_counts = {}
current_campus = ""  # Tracks the current campus being processed

# Dictionary to store the seat capacity for each campus
seat_capacity = {
    "Patan Multiple Campus": 144, "Amrit Campus": 144, "Bhaktapur Multiple Campus": 72, 
    "Padmakanya Multiple Campus": 72, "St. Xavier's College": 48, "Kathford International College of Engineering and Management": 48, 
    "New Summit College": 48, "Prime College": 48, "St. Lawrence College": 36, 
    "College of Applied Business and Technology": 36, "Kathmandu BernHardt College": 48, 
    "Deerwalk Institute of Technology": 48, "Vedas College": 48, "Texas International College": 48, 
    "Ambition College": 36, "National College of Computer Studies": 48, "Orchid International College": 48, 
    "Sagarmatha College of Science & Technology": 48, "Nagarjuna College of Information Technology": 36, 
    "Academia International College": 48, "Himalaya College of Engineering": 48, 
    "Asian School of Management and Technology": 48, "Madan Bhandari Memorial College": 48, 
    "Nepalaya College": 36, "Asian College of Higher Studies": 48, "Trinity International College": 48, 
    "Samriddhi College": 48, "Swastik College": 36, "Kathmandu College of Technology": 36, "NIST": 36, 
    "Siddhanath Science Campus": 72, "Ramswaru Ramsagar Multiple Campus": 72, "Mechi Multiple Campus": 36, 
    "Shreeyantra College": 48, "Central Campus of Technology": 36, "Birendra Memorial College": 48, 
    "Godawari College": 36, "Mahendra Morang Adarsh Multiple Campus": 72, "Birat Kshitiz College": 36, 
    "Nihareeka College": 36, "Birat Multiple College": 36, "AIMS College": 36, 
    "Himalaya Darshan College": 36, "National Infotech": 48, "Hetauda City College": 36, 
    "Birendra Multiple Campus": 72, "Chitwan College of Technology": 36, "Lumbini ICT Campus": 48, 
    "Prithvi Narayan Campus": 72, "Mount Annapurna Campus": 36, "Soch College of IT": 36, 
    "Butwal Multiple Campus": 72, "Lumbini City College": 36, "Nepathya College": 36, 
    "Bhairahawa Multiple Campus": 72, "Mahendra Multiple Campus, Nepalgunj": 72, 
    "Banke Bageshwori Campus, Nepalgunj": 36, "Nepalgunj Campus": 36, "Mahendra Multiple Campus, Dang": 36, 
    "Ambikeshwari Campus": 36
}

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
            closest_match = difflib.get_close_matches(text, seat_capacity.keys(), n=1, cutoff=0.6)

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
    # Write the final campus counts and pass percentages to the result file
    with open(final_result_file, 'w') as f:
        for campus, passed_students in campus_counts.items():
            total_seats = seat_capacity.get(campus, 0)
            if total_seats > 0:
                pass_percentage = (passed_students / total_seats) * 100
                f.write(f'{campus}: {passed_students} ({pass_percentage:.2f}%)\n')
                print(f'{campus}: {passed_students} ({pass_percentage:.2f}%)')  # Display the result
else:
    print("No campuses found to write to the file.")

# Summary
print(f'Counts and percentages saved to {final_result_file}')
print(f'All extracted text saved to {extracted_text_file}')
