"""
Executive Summary Page
"""
import streamlit as st
from utils.page_utils import init_page
from utils.insights import get_top_motivators, get_top_barriers

# Initialize page with filters
df = init_page()

st.title("📊 Executive Summary")

# Survey Introduction
st.markdown("""
This survey explores attitudes toward AI-powered personal assistants that help manage daily life tasks. 
We gathered responses from **{:,} participants** across the Netherlands and the United Kingdom.
""".format(len(df)))

st.markdown("---")

# Key Metrics
st.subheader("💡 Key Insights")

total = len(df)

# Row 1
col1, col2 = st.columns(2)

with col1:
    if 'Q5_1' in df.columns:
        comfortable = len(df[df['Q5_1'].isin([4, 5])])
        pct = comfortable / total * 100 if total > 0 else 0
        st.metric(label="Open to Proactive AI", value=f"{pct:.0f}%")
        st.caption("Would feel comfortable using an AI assistant that proactively helps manage their daily life")

with col2:
    if 'Q7_1' in df.columns:
        uncomfortable = len(df[df['Q7_1'].isin([1, 2])])
        pct = uncomfortable / total * 100 if total > 0 else 0
        st.metric(label="Privacy Concerned", value=f"{pct:.0f}%")
        st.caption("Are uncomfortable with an AI assistant connecting to their calendar and email")

st.markdown("")

# Row 2
col1, col2 = st.columns(2)

with col1:
    if 'Q3' in df.columns:
        daily = len(df[df['Q3'] == 'Daily'])
        pct = daily / total * 100 if total > 0 else 0
        st.metric(label="Daily AI Users", value=f"{pct:.0f}%")
        st.caption("Already use AI tools on a daily basis")

with col2:
    if 'Q9_1' in df.columns:
        uncomfortable = len(df[df['Q9_1'].isin([1, 2])])
        pct = uncomfortable / total * 100 if total > 0 else 0
        st.metric(label="Uncomfortable in Public", value=f"{pct:.0f}%")
        st.caption("Would feel uncomfortable speaking to an AI assistant in public")

st.markdown("")

# Row 3
col1, col2 = st.columns(2)

with col1:
    if 'Q8' in df.columns:
        text_only = len(df[df['Q8'] == 'Text only'])
        pct = text_only / total * 100 if total > 0 else 0
        st.metric(label="Prefer Text Only", value=f"{pct:.0f}%")
        st.caption("Prefer interacting with AI through text rather than voice")

with col2:
    if 'Q12' in df.columns:
        with_me = len(df[df['Q12'] == 'Do it with me (helpful partner)'])
        pct = with_me / total * 100 if total > 0 else 0
        st.metric(label="Want Collaborative AI", value=f"{pct:.0f}%")
        st.caption("Prefer AI to work with them as a partner rather than fully automating tasks")

st.markdown("---")

# Key Findings
st.subheader("🔍 Key Findings")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**🍽️ Biggest Pain Point**")
    st.info("**Meal planning and cooking** is the most mentioned task people want help with — deciding what to eat, finding recipes, and making grocery lists.")

with col2:
    st.markdown("**📈 Biggest Opportunity**")
    st.info("**Discovering new music, movies, books, or content** shows the largest gap between current usage and desired features — an untapped area for AI assistance.")

st.markdown("---")

# Top Motivators and Barriers
col1, col2 = st.columns(2)

with col1:
    st.subheader("✅ Top 3 Motivators")
    motivators = get_top_motivators(df)
    if motivators:
        for i, (motivator, count) in enumerate(motivators, 1):
            pct = (count / total * 100) if total > 0 else 0
            # Shorter labels
            short_label = motivator.replace("It ", "").replace("It's ", "")
            if len(short_label) > 40:
                short_label = short_label[:37] + "..."
            st.markdown(f"**{i}.** {short_label}")
            st.progress(pct / 100, text=f"{count} ({pct:.0f}%)")
    else:
        st.info("No data available.")

with col2:
    st.subheader("⚠️ Top 3 Barriers")
    barriers = get_top_barriers(df)
    if barriers:
        for i, (barrier, count) in enumerate(barriers, 1):
            pct = (count / total * 100) if total > 0 else 0
            # Shorter labels
            short_label = barrier.replace("I ", "").replace("It ", "")
            if len(short_label) > 40:
                short_label = short_label[:37] + "..."
            st.markdown(f"**{i}.** {short_label}")
            st.progress(pct / 100, text=f"{count} ({pct:.0f}%)")
    else:
        st.info("No data available.")
