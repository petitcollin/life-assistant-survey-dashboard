"""
Survey Questions Page
"""
import streamlit as st
from utils.page_utils import init_page

# Initialize page with filters
df = init_page()

st.title("📋 Survey Questions")
st.markdown("---")

st.write("This page lists all the questions from the AI Life Assistant Survey.")

st.markdown("---")

st.subheader("Q1. How old are you?")
st.write("**Type:** Single choice")
st.write("- 18–24")
st.write("- 25–34")
st.write("- 35–44")
st.write("- 45–54")
st.write("- 55+")

st.markdown("---")

st.subheader("Q2. How do you identify?")
st.write("**Type:** Single choice")
st.write("- Male")
st.write("- Female")
st.write("- Non-binary")

st.markdown("---")

st.subheader("Q3. How often do you use AI tools such as ChatGPT, Gemini, or others?")
st.write("**Type:** Single choice")
st.write("- Daily")
st.write("- Occasionally")
st.write("- I've only tried it once or twice")
st.write("- I don't use AI tools")

st.markdown("---")

st.subheader("Q4. For which of the following do you typically use AI tools?")
st.write("**Type:** Multiple choice (Select all that apply)")
st.write("- Planning or organizing my day, tasks, or schedule")
st.write("- Brainstorming ideas or creative content")
st.write("- Learning or studying something new")
st.write("- Online shopping or comparing products")
st.write("- Managing money or tracking expenses")
st.write("- Getting health, fitness, or wellness advice")
st.write("- Finding recipes and meal planning")
st.write("- Planning trips or activities")
st.write("- Searching for information, answering questions")
st.write("- Social or relationship advice")
st.write("- Getting motivation or mental health support")
st.write("- Practicing conversations or preparing for interviews")
st.write("- Helping with home projects or DIY tasks")
st.write("- Discovering new music, movies, books, or content")
st.write("- Other: please specify")

st.markdown("---")

st.subheader("Q5. How comfortable would you feel using a personal AI assistant that proactively helps you manage your daily life?")
st.write("**Type:** 5-point Likert scale")
st.write("1 = Not open at all → 5 = Very open")

st.markdown("---")

st.subheader("Q6. Which of the following would you most want your personal AI assistant to help you with?")
st.write("**Type:** Multiple choice (Select all that apply)")
st.write("- Planning or organizing my day, tasks, or schedule")
st.write("- Brainstorming ideas or creative content")
st.write("- Learning or studying something new")
st.write("- Online shopping or comparing products")
st.write("- Managing money or tracking expenses")
st.write("- Getting health, fitness, or wellness advice")
st.write("- Finding recipes and meal planning")
st.write("- Planning trips or activities")
st.write("- Searching for information, answering questions")
st.write("- Social or relationship advice")
st.write("- Getting motivation or mental health support")
st.write("- Practicing conversations or preparing for interviews")
st.write("- Helping with home projects or DIY tasks")
st.write("- Discovering new music, movies, books, or content")
st.write("- Other: please specify")

st.markdown("---")

st.subheader("Q7. How comfortable would you be with an AI assistant accessing your calendar and email to help you?")
st.write("**Type:** 5-point Likert scale")
st.write("1 = Not comfortable at all → 5 = Very comfortable")

st.markdown("---")

st.subheader("Q8. How would you prefer to interact with your AI assistant?")
st.write("**Type:** Single choice")
st.write("- Text only")
st.write("- Voice only")
st.write("- Both (text and voice)")

st.markdown("---")

st.subheader("Q9. How comfortable would you be speaking to an AI assistant in public?")
st.write("**Type:** 5-point Likert scale")
st.write("1 = Not comfortable at all → 5 = Very comfortable")

st.markdown("---")

st.subheader("Q10. What matters to you most when thinking about using an AI assistant?")
st.write("**Type:** Multiple choice (Select all that apply)")
st.write("- It saves me time or makes my life easier")
st.write("- It helps me make better decisions")
st.write("- It helps me save money")
st.write("- It respects my privacy and data")
st.write("- It consistently delivers high-quality, accurate results")
st.write("- It's free or affordable")
st.write("- It feels natural and human-like to interact with")
st.write("- It has a trusted brand or reputation")
st.write("- It learns and improves based on my habits")
st.write("- It integrates well with the apps and tools I already use")

st.markdown("---")

st.subheader("Q11. What would make you NOT want to use a personal AI assistant?")
st.write("**Type:** Multiple choice (Select all that apply)")
st.write("- I don't trust how my data would be used")
st.write("- It feels too robotic or impersonal")
st.write("- It makes mistakes or gives unreliable answers")
st.write("- It takes too much effort to set up or use")
st.write("- It doesn't integrate well with the tools I already use")
st.write("- It's too expensive")
st.write("- I worry it could replace human interaction")
st.write("- I don't see a clear benefit compared to what I already use")
st.write("- I prefer to stay in control and do things myself")

st.markdown("---")

st.subheader("Q12. How would you prefer your AI assistant to behave?")
st.write("**Type:** Single choice")
st.write("- Do it with me (helpful partner)")
st.write("- Do it for me (automatic)")
st.write("- It depends on the task")

st.markdown("---")

st.subheader("Q13. Before we wrap up — what time-consuming or repetitive tasks in your day would you want a digital AI assistant to help with?")
st.write("**Type:** Open text")

st.markdown("---")

st.subheader("Q14. Why do you find these tasks frustrating or time-consuming?")
st.write("**Type:** Open text")

st.markdown("---")

st.subheader("Q15. How would you expect an AI assistant to help with these tasks?")
st.write("**Type:** Open text")

