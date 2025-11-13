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
        /* Ensure sidebar navigation is visible */
        [data-testid="stSidebarNav"] {
            display: block !important;
        }
        /* Hide only the app page link from sidebar navigation */
        [data-testid="stSidebarNav"] a[href*="app"]:not([href*="pages"]),
        [data-testid="stSidebarNav"] a[href="/"] {
            display: none !important;
        }
        </style>
        <script>
        function hideAppPage() {
            const sidebarNav = document.querySelector('[data-testid="stSidebarNav"]');
            if (sidebarNav) {
                const links = sidebarNav.querySelectorAll('a');
                links.forEach(link => {
                    const href = link.getAttribute('href') || '';
                    const text = link.textContent || '';
                    // Only hide links that are specifically the "app" page, not pages
                    if ((href === '/' || href.includes('/app') || text.toLowerCase().includes('app')) && 
                        !href.includes('pages') && 
                        !text.includes('📊') && 
                        !text.includes('👥') && 
                        !text.includes('🤖') && 
                        !text.includes('💚') && 
                        !text.includes('⚙️') && 
                        !text.includes('🚀') && 
                        !text.includes('💡') && 
                        !text.includes('📋')) {
                        const listItem = link.closest('li') || link.closest('[role="listitem"]');
                        if (listItem) {
                            listItem.style.display = 'none';
                        }
                    }
                });
            }
        }
        // Run after DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', hideAppPage);
        } else {
            hideAppPage();
        }
        setTimeout(hideAppPage, 500);
        setTimeout(hideAppPage, 1000);
        </script>
        <style>
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

