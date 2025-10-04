# app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="D-Mart", page_icon="🧾", layout="wide")

st.title("🧾 D-Mart Invoice Checker")
st.write("Upload your invoice CSV to search, clean, and verify items easily.")

# Step 1: Upload CSV
uploaded_file = st.file_uploader("📂 Upload Invoice CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")

    # Step 2: Data cleaning
    with st.expander("🧹 Data Cleaning & Preprocessing", expanded=False):
        st.write("Select cleaning options below:")
        if st.checkbox("Remove duplicates"):
            df = df.drop_duplicates()
        if st.checkbox("Trim spaces in column names and data"):
            df.columns = df.columns.str.strip()
            df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        if st.checkbox("Fill missing values with 0"):
            df = df.fillna(0)
        st.dataframe(df)

    # Step 3: Verification Tab
    st.subheader("🧩 Verify and Tick Items")

    search_query = st.text_input("🔍 Search item name:")
    filtered_df = df[df["Particulars"].str.contains(search_query, case=False, na=False)] if search_query else df

    filtered_df["Verified"] = False
    verified = []
    for i, row in filtered_df.iterrows():
        col1, col2, col3, col4, col5 = st.columns([3,1,1,1,1])
        with col1:
            st.text(row["Particulars"])
        with col2:
            st.text(row["Qty"])
        with col3:
            st.text(row["Rate"])
        with col4:
            st.text(row["Value"])
        with col5:
            tick = st.checkbox("✔", key=i)
            if tick:
                verified.append(i)
                filtered_df.loc[i, "Verified"] = True

    # Step 4: Download Updated CSV
    st.subheader("💾 Download Updated Invoice")
    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Updated CSV", csv_data, "verified_invoice.csv", "text/csv")
else:
    st.info("👆 Upload a CSV file to get started.")
