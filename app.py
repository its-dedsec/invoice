import streamlit as st
import pandas as pd

st.set_page_config(page_title="🧾 Smart Invoice Verifier", layout="wide")

st.title("🧾 Smart Invoice Verifier")

uploaded_file = st.file_uploader("📤 Upload Invoice CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df['Verified'] = False  # add status column

    if 'verified_items' not in st.session_state:
        st.session_state.verified_items = set()

    st.success("✅ Invoice loaded successfully!")
    total_items = len(df)
    remaining_items = total_items - len(st.session_state.verified_items)

    # Header stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📊 Total Items", total_items)
    with col2:
        st.metric("🕒 Remaining Items", remaining_items)

    # Search bar
    search_query = st.text_input("🔍 Search Item by Name").strip().lower()
    if search_query:
        filtered_df = df[df['Item'].str.lower().str.contains(search_query, na=False)]
    else:
        filtered_df = df.copy()

    st.write("### 🛒 Items List")

    for i, row in filtered_df.iterrows():
        item_name = row['Item']
        verified = i in st.session_state.verified_items

        cols = st.columns([3, 1])
        cols[0].write(f"**{item_name}**")

        if verified:
            cols[1].success("✅ Verified")
        else:
            if cols[1].button(f"Verify {i}", key=f"verify_{i}"):
                st.session_state.verified_items.add(i)
                st.rerun()

    # Remaining counter
    remaining_items = total_items - len(st.session_state.verified_items)
    st.info(f"🧾 Remaining Items to Verify: {remaining_items}")

    # Option to download verified version
    if remaining_items == 0:
        st.success("🎉 All items verified!")
        df['Verified'] = df.index.isin(st.session_state.verified_items)
        st.download_button(
            label="💾 Download Verified Invoice CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name='verified_invoice.csv',
            mime='text/csv'
        )
else:
    st.info("Please upload your invoice CSV to begin.")
