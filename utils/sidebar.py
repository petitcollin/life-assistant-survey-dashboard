"""
Sidebar filter utilities.
"""
import streamlit as st
import pandas as pd
from utils.data_loader import get_filtered_data


def get_filter_state():
    """Get or initialize the filter state dictionary."""
    if 'filter_state' not in st.session_state:
        st.session_state.filter_state = {
            'country': [],
            'age': [],
            'gender': [],
            'usage': []
        }
    return st.session_state.filter_state


def render_sidebar_filters(df_processed):
    """Render sidebar filters and return filtered data."""
    
    # Get the persistent filter state
    filter_state = get_filter_state()
    
    with st.sidebar:
        # Country filter
        st.write("**Country**")
        available_countries = sorted([c for c in df_processed['Country'].unique() if pd.notna(c)]) if 'Country' in df_processed.columns else []
        country_options = ['NL', 'UK']
        
        selected_countries = st.multiselect(
            "Select countries",
            options=country_options,
            default=filter_state['country'] if filter_state['country'] else [],
            key='country_multiselect',
            label_visibility="collapsed"
        )
        filter_state['country'] = selected_countries
        
        if len(selected_countries) > 0:
            st.caption(f"✓ {len(selected_countries)} selected")
        else:
            st.caption("No filter (showing all)")
        
        st.markdown("---")
        
        # Age filter
        st.write("**Age Group**")
        age_options = sorted([age for age in df_processed['Q1'].unique() if pd.notna(age)])
        
        selected_ages = st.multiselect(
            "Select age groups",
            options=age_options,
            default=filter_state['age'] if filter_state['age'] else [],
            key='age_multiselect',
            label_visibility="collapsed"
        )
        filter_state['age'] = selected_ages
        
        if len(selected_ages) > 0:
            st.caption(f"✓ {len(selected_ages)} selected")
        else:
            st.caption("No filter (showing all)")
        
        st.markdown("---")
        
        # Gender filter
        st.write("**Gender**")
        gender_options = sorted([g for g in df_processed['Q2'].unique() if pd.notna(g)])
        
        selected_genders = st.multiselect(
            "Select genders",
            options=gender_options,
            default=filter_state['gender'] if filter_state['gender'] else [],
            key='gender_multiselect',
            label_visibility="collapsed"
        )
        filter_state['gender'] = selected_genders
        
        if len(selected_genders) > 0:
            st.caption(f"✓ {len(selected_genders)} selected")
        else:
            st.caption("No filter (showing all)")
        
        st.markdown("---")
        
        # Usage frequency filter
        st.write("**AI Usage Frequency**")
        usage_options = sorted([u for u in df_processed['Q3'].unique() if pd.notna(u)])
        
        selected_usage = st.multiselect(
            "Select usage frequency",
            options=usage_options,
            default=filter_state['usage'] if filter_state['usage'] else [],
            key='usage_multiselect',
            label_visibility="collapsed"
        )
        filter_state['usage'] = selected_usage
        
        if len(selected_usage) > 0:
            st.caption(f"✓ {len(selected_usage)} selected")
        else:
            st.caption("No filter (showing all)")
        
        st.markdown("---")
        
        # Apply filters - only include countries that exist in data
        country_filter = [c for c in selected_countries if c in available_countries]
        
        df_filtered = get_filtered_data(
            df_processed, 
            selected_ages, 
            selected_genders, 
            selected_usage,
            country_filter
        )
        
        # Show filtered count
        st.metric("Responses", len(df_filtered))
        
        # Reset button
        if st.button("Reset Filters", use_container_width=True, key='reset_filters'):
            st.session_state.filter_state = {
                'country': [],
                'age': [],
                'gender': [],
                'usage': []
            }
            # Clear the multiselect widget states
            if 'country_multiselect' in st.session_state:
                del st.session_state['country_multiselect']
            if 'age_multiselect' in st.session_state:
                del st.session_state['age_multiselect']
            if 'gender_multiselect' in st.session_state:
                del st.session_state['gender_multiselect']
            if 'usage_multiselect' in st.session_state:
                del st.session_state['usage_multiselect']
            st.rerun()
    
    return df_filtered
