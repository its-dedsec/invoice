import streamlit as st
import cv2
import numpy as np
from PIL import Image
import easyocr
import pandas as pd

st.set_page_config(page_title="Invoice OCR", layout="wide")
st.title("🧾 Invoice OCR & Analysis")

# Initialize EasyOCR
reader = easyocr.Reader(['en'])

# ---------- Image Preprocessing ----------
def preprocess_image(image):
    img = np.array(image.convert("RGB"))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Thresholding
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    # Denoising
    cleaned = cv2.medianBlur(thresh, 3)
    return cleaned

# ---------- OCR Extraction ----------
def extract_text(image):
    results = reader.readtext(image, detail=0, paragraph=True)
    return results

# ---------- Parsing ----------
def parse_invoice(lines):
    items = []
    skip_keywords = ["TOTAL", "ITEMS", "GST", "CASHIER", "BILL", "TAX", "AMOUNT"]

    for line in lines:
        if any(word in line.upper() for word in skip_keywords):
            continue

        parts = line.split()
        if len(parts) >= 4:
            try:
                qty, rate, value = map(float, parts[-3:])
                item = " ".join(parts[:-3])
                items.append([item, qty, rate, value])
            except ValueError:
                continue
    return items

# ---------- Streamlit App ----------
uploaded_file = st.file_uploader("Upload Invoice Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)

    # Create tabs
    tab1, tab2 = st.tabs(["🧹 Preprocessing", "🔎 OCR & Parsing"])

    with tab1:
        st.subheader("Original Invoice")
        st.image(image, caption="Uploaded Invoice", use_container_width=True)

        st.subheader("Cleaned Invoice")
        cleaned_img = preprocess_image(image)
        st.image(cleaned_img, caption="Preprocessed for OCR", use_container_width=True, channels="GRAY")

    with tab2:
        st.subheader("Extracted Data")
        results = extract_text(cleaned_img)
        items = parse_invoice(results)

        if items:
            df = pd.DataFrame(items, columns=["Item", "Qty", "Rate", "Value"])
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("Could not parse structured data from invoice.")
