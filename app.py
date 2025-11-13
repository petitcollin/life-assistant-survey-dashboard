"""
Main Streamlit App - AI Life Assistant Survey Dashboard
"""
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="AI Life Assistant Survey Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Redirect to Executive Summary
try:
    st.switch_page("pages/1_📊_Executive_Summary.py")
except Exception as e:
    # Fallback: if switch_page fails, just show a message and link
    st.title("AI Life Assistant Survey Dashboard")
    st.info("Please navigate to the Executive Summary page from the sidebar.")
    st.markdown("Or click here: [Executive Summary](pages/1_📊_Executive_Summary.py)")
    
    # Ensure sidebar navigation is visible
    st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {
        display: block !important;
    }
    </style>
    """, unsafe_allow_html=True)

