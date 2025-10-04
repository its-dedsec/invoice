# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# Page setup
# ---------------------------
st.set_page_config(page_title="🧾 Smart Invoice Checker", page_icon="🛒", layout="centered")

st.title("🛒 Smart Supermarket Invoice Checker")
st.caption("For easy verification of supermarket bills — mobile friendly & visual 📱")

# ---------------------------
# Upload CSV
# ---------------------------
uploaded_file = st.file_uploader("📂 Upload your invoice CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")

    # ---------------------------
    # Cleaning section
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

    # Add verified column if missing
    if "Verified" not in df.columns:
        df["Verified"] = False

    # ---------------------------
    # Summary section (Top Stats)
    # ---------------------------
    st.markdown("### 📊 Summary Dashboard")

    total_items = len(df)
    verified_count = df["Verified"].sum()
    remaining_count = total_items - verified_count

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="🧾 Total Items", value=total_items)
    with col2:
        st.metric(label="✅ Verified Items", value=verified_count)
    with col3:
        st.metric(label="⏳ Remaining", value=remaining_count)

    # Simple donut chart
    chart_data = pd.DataFrame({
        "Status": ["Verified", "Remaining"],
        "Count": [verified_count, remaining_count]
    })
    fig = px.pie(chart_data, values="Count", names="Status", color="Status",
                 color_discrete_map={"Verified": "#28a745", "Remaining": "#ffc107"},
                 hole=0.4, title="Verification Progress")
    st.plotly_chart(fig, use_container_width=True)

    # ---------------------------
    # Verification section
    # ---------------------------
    st.markdown("### 🧩 Verify Your Items")

    search_query = st.text_input("🔍 Search for an item (optional):")
    filtered_df = (
        df[df["Particulars"].str.contains(search_query, case=False, na=False)]
        if search_query
        else df.copy()
    )

    verified_indices = []

    for i, row in filtered_df.iterrows():
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(
                    f"**{row['Particulars']}**  \nQty: {row['Qty']} | Rate: {row['Rate']} | Value: {row['Value']}"
                )
            with col2:
                tick = st.checkbox("✔", key=i, value=row["Verified"])
                if tick:
                    verified_indices.append(i)

    # Update verification status
    df.loc[verified_indices, "Verified"] = True

    # ---------------------------
    # Remaining items display
    # ---------------------------
    remaining_items = df[df["Verified"] == False]

    st.markdown("### 🧮 Remaining Items")
    if len(remaining_items) == 0:
        st.success("🎉 All items verified! Great job!")
    else:
        st.warning(f"⚠️ {len(remaining_items)} items are still unchecked.")
        st.dataframe(
            remaining_items[["Particulars", "Qty", "Rate", "Value"]],
            use_container_width=True
        )

else:
    st.info("👆 Upload your invoice CSV to get started.")
