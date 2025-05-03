import streamlit as st
import pandas as pd
import random
from io import BytesIO  # ADD THIS LINE

st.title("Marks Distribution Generator")

uploaded_file = st.file_uploader("Upload your Excel file with Total Marks", type=['xlsx'])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # ... rest of your logic ...

    result_df = pd.DataFrame(results)

    st.success("Marks distribution generated successfully!")

    st.dataframe(result_df)

    @st.cache_data
    def convert_df(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        processed_data = output.getvalue()
        return processed_data

    excel = convert_df(result_df)

    st.download_button(
        label="Download Marks Distribution as Excel",
        data=excel,
        file_name='marks_distribution.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
