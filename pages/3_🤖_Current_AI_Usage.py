"""
Current AI Usage Page
"""
import streamlit as st
from utils.page_utils import init_page
from utils.charts import create_bar_chart, create_comparison_chart
from utils.data_loader import get_multiple_choice_counts, Q4_LABELS, Q6_LABELS
import pandas as pd

# Initialize page with filters
df = init_page()

st.title("🤖 Current AI Usage")
st.markdown("---")

# AI Usage Frequency
st.subheader("AI Usage Frequency")
usage_freq = df['Q3'].value_counts()
fig = create_bar_chart(usage_freq, title="How often do you use AI tools?", orientation='v', show_percentage=True)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Current Use Cases
st.subheader("Current AI Use Cases")
q4_counts = get_multiple_choice_counts(df, 'Q4_', Q4_LABELS)
if len(q4_counts) > 0:
    # Calculate percentages based on total number of respondents
    total_responses = len(df)
    
    # Create chart with percentages (using total_responses as denominator)
    fig = create_bar_chart(q4_counts, title="For which of the following do you typically use AI tools?", orientation='h', show_percentage=True, total_responses=total_responses)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for current AI use cases.")

st.markdown("---")

# Desired Features
st.subheader("Desired Features")
st.write("Which of the following would you most want your personal AI assistant to help you with?")
q6_counts = get_multiple_choice_counts(df, 'Q6_', Q6_LABELS)
if len(q6_counts) > 0:
    # Calculate percentages based on total number of respondents
    total_responses = len(df)
    
    # Create chart with percentages (using total_responses as denominator)
    fig = create_bar_chart(q6_counts, title="", orientation='h', show_percentage=True, total_responses=total_responses)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for desired features.")

st.markdown("---")

# Comparison: Current vs Desired
st.subheader("Current Usage vs Desired Features")
q4_counts = get_multiple_choice_counts(df, 'Q4_', Q4_LABELS)
q6_counts = get_multiple_choice_counts(df, 'Q6_', Q6_LABELS)

# Align the data for comparison
q4_dict = q4_counts.to_dict()
q6_dict = q6_counts.to_dict()

# Create comparison data for all features with both current and desired data
comparison_data = []
all_features = set(list(q4_dict.keys()) + list(q6_dict.keys()))
for feature in all_features:
    current = q4_dict.get(feature, 0)
    desired = q6_dict.get(feature, 0)
    gap = desired - current
    if gap > 0:  # Only include features where desired > current
        comparison_data.append({
            'Feature': feature,
            'Current Usage': current,
            'Desired': desired,
            'Gap': gap
        })

if comparison_data:
    comparison_df = pd.DataFrame(comparison_data).sort_values('Gap', ascending=False).head(10)
    
    if len(comparison_df) > 0:
        fig = create_comparison_chart(
            comparison_df.set_index('Feature')['Current Usage'],
            comparison_df.set_index('Feature')['Desired'],
            'Current Usage',
            'Desired Features',
            title="Current Usage vs Desired Features (Top 10 by Gap)"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No comparison data available.")
else:
    st.info("No comparison data available.")

