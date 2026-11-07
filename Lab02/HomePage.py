import streamlit as st

st.set_page_config(
    page_title="Sleep Schedule Tracker",
    page_icon="🌙",
    layout="wide"
)
st.sidebar.title("Navigation")

if st.sidebar.button("🏠 Home"):
    st.switch_page("HomePage.py")

if st.sidebar.button("📝 Survey"):
    st.switch_page("pages/Survey.py")

if st.sidebar.button("📊 Visuals"):
    st.switch_page("pages/Visuals.py")
st.title("🌙 Sleep Schedule Tracker")

st.subheader("Welcome!")

st.write("""
Welcome to the Sleep Schedule Tracker!

This website explores sleep habits and helps students
understand their sleeping patterns.

Using Python and Streamlit, we can collect sleep data,
analyze sleeping habits, and display interactive graphs.
""")

st.divider()

st.header("What Can You Do Here?")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Sleep Survey")
    st.write("""
    Record your sleep schedule by entering:

    - The day of the week
    - Your bedtime
    - Your wake-up time

    The website automatically calculates how many
    hours you slept and saves your response.
    """)

with col2:
    st.subheader("📊 Sleep Visualizations")
    st.write("""
    Explore four different graphs:

    1. Weekly Sleep Hours
    2. Interactive Daily Sleep Comparison
    3. Distribution of Survey Sleep Hours
    4. Interactive Sleep Survey Comparison
    """)

st.divider()

st.header("Why Track Sleep?")

st.write("""
Tracking your sleep schedule can help you identify
patterns in your daily routine.

This project compares sleep duration across different
days and allows users to explore their sleeping habits.
""")

st.info(
    "Use the sidebar on the left to visit the "
    "Survey and Visuals pages."
)

st.caption(
    "Georgia Tech CS 1301 - Web Development Lab 2"
)
