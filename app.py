# app.py
import streamlit as st
import pandas as pd

# ---------------------------
# Page setup
# ---------------------------
st.set_page_config(page_title="Invoice Checker", page_icon="🧾", layout="centered")

st.title("🧾 Supermarket Invoice Checker")
st.caption("Check and verify your items easily — optimized for mobile view 📱")

# ---------------------------
# File upload
# ---------------------------
uploaded_file = st.file_uploader("📂 Upload your invoice CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")

    # ---------------------------
    # Cleaning and preprocessing
    # ---------------------------
    with st.expander("🧹 Clean & Preprocess Data"):
        st.write("Choose cleaning options:")
        if st.checkbox("Remove duplicates"):
            df = df.drop_duplicates()
        if st.checkbox("Trim spaces in column names and values"):
            df.columns = df.columns.str.strip()
            df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        if st.checkbox("Fill missing values with 0"):
            df = df.fillna(0)

        st.dataframe(df, use_container_width=True)

    # ---------------------------
    # Verification section
    # ---------------------------
    st.subheader("✅ Verify Items")

    search_query = st.text_input("🔍 Search for item name (optional):")

    # Filter items by search query
    filtered_df = (
        df[df["Particulars"].str.contains(search_query, case=False, na=False)]
        if search_query
        else df.copy()
    )

    # Add verified column (if not already present)
    if "Verified" not in filtered_df.columns:
        filtered_df["Verified"] = False

    verified_indices = []

    for i, row in filtered_df.iterrows():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**{row['Particulars']}**  \nQty: {row['Qty']} | Rate: {row['Rate']} | Value: {row['Value']}")
        with col2:
            tick = st.checkbox("✔", key=i)
            if tick:
                verified_indices.append(i)

    # Update verification status
    filtered_df.loc[verified_indices, "Verified"] = True

    # ---------------------------
    # Remaining items section
    # ---------------------------
    st.subheader("🧮 Remaining Items")

    remaining_items = filtered_df[filtered_df["Verified"] == False]

    if len(remaining_items) == 0:
        st.success("🎉 All items verified! Great job!")
    else:
        st.warning(f"{len(remaining_items)} items remaining:")
        st.dataframe(remaining_items[["Particulars", "Qty", "Rate", "Value"]], use_container_width=True)

else:
    st.info("👆 Upload your CSV file to begin verifying items.")
