import streamlit as st
import pandas as pd
import random
from io import BytesIO

st.title("Marks Distribution Generator")

uploaded_file = st.file_uploader("Upload your Excel file with Total Marks", type=['xlsx'])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Check if 'Total Marks' column exists
    if 'Total Marks' not in df.columns:
        st.error("The Excel file must have a 'Total Marks' column.")
    else:
        results = []

        for index, row in df.iterrows():
            total_marks = row['Total Marks']

            # Ensure it's numeric (if not, set to 0)
            try:
                total_marks = int(total_marks)
            except (ValueError, TypeError):
                total_marks = 0

            # Part A: Random 0-2 marks for 5 questions
            part_a = [random.randint(0, 2) for _ in range(5)]
            part_a_total = sum(part_a)

            # Part B: Remaining marks
            remaining = total_marks - part_a_total

            # Random distribution for Part B (5 questions, each 0–8)
            part_b = [0] * 5
            for i in range(max(0, remaining)):
                available = [idx for idx in range(5) if part_b[idx] < 8]
                if not available:
                    break
                pick = random.choice(available)
                part_b[pick] += 1

            part_b_total = sum(part_b)

            results.append({
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
            })

        if results:  # ✅ Only proceed if we have results
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
