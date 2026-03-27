import streamlit as st
import pandas as pd
import plotly.express as px

# Page settings
st.set_page_config(page_title="Mobile Usage Dashboard", page_icon="📱", layout="wide")

# Load data
df = pd.read_csv("mobile_usage_cleaned.csv")

# Title
st.title("📱 Mobile Usage Analysis Dashboard")
st.write("This dashboard shows insights from the cleaned mobile usage dataset.")

# Sidebar filters
st.sidebar.header("Filter Data")

gender_filter = st.sidebar.multiselect(
    "Select Gender",
    options=df["Gender"].dropna().unique(),
    default=df["Gender"].dropna().unique()
)

dept_filter = st.sidebar.multiselect(
    "Select Department",
    options=df["Department"].dropna().unique(),
    default=df["Department"].dropna().unique()
)

app_filter = st.sidebar.multiselect(
    "Select Most Used App",
    options=df["Most_Used_App"].dropna().unique(),
    default=df["Most_Used_App"].dropna().unique()
)

# Apply filters
filtered_df = df[
    (df["Gender"].isin(gender_filter)) &
    (df["Department"].isin(dept_filter)) &
    (df["Most_Used_App"].isin(app_filter))
]

# Metrics
st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Students", len(filtered_df))
col2.metric("Average Age", round(filtered_df["Age"].mean(), 2))
col3.metric("Avg Screen Time", round(filtered_df["Screen_Time_Hours"].mean(), 2))
col4.metric("Avg Sleep Hours", round(filtered_df["Sleep_Hours"].mean(), 2))

# Show data
st.subheader("🗂 Filtered Dataset")
st.dataframe(filtered_df, use_container_width=True)

# Charts
st.subheader("📈 Visualizations")

# 1. Gender Count
fig1 = px.histogram(
    filtered_df,
    x="Gender",
    title="Gender Distribution",
    text_auto=True
)
st.plotly_chart(fig1, use_container_width=True)

# 2. Department Count
fig2 = px.histogram(
    filtered_df,
    x="Department",
    title="Department-wise Student Count",
    text_auto=True
)
st.plotly_chart(fig2, use_container_width=True)

# 3. Most Used App
fig3 = px.histogram(
    filtered_df,
    x="Most_Used_App",
    title="Most Used App Distribution",
    text_auto=True
)
st.plotly_chart(fig3, use_container_width=True)

# 4. Screen Time vs Sleep Hours
fig4 = px.scatter(
    filtered_df,
    x="Screen_Time_Hours",
    y="Sleep_Hours",
    color="Gender",
    hover_data=["Department", "Most_Used_App"],
    title="Screen Time vs Sleep Hours"
)
st.plotly_chart(fig4, use_container_width=True)

# 5. Social Media Hours vs Battery Usage
fig5 = px.scatter(
    filtered_df,
    x="Social_Media_Hours",
    y="Battery_Usage_%",
    color="Most_Used_App",
    hover_data=["Gender", "Department"],
    title="Social Media Hours vs Battery Usage"
)
st.plotly_chart(fig5, use_container_width=True)

# 6. Average Screen Time by Department
avg_screen = filtered_df.groupby("Department", as_index=False)["Screen_Time_Hours"].mean()
fig6 = px.bar(
    avg_screen,
    x="Department",
    y="Screen_Time_Hours",
    title="Average Screen Time by Department",
    text_auto=True
)
st.plotly_chart(fig6, use_container_width=True)

# Download cleaned filtered data
st.subheader("⬇ Download Filtered Data")
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="filtered_mobile_usage_data.csv",
    mime="text/csv"
)