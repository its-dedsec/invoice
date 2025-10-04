import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Invoice Data Cleaner", layout="wide")

st.title("🧾 Invoice Database Manager")

# Upload CSV
uploaded_file = st.file_uploader("📤 Upload Invoice CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")

    # Display initial database info
    total_items = len(df)
    st.metric(label="📊 Total Items in Database", value=total_items)

    st.subheader("🧹 Data Cleaning & Preprocessing")
    st.write("Click below to clean and preprocess your data.")
    
    # Button to trigger cleaning
    if st.button("🧽 Clean Data"):
        df = df.drop_duplicates().dropna()
        st.success("✅ Data cleaned successfully!")

        # Show summary chart (graphical UI)
        fig = px.histogram(df, x=df.columns[0], title="📦 Item Distribution (Post-Cleaning)")
        st.plotly_chart(fig, use_container_width=True)

        # Show verify section
        st.subheader("🔍 Verification Section")

        # Show remaining items before verification
        remaining_items = len(df)
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="🗂️ Items After Cleaning", value=remaining_items)
        with col2:
            st.metric(label="⏳ Remaining Items to Verify", value=remaining_items)

        # Button instead of checkbox
        if st.button("✅ Verify & Update Database"):
            st.success("🎉 Verification complete! Database updated.")
            st.dataframe(df)

else:
    st.info("Please upload a CSV file to get started.")
