import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(
    page_title="Sleep Visualizations",
    page_icon="📊",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent

st.title("📊 Sleep Schedule Visualizations")

st.write(
    "Explore sleep patterns using JSON and CSV data."
)

# ==========================================
# PART 1: JSON VISUALIZATIONS
# ==========================================

st.header("Part 1: Weekly Sleep Data")

with open(BASE_DIR / "data.json", "r") as file:
    data = json.load(file)

days = []
sleep_hours = []

for item in data["data_points"]:
    days.append(item["label"])
    sleep_hours.append(item["value"])

# ==========================================
# GRAPH 1: STATIC BAR CHART
# ==========================================

st.subheader("Graph 1: Weekly Sleep Hours")

fig1, ax1 = plt.subplots()

ax1.bar(
    days,
    sleep_hours,
    color="steelblue"
)

ax1.set_title("Hours Slept Each Day")
ax1.set_xlabel("Day of the Week")
ax1.set_ylabel("Hours of Sleep")
ax1.set_ylim(0, 12)

plt.setp(
    ax1.get_xticklabels(),
    rotation=30,
    ha="right"
)

fig1.tight_layout()

st.pyplot(fig1)
plt.close(fig1)

st.write(
    "This static graph shows the hours of sleep "
    "recorded for each day in the JSON dataset."
)

st.divider()

# ==========================================
# GRAPH 2: DYNAMIC LINE CHART
# ==========================================

st.subheader("Graph 2: Interactive Sleep Comparison")

if "selected_days" not in st.session_state:
    st.session_state.selected_days = days.copy()

selected_days = st.multiselect(
    "Select days to compare:",
    days,
    key="selected_days"
)

filtered_days = []
filtered_hours = []

for i in range(len(days)):
    if days[i] in selected_days:
        filtered_days.append(days[i])
        filtered_hours.append(sleep_hours[i])

if len(filtered_days) > 0:

    fig2, ax2 = plt.subplots()

    ax2.plot(
        filtered_days,
        filtered_hours,
        marker="o",
        color="purple",
        linewidth=2
    )

    ax2.axhline(
        y=8,
        color="red",
        linestyle="--",
        label="8-Hour Reference"
    )

    ax2.set_title("Selected Days: Sleep Comparison")
    ax2.set_xlabel("Day of the Week")
    ax2.set_ylabel("Hours of Sleep")
    ax2.set_ylim(0, 12)
    ax2.legend()

    fig2.tight_layout()

    st.pyplot(fig2)
    plt.close(fig2)

    selected_average = (
        sum(filtered_hours) / len(filtered_hours)
    )

    st.write(
        "Average for selected days:",
        round(selected_average, 2),
        "hours"
    )

else:
    st.warning("Please select at least one day.")

st.write(
    "This dynamic line chart changes when "
    "different days are selected."
)

st.divider()

# ==========================================
# PART 2: CSV VISUALIZATIONS
# ==========================================

st.header("Part 2: Sleep Survey Data")

CSV_FILE = BASE_DIR / "data.csv"

if CSV_FILE.exists() and CSV_FILE.stat().st_size > 0:

    df = pd.read_csv(CSV_FILE)

    required_columns = [
        "Day", "Bedtime", "WakeTime", "Hours"
    ]

    if all(col in df.columns for col in required_columns):

        df["Hours"] = pd.to_numeric(
            df["Hours"],
            errors="coerce"
        )

        df = df.dropna(
            subset=["Day", "Hours"]
        )

        df = df[
            (df["Hours"] >= 0) &
            (df["Hours"] <= 24)
        ]

        if len(df) > 0:

            # ==================================
            # GRAPH 3: STATIC HISTOGRAM
            # ==================================

            st.subheader(
                "Graph 3: Sleep Duration Distribution"
            )

            fig3, ax3 = plt.subplots()

            ax3.hist(
                df["Hours"],
                bins=range(0, 26),
                color="mediumseagreen",
                edgecolor="black"
            )

            ax3.set_title(
                "Distribution of Recorded Sleep Hours"
            )

            ax3.set_xlabel("Hours of Sleep")
            ax3.set_ylabel("Number of Responses")

            fig3.tight_layout()

            st.pyplot(fig3)
            plt.close(fig3)

            st.write(
                "This static histogram shows how "
                "sleep durations are distributed "
                "across all survey responses."
            )

            st.divider()

            # ==================================
            # GRAPH 4: DYNAMIC SCATTER PLOT
            # ==================================

            st.subheader(
                "Graph 4: Interactive Sleep Survey"
            )

            all_days = [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday"
            ]

            if "survey_day" not in st.session_state:
                st.session_state.survey_day = "All Days"

            selected_day = st.selectbox(
                "Choose a day to analyze:",
                ["All Days"] + all_days,
                key="survey_day"
            )

            if selected_day == "All Days":
                filtered_df = df.copy()

            else:
                filtered_df = df[
                    df["Day"] == selected_day
                ].copy()

            filtered_df = filtered_df.reset_index(
                drop=True
            )

            filtered_df["Response"] = (
                filtered_df.index + 1
            )

            if len(filtered_df) > 0:

                fig4, ax4 = plt.subplots()

                ax4.scatter(
                    filtered_df["Response"],
                    filtered_df["Hours"],
                    color="darkorange",
                    s=80
                )

                ax4.set_title(
                    "Survey Sleep Hours: " + selected_day
                )

                ax4.set_xlabel("Response Number")
                ax4.set_ylabel("Hours of Sleep")
                ax4.set_ylim(0, 24)

                fig4.tight_layout()

                st.pyplot(fig4)
                plt.close(fig4)

                st.write(
                    "Responses displayed:",
                    len(filtered_df)
                )

                # ==================================
                # EXTRA CREDIT: MEAN AND MEDIAN
                # ==================================

                st.subheader("Sleep Statistics")

                mean_sleep = filtered_df["Hours"].mean()
                median_sleep = filtered_df["Hours"].median()

                # Store previous values in session state
                if "previous_mean" not in st.session_state:
                    st.session_state.previous_mean = mean_sleep

                if "previous_median" not in st.session_state:
                    st.session_state.previous_median = median_sleep

                # Calculate changes from previous selection
                mean_change = (
                    mean_sleep - st.session_state.previous_mean
                )

                median_change = (
                    median_sleep - st.session_state.previous_median
                )

                # Display updated statistics
                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Mean Sleep Hours",
                        f"{mean_sleep:.2f}",
                        delta=f"{mean_change:+.2f}"
                    )

                with col2:
                    st.metric(
                        "Median Sleep Hours",
                        f"{median_sleep:.2f}",
                        delta=f"{median_change:+.2f}"
                    )

                # Save current values for next interaction
                st.session_state.previous_mean = mean_sleep
                st.session_state.previous_median = median_sleep

                st.caption(
                    "Changes are compared with the "
                    "previous visualization update."
                )

            else:
                st.info(
                    "No responses recorded for "
                    "this selected day."
                )

        else:
            st.info(
                "Submit survey responses to "
                "generate the CSV graphs."
            )

    else:
        st.error(
            "The CSV file is missing required columns."
        )

else:
    st.info(
        "No CSV data available. "
        "Visit the Survey page to add responses."
    )
