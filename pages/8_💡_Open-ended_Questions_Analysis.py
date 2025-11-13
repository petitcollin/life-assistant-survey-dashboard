"""
Insights & Analysis Page
"""
import streamlit as st
from utils.page_utils import init_page
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re
from utils.text_categorizer import (
    categorize_responses,
    get_sample_responses_by_category,
    Q13_CATEGORIES, 
    Q14_CATEGORIES, 
    Q15_CATEGORIES
)
from utils.charts import create_bar_chart

# Initialize page with filters
df = init_page()

st.title("💡 Open-ended Questions Analysis")
st.markdown("---")

# Text Analysis
st.subheader("Text Response Analysis")

def analyze_text_responses_english(df, column='Q13'):
    """Analyze English text responses from pre-translated columns."""
    # Use the English column directly
    english_column = f"{column}_english"
    
    if english_column not in df.columns:
        # Fallback to original if English doesn't exist
        if column in df.columns:
            english_column = column
        else:
            return None
    
    # Get responses
    responses = df[english_column].dropna().astype(str).tolist()
    
    # Filter out empty/invalid responses
    valid_responses = [r for r in responses if r and r.lower() not in ['nan', 'none', '']]
    
    if not valid_responses:
        return None
    
    # Word frequency analysis
    all_words = []
    for response in valid_responses:
        words = re.findall(r'\b\w+\b', response.lower())
        # Filter out common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'this', 'that', 'these', 'those', 'would', 'could', 
            'should', 'from', 'have', 'has', 'had', 'was', 'were', 'been', 'being', 
            'are', 'is', 'am', 'be', 'do', 'does', 'did', 'will', 'can', 'may', 
            'might', 'must', 'shall', 'want', 'wants', 'need', 'needs', 'get', 
            'gets', 'got', 'make', 'makes', 'made', 'help', 'helps', 'assistant'
        }
        words = [w for w in words if len(w) > 3 and w not in stop_words]
        all_words.extend(words)
    
    word_freq = Counter(all_words)
    top_words = word_freq.most_common(20)
    
    return {
        'total_responses': len(valid_responses),
        'top_words': top_words,
        'sample_responses': valid_responses[:10]
    }

tab1, tab2, tab3, tab4 = st.tabs(["Q13 - Time-consuming Tasks", "Q14 - Why Frustrating/Time-consuming", "Q15 - How AI Should Help", "Raw Data"])

with tab1:
    st.write("**What time-consuming or repetitive tasks would you want a digital AI assistant to help with?**")
    
    # Categorization
    st.subheader("Response Categories")
    q13_categories = categorize_responses(df, 'Q13', Q13_CATEGORIES)
    if q13_categories:
        # Sort by count descending (most to least)
        q13_categories_sorted = dict(sorted(q13_categories.items(), key=lambda x: x[1], reverse=True))
        q13_cat_series = pd.Series(q13_categories_sorted)
        
        # Create bar chart (sorted from most to least)
        fig = create_bar_chart(q13_cat_series, title="", orientation='h', show_percentage=True, total_responses=len(df))
        st.plotly_chart(fig, use_container_width=True)
        
        # Show sample responses per category
        st.subheader("Sample Responses by Category")
        q13_samples = get_sample_responses_by_category(df, 'Q13', Q13_CATEGORIES, num_samples=3)
        
        # Display samples in order of category frequency (most to least)
        for category in q13_categories_sorted.keys():
            if category in q13_samples and len(q13_samples[category]) > 0:
                st.write(f"**{category}** ({q13_categories_sorted[category]} responses):")
                for i, response in enumerate(q13_samples[category], 1):
                    st.write(f"  {i}. {response}")
                st.write("")
    else:
        st.info("No data available for Q13.")

with tab2:
    st.write("**Why do you find these tasks frustrating or time-consuming?**")
    
    # Categorization
    st.subheader("Response Categories")
    q14_categories = categorize_responses(df, 'Q14', Q14_CATEGORIES)
    if q14_categories:
        # Sort by count descending (most to least)
        q14_categories_sorted = dict(sorted(q14_categories.items(), key=lambda x: x[1], reverse=True))
        q14_cat_series = pd.Series(q14_categories_sorted)
        
        # Create bar chart (sorted from most to least)
        fig = create_bar_chart(q14_cat_series, title="", orientation='h', show_percentage=True, total_responses=len(df))
        st.plotly_chart(fig, use_container_width=True)
        
        # Show sample responses per category
        st.subheader("Sample Responses by Category")
        q14_samples = get_sample_responses_by_category(df, 'Q14', Q14_CATEGORIES, num_samples=3)
        
        # Display samples in order of category frequency (most to least)
        for category in q14_categories_sorted.keys():
            if category in q14_samples and len(q14_samples[category]) > 0:
                st.write(f"**{category}** ({q14_categories_sorted[category]} responses):")
                for i, response in enumerate(q14_samples[category], 1):
                    st.write(f"  {i}. {response}")
                st.write("")
    else:
        st.info("No responses available for Q14.")

with tab3:
    st.write("**How would you expect an AI assistant to help with these tasks?**")
    
    # Categorization
    st.subheader("Response Categories")
    q15_categories = categorize_responses(df, 'Q15', Q15_CATEGORIES)
    if q15_categories:
        # Sort by count descending (most to least)
        q15_categories_sorted = dict(sorted(q15_categories.items(), key=lambda x: x[1], reverse=True))
        q15_cat_series = pd.Series(q15_categories_sorted)
        
        # Create bar chart (sorted from most to least)
        fig = create_bar_chart(q15_cat_series, title="", orientation='h', show_percentage=True, total_responses=len(df))
        st.plotly_chart(fig, use_container_width=True)
        
        # Show sample responses per category
        st.subheader("Sample Responses by Category")
        q15_samples = get_sample_responses_by_category(df, 'Q15', Q15_CATEGORIES, num_samples=3)
        
        # Display samples in order of category frequency (most to least)
        for category in q15_categories_sorted.keys():
            if category in q15_samples and len(q15_samples[category]) > 0:
                st.write(f"**{category}** ({q15_categories_sorted[category]} responses):")
                for i, response in enumerate(q15_samples[category], 1):
                    st.write(f"  {i}. {response}")
                st.write("")
    else:
        st.info("No responses available for Q15.")

with tab4:
    st.write("**Raw Data - Q13, Q14, Q15 (English)**")
    
    # Create a dataframe with just the three English columns
    raw_data_columns = []
    column_names = []
    
    if 'Q13_english' in df.columns:
        raw_data_columns.append(df['Q13_english'])
        column_names.append('Q13 - Time-consuming Tasks')
    elif 'Q13' in df.columns:
        raw_data_columns.append(df['Q13'])
        column_names.append('Q13 - Time-consuming Tasks')
    
    if 'Q14_english' in df.columns:
        raw_data_columns.append(df['Q14_english'])
        column_names.append('Q14 - Why Frustrating/Time-consuming')
    elif 'Q14' in df.columns:
        raw_data_columns.append(df['Q14'])
        column_names.append('Q14 - Why Frustrating/Time-consuming')
    
    if 'Q15_english' in df.columns:
        raw_data_columns.append(df['Q15_english'])
        column_names.append('Q15 - How AI Should Help')
    elif 'Q15' in df.columns:
        raw_data_columns.append(df['Q15'])
        column_names.append('Q15 - How AI Should Help')
    
    if raw_data_columns:
        raw_df = pd.concat(raw_data_columns, axis=1)
        raw_df.columns = column_names
        
        # Filter out rows where all three columns are empty/NaN
        raw_df = raw_df.dropna(how='all')
        
        st.dataframe(raw_df, use_container_width=True, hide_index=False)
        st.write(f"**Total rows:** {len(raw_df)}")
    else:
        st.warning("No English columns found for Q13, Q14, or Q15.")

