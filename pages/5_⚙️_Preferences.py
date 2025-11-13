"""
Preferences Page
"""
import streamlit as st
from utils.page_utils import init_page
from utils.charts import create_pie_chart, create_bar_chart
import pandas as pd

# Initialize page with filters
df = init_page()

st.title("⚙️ Preferences")
st.markdown("---")

# Interaction Method Preference
st.subheader("Interaction Method Preference")
st.write("How would you prefer to interact with your AI assistant?")

if 'Q8' in df.columns:
    interaction_dist = df['Q8'].value_counts()
    if len(interaction_dist) > 0:
        fig = create_pie_chart(interaction_dist, title="", show_labels=True, show_legend=True)
        # Update to show only percentages on slices
        fig.update_traces(textinfo='percent', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Assistant Behavior Preference
st.subheader("Assistant Behavior Preference")
st.write("How would you prefer your AI assistant to behave?")

if 'Q12' in df.columns:
    behavior_dist = df['Q12'].value_counts()
    if len(behavior_dist) > 0:
        fig = create_bar_chart(behavior_dist, title="", orientation='v', show_percentage=True)
        # Adjust layout to prevent label cutoff
        fig.update_layout(
            margin=dict(l=220, r=50, t=50, b=50),
            xaxis=dict(tickangle=-20, automargin=True)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Behavior Statistics table
        st.write("**Behavior Statistics**")
        behavior_df = behavior_dist.reset_index()
        behavior_df.columns = ['Behavior', 'Count']
        behavior_df['Percentage'] = (behavior_df['Count'] / len(df) * 100).round(1)
        st.dataframe(behavior_df, use_container_width=True, hide_index=True, column_config={
            "Behavior": st.column_config.TextColumn("Behavior", width="medium"),
            "Count": st.column_config.NumberColumn("Count", width="small"),
            "Percentage": st.column_config.NumberColumn("Percentage", width="small", format="%.1f%%")
        })

st.markdown("---")

# Cross-tabulations
st.subheader("Interaction Method by Gender")
if 'Q8' in df.columns and 'Q2' in df.columns:
    cross_tab = pd.crosstab(df['Q8'], df['Q2'], margins=True)
    st.dataframe(cross_tab, use_container_width=True, hide_index=True)

st.markdown("---")

st.subheader("Behavior Preference by Age Group")
if 'Q12' in df.columns and 'Q1' in df.columns:
    cross_tab = pd.crosstab(df['Q12'], df['Q1'], margins=True)
    st.dataframe(cross_tab, use_container_width=True, hide_index=True)

st.markdown("---")

st.subheader("Behavior Preference by Gender")
if 'Q12' in df.columns and 'Q2' in df.columns:
    cross_tab = pd.crosstab(df['Q12'], df['Q2'], margins=True)
    st.dataframe(cross_tab, use_container_width=True, hide_index=True)

