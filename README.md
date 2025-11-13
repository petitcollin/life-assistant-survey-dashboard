# AI Life Assistant Survey Dashboard

An interactive dashboard for analyzing survey data on AI Life Assistants, built with Streamlit and Plotly.

## Features

- **Executive Summary**: Key insights and top motivators/barriers
- **Demographics**: Age and gender distributions
- **Current AI Usage**: Usage frequency, current use cases, and desired features
- **Comfort & Trust**: Comfort levels with proactive AI, data access, and public usage
- **Preferences**: Interaction methods and assistant behavior preferences
- **Motivations & Barriers**: What matters most and what prevents usage
- **Open-ended Questions Analysis**: Categorized text responses with sample quotes
- **Survey Questions**: Complete list of all survey questions

## Local Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the dashboard:**
   ```bash
   streamlit run app.py --server.port 8502
   ```

   Or use the provided script:
   ```bash
   ./run.sh
   ```

3. **Access the dashboard:**
   - Local: http://localhost:8502
   - Network: http://YOUR_IP:8502

## Deployment to Streamlit Community Cloud

### Option 1: Deploy from GitHub (Recommended)

1. **Create a GitHub repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: AI Life Assistant Survey Dashboard"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository and branch
   - Set the main file path to: `app.py`
   - Click "Deploy"

3. **Your app will be live at:**
   `https://YOUR_APP_NAME.streamlit.app`

### Option 2: Deploy from Local Files

1. **Install Streamlit CLI:**
   ```bash
   pip install streamlit
   ```

2. **Deploy directly:**
   ```bash
   streamlit deploy
   ```

   Follow the prompts to authenticate and deploy.

## Project Structure

```
life-assistant-survey-2/
├── app.py                          # Main Streamlit app entry point
├── pages/                          # Multi-page dashboard structure
│   ├── 1_📊_Executive_Summary.py
│   ├── 2_👥_Demographics.py
│   ├── 3_🤖_Current_AI_Usage.py
│   ├── 4_💚_Comfort_&_Trust.py
│   ├── 5_⚙️_Preferences.py
│   ├── 7_🚀_Motivations_&_Barriers.py
│   ├── 8_💡_Open-ended_Questions_Analysis.py
│   └── 9_📋_Survey_Questions.py
├── utils/                          # Utility modules
│   ├── data_loader.py              # Data loading and preprocessing
│   ├── charts.py                   # Chart creation functions
│   ├── insights.py                 # Insight extraction
│   ├── page_utils.py               # Page initialization utilities
│   ├── sidebar.py                  # Sidebar filter component
│   └── text_categorizer.py         # Text categorization for open-ended questions
├── data/                           # Survey data files
│   ├── Life Assistant survey 2.xlsx
│   └── ...
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Data Files

The dashboard expects data files in the `data/` directory:
- `Life Assistant survey 2.xlsx` (primary data source with English translations)
- Fallback to `ORD-95068-Z6P5Y2_2025-11-12_DD.xlsx` or CSV if Excel not available

## Requirements

- Python 3.9+
- See `requirements.txt` for all dependencies

## Notes

- The dashboard uses Streamlit's caching for performance
- Filters persist across all pages via session state
- Data is automatically preprocessed with value labels and translations
- The app opens directly to the Executive Summary page

