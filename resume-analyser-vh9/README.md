# AI Resume Analyzer

## veeresh

## Description:

AI Resume Analyzer is a Streamlit application that allows users to upload a resume (PDF)
and compare it against a given job description using Google Gemini AI.
It provides personalized feedback, highlights strengths and weaknesses,
and suggests improvements with relevant courses and skills.

## Key Features:

- Extracts text from both text-based and image-based PDF resumes
- Uses Google Gemini AI for intelligent resume analysis
- Option to compare the resume with a custom job description
- Outputs strengths, weaknesses, missing skills, and course suggestions
- Easy-to-use, responsive Streamlit interface

## Requirements:

- Python 3.x
- streamlit
- python-dotenv
- google-generativeai
- pdf2image
- pdfplumber
- pytesseract
- pillow

## Additional Setup:

1. Install Tesseract-OCR:

   - Windows: https://github.com/tesseract-ocr/tesseract
   - Linux: sudo apt install tesseract-ocr
   - Mac: brew install tesseract

2. Set the correct path in the code:
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

3. Set your Google API Key in a `.env` file:
   Create a file named `.env` in the root directory and add:
   GOOGLE_API_KEY=your_api_key_here

## Installation:

1. Clone the repository or copy the project files.
2. Install the required dependencies:
   pip install -r requirements.txt

3. Ensure Tesseract and Poppler (for pdf2image) are installed properly.

## Usage:

Run the app with:
streamlit run app.py

## Steps:

1. Upload your resume in PDF format.
2. Optionally paste a job description for matching.
3. Click "Analyze Resume" to get detailed feedback.

## Output:

- Resume text extraction
- Evaluation summary from Gemini AI
- Matching insights with job description
- Skills to improve
- Suggested courses
- Strengths & Weaknesses

## Author:

Developed by Veeresh
Instagram: @veeresh_h9
LinkedIn: https://www.linkedin.com/in/veeresh-hajanale-63a587272

## Powered by:

- Streamlit
- Google Gemini AI
