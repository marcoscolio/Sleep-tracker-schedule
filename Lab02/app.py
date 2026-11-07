
import streamlit as st

st.set_page_config(
    page_title="Sleep Schedule Tracker",
    page_icon="🌙",
    layout="wide"
)

def home():
    st.title("🌙 Sleep Schedule Tracker")
    st.subheader("Welcome!")
    st.write(
        "This website explores sleep habits and helps "
        "students understand their sleeping patterns."
    )
    st.header("What Can You Do Here?")
    st.write("📝 **Survey:** Record your sleep schedule.")
    st.write("📊 **Visuals:** Explore four sleep graphs.")
    st.info("Use the sidebar to navigate between pages.")

pages = [
    st.Page(home, title="Home", icon="🏠", default=True),
    st.Page("pages/Survey.py", title="Survey", icon="📝"),
    st.Page("pages/Visuals.py", title="Visuals", icon="📊")
]

navigation = st.navigation(pages)
navigation.run()
