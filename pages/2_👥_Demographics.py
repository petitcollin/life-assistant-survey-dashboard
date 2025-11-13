"""
Demographics Page
"""
import streamlit as st
from utils.page_utils import init_page
from utils.charts import create_bar_chart, create_pie_chart

# Initialize page with filters
df = init_page()

st.title("👥 Demographics")
st.markdown("---")

# Age Distribution
st.subheader("Age Groups")
age_dist = df['Q1'].value_counts()
if len(age_dist) > 0:
    fig = create_bar_chart(age_dist, title="", orientation='v', show_percentage=True)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Gender Distribution
st.subheader("Gender Distribution")
gender_dist = df['Q2'].value_counts()
if len(gender_dist) > 0:
    fig = create_pie_chart(gender_dist, title="", show_labels=True, show_legend=True)
    st.plotly_chart(fig, use_container_width=True)

