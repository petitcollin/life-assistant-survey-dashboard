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
        /* Ensure sidebar navigation is visible and not hidden */
        [data-testid="stSidebarNav"] {
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
        }
        /* Compact sidebar styling */
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div {
            padding-top: 0.25rem;
            padding-bottom: 0.25rem;
        }
        [data-testid="stSidebar"] .stSelectbox > label {
            margin-bottom: 0.1rem;
            font-size: 0.9rem;
        }
        [data-testid="stSidebar"] [data-testid="stMetricValue"] {
            font-size: 1.1rem;
        }
        [data-testid="stSidebar"] [data-testid="stMetricLabel"] {
            font-size: 0.85rem;
        }
        [data-testid="stSidebar"] .stButton > button {
            padding: 0.3rem;
            font-size: 0.9rem;
            margin-top: 0.3rem;
        }
        [data-testid="stSidebar"] {
            padding-top: 1rem;
        }
        </style>
        <script>
        // Only hide the "app" page link, keep all other navigation visible
        function hideAppPageOnly() {
            const sidebarNav = document.querySelector('[data-testid="stSidebarNav"]');
            if (sidebarNav) {
                // Make sure navigation is visible
                sidebarNav.style.display = 'block';
                sidebarNav.style.visibility = 'visible';
                
                const links = sidebarNav.querySelectorAll('a');
                links.forEach(link => {
                    const href = link.getAttribute('href') || '';
                    const text = (link.textContent || '').trim().toLowerCase();
                    
                    // Only hide if it's specifically the app page (no emoji, just "app" or root)
                    if (href === '/' || (href.includes('app') && !href.includes('pages') && text === 'app')) {
                        const listItem = link.closest('li') || link.closest('[role="listitem"]');
                        if (listItem) {
                            listItem.style.display = 'none';
                        }
                    }
                });
            }
        }
        // Run after a delay to ensure DOM is ready
        setTimeout(hideAppPageOnly, 100);
        setTimeout(hideAppPageOnly, 500);
        </script>
    """, unsafe_allow_html=True)


def init_page():
    """Initialize page with data loading and sidebar filters."""
    # Apply compact sidebar CSS
    apply_compact_sidebar_css()
    
    # Initialize data if not already loaded
    if 'data_loaded' not in st.session_state:
        df_raw = load_data()
        df_processed = preprocess_data(df_raw)
        st.session_state.df_processed = df_processed
        st.session_state.data_loaded = True
    
    # Render sidebar filters and get filtered data
    df = render_sidebar_filters(st.session_state.df_processed)
    
    return df

