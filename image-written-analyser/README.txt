Image Text Analyzer

Description:
-------------
Image Text Analyzer is a Streamlit app that allows users to upload handwritten images
and get instant analysis on the extracted text, writing slant, pen pressure, and line spacing.

It leverages the power of Tesseract OCR for text extraction and OpenCV for image analysis.

Features:
----------
- Text extraction from images using Tesseract OCR
- Writing slant angle detection
- Pen pressure estimation (light, moderate, heavy)
- Line spacing analysis (tight or wide)
- Clean and user-friendly Streamlit interface

Requirements:
--------------
- Python 3.x
- streamlit
- opencv-python
- numpy
- pytesseract
- pillow

Also make sure Tesseract-OCR is installed:
- Download from: https://github.com/tesseract-ocr/tesseract
- Set the correct path in the script for:
  pytesseract.pytesseract.tesseract_cmd

Example:
---------
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

Installation:
--------------
1. Install Python dependencies:
   pip install -r requirements.txt

2. Install Tesseract-OCR:
   - Windows: https://github.com/tesseract-ocr/tesseract
   - Linux: sudo apt install tesseract-ocr
   - Mac: brew install tesseract

3. Update the tesseract_cmd path in the Python script to match your installation.

Usage:
-------
Run the app with:
   streamlit run app.py

Then upload an image containing handwriting.

Output:
--------
- Extracted text from image
- Slant angle of handwriting in degrees
- Pen pressure level (emoji-coded)
- Line spacing type

Author:
--------
Veeresh
Instagram: @veeresh_h9
Linkdin: https://www.linkedin.com/in/veeresh-hajanale-63a587272