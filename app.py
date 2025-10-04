import streamlit as st
import pandas as pd
import easyocr
from PIL import Image
import re

st.set_page_config(page_title="Invoice Checker", page_icon="🧾", layout="centered")

st.title("🧾 Supermarket Invoice Checker (OCR Powered)")

# Initialize EasyOCR (load once)
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])

reader = load_ocr()

# Upload invoice image
uploaded_file = st.file_uploader("Upload your supermarket invoice", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Invoice", use_column_width=True)

    with st.spinner("🔍 Extracting text using OCR..."):
        result = reader.readtext(image)
        lines = [res[1] for res in result]

    # Refined regex for pattern: ITEM_NAME + 3 numeric columns (Qty, Rate, Value)
    pattern = re.compile(
        r"^([A-Za-z0-9\s\-\&\(\)\.\/]+?)\s+([\d]+\.?\d*)\s+([\d]+\.?\d*)\s+([\d]+\.?\d*)$"
    )

    items = []
    for line in lines:
        line = line.strip()
        # Skip headings or totals
        if any(skip in line.upper() for skip in ["QTY", "RATE", "VALUE", "TOTAL", "RS.", "AMOUNT"]):
            continue

        match = pattern.match(line)
        if match:
            item, qty, rate, value = match.groups()
            items.append([item.strip(), float(qty), float(rate), float(value)])

    if items:
        df = pd.DataFrame(items, columns=["Item", "Qty", "Rate", "Value"])
        df["Checked"] = False

        st.success(f"✅ Extracted {len(df)} items successfully!")

        # Search bar
        search_query = st.text_input("🔍 Search for an item")

        if search_query:
            filtered_df = df[df["Item"].str.contains(search_query, case=False, na=False)]
        else:
            filtered_df = df

        # Checklist display
        st.subheader("🧺 Items")
        for i in range(len(filtered_df)):
            item = filtered_df.iloc[i]["Item"]
            qty = filtered_df.iloc[i]["Qty"]
            value = filtered_df.iloc[i]["Value"]

            checked = st.checkbox(f"{item} | Qty: {qty} | ₹{value}", key=item)
            df.loc[df["Item"] == item, "Checked"] = checked

        # Summary
        st.subheader("📋 Summary")
        checked_items = df[df["Checked"]]
        unchecked_items = df[~df["Checked"]]

        st.write(f"✅ Checked: {len(checked_items)} / {len(df)} items")

        with st.expander("Show unchecked items"):
            st.table(unchecked_items[["Item", "Qty", "Value"]])

        with st.expander("Show all extracted items"):
            st.table(df)
    else:
        st.error("❌ Could not find structured lines. Here’s the raw OCR output:")
        st.write(lines)
else:
    st.info("👆 Upload an invoice image to get started!")
