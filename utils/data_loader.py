"""
Data loading and preprocessing utilities for the AI Life Assistant Survey dashboard.
"""
import pandas as pd
import streamlit as st

# Value labels mapping based on survey structure
VALUE_LABELS = {
    'Q1': {
        1: '18-24',
        2: '25-34',
        3: '35-44',
        4: '45-54',
        5: '55+'
    },
    'Q2': {
        1: 'Male',
        2: 'Female',
        3: 'Non-binary'
    },
    'Q3': {
        1: 'Daily',
        2: 'Occasionally',
        3: "I've only tried it once or twice",
        4: "I don't use AI tools"
    },
    'Q8': {
        1: 'Text only',
        2: 'Voice only',
        3: 'Both (text and voice)'
    },
    'Q12': {
        1: 'Do it with me (helpful partner)',
        2: 'Do it for me (automatic)',
        3: 'It depends on the task'
    }
}

# Question labels for multiple choice questions
Q4_LABELS = {
    'Q4_1': 'Planning or organizing my day, tasks, or schedule',
    'Q4_2': 'Brainstorming ideas or creative content',
    'Q4_3': 'Learning or studying something new',
    'Q4_4': 'Online shopping or comparing products',
    'Q4_5': 'Managing money or tracking expenses',
    'Q4_6': 'Getting health, fitness, or wellness advice',
    'Q4_7': 'Finding recipes and meal planning',
    'Q4_8': 'Planning trips or activities',
    'Q4_9': 'Searching for information, answering questions',
    'Q4_10': 'Social or relationship advice',
    'Q4_11': 'Getting motivation or mental health support',
    'Q4_12': 'Practicing conversations or preparing for interviews',
    'Q4_13': 'Helping with home projects or DIY tasks',
    'Q4_14': 'Discovering new music, movies, books, or content',
    'Q4_15': 'Other'
}

Q6_LABELS = {
    'Q6_1': 'Planning or organizing my day, tasks, or schedule',
    'Q6_2': 'Brainstorming ideas or creative content',
    'Q6_3': 'Learning or studying something new',
    'Q6_4': 'Online shopping or comparing products',
    'Q6_5': 'Managing money or tracking expenses',
    'Q6_6': 'Getting health, fitness, or wellness advice',
    'Q6_7': 'Finding recipes and meal planning',
    'Q6_8': 'Planning trips or activities',
    'Q6_9': 'Searching for information, answering questions',
    'Q6_10': 'Social or relationship advice',
    'Q6_11': 'Getting motivation or mental health support',
    'Q6_12': 'Practicing conversations or preparing for interviews',
    'Q6_13': 'Helping with home projects or DIY tasks',
    'Q6_14': 'Discovering new music, movies, books, or content',
    'Q6_15': 'Other'
}

Q10_LABELS = {
    'Q10_1': 'It saves me time or makes my life easier',
    'Q10_2': 'It helps me make better decisions',
    'Q10_3': 'It helps me save money',
    'Q10_4': 'It respects my privacy and data',
    'Q10_5': 'It consistently delivers high-quality, accurate results',
    'Q10_6': "It's free or affordable",
    'Q10_7': 'It feels natural and human-like to interact with',
    'Q10_8': 'It has a trusted brand or reputation',
    'Q10_9': 'It learns and improves based on my habits',
    'Q10_10': 'It integrates well with the apps and tools I already use'
}

Q11_LABELS = {
    'Q11_1': "I don't trust how my data would be used",
    'Q11_2': 'It feels too robotic or impersonal',
    'Q11_3': 'It makes mistakes or gives unreliable answers',
    'Q11_4': 'It takes too much effort to set up or use',
    'Q11_5': "It doesn't integrate well with the tools I already use",
    'Q11_6': "It's too expensive",
    'Q11_7': 'I worry it could replace human interaction',
    'Q11_8': "I don't see a clear benefit compared to what I already use",
    'Q11_9': 'I prefer to stay in control and do things myself'
}

LIKERT_LABELS = {
    1: '1 (Low)',
    2: '2',
    3: '3 (Neutral)',
    4: '4',
    5: '5 (High)'
}


@st.cache_data
def load_data(cache_version="v2.0"):
    """Load the survey data from Excel file."""
    # Try the new Excel file first (1000 records), then fallback to others
    try:
        df = pd.read_excel('data/Life Assistant survey 2 (1).xlsx')
    except:
        try:
            df = pd.read_excel('data/Life Assistant survey 2.xlsx')
        except:
            try:
                df = pd.read_excel('data/ORD-95068-Z6P5Y2_2025-11-12_DD.xlsx')
            except:
                df = pd.read_csv('data/Life_Assistant_survey_2.csv')
    return df


@st.cache_data
def preprocess_data(df, cache_version="v2.0"):
    """Preprocess the data with value labels and clean missing values."""
    df_processed = df.copy()
    
    # Apply value labels only to categorical questions (not Likert scales)
    for col, labels in VALUE_LABELS.items():
        if col in df_processed.columns:
            df_processed[col] = df_processed[col].map(labels).fillna(df_processed[col])
    
    # Keep Likert scale columns (Q5_1, Q7_1, Q9_1) as numeric - don't convert them
    
    # Create readable column names for multiple choice questions
    # Note: We don't rename Q4 and Q6 to avoid duplicate column names (they share the same labels)
    # Instead, we'll access them by their original names and map to labels when displaying
    
    # Q10 - Motivations (rename these as they don't conflict)
    q10_mapping = {col: Q10_LABELS.get(col, col) for col in df.columns if col.startswith('Q10_')}
    
    # Q11 - Barriers (rename these as they don't conflict)
    q11_mapping = {col: Q11_LABELS.get(col, col) for col in df.columns if col.startswith('Q11_')}
    
    # Combine mappings (only Q10 and Q11 to avoid duplicates)
    column_mapping = {**q10_mapping, **q11_mapping}
    df_processed = df_processed.rename(columns=column_mapping)
    
    # Normalize English column names (handle both Q13_English and Q13_english)
    english_col_mapping = {}
    for col in df_processed.columns:
        if col == 'Q13_English':
            english_col_mapping[col] = 'Q13_english'
        elif col == 'Q14_English':
            english_col_mapping[col] = 'Q14_english'
        elif col == 'Q15_English':
            english_col_mapping[col] = 'Q15_english'
    if english_col_mapping:
        df_processed = df_processed.rename(columns=english_col_mapping)
    
    return df_processed


def get_filtered_data(df, age_filter=None, gender_filter=None, usage_filter=None):
    """Apply filters to the dataset."""
    df_filtered = df.copy()
    
    if age_filter and age_filter != 'All':
        df_filtered = df_filtered[df_filtered['Q1'] == age_filter]
    
    if gender_filter and gender_filter != 'All':
        df_filtered = df_filtered[df_filtered['Q2'] == gender_filter]
    
    if usage_filter and usage_filter != 'All':
        df_filtered = df_filtered[df_filtered['Q3'] == usage_filter]
    
    return df_filtered


def get_multiple_choice_counts(df, question_prefix, labels_dict):
    """Get counts for multiple choice questions."""
    counts = {}
    
    # First, try to find original column names (Q4_1, Q4_2, etc.) in the dataframe
    # These exist for Q4 and Q6 because we don't rename them to avoid duplicate column names
    cols = [col for col in df.columns if col.startswith(question_prefix) and not col.endswith('_other')]
    
    # If no original columns found, the columns might have been renamed (Q10, Q11)
    # In that case, look for the renamed labels directly
    if not cols:
        # Check if the labels from labels_dict exist as column names (renamed columns)
        for original_col, label in labels_dict.items():
            if label in df.columns:
                cols.append(label)
    
    # Process each column
    for col in cols:
        if col in df.columns:
            # Determine the label to use
            # If col is an original name (Q4_1, etc.), use the label from dict
            # If col is already a label (renamed), use it directly
            if col in labels_dict.values():
                label = col  # Already renamed to label
            else:
                label = labels_dict.get(col, col)  # Get label from dict
            
            col_data = df[col]
            
            # Handle case where column access returns DataFrame (duplicate names)
            if isinstance(col_data, pd.DataFrame):
                # Get first column if multiple exist
                col_data = col_data.iloc[:, 0]
            
            try:
                # Convert to numeric, fill NaN with 0, then sum
                value = pd.to_numeric(col_data, errors='coerce').fillna(0).sum()
                counts[label] = int(value) if not pd.isna(value) else 0
            except (ValueError, TypeError):
                counts[label] = 0
    
    return pd.Series(counts).sort_values(ascending=False)


def get_likert_distribution(df, col):
    """Get distribution for Likert scale questions."""
    if col not in df.columns:
        return pd.Series()
    
    distribution = df[col].value_counts().sort_index()
    return distribution

