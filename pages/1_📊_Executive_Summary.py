"""
Executive Summary Page
"""
import streamlit as st
from utils.page_utils import init_page
from utils.insights import get_top_motivators, get_top_barriers, generate_key_insights

# Initialize page with filters
df = init_page()

st.title("📊 Executive Summary")

# Survey Introduction
st.markdown("""
This survey explores attitudes toward AI-powered personal assistants that help manage daily life tasks. 
We gathered responses from **{:,} participants** across the Netherlands and the United Kingdom to understand 
current AI usage, comfort levels with proactive AI assistance, and key motivators and barriers to adoption.
""".format(len(df)))

st.markdown("---")

# Key Insights
st.subheader("💡 Key Insights")
insights = generate_key_insights(df)
for insight in insights:
    st.markdown(f"- {insight}")

st.markdown("---")

# Top Motivators and Barriers
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 3 Motivators")
    motivators = get_top_motivators(df)
    if motivators:
        for i, (motivator, count) in enumerate(motivators, 1):
            pct = (count / len(df) * 100) if len(df) > 0 else 0
            st.write(f"{i}. {motivator}: {count} ({pct:.1f}%)")
    else:
        st.info("No data available.")

with col2:
    st.subheader("Top 3 Barriers")
    barriers = get_top_barriers(df)
    if barriers:
        for i, (barrier, count) in enumerate(barriers, 1):
            pct = (count / len(df) * 100) if len(df) > 0 else 0
            st.write(f"{i}. {barrier}: {count} ({pct:.1f}%)")
    else:
        st.info("No data available.")

