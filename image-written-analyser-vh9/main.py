import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image
import tempfile

# Configure tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # 🔁 Update this path

st.set_page_config(page_title="📝 Image Text Analyzer", layout="centered")

st.title("✍️ Image Text Analyzer")
st.markdown("Upload an image of writing and get instant insights!")

uploaded_file = st.file_uploader("📤 Upload written Image", type=["jpg", "png", "jpeg"])

def extract_text(image):
    text = pytesseract.image_to_string(image)
    return text.strip()

def analyze_slant(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 150)
    slant_angles = []

    if lines is not None:
        for rho, theta in lines[:, 0]:
            angle = np.degrees(theta)
            slant_angles.append(angle)

        avg_angle = np.mean(slant_angles)
        if avg_angle > 90:
            avg_angle = 180 - avg_angle
        return round(avg_angle - 90, 2)
    return "Not Detected"

def analyze_pressure(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    avg_intensity = np.mean(gray)
    if avg_intensity < 100:
        return "🖋️ Heavy Pressure"
    elif avg_intensity < 150:
        return "✒️ Moderate Pressure"
    else:
        return "🖊️ Light Pressure"

def analyze_spacing(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)[1]
    horizontal_projection = np.sum(thresh, axis=1)
    gaps = np.where(horizontal_projection < 10)[0]
    if len(gaps) > 20:
        return "📏 Wide Line Spacing"
    else:
        return "📐 Tight Line Spacing"

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='🖼️ Uploaded Handwriting', use_column_width=True)

    image_cv = np.array(image.convert('RGB'))

    with st.spinner("🔍 Extracting Text..."):
        text = extract_text(image)
        st.subheader("📄 Extracted Text:")
        st.code(text if text else "No text found.")

    with st.spinner("🧠 Analyzing Handwriting..."):
        slant = analyze_slant(image_cv)
        pressure = analyze_pressure(image_cv)
        spacing = analyze_spacing(image_cv)

        st.subheader("🔎 Analysis Report")
        st.write(f"**Slant Angle:** `{slant}°`")
        st.write(f"**Pen Pressure:** {pressure}")
        st.write(f"**Line Spacing:** {spacing}")

    st.success("✅ Analysis Complete!")

else:
    st.info("👆 Upload an image to begin analysis.")

st.markdown("---")
st.markdown("""<p style= 'text-align: center;' >Powered by <b>Streamlit</b> and <b>Google Gemini AI</b> | Developed by >> <a href="https://www.linkedin.com/in/veeresh-hajanale-63a587272"  target="_blank" style='text-decoration: none; color: #FFFFFF'><b>veeresh</b></a></p>""", unsafe_allow_html=True)

