"""
Utility functions for page initialization.
"""
import streamlit as st
import sys
import os

# Add utils to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.sidebar import render_sidebar_filters
from utils.data_loader import load_data, preprocess_data


def apply_compact_sidebar_css():
    """Apply compact CSS to sidebar to fit everything without scrolling."""
    st.markdown("""
        <style>
        /* Ensure sidebar navigation is ALWAYS visible */
        [data-testid="stSidebarNav"],
        [data-testid="stSidebarNav"] ul,
        [data-testid="stSidebarNav"] li {
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
        }
        
        /* Compact sidebar styling for filters only */
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div {
            padding-top: 0.25rem;
            padding-bottom: 0.25rem;
        }
        [data-testid="stSidebar"] .stSelectbox > label {
            margin-bottom: 0.1rem;
            font-size: 0.9rem;
        }
        [data-testid="stSidebar"] .stCheckbox {
            margin-bottom: 0.1rem;
        }
        [data-testid="stSidebar"] .stCheckbox > label {
            font-size: 0.9rem;
            padding-top: 0.1rem;
            padding-bottom: 0.1rem;
        }
        [data-testid="stSidebar"] [data-testid="stMetricValue"] {
            font-size: 1.1rem;
        }
        [data-testid="stSidebar"] [data-testid="stMetricLabel"] {
            font-size: 0.85rem;
        }
        [data-testid="stSidebar"] .stButton > button {
            padding: 0.3rem;
            font-size: 0.85rem;
            margin-top: 0.2rem;
            margin-bottom: 0.2rem;
        }
        [data-testid="stSidebar"] .stCaption {
            font-size: 0.8rem;
            margin-top: 0.1rem;
            margin-bottom: 0.3rem;
        }
        </style>
        <script>
        // Ensure navigation is visible and only hide the "app" page link
        function ensureNavVisible() {
            const sidebarNav = document.querySelector('[data-testid="stSidebarNav"]');
            if (sidebarNav) {
                // Force navigation to be visible
                sidebarNav.style.display = 'block';
                sidebarNav.style.visibility = 'visible';
                sidebarNav.style.opacity = '1';
                
                // Only hide the "app" page link (root or app.py)
                const links = sidebarNav.querySelectorAll('a');
                links.forEach(link => {
                    const href = link.getAttribute('href') || '';
                    const text = (link.textContent || '').trim();
                    
                    // Only hide if it's the root "/" or "app" without pages
                    if (href === '/' || (href.includes('/app') && !href.includes('pages') && text.toLowerCase() === 'app')) {
                        const listItem = link.closest('li') || link.closest('[role="listitem"]');
                        if (listItem) {
                            listItem.style.display = 'none';
                        }
                    } else {
                        // Make sure all other links are visible
                        const listItem = link.closest('li') || link.closest('[role="listitem"]');
                        if (listItem) {
                            listItem.style.display = 'block';
                            listItem.style.visibility = 'visible';
                        }
                    }
                });
            }
        }
        // Run multiple times to ensure it works
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', ensureNavVisible);
        } else {
            ensureNavVisible();
        }
        setTimeout(ensureNavVisible, 100);
        setTimeout(ensureNavVisible, 500);
        setTimeout(ensureNavVisible, 1000);
        </script>
    """, unsafe_allow_html=True)


def init_page():
    """Initialize page with data loading and sidebar filters."""
    # Apply compact sidebar CSS
    apply_compact_sidebar_css()
    
    # Cache version to force refresh when data changes
    CACHE_VERSION = "v2.3"
    
    # Initialize data - always reload to ensure we have the latest
    # Check if we need to reload based on cache version
    if 'cache_version' not in st.session_state or st.session_state.cache_version != CACHE_VERSION:
        df_raw = load_data(cache_version=CACHE_VERSION)
        df_processed = preprocess_data(df_raw, cache_version=CACHE_VERSION)
        st.session_state.df_processed = df_processed
        st.session_state.cache_version = CACHE_VERSION
        st.session_state.data_loaded = True
    elif 'df_processed' not in st.session_state:
        # Fallback: load if session state is missing
        df_raw = load_data(cache_version=CACHE_VERSION)
        df_processed = preprocess_data(df_raw, cache_version=CACHE_VERSION)
        st.session_state.df_processed = df_processed
        st.session_state.cache_version = CACHE_VERSION
        st.session_state.data_loaded = True
    
    # Render sidebar filters and get filtered data
    df = render_sidebar_filters(st.session_state.df_processed)
    
    return df

