"""
Chart creation utilities for the AI Life Assistant Survey dashboard.
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Color schemes
LIKERT_COLORS = {
    1: '#d62728',  # Red - negative
    2: '#ff7f0e',  # Orange
    3: '#bcbd22',  # Yellow - neutral
    4: '#2ca02c',  # Light green
    5: '#1f77b4'   # Blue - positive
}


def create_bar_chart(data, x=None, y=None, title="", orientation='v', color=None, color_scale=None, show_percentage=False, yaxis_max=None, total_responses=None):
    """Create a bar chart.
    
    Args:
        total_responses: Total number of respondents for percentage calculation.
                        If None and show_percentage=True, uses sum of values (for single-choice questions).
                        If provided, uses this as denominator (for multiple-choice questions).
    """
    if isinstance(data, pd.Series):
        df = data.reset_index()
        df.columns = ['Category', 'Count']
        x_col = 'Category'
        y_col = 'Count'
        # Use total_responses if provided, otherwise use sum (for single-choice)
        total = total_responses if total_responses is not None else (data.sum() if show_percentage else None)
        # For horizontal charts, reverse order so highest value appears at top
        if orientation == 'h':
            df = df.iloc[::-1].reset_index(drop=True)
    else:
        df = data
        x_col = x or df.columns[0]
        y_col = y or df.columns[1]
        # Use total_responses if provided, otherwise use sum (for single-choice)
        total = total_responses if total_responses is not None else (df[y_col].sum() if show_percentage else None)
        # For horizontal charts, reverse order so highest value appears at top
        if orientation == 'h':
            df = df.iloc[::-1].reset_index(drop=True)
    
    # Create the base figure
    fig = px.bar(
        df,
        x=x_col if orientation == 'v' else y_col,
        y=y_col if orientation == 'v' else x_col,
        orientation=orientation,
        title=title,
        color=color,
        color_continuous_scale=color_scale
    )
    
    # Add percentage labels if requested
    if show_percentage and total:
        df['Percentage'] = (df[y_col] / total * 100).round(1)
        text_values = [f"{int(row[y_col])} ({row['Percentage']}%)" for _, row in df.iterrows()]
        fig.update_traces(text=text_values, textposition='outside')
    else:
        text_values = [str(int(val)) for val in df[y_col]]
        fig.update_traces(text=text_values, textposition='outside')
    
    # Set y-axis range if specified or if showing percentages (to accommodate labels)
    if orientation == 'v':
        if yaxis_max is not None:
            fig.update_layout(yaxis=dict(range=[0, yaxis_max]))
        elif show_percentage:
            # Auto-adjust y-axis to accommodate labels (add 25% padding for labels above bars)
            max_value = df[y_col].max()
            fig.update_layout(yaxis=dict(range=[0, max_value * 1.25]))
    else:
        if yaxis_max is not None:
            fig.update_layout(xaxis=dict(range=[0, yaxis_max]))
        elif show_percentage:
            max_value = df[y_col].max()
            fig.update_layout(xaxis=dict(range=[0, max_value * 1.25]))
    
    fig.update_layout(
        template='plotly_white',
        margin=dict(l=50, r=50, t=50, b=50),
        showlegend=False
    )
    
    return fig


def create_likert_chart(data, title="", labels=None):
    """Create a Likert scale visualization (diverging bar chart)."""
    if labels is None:
        labels = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}
    
    # Prepare data
    values = []
    labels_list = []
    colors_list = []
    
    for i in range(1, 6):
        count = data.get(i, 0)
        values.append(count)
        labels_list.append(labels.get(i, str(i)))
        colors_list.append(LIKERT_COLORS.get(i, '#7f7f7f'))
    
    # Create diverging bar chart
    fig = go.Figure()
    
    # Negative side (1-3)
    fig.add_trace(go.Bar(
        y=labels_list[:3],
        x=[-v for v in values[:3]],
        orientation='h',
        marker_color=colors_list[:3],
        text=[f'{v}' for v in values[:3]],
        textposition='outside',
        name='Negative'
    ))
    
    # Positive side (4-5)
    fig.add_trace(go.Bar(
        y=labels_list[3:],
        x=values[3:],
        orientation='h',
        marker_color=colors_list[3:],
        text=[f'{v}' for v in values[3:]],
        textposition='outside',
        name='Positive'
    ))
    
    fig.update_layout(
        title=title,
        template='plotly_white',
        showlegend=False,
        height=300,
        xaxis=dict(
            title="Number of Responses",
            range=[-max(values[:3]) * 1.2 if values[:3] else -10, max(values[3:]) * 1.2 if values[3:] else 10],
            nticks=6  # Limit to ~6 tick marks for cleaner display
        ),
        yaxis=dict(title="")
    )
    
    return fig


def create_pie_chart(data, title="", hole=0.4, show_labels=True, show_legend=True):
    """Create a pie or donut chart."""
    if isinstance(data, pd.Series):
        df = data.reset_index()
        df.columns = ['Category', 'Count']
    else:
        df = data
    
    fig = px.pie(
        df,
        values=df.columns[1],
        names=df.columns[0],
        title=title,
        hole=hole
    )
    
    fig.update_layout(
        template='plotly_white',
        showlegend=show_legend
    )
    
    if show_labels:
        fig.update_traces(textinfo='percent', textposition='outside')
    else:
        fig.update_traces(textinfo='none')
    
    return fig


def create_comparison_chart(data1, data2, labels1, labels2, title=""):
    """Create a grouped bar chart comparing two datasets."""
    # Prepare data
    categories = list(set(list(data1.index) + list(data2.index)))
    
    values1 = [data1.get(cat, 0) for cat in categories]
    values2 = [data2.get(cat, 0) for cat in categories]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name=labels1,
        x=categories,
        y=values1,
        marker_color='#1f77b4'
    ))
    
    fig.add_trace(go.Bar(
        name=labels2,
        x=categories,
        y=values2,
        marker_color='#ff7f0e'
    ))
    
    fig.update_layout(
        title=title,
        template='plotly_white',
        barmode='group',
        xaxis_tickangle=-45,
        height=500
    )
    
    return fig


def create_heatmap(data, title=""):
    """Create a heatmap chart."""
    fig = px.imshow(
        data,
        title=title,
        color_continuous_scale='Viridis',
        aspect='auto'
    )
    
    fig.update_layout(template='plotly_white')
    
    return fig

