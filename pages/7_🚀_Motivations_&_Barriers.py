"""
Motivations & Barriers Page
"""
import streamlit as st
from utils.page_utils import init_page
from utils.charts import create_bar_chart
from utils.data_loader import get_multiple_choice_counts, Q10_LABELS, Q11_LABELS
import pandas as pd

# Initialize page with filters
df = init_page()

st.title("🚀 Motivations & Barriers")
st.markdown("---")

# Motivations
st.subheader("What Matters Most")
st.write("What matters to you most when thinking about using an AI assistant?")

q10_counts = get_multiple_choice_counts(df, 'Q10_', Q10_LABELS)
if len(q10_counts) > 0:
    # Calculate percentages based on total number of respondents
    total_responses = len(df)
    
    # Create chart with percentages (using total_responses as denominator)
    fig = create_bar_chart(q10_counts, title="", orientation='h', show_percentage=True, total_responses=total_responses)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for motivations.")

st.markdown("---")

# Barriers
st.subheader("What Would Prevent Usage")
st.write("What would make you NOT want to use a personal AI assistant?")

q11_counts = get_multiple_choice_counts(df, 'Q11_', Q11_LABELS)
if len(q11_counts) > 0:
    # Calculate percentages based on total number of respondents
    total_responses = len(df)
    
    # Create chart with percentages (using total_responses as denominator)
    fig = create_bar_chart(q11_counts, title="", orientation='h', show_percentage=True, total_responses=total_responses)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for barriers.")

st.markdown("---")

# Summary Insights
st.subheader("💡 Key Takeaways")

col1, col2 = st.columns(2)

with col1:
    st.success("**Top 3 Motivators:**")
    if len(q10_counts) > 0:
        for i, (motivator, count) in enumerate(q10_counts.head(3).items(), 1):
            st.write(f"{i}. {motivator} ({count} responses)")
    else:
        st.write("No data available.")

with col2:
    st.error("**Top 3 Barriers:**")
    if len(q11_counts) > 0:
        for i, (barrier, count) in enumerate(q11_counts.head(3).items(), 1):
            st.write(f"{i}. {barrier} ({count} responses)")
    else:
        st.write("No data available.")

