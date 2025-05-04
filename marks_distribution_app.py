import streamlit as st
import pandas as pd
import numpy as np
import random
from io import BytesIO

st.title("Marks Distribution App")

uploaded_file = st.file_uploader("Upload an Excel file with a 'Total Marks' column", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    results = []

    for idx, row in df.iterrows():
        # Safely convert 'Total Marks' to int, handle invalid/missing cases
        try:
            total_marks = int(row['Total Marks'])
        except (ValueError, TypeError):
            total_marks = 0  # You can choose to skip rows instead of setting to 0

        # Part A: distribute randomly but ensure sum <= total_marks and each <= 2
        part_a = [0] * 5
        remaining_a = min(total_marks, 10)  # Max 10 total across 5 questions (2 per question)

        while remaining_a > 0:
            available = [i for i in range(5) if part_a[i] < 2]
            if not available:
                break
            pick = random.choice(available)
            part_a[pick] += 1
            remaining_a -= 1

        part_a_total = sum(part_a)

        # Part B: distribute remaining marks (if any)
        remaining = total_marks - part_a_total
        part_b = [0] * 5

        while remaining > 0:
            available = [i for i in range(5) if part_b[i] < 8]
            if not available:
                break
            pick = random.choice(available)
            max_add = min(8 - part_b[pick], remaining)
            add = random.randint(1, max_add)
            part_b[pick] += add
            remaining -= add

        part_b_total = sum(part_b)

        result = {
            'Total Marks': total_marks,
            'Part A Q1': part_a[0],
            'Part A Q2': part_a[1],
            'Part A Q3': part_a[2],
            'Part A Q4': part_a[3],
            'Part A Q5': part_a[4],
            'Part A Total': part_a_total,
            'Part B Q1': part_b[0],
            'Part B Q2': part_b[1],
            'Part B Q3': part_b[2],
            'Part B Q4': part_b[3],
            'Part B Q5': part_b[4],
            'Part B Total': part_b_total,
        }
        results.append(result)

    result_df = pd.DataFrame(results)
    st.dataframe(result_df)

    # Function to convert DataFrame to Excel in-memory
    def convert_df_to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        processed_data = output.getvalue()
        return processed_data

    excel = convert_df_to_excel(result_df)

    st.download_button(
        label="Download distribution as Excel",
        data=excel,
        file_name='marks_distribution_result.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
