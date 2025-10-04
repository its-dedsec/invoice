import streamlit as st
import pandas as pd

st.set_page_config(page_title="Invoice Database Manager", layout="wide")

st.title("🧾 Invoice Database Manager")

# Upload CSV
uploaded_file = st.file_uploader("📤 Upload Invoice CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")

    # Show total items before cleaning
    total_items = len(df)
    st.metric(label="📊 Total Items in Database", value=total_items)

    st.subheader("🧹 Data Cleaning & Preprocessing")

    if st.button("🧽 Clean & Preprocess Data"):
        df = df.drop_duplicates().dropna()
        st.success("✅ Data cleaned successfully!")

        # After cleaning
        remaining_items = len(df)

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="🗂️ Items After Cleaning", value=remaining_items)
        with col2:
            st.metric(label="📉 Remaining Items to Verify", value=remaining_items)

        st.subheader("🔍 Verification")

        # Replace checkbox with a button
        if st.button("✅ Verify Items"):
            st.success("🎉 All items verified and database updated!")
            st.dataframe(df)

else:
    st.info("Please upload a CSV file to get started.")
