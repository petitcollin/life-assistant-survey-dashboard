"""
Export Data Page
"""
import streamlit as st
from utils.page_utils import init_page
import pandas as pd
from io import BytesIO
import numpy as np

# Initialize page with filters
df = init_page()

st.title("📥 Export Data")
st.markdown("---")

st.write("Download the survey data with readable column names and labels.")

# Question mappings for readable headers
QUESTION_MAPPINGS = {
    'Country': 'Country',
    'Q1': 'Age Group',
    'Q2': 'Gender',
    'Q3': 'How often do you use AI tools?',
    'Q4_1': 'Current Use: Planning or organizing my day, tasks, or schedule',
    'Q4_2': 'Current Use: Brainstorming ideas or creative content',
    'Q4_3': 'Current Use: Learning or studying something new',
    'Q4_4': 'Current Use: Online shopping or comparing products',
    'Q4_5': 'Current Use: Managing money or tracking expenses',
    'Q4_6': 'Current Use: Getting health, fitness, or wellness advice',
    'Q4_7': 'Current Use: Finding recipes and meal planning',
    'Q4_8': 'Current Use: Planning trips or activities',
    'Q4_9': 'Current Use: Searching for information, answering questions',
    'Q4_10': 'Current Use: Social or relationship advice',
    'Q4_11': 'Current Use: Getting motivation or mental health support',
    'Q4_12': 'Current Use: Practicing conversations or preparing for interviews',
    'Q4_13': 'Current Use: Helping with home projects or DIY tasks',
    'Q4_14': 'Current Use: Discovering new music, movies, books, or content',
    'Q4_15': 'Current Use: Other',
    'Q5_1': 'Comfort with proactive AI assistant (1=Not open at all, 5=Very open)',
    'Q6_1': 'Desired: Planning or organizing my day, tasks, or schedule',
    'Q6_2': 'Desired: Brainstorming ideas or creative content',
    'Q6_3': 'Desired: Learning or studying something new',
    'Q6_4': 'Desired: Online shopping or comparing products',
    'Q6_5': 'Desired: Managing money or tracking expenses',
    'Q6_6': 'Desired: Getting health, fitness, or wellness advice',
    'Q6_7': 'Desired: Finding recipes and meal planning',
    'Q6_8': 'Desired: Planning trips or activities',
    'Q6_9': 'Desired: Searching for information, answering questions',
    'Q6_10': 'Desired: Social or relationship advice',
    'Q6_11': 'Desired: Getting motivation or mental health support',
    'Q6_12': 'Desired: Practicing conversations or preparing for interviews',
    'Q6_13': 'Desired: Helping with home projects or DIY tasks',
    'Q6_14': 'Desired: Discovering new music, movies, books, or content',
    'Q6_15': 'Desired: Other',
    'Q7_1': 'Comfort with calendar/email access (1=Not comfortable at all, 5=Very comfortable)',
    'Q8': 'Preferred interaction method',
    'Q9_1': 'Comfort speaking to AI in public (1=Very uncomfortable, 5=Very comfortable)',
    'Q10_1': 'Motivator: It saves me time or makes my life easier',
    'Q10_2': 'Motivator: It helps me make better decisions',
    'Q10_3': 'Motivator: It helps me save money',
    'Q10_4': 'Motivator: It respects my privacy and data',
    'Q10_5': 'Motivator: It consistently delivers high-quality, accurate results',
    'Q10_6': 'Motivator: It\'s free or affordable',
    'Q10_7': 'Motivator: It feels natural and human-like to interact with',
    'Q10_8': 'Motivator: It has a trusted brand or reputation',
    'Q10_9': 'Motivator: It learns and improves based on my habits',
    'Q10_10': 'Motivator: It integrates well with the apps and tools I already use',
    'Q11_1': 'Barrier: I don\'t trust how my data would be used',
    'Q11_2': 'Barrier: It feels too robotic or impersonal',
    'Q11_3': 'Barrier: It makes mistakes or gives unreliable answers',
    'Q11_4': 'Barrier: It takes too much effort to set up or use',
    'Q11_5': 'Barrier: It doesn\'t integrate well with the tools I already use',
    'Q11_6': 'Barrier: It\'s too expensive',
    'Q11_7': 'Barrier: I worry it could replace human interaction',
    'Q11_8': 'Barrier: I don\'t see a clear benefit compared to what I already use',
    'Q11_9': 'Barrier: I prefer to stay in control and do things myself',
    'Q12': 'Preferred assistant behavior',
    'Q13': 'Time-consuming tasks (original)',
    'Q13_english': 'Time-consuming tasks',
    'Q13_English': 'Time-consuming tasks',
    'Q14': 'Why frustrating/time-consuming (original)',
    'Q14_english': 'Why do you find these tasks frustrating or time-consuming?',
    'Q14_English': 'Why do you find these tasks frustrating or time-consuming?',
    'Q15': 'How AI should help (original)',
    'Q15_english': 'How would you expect an AI assistant to help with these tasks?',
    'Q15_English': 'How would you expect an AI assistant to help with these tasks?',
}

def create_readable_dataframe(df):
    """Create a dataframe with readable column names."""
    from utils.data_loader import Q10_LABELS, Q11_LABELS
    
    df_export = df.copy()
    
    # Rename columns to readable names
    column_mapping = {}
    for col in df_export.columns:
        if col in QUESTION_MAPPINGS:
            column_mapping[col] = QUESTION_MAPPINGS[col]
        # Check if column was renamed during preprocessing (Q10 and Q11)
        elif col in Q10_LABELS.values():
            # This is a renamed Q10 column, find the original
            for orig_col, label in Q10_LABELS.items():
                if label == col:
                    column_mapping[col] = f'Motivator: {label}'
                    break
        elif col in Q11_LABELS.values():
            # This is a renamed Q11 column
            for orig_col, label in Q11_LABELS.items():
                if label == col:
                    column_mapping[col] = f'Barrier: {label}'
                    break
        elif col.startswith('Q4_') and col not in QUESTION_MAPPINGS:
            # Handle any Q4 columns we might have missed
            column_mapping[col] = f'Current Use: {col}'
        elif col.startswith('Q6_') and col not in QUESTION_MAPPINGS:
            # Handle any Q6 columns we might have missed
            column_mapping[col] = f'Desired: {col}'
        elif col.startswith('Q10_') and col not in QUESTION_MAPPINGS:
            # Handle any Q10 columns we might have missed
            column_mapping[col] = f'Motivator: {col}'
        elif col.startswith('Q11_') and col not in QUESTION_MAPPINGS:
            # Handle any Q11 columns we might have missed
            column_mapping[col] = f'Barrier: {col}'
    
    df_export = df_export.rename(columns=column_mapping)
    
    # For multiple choice questions, convert 1/0 to Yes/No for readability
    yes_no_columns = [col for col in df_export.columns if any(x in col for x in ['Current Use:', 'Desired:', 'Motivator:', 'Barrier:'])]
    for col in yes_no_columns:
        if col in df_export.columns:
            # Convert numeric to Yes/No
            df_export[col] = df_export[col].apply(
                lambda x: 'Yes' if (x == 1 or x is True or x == '1') 
                         else ('No' if (x == 0 or x is False or x == '0' or pd.isna(x)) else x)
            )
    
    return df_export

# Create readable dataframe
df_readable = create_readable_dataframe(df)

# Display preview
st.subheader("Data Preview")
st.write(f"**Total responses:** {len(df_readable)}")
st.dataframe(df_readable.head(10), use_container_width=True)

st.markdown("---")

# Export options
st.subheader("Download Data")

col1, col2 = st.columns(2)

with col1:
    st.write("**Download as CSV**")
    csv = df_readable.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📄 Download CSV",
        data=csv,
        file_name=f"life_assistant_survey_data_{len(df_readable)}_responses.csv",
        mime="text/csv",
        use_container_width=True
    )

with col2:
    st.write("**Download as Excel**")
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_readable.to_excel(writer, index=False, sheet_name='Survey Data')
    excel_data = output.getvalue()
    st.download_button(
        label="📊 Download Excel",
        data=excel_data,
        file_name=f"life_assistant_survey_data_{len(df_readable)}_responses.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

st.markdown("---")

# Information about the data
with st.expander("ℹ️ About the Export"):
    st.write("""
    **Data Format:**
    - All column names use the actual survey questions instead of codes (Q1, Q2, etc.)
    - Multiple choice questions (Q4, Q6, Q10, Q11) show "Yes" or "No" for each option
    - Likert scale questions (Q5, Q7, Q9) show the numeric value (1-5) with descriptions in the column name
    - Text responses (Q13, Q14, Q15) include both original and English translations
    
    **Filters Applied:**
    - The exported data reflects any filters you've applied in the sidebar
    - To export all data, use "Reset Filters" in the sidebar first
    """)

