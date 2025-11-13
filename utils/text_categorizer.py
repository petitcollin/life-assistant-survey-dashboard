"""
Text categorization utilities for survey responses.
"""
import re
from typing import List, Dict, Tuple

# Category definitions with keywords
Q13_CATEGORIES = {
    "Doesn't know / No response": ["don't know", "no idea", "nothing", "none", "n/a", "na", ""],
    "Doesn't want to use AI": ["don't want", "not interested", "no need", "don't need", "not want"],
    "Travel booking / Planning trips": ["travel", "trip", "booking", "flight", "hotel", "vacation", "holiday", "itinerary", "destination"],
    "Learning / Studying": ["learn", "study", "studying", "education", "course", "training", "skill", "language", "reading"],
    "Budgeting / Financial management": ["budget", "money", "expense", "financial", "finance", "spending", "saving", "bill", "payment", "accounting"],
    "Food / Meal planning": ["food", "meal", "recipe", "cooking", "grocery", "shopping food", "dinner", "lunch", "breakfast", "eating"],
    "Scheduling / Calendar / Time management": ["schedule", "calendar", "appointment", "meeting", "time management", "organize day", "planning day", "agenda"],
    "Shopping / Product comparison": ["shopping", "buy", "purchase", "product", "compare", "price", "online shopping"],
    "Health / Fitness / Wellness": ["health", "fitness", "exercise", "workout", "wellness", "doctor", "medical", "diet", "nutrition"],
    "Home projects / DIY": ["home", "diy", "project", "repair", "maintenance", "house", "cleaning", "organize home"],
    "Email / Communication": ["email", "message", "communication", "reply", "inbox", "mail"],
    "Research / Information gathering": ["research", "information", "find", "search", "look up", "gather"],
    "Social / Relationship": ["social", "relationship", "friend", "dating", "conversation"],
    "Work / Professional tasks": ["work", "job", "professional", "task", "project work", "report", "presentation"],
    "Entertainment / Content discovery": ["music", "movie", "book", "entertainment", "content", "discover"],
    "Other": []  # Catch-all for unmatched responses
}

Q14_CATEGORIES = {
    "Doesn't know / No response": ["don't know", "no idea", "nothing", "none", "n/a", "na", ""],
    "Time-consuming": ["time", "takes long", "long time", "time consuming", "too much time", "waste time"],
    "Repetitive / Boring": ["repetitive", "boring", "monotonous", "tedious", "same thing", "over and over"],
    "Complex / Difficult": ["complex", "difficult", "hard", "complicated", "confusing", "challenging"],
    "Overwhelming / Too many options": ["overwhelming", "too many", "options", "choices", "decisions"],
    "Lack of knowledge / Skills": ["don't know how", "lack knowledge", "no skill", "inexperience"],
    "Administrative burden": ["paperwork", "admin", "administrative", "forms", "documentation"],
    "Decision fatigue": ["decisions", "decide", "choice", "choose", "decision fatigue"],
    "Other": []
}

Q15_CATEGORIES = {
    "Doesn't know / No response": ["don't know", "no idea", "nothing", "none", "n/a", "na", ""],
    "Automate / Do it for me": ["automate", "automatic", "do it for me", "handle", "take care", "complete"],
    "Organize / Structure": ["organize", "structure", "arrange", "sort", "categorize"],
    "Remind / Notify": ["remind", "notification", "alert", "notify", "remember"],
    "Research / Find information": ["research", "find", "search", "look up", "gather", "information"],
    "Plan / Schedule": ["plan", "schedule", "arrange", "coordinate", "organize time"],
    "Compare / Analyze": ["compare", "analyze", "evaluate", "review", "assess"],
    "Simplify / Streamline": ["simplify", "streamline", "make easier", "reduce", "minimize"],
    "Learn / Teach": ["learn", "teach", "explain", "guide", "help understand"],
    "Other": []
}


def categorize_text(text: str, categories: Dict[str, List[str]]) -> str:
    """
    Categorize a text response based on keyword matching.
    
    Args:
        text: The text to categorize
        categories: Dictionary mapping category names to keyword lists
    
    Returns:
        The category name, or "Other" if no match found
    """
    import pandas as pd
    
    if not text or (isinstance(text, float) and pd.isna(text)) or str(text).lower().strip() in ['nan', 'none', '']:
        return "Doesn't know / No response"
    
    text_lower = str(text).lower()
    
    # Check each category (excluding "Other" and "Doesn't know")
    for category, keywords in categories.items():
        if category in ["Other", "Doesn't know / No response"]:
            continue
        for keyword in keywords:
            if keyword in text_lower:
                return category
    
    # Check for "Doesn't know" patterns
    if any(keyword in text_lower for keyword in categories.get("Doesn't know / No response", [])):
        return "Doesn't know / No response"
    
    # Default to "Other"
    return "Other"


def categorize_responses(df, column_prefix: str, categories: Dict[str, List[str]]) -> Dict[str, int]:
    """
    Categorize all responses in a column.
    
    Args:
        df: DataFrame containing the data
        column_prefix: Column prefix (e.g., 'Q13')
        categories: Dictionary mapping category names to keyword lists
    
    Returns:
        Dictionary mapping category names to counts
    """
    import pandas as pd
    
    # Try English column first
    english_column = f"{column_prefix}_english"
    if english_column in df.columns:
        column = english_column
    elif column_prefix in df.columns:
        column = column_prefix
    else:
        return {}
    
    # Get all responses
    responses = df[column].dropna().astype(str).tolist()
    
    # Categorize each response
    category_counts = {}
    for response in responses:
        category = categorize_text(response, categories)
        category_counts[category] = category_counts.get(category, 0) + 1
    
    return category_counts


def get_sample_responses_by_category(df, column_prefix: str, categories: Dict[str, List[str]], num_samples: int = 3) -> Dict[str, List[str]]:
    """
    Get sample responses for each category.
    
    Args:
        df: DataFrame containing the data
        column_prefix: Column prefix (e.g., 'Q13')
        categories: Dictionary mapping category names to keyword lists
        num_samples: Number of sample responses per category
    
    Returns:
        Dictionary mapping category names to lists of sample responses
    """
    import pandas as pd
    
    # Try English column first
    english_column = f"{column_prefix}_english"
    if english_column in df.columns:
        column = english_column
    elif column_prefix in df.columns:
        column = column_prefix
    else:
        return {}
    
    # Get all responses with their indices
    responses = df[column].dropna().astype(str)
    
    # Filter out invalid responses
    valid_responses = responses[responses.str.lower().str.strip().isin(['nan', 'none', '']) == False]
    
    # Categorize and group responses
    category_responses = {}
    for idx, response in valid_responses.items():
        category = categorize_text(response, categories)
        if category not in category_responses:
            category_responses[category] = []
        category_responses[category].append(str(response))
    
    # Limit to num_samples per category
    for category in category_responses:
        category_responses[category] = category_responses[category][:num_samples]
    
    return category_responses

