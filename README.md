I am trying to create a python program that extracts text from a pdf of scanned images and manipulates the extracted text.

Since the pdf is a pdf of scanned images, I used EasyOCR to extract the text from the images.
The pdf file is converted to images by using pdf2image.

The main idea is to extract the symbol numbers from the result.pdf file and write the number of symbol numbers that starts with 79 for each corresponding college in the final.txt file.

If you open the final.txt file, you can see the code works and the count of the symbol numbers starting with 79 for the corresponding college is written in the file.
But there is a small problem.
In the result.pdf file, there are a total of 60 colleges but in the final.txt file, only the count of 54 colleges are written.

The count for 6 colleges are missing.

Now here is the catch. Actually the count of the remaining 6 colleges are not missing. They are added to the count of the college just above them.

Example:
3. Bhaktapur Multiple Campus : 103
This is actually the sum of Bhaktapur Multiple Campus(47) and Padmakanya Multiple Campus(56)(missing in final.txt).

32. Ramswarup Ramsagar Multiple Campus : 46
This is actually the sum of Ramswarup Campus(19) and Mechi Multiple Campus(27)(missing in final.txt).

I cannot solve this problem.

Now what I analyzed and found is, a space {" "} may be the culprit here (yes a missing space)
If you see the result.pdf file, for every college that is missing, a space is missing between the dot and the first letter of the campus name.

![image](https://github.com/user-attachments/assets/c2c0855a-5222-45fa-9415-6e04266b4f60)
![image](https://github.com/user-attachments/assets/aade5f85-72a7-43d1-8310-001fd3d83196)

As seen in the image above, there is no space between the dot and the first letter of the campus name.

All the other places where there is a space, the code works well and expected result is written in the final.txt file.

![image](https://github.com/user-attachments/assets/1e9565fb-7ad9-4e7d-aaae-a37b7d414e39)


The error might be how I (ChatGPT) wrote the regex to identify the campus name from the symbol numbers.
Or the error might lie in any part of the code that I am totally unaware of.





