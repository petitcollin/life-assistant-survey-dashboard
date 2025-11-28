"""
Text categorization utilities for survey responses.
Refined categories based on analysis of ~2000 responses.
"""
import re
from typing import List, Dict, Tuple

# Q13: What time-consuming or repetitive tasks would you want an AI assistant to help with?
Q13_CATEGORIES = {
    "Nothing / Don't know": ["nothing", "none", "n/a", "na", "dont know", "don't know", "no idea", "not sure", "can't think", "cant think", "not applicable", "no answer", "not really"],
    "Meal planning / Cooking / Recipes": ["meal", "cook", "recipe", "food", "dinner", "lunch", "breakfast", "grocery", "groceries", "shopping list", "menu", "eat", "what to have"],
    "Work / Professional tasks": ["work", "job", "office", "meeting", "project", "business", "professional", "report", "presentation", "colleague"],
    "Scheduling / Calendar / Planning": ["schedule", "calendar", "appointment", "planning my", "organiz", "organis", "diary", "agenda", "time management"],
    "Research / Information gathering": ["research", "compar", "information", "search for", "looking for", "finding", "look up", "gather info"],
    "Email / Messages / Communication": ["email", "e-mail", "inbox", "mail", "messages", "messaging", "reply", "respond"],
    "Finances / Budget / Expenses": ["finance", "financ", "money", "budget", "expense", "bank", "tax", "taxes", "bills", "payment", "saving", "accounting"],
    "Admin / Paperwork / Forms": ["admin", "paperwork", "document", "forms", "bureaucra", "filing", "insurance", "government"],
    "Shopping / Comparing products": ["shop", "buy", "purchase", "order", "online shop", "product", "price"],
    "Cleaning / Housework / Chores": ["clean", "housework", "household", "chores", "laundry", "tidy", "tidying", "vacuum", "washing"],
    "Travel / Trips / Booking": ["travel", "trip", "holiday", "vacation", "flight", "booking", "hotel", "destination"],
    "Health / Medical / Fitness": ["health", "medical", "doctor", "fitness", "exercise", "gym", "wellness", "diet"],
    "Learning / Studying": ["learn", "study", "education", "course", "training", "skill", "language"],
    "Other": []
}

# Q14: Why do you find these tasks frustrating or time-consuming?
Q14_CATEGORIES = {
    "Nothing / Don't know": ["nothing", "none", "n/a", "na", "dont know", "don't know", "no idea", "not sure", "not applicable"],
    "Time-consuming / Takes too long": ["time", "takes long", "long time", "time consuming", "too much time", "hours", "slow", "duration"],
    "Repetitive / Boring / Tedious": ["repetitive", "boring", "monotonous", "tedious", "same thing", "over and over", "dull", "routine", "mundane"],
    "Complex / Difficult": ["complex", "difficult", "hard", "complicated", "confusing", "challenging", "tricky"],
    "Overwhelming / Too much": ["overwhelming", "too many", "too much", "overload", "stress", "pressure"],
    "Lack of interest / Motivation": ["interest", "motivation", "enjoy", "like doing", "hate", "dislike", "not fun", "annoying"],
    "Requires effort / Energy": ["effort", "energy", "tiring", "exhausting", "draining", "mental", "concentration"],
    "Forgetting / Hard to track": ["forget", "remember", "memory", "keep track", "lose track", "oversight"],
    "Decision fatigue": ["decision", "decide", "choice", "choose", "options", "what to"],
    "Other": []
}

# Q15: How would you expect an AI assistant to help with these tasks?
Q15_CATEGORIES = {
    "Nothing / Don't know": ["nothing", "none", "n/a", "na", "dont know", "don't know", "no idea", "not sure"],
    "Provide suggestions / Recommendations": ["suggest", "suggestion", "option", "recommend", "idea", "proposal", "advice", "tip"],
    "Search / Research / Find information": ["search", "research", "find", "look up", "gather", "information", "answer"],
    "Save time / Make faster": ["save time", "faster", "quick", "speed", "efficient", "less time"],
    "Organize / Plan / Schedule": ["organize", "plan", "schedule", "arrange", "structure", "manage", "coordinate"],
    "Create / Generate content": ["create", "generate", "make", "produce", "write", "draft", "compose"],
    "Automate / Do it for me": ["automate", "automatic", "do it for me", "take over", "handle", "complete", "do the"],
    "Remind / Notify": ["remind", "notification", "alert", "notify", "remember", "prompt"],
    "Simplify / Make easier": ["easier", "simple", "simplify", "easy", "less effort", "streamline"],
    "Compare / Analyze": ["compare", "analyze", "evaluate", "review", "assess", "calculate"],
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
        return "Nothing / Don't know"
    
    text_lower = str(text).lower()
    
    # Check for "Nothing / Don't know" patterns first
    nothing_keywords = categories.get("Nothing / Don't know", [])
    if any(keyword in text_lower for keyword in nothing_keywords):
        return "Nothing / Don't know"
    
    # Check each category (excluding "Other" and "Nothing / Don't know")
    for category, keywords in categories.items():
        if category in ["Other", "Nothing / Don't know"]:
            continue
        for keyword in keywords:
            if keyword in text_lower:
                return category
    
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
    
    # Try English column first, then original column
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
    
    # Try English column first, then original column
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
    valid_responses = responses[~responses.str.lower().str.strip().isin(['nan', 'none', ''])]
    
    # Categorize and group responses
    category_responses = {}
    for idx, response in valid_responses.items():
        # Filter out very short responses
        if len(str(response).strip()) < 5:
            continue
        category = categorize_text(response, categories)
        if category not in category_responses:
            category_responses[category] = []
        # Only add if not too long and somewhat informative
        if len(response) < 300:
            category_responses[category].append(str(response))
    
    # Limit to num_samples per category
    for category in category_responses:
        category_responses[category] = category_responses[category][:num_samples]
    
    return category_responses
