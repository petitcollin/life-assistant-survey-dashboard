"""
Sidebar filter utilities.
"""
import streamlit as st
import pandas as pd
from utils.data_loader import get_filtered_data


def render_sidebar_filters(df_processed):
    """Render sidebar filters and return filtered data."""
    with st.sidebar:
        # Age filter
        age_options = ['All'] + sorted([age for age in df_processed['Q1'].unique() if pd.notna(age)])
        age_filter = st.selectbox(
            "Age Group",
            age_options,
            key='age_filter',
            label_visibility="visible"
        )
        
        # Gender filter
        gender_options = ['All'] + sorted([g for g in df_processed['Q2'].unique() if pd.notna(g)])
        gender_filter = st.selectbox(
            "Gender",
            gender_options,
            key='gender_filter',
            label_visibility="visible"
        )
        
        # Usage frequency filter
        usage_options = ['All'] + sorted([u for u in df_processed['Q3'].unique() if pd.notna(u)])
        usage_filter = st.selectbox(
            "AI Usage Frequency",
            usage_options,
            key='usage_filter',
            label_visibility="visible"
        )
        
        # Apply filters
        df_filtered = get_filtered_data(df_processed, age_filter, gender_filter, usage_filter)
        
        # Show filtered count
        st.metric("Responses", len(df_filtered))
        
        # Reset button
        if st.button("Reset Filters", use_container_width=True, key='reset_filters'):
            st.session_state.age_filter = 'All'
            st.session_state.gender_filter = 'All'
            st.session_state.usage_filter = 'All'
            st.rerun()
    
    return df_filtered

