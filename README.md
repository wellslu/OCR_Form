# OCR_Form
prerequisite: please install Tesseract and check your computer environment.
## Original image
![ori_img](ex.png)
## Part 1: Process Image with Morphology
### Separate each line and find the position of value by morphology with OpenCV
![part1_img](separate_word.png)
## Part 2: Crop the Location of the Words in the Image and OCR
### Crop the image and transfer each value to strings with Tesseract
![part2_img](result.png)
