"""
Sidebar filter utilities.
"""
import streamlit as st
import pandas as pd
from utils.data_loader import get_filtered_data


def render_sidebar_filters(df_processed):
    """Render sidebar filters and return filtered data."""
    with st.sidebar:
        # Country filter - Multi-select with checkboxes
        st.write("**Country**")
        # Get available countries from data
        available_countries = sorted([c for c in df_processed['Country'].unique() if pd.notna(c)]) if 'Country' in df_processed.columns else []
        # Always show both NL and UK options
        country_options = ['NL', 'UK']
        country_filter_selected = []
        
        for country in country_options:
            checkbox_key = f'country_checkbox_{country}'
            # Set default value only if key doesn't exist yet
            if checkbox_key not in st.session_state:
                st.session_state[checkbox_key] = True  # Default: both selected
            
            # Show checkbox - let Streamlit manage state via key
            checked = st.checkbox(
                country,
                key=checkbox_key,
                label_visibility="visible"
            )
            
            # Only add to filter if checked AND country exists in data
            if checked and country in available_countries:
                country_filter_selected.append(country)
        
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
                st.session_state[checkbox_key] = False  # Default: not selected
            
            checked = st.checkbox(
                age,
                key=checkbox_key,
                label_visibility="visible"
            )
            if checked:
                age_filter_selected.append(age)
        
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
                st.session_state[checkbox_key] = False  # Default: not selected
            
            checked = st.checkbox(
                gender,
                key=checkbox_key,
                label_visibility="visible"
            )
            if checked:
                gender_filter_selected.append(gender)
        
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
                st.session_state[checkbox_key] = False  # Default: not selected
            
            checked = st.checkbox(
                usage,
                key=checkbox_key,
                label_visibility="visible"
            )
            if checked:
                usage_filter_selected.append(usage)
        
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
            # Reset country checkboxes to True (default)
            for country in country_options:
                st.session_state[f'country_checkbox_{country}'] = True
            # Reset other checkboxes to False
            for age in age_options:
                st.session_state[f'age_checkbox_{age}'] = False
            for gender in gender_options:
                st.session_state[f'gender_checkbox_{gender}'] = False
            for usage in usage_options:
                st.session_state[f'usage_checkbox_{usage}'] = False
            st.rerun()
    
    return df_filtered
