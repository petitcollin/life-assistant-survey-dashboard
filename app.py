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
import streamlit as st
st.switch_page("pages/1_📊_Executive_Summary.py")

