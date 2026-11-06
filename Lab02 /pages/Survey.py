import streamlit as st
import pandas as pd
import csv
from pathlib import Path
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Sleep Survey",
    page_icon="📝",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = BASE_DIR / "data.csv"

st.title("📝 Sleep Schedule Survey")

st.write("""
Enter your sleep schedule below.

Your response will be saved and used to create
the graphs on the Visuals page.
""")

# ==========================================
# SURVEY FORM
# ==========================================

with st.form("sleep_survey"):

    day = st.selectbox(
        "What day are you recording?",
        [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]
    )

    bedtime = st.text_input(
        "What time did you go to bed? (HH:MM)",
        placeholder="23:30"
    )

    wake_time = st.text_input(
        "What time did you wake up? (HH:MM)",
        placeholder="07:30"
    )

    submitted = st.form_submit_button(
        "Submit Sleep Schedule"
    )

# ==========================================
# PROCESS THE RESPONSE
# ==========================================

if submitted:

    if bedtime.strip() == "" or wake_time.strip() == "":
        st.error("Please enter both times.")

    else:

        try:
            bed = datetime.strptime(
                bedtime.strip(), "%H:%M"
            )

            wake = datetime.strptime(
                wake_time.strip(), "%H:%M"
            )

            # Handle sleeping past midnight
            if wake <= bed:
                wake = wake + timedelta(days=1)

            difference = wake - bed

            hours_slept = round(
                difference.total_seconds() / 3600,
                2
            )

            # Save the response to CSV
            with open(
                CSV_FILE,
                "a",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    day,
                    bedtime.strip(),
                    wake_time.strip(),
                    hours_slept
                ])

            st.success("Sleep schedule saved!")

            st.write("Day:", day)
            st.write("Bedtime:", bedtime)
            st.write("Wake-up time:", wake_time)

            st.metric(
                "Total Hours Slept",
                f"{hours_slept:.2f} hours"
            )

        except ValueError:

            st.error(
                "Invalid time format. Use HH:MM "
                "in 24-hour time, such as 23:30."
            )

# ==========================================
# DISPLAY SAVED DATA
# ==========================================

st.divider()

st.header("📋 Recorded Sleep Schedules")

if CSV_FILE.exists():

    df = pd.read_csv(CSV_FILE)

    if len(df) > 0:

        st.dataframe(
            df,
            use_container_width=True
        )

        st.write(
            "Total responses:",
            len(df)
        )

        average_sleep = df["Hours"].mean()

        st.metric(
            "Average Sleep Duration",
            f"{average_sleep:.2f} hours"
        )

    else:
        st.info(
            "No responses yet. Submit your first schedule!"
        )

else:
    st.info("No survey data available.")
