"""
Insight extraction utilities for the AI Life Assistant Survey dashboard.
"""
import pandas as pd
import numpy as np
from collections import Counter
import re
import streamlit as st


def get_top_motivators(df):
    """Get top 3 motivators from Q10."""
    from utils.data_loader import Q10_LABELS
    
    counts = {}
    for original_col, label in Q10_LABELS.items():
        if label in df.columns:
            counts[label] = int(df[label].sum())
    
    if not counts:
        return []
    
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_counts[:3]


def get_top_barriers(df):
    """Get top 3 barriers from Q11."""
    from utils.data_loader import Q11_LABELS
    
    counts = {}
    for original_col, label in Q11_LABELS.items():
        if label in df.columns:
            counts[label] = int(df[label].sum())
    
    if not counts:
        return []
    
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_counts[:3]


def generate_key_insights(df):
    """Generate a list of key insights from the data."""
    insights = []
    total = len(df)
    
    # 1. Adoption Readiness - Comfort with Proactive AI
    if 'Q5_1' in df.columns:
        comfortable = len(df[df['Q5_1'].isin([4, 5])])
        uncomfortable = len(df[df['Q5_1'].isin([1, 2])])
        comfortable_pct = (comfortable / total * 100) if total > 0 else 0
        uncomfortable_pct = (uncomfortable / total * 100) if total > 0 else 0
        insights.append(f"🎯 Adoption Readiness: {comfortable_pct:.1f}% are open to proactive AI assistants, while {uncomfortable_pct:.1f}% are resistant - showing a significant divide in readiness")
    
    # 2. Privacy Concerns - Calendar/Email Access
    if 'Q7_1' in df.columns:
        uncomfortable = len(df[df['Q7_1'].isin([1, 2])])
        uncomfortable_pct = (uncomfortable / total * 100) if total > 0 else 0
        insights.append(f"🔒 Privacy Concerns: {uncomfortable_pct:.1f}% are uncomfortable with AI accessing their calendar and email, highlighting data privacy as a critical barrier")
    
    # 3. Public Usage Comfort
    if 'Q9_1' in df.columns:
        uncomfortable = len(df[df['Q9_1'].isin([1, 2])])
        uncomfortable_pct = (uncomfortable / total * 100) if total > 0 else 0
        insights.append(f"📢 Social Acceptance: {uncomfortable_pct:.1f}% feel uncomfortable speaking to AI assistants in public, indicating social acceptance challenges")
    
    # 4. Interaction Preference
    if 'Q8' in df.columns:
        text_only = len(df[df['Q8'] == 'Text only'])
        text_pct = (text_only / total * 100) if total > 0 else 0
        insights.append(f"💬 Interaction Preference: {text_pct:.1f}% prefer text-only interaction, suggesting users value privacy and discretion over voice convenience")
    
    # 5. Control Preference
    if 'Q12' in df.columns:
        with_me = len(df[df['Q12'] == 'Do it with me (helpful partner)'])
        for_me = len(df[df['Q12'] == 'Do it for me (automatic)'])
        with_me_pct = (with_me / total * 100) if total > 0 else 0
        for_me_pct = (for_me / total * 100) if total > 0 else 0
        insights.append(f"⚖️ Control Preference: {with_me_pct:.1f}% want a collaborative 'do it with me' approach vs {for_me_pct:.1f}% preferring full automation, showing users value control")
    
    # 6. AI Usage Frequency
    if 'Q3' in df.columns:
        no_usage = len(df[df['Q3'] == "I don't use AI tools"])
        daily = len(df[df['Q3'] == 'Daily'])
        no_usage_pct = (no_usage / total * 100) if total > 0 else 0
        daily_pct = (daily / total * 100) if total > 0 else 0
        insights.append(f"📊 Usage Patterns: {no_usage_pct:.1f}% don't use AI tools at all, while {daily_pct:.1f}% use them daily - indicating significant growth potential among non-users")
    
    # 7. Feature Gap Analysis - Compare Q4 vs Q6
    from utils.data_loader import get_multiple_choice_counts, Q4_LABELS, Q6_LABELS
    q4_counts = get_multiple_choice_counts(df, 'Q4_', Q4_LABELS)
    q6_counts = get_multiple_choice_counts(df, 'Q6_', Q6_LABELS)
    
    if len(q4_counts) > 0 and len(q6_counts) > 0:
        # Find the feature with the largest gap (desired - current)
        q4_dict = q4_counts.to_dict()
        q6_dict = q6_counts.to_dict()
        gaps = {}
        for feature in set(list(q4_dict.keys()) + list(q6_dict.keys())):
            current = q4_dict.get(feature, 0)
            desired = q6_dict.get(feature, 0)
            gap = desired - current
            if gap > 0:
                gaps[feature] = gap
        
        if gaps:
            top_gap_feature = max(gaps.items(), key=lambda x: x[1])
            gap_pct = (top_gap_feature[1] / total * 100) if total > 0 else 0
            # Truncate long feature names
            feature_name = top_gap_feature[0][:50] + "..." if len(top_gap_feature[0]) > 50 else top_gap_feature[0]
            insights.append(f"📈 Feature Opportunity: '{feature_name}' shows the largest gap between desired ({q6_dict.get(top_gap_feature[0], 0)}) and current usage ({q4_dict.get(top_gap_feature[0], 0)}), representing {gap_pct:.1f}% untapped demand")
    
    # 8. Demographics - Age Distribution
    if 'Q1' in df.columns:
        age_55_plus = len(df[df['Q1'] == '55+'])
        age_18_34 = len(df[df['Q1'].isin(['18-24', '25-34'])])
        age_55_pct = (age_55_plus / total * 100) if total > 0 else 0
        age_18_34_pct = (age_18_34 / total * 100) if total > 0 else 0
        insights.append(f"👥 Demographics: {age_55_pct:.1f}% of respondents are 55+, while {age_18_34_pct:.1f}% are under 35, which may influence AI adoption patterns and preferences")
    
    return insights

