"""
Sidebar filter utilities.
"""
import streamlit as st
import pandas as pd
from utils.data_loader import get_filtered_data


def render_sidebar_filters(df_processed):
    """Render sidebar filters and return filtered data."""
    with st.sidebar:
        # Initialize session state for multi-select filters
        if 'country_filter_selected' not in st.session_state:
            # Default: both countries selected
            st.session_state.country_filter_selected = ['NL', 'UK']
        if 'age_filter_selected' not in st.session_state:
            st.session_state.age_filter_selected = []
        if 'gender_filter_selected' not in st.session_state:
            st.session_state.gender_filter_selected = []
        if 'usage_filter_selected' not in st.session_state:
            st.session_state.usage_filter_selected = []
        
        # Country filter - Multi-select with checkboxes
        st.write("**Country**")
        country_options = sorted([c for c in df_processed['Country'].unique() if pd.notna(c)])
        country_filter_selected = []
        for country in country_options:
            checkbox_key = f'country_checkbox_{country}'
            if checkbox_key not in st.session_state:
                # Default: both countries selected
                st.session_state[checkbox_key] = country in ['NL', 'UK']
            checked = st.checkbox(
                country,
                value=st.session_state[checkbox_key],
                key=checkbox_key,
                label_visibility="visible"
            )
            if checked:
                country_filter_selected.append(country)
        st.session_state.country_filter_selected = country_filter_selected
        
        # Show active filter count
        if len(country_filter_selected) > 0:
            st.caption(f"✓ {len(country_filter_selected)} selected")
        else:
            st.caption("No filter (showing all)")
        
        st.markdown("---")
        
        # Age filter - Multi-select with checkboxes
        st.write("**Age Group**")
        age_options = sorted([age for age in df_processed['Q1'].unique() if pd.notna(age)])
        age_filter_selected = []
        for age in age_options:
            checkbox_key = f'age_checkbox_{age}'
            if checkbox_key not in st.session_state:
                st.session_state[checkbox_key] = False
            checked = st.checkbox(
                age,
                value=st.session_state[checkbox_key],
                key=checkbox_key,
                label_visibility="visible"
            )
            if checked:
                age_filter_selected.append(age)
        st.session_state.age_filter_selected = age_filter_selected
        
        # Show active filter count
        if len(age_filter_selected) > 0:
            st.caption(f"✓ {len(age_filter_selected)} selected")
        else:
            st.caption("No filter (showing all)")
        
        st.markdown("---")
        
        # Gender filter - Multi-select with checkboxes
        st.write("**Gender**")
        gender_options = sorted([g for g in df_processed['Q2'].unique() if pd.notna(g)])
        gender_filter_selected = []
        for gender in gender_options:
            checkbox_key = f'gender_checkbox_{gender}'
            if checkbox_key not in st.session_state:
                st.session_state[checkbox_key] = False
            checked = st.checkbox(
                gender,
                value=st.session_state[checkbox_key],
                key=checkbox_key,
                label_visibility="visible"
            )
            if checked:
                gender_filter_selected.append(gender)
        st.session_state.gender_filter_selected = gender_filter_selected
        
        # Show active filter count
        if len(gender_filter_selected) > 0:
            st.caption(f"✓ {len(gender_filter_selected)} selected")
        else:
            st.caption("No filter (showing all)")
        
        st.markdown("---")
        
        # Usage frequency filter - Multi-select with checkboxes
        st.write("**AI Usage Frequency**")
        usage_options = sorted([u for u in df_processed['Q3'].unique() if pd.notna(u)])
        usage_filter_selected = []
        for usage in usage_options:
            checkbox_key = f'usage_checkbox_{usage}'
            if checkbox_key not in st.session_state:
                st.session_state[checkbox_key] = False
            checked = st.checkbox(
                usage,
                value=st.session_state[checkbox_key],
                key=checkbox_key,
                label_visibility="visible"
            )
            if checked:
                usage_filter_selected.append(usage)
        st.session_state.usage_filter_selected = usage_filter_selected
        
        # Show active filter count
        if len(usage_filter_selected) > 0:
            st.caption(f"✓ {len(usage_filter_selected)} selected")
        else:
            st.caption("No filter (showing all)")
        
        st.markdown("---")
        
        # Apply filters
        df_filtered = get_filtered_data(
            df_processed, 
            age_filter_selected, 
            gender_filter_selected, 
            usage_filter_selected,
            country_filter_selected
        )
        
        # Show filtered count
        st.metric("Responses", len(df_filtered))
        
        # Reset button
        if st.button("Reset Filters", use_container_width=True, key='reset_filters'):
            # Reset country filters to default (both selected)
            for country in country_options:
                st.session_state[f'country_checkbox_{country}'] = country in ['NL', 'UK']
            # Clear all other checkbox states
            for age in age_options:
                st.session_state[f'age_checkbox_{age}'] = False
            for gender in gender_options:
                st.session_state[f'gender_checkbox_{gender}'] = False
            for usage in usage_options:
                st.session_state[f'usage_checkbox_{usage}'] = False
            st.session_state.country_filter_selected = ['NL', 'UK']
            st.session_state.age_filter_selected = []
            st.session_state.gender_filter_selected = []
            st.session_state.usage_filter_selected = []
            st.rerun()
    
    return df_filtered

