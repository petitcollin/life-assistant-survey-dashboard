"""
Comfort & Trust Page
"""
import streamlit as st
from utils.page_utils import init_page
from utils.charts import create_likert_chart
from utils.data_loader import get_likert_distribution, LIKERT_LABELS

# Initialize page with filters
df = init_page()

st.title("💚 Comfort & Trust")
st.markdown("---")

# Comfort with Proactive AI Assistant
st.subheader("Comfort with Proactive AI Assistant")
st.write("How comfortable would you feel using a personal AI assistant that proactively helps you manage your daily life?")

q5_dist = get_likert_distribution(df, 'Q5_1')
if len(q5_dist) > 0:
    q5_dict = q5_dist.to_dict()
    fig = create_likert_chart(q5_dict, title="", labels=LIKERT_LABELS)
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistics
    total = len(df)
    comfortable = len(df[df['Q5_1'].isin([4, 5])])
    neutral = len(df[df['Q5_1'] == 3])
    uncomfortable = len(df[df['Q5_1'].isin([1, 2])])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Comfortable (4-5):** {comfortable} ({comfortable/total*100:.1f}%)")
    with col2:
        st.markdown(f"**Neutral (3):** {neutral} ({neutral/total*100:.1f}%)")
    with col3:
        st.markdown(f"**Uncomfortable (1-2):** {uncomfortable} ({uncomfortable/total*100:.1f}%)")

st.markdown("---")

# Comfort with Calendar/Email Access
st.subheader("Comfort with Calendar/Email Access")
st.write("How comfortable would you be with an AI assistant accessing your calendar and email to help you?")

q7_dist = get_likert_distribution(df, 'Q7_1')
if len(q7_dist) > 0:
    q7_dict = q7_dist.to_dict()
    fig = create_likert_chart(q7_dict, title="", labels=LIKERT_LABELS)
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistics
    total = len(df)
    comfortable = len(df[df['Q7_1'].isin([4, 5])])
    neutral = len(df[df['Q7_1'] == 3])
    uncomfortable = len(df[df['Q7_1'].isin([1, 2])])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Comfortable (4-5):** {comfortable} ({comfortable/total*100:.1f}%)")
    with col2:
        st.markdown(f"**Neutral (3):** {neutral} ({neutral/total*100:.1f}%)")
    with col3:
        st.markdown(f"**Uncomfortable (1-2):** {uncomfortable} ({uncomfortable/total*100:.1f}%)")

st.markdown("---")

# Comfort Speaking to AI in Public
st.subheader("Comfort Speaking to AI in Public")
st.write("How comfortable would you be speaking to an AI assistant in public?")

q9_dist = get_likert_distribution(df, 'Q9_1')
if len(q9_dist) > 0:
    q9_dict = q9_dist.to_dict()
    fig = create_likert_chart(q9_dict, title="", labels=LIKERT_LABELS)
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistics
    total = len(df)
    comfortable = len(df[df['Q9_1'].isin([4, 5])])
    neutral = len(df[df['Q9_1'] == 3])
    uncomfortable = len(df[df['Q9_1'].isin([1, 2])])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Comfortable (4-5):** {comfortable} ({comfortable/total*100:.1f}%)")
    with col2:
        st.markdown(f"**Neutral (3):** {neutral} ({neutral/total*100:.1f}%)")
    with col3:
        st.markdown(f"**Uncomfortable (1-2):** {uncomfortable} ({uncomfortable/total*100:.1f}%)")

