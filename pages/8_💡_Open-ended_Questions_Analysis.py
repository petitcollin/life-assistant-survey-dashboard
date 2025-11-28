"""
Open-ended Questions Analysis Page
"""
import streamlit as st
from utils.page_utils import init_page
import pandas as pd
from utils.text_categorizer import (
    categorize_responses,
    get_sample_responses_by_category,
    Q13_CATEGORIES, 
    Q14_CATEGORIES, 
    Q15_CATEGORIES
)
from utils.charts import create_bar_chart

# Initialize page with filters
df = init_page()

st.title("💡 Open-ended Questions Analysis")
st.markdown("""
Analysis of free-text responses where participants described their needs and expectations 
for AI assistance in their daily lives.
""")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    "🎯 Tasks for AI Help", 
    "😤 Why Frustrating", 
    "🤖 How AI Should Help", 
    "📄 Raw Data"
])

with tab1:
    st.subheader("What tasks would you want an AI assistant to help with?")
    st.caption("Q13: What time-consuming or repetitive tasks in your daily life would you want a digital AI assistant to help you with?")
    
    q13_categories = categorize_responses(df, 'Q13', Q13_CATEGORIES)
    if q13_categories:
        # Sort by count descending
        q13_categories_sorted = dict(sorted(q13_categories.items(), key=lambda x: x[1], reverse=True))
        q13_cat_series = pd.Series(q13_categories_sorted)
        
        # Key insight
        top_category = list(q13_categories_sorted.keys())[0]
        top_count = list(q13_categories_sorted.values())[0]
        if top_category != "Nothing / Don't know":
            # Find top non-nothing category
            for cat, cnt in q13_categories_sorted.items():
                if cat not in ["Nothing / Don't know", "Other"]:
                    top_category = cat
                    top_count = cnt
                    break
        
        st.info(f"**Top task:** {top_category} — mentioned by {top_count} respondents ({top_count/len(df)*100:.1f}%)")
        
        # Bar chart
        fig = create_bar_chart(q13_cat_series, title="", orientation='h', show_percentage=True, total_responses=len(df))
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)
        
        # Sample responses (collapsed by default)
        with st.expander("📝 View sample responses by category"):
            q13_samples = get_sample_responses_by_category(df, 'Q13', Q13_CATEGORIES, num_samples=3)
            for category in q13_categories_sorted.keys():
                if category in q13_samples and len(q13_samples[category]) > 0:
                    st.markdown(f"**{category}** ({q13_categories_sorted[category]} responses)")
                    for response in q13_samples[category]:
                        st.markdown(f"- _{response}_")
                    st.markdown("")
    else:
        st.info("No data available for Q13.")

with tab2:
    st.subheader("Why are these tasks frustrating or time-consuming?")
    st.caption("Q14: Why do you find these tasks frustrating or time-consuming?")
    
    q14_categories = categorize_responses(df, 'Q14', Q14_CATEGORIES)
    if q14_categories:
        # Sort by count descending
        q14_categories_sorted = dict(sorted(q14_categories.items(), key=lambda x: x[1], reverse=True))
        q14_cat_series = pd.Series(q14_categories_sorted)
        
        # Key insight
        for cat, cnt in q14_categories_sorted.items():
            if cat not in ["Nothing / Don't know", "Other"]:
                st.info(f"**Top reason:** {cat} — mentioned by {cnt} respondents ({cnt/len(df)*100:.1f}%)")
                break
        
        # Bar chart
        fig = create_bar_chart(q14_cat_series, title="", orientation='h', show_percentage=True, total_responses=len(df))
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Sample responses
        with st.expander("📝 View sample responses by category"):
            q14_samples = get_sample_responses_by_category(df, 'Q14', Q14_CATEGORIES, num_samples=3)
            for category in q14_categories_sorted.keys():
                if category in q14_samples and len(q14_samples[category]) > 0:
                    st.markdown(f"**{category}** ({q14_categories_sorted[category]} responses)")
                    for response in q14_samples[category]:
                        st.markdown(f"- _{response}_")
                    st.markdown("")
    else:
        st.info("No data available for Q14.")

with tab3:
    st.subheader("How should an AI assistant help?")
    st.caption("Q15: How would you expect an AI assistant to help with these tasks?")
    
    q15_categories = categorize_responses(df, 'Q15', Q15_CATEGORIES)
    if q15_categories:
        # Sort by count descending
        q15_categories_sorted = dict(sorted(q15_categories.items(), key=lambda x: x[1], reverse=True))
        q15_cat_series = pd.Series(q15_categories_sorted)
        
        # Key insight
        for cat, cnt in q15_categories_sorted.items():
            if cat not in ["Nothing / Don't know", "Other"]:
                st.info(f"**Top expectation:** {cat} — mentioned by {cnt} respondents ({cnt/len(df)*100:.1f}%)")
                break
        
        # Bar chart
        fig = create_bar_chart(q15_cat_series, title="", orientation='h', show_percentage=True, total_responses=len(df))
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Sample responses
        with st.expander("📝 View sample responses by category"):
            q15_samples = get_sample_responses_by_category(df, 'Q15', Q15_CATEGORIES, num_samples=3)
            for category in q15_categories_sorted.keys():
                if category in q15_samples and len(q15_samples[category]) > 0:
                    st.markdown(f"**{category}** ({q15_categories_sorted[category]} responses)")
                    for response in q15_samples[category]:
                        st.markdown(f"- _{response}_")
                    st.markdown("")
    else:
        st.info("No data available for Q15.")

with tab4:
    st.subheader("Raw Responses")
    st.caption("All open-ended responses (Q13, Q14, Q15)")
    
    # Build dataframe with available columns
    raw_data_columns = []
    column_names = []
    
    for q, label in [
        ('Q13', 'Q13 - Tasks for AI Help'),
        ('Q14', 'Q14 - Why Frustrating'),
        ('Q15', 'Q15 - How AI Should Help')
    ]:
        english_col = f"{q}_english"
        if english_col in df.columns:
            raw_data_columns.append(df[english_col])
            column_names.append(label)
        elif q in df.columns:
            raw_data_columns.append(df[q])
            column_names.append(label)
    
    if raw_data_columns:
        raw_df = pd.concat(raw_data_columns, axis=1)
        raw_df.columns = column_names
        raw_df = raw_df.dropna(how='all')
        
        # Add search/filter
        search_term = st.text_input("🔍 Search responses", placeholder="Type to filter...")
        
        if search_term:
            mask = raw_df.apply(lambda row: row.astype(str).str.contains(search_term, case=False, na=False).any(), axis=1)
            filtered_df = raw_df[mask]
            st.write(f"**Found {len(filtered_df)} matching responses**")
            st.dataframe(filtered_df, use_container_width=True, height=400)
        else:
            st.write(f"**Total responses:** {len(raw_df)}")
            st.dataframe(raw_df, use_container_width=True, height=400)
    else:
        st.warning("No open-ended response columns found.")
