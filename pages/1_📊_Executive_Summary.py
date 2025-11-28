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

# Key Metrics Row
st.subheader("💡 Key Insights at a Glance")

total = len(df)

# Row 1: Adoption & Comfort
col1, col2, col3 = st.columns(3)

with col1:
    if 'Q5_1' in df.columns:
        comfortable = len(df[df['Q5_1'].isin([4, 5])])
        pct = comfortable / total * 100 if total > 0 else 0
        st.metric(
            label="Open to Proactive AI",
            value=f"{pct:.0f}%",
            help="Respondents rating 4-5 on comfort with proactive AI assistants"
        )

with col2:
    if 'Q7_1' in df.columns:
        uncomfortable = len(df[df['Q7_1'].isin([1, 2])])
        pct = uncomfortable / total * 100 if total > 0 else 0
        st.metric(
            label="Privacy Concerned",
            value=f"{pct:.0f}%",
            help="Uncomfortable with AI accessing calendar/email (rating 1-2)"
        )

with col3:
    if 'Q3' in df.columns:
        daily = len(df[df['Q3'] == 'Daily'])
        pct = daily / total * 100 if total > 0 else 0
        st.metric(
            label="Daily AI Users",
            value=f"{pct:.0f}%",
            help="Respondents who use AI tools daily"
        )

# Row 2: Preferences
col1, col2, col3 = st.columns(3)

with col1:
    if 'Q8' in df.columns:
        text_only = len(df[df['Q8'] == 'Text only'])
        pct = text_only / total * 100 if total > 0 else 0
        st.metric(
            label="Prefer Text Only",
            value=f"{pct:.0f}%",
            help="Prefer text over voice interaction"
        )

with col2:
    if 'Q12' in df.columns:
        with_me = len(df[df['Q12'] == 'Do it with me (helpful partner)'])
        pct = with_me / total * 100 if total > 0 else 0
        st.metric(
            label="Want Collaborative AI",
            value=f"{pct:.0f}%",
            help="Prefer 'do it with me' over full automation"
        )

with col3:
    if 'Q9_1' in df.columns:
        uncomfortable = len(df[df['Q9_1'].isin([1, 2])])
        pct = uncomfortable / total * 100 if total > 0 else 0
        st.metric(
            label="Uncomfortable in Public",
            value=f"{pct:.0f}%",
            help="Uncomfortable speaking to AI in public (rating 1-2)"
        )

st.markdown("---")

# Biggest Opportunity
st.subheader("📈 Biggest Opportunity")

from utils.data_loader import get_multiple_choice_counts, Q4_LABELS, Q6_LABELS

q4_counts = get_multiple_choice_counts(df, 'Q4_', Q4_LABELS)
q6_counts = get_multiple_choice_counts(df, 'Q6_', Q6_LABELS)

if len(q4_counts) > 0 and len(q6_counts) > 0:
    q4_dict = q4_counts.to_dict()
    q6_dict = q6_counts.to_dict()
    gaps = {}
    for feature in set(list(q4_dict.keys()) + list(q6_dict.keys())):
        current = q4_dict.get(feature, 0)
        desired = q6_dict.get(feature, 0)
        gap = desired - current
        if gap > 0:
            gaps[feature] = (gap, current, desired)
    
    if gaps:
        top_gap = max(gaps.items(), key=lambda x: x[1][0])
        feature_name = top_gap[0]
        gap, current, desired = top_gap[1]
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"**{feature_name}**")
            st.caption("Largest gap between desired and current usage")
        with col2:
            st.metric("Current", current)
        with col3:
            st.metric("Desired", desired, delta=f"+{gap}")

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
