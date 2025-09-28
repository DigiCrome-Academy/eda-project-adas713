import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

df = pd.read_csv("students_performance.csv")  
df = df.rename(columns={'race/ethnicity':'ethnic_group', 'parental level of education':'parent_education', 'test preparation course':'test_prep', 'math score': 'math_score', 'reading score': 'reading_score', 'writing score': 'writing_score'})

# Step 3: App Layout
st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

st.title("📊 Student Performance Dashboard")
st.markdown("""
This interactive dashboard allows you to explore student scores across subjects and demographics.
Filter by gender and/or ethnic group to see detailed visualizations.
""")

# Sidebar Filters
selected_gender = st.sidebar.radio("Select Gender", options=df["gender"].unique(), index = 0)
selected_ethnic = st.sidebar.multiselect("Select Ethnic Group", options=df["ethnic_group"].unique(), default=df["ethnic_group"].unique())
selected_parent = st.sidebar.multiselect("Select Parent Education", options=df["parent_education"].unique(), default=df["parent_education"].unique())
selected_lunch = st.sidebar.radio("Select Lunch Status", options=df["lunch"].unique(), index = 0)
selected_testprep = st.sidebar.radio("Select Test Prep Status", options=df["test_prep"].unique(), index = 0)

filtered_df = df[
    (df["gender"] == selected_gender) &
    (df["ethnic_group"].isin(selected_ethnic)) &
    (df["parent_education"].isin(selected_parent)) &
    (df["lunch"] == selected_lunch) &
    (df["test_prep"] == selected_testprep)
]




#Overall metrics
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Average Math Score", f"{filtered_df['math_score'].mean():.2f}")
col2.metric("Average Reading Score", f"{filtered_df['reading_score'].mean():.2f}")
col3.metric("Average Writing Score", f"{filtered_df['writing_score'].mean():.2f}")


st.subheader("Univariate Analysis")
#histograms of individual subjects

st.markdown("#### Histograms")
fig, axes = plt.subplots(1, 3, figsize=(18,5))

sns.histplot(filtered_df["math_score"], ax=axes[0])
axes[0].set_title("Histogram of Math Scores")
axes[0].set_xlabel("Math Score")
axes[0].set_ylabel("Count")


sns.histplot(filtered_df["reading_score"], ax=axes[1])
axes[1].set_title("Histogram of Reading Scores")
axes[1].set_xlabel("Reading Score")
axes[1].set_ylabel("Count")


sns.histplot(filtered_df["writing_score"], ax=axes[2])
axes[2].set_title("Histogram of Writing Scores")
axes[2].set_xlabel("Writing Score")
axes[2].set_ylabel("Count")
st.pyplot(fig)

st.markdown("#### Bar Charts")

st.write("### Ethnic Group Counts")
st.bar_chart(filtered_df["ethnic_group"].value_counts())

st.write("### Parental Education Level Counts")
st.bar_chart(filtered_df["parent_education"].value_counts())





st.subheader("Bivariate Analysis")
st.markdown("#### Scatter Plots")

fig, axes = plt.subplots(1, 3, figsize=(18,5))
sns.scatterplot(x='math_score', y='reading_score', data=filtered_df, ax=axes[0])
axes[0].set_title("Math vs Reading Scores")
axes[0].set_xlabel("Math Score")
axes[0].set_ylabel("Reading Score")

sns.scatterplot(x='math_score', y='writing_score', data=filtered_df, ax=axes[1])
axes[1].set_title("Math vs Writing Scores")
axes[1].set_xlabel("Math Score")
axes[1].set_ylabel("Writing Score")

sns.scatterplot(x='reading_score', y='writing_score', data=filtered_df, ax=axes[2])
axes[2].set_title("Reading vs Writing Scores")
axes[2].set_xlabel("Reading Score")
axes[2].set_ylabel("Writing Score")
st.pyplot(fig)

st.markdown("#### Box Plots")
st.markdown("##### Ethnic Group")
fig, axes = plt.subplots(1, 3, figsize=(18,5))
sns.boxplot(x='ethnic_group', y='math_score', data=filtered_df, ax=axes[0])
axes[0].set_title("Math Scores by Ethnic Group")

sns.boxplot(x='ethnic_group', y='reading_score', data=filtered_df, ax=axes[1])
axes[1].set_title("Reading Scores by Ethnic Group")

sns.boxplot(x='ethnic_group', y='writing_score', data=filtered_df, ax=axes[2])
axes[2].set_title("Writing Scores by Ethnic Group")
st.pyplot(fig)

st.markdown("##### Parental Education Level")
fig, axes = plt.subplots(1, 3, figsize=(18,5))
sns.boxplot(x='parent_education', y='math_score', data=filtered_df, ax=axes[0])
axes[0].set_title("Math Scores by Parental Education Level")
axes[0].tick_params(axis='x', rotation=90)

sns.boxplot(x='parent_education', y='reading_score', data=filtered_df, ax=axes[1])
axes[1].set_title("Reading Scores by Parental Education Level")
axes[1].tick_params(axis='x', rotation=90)

sns.boxplot(x='parent_education', y='writing_score', data=filtered_df, ax=axes[2])
axes[2].set_title("Writing Scores by Parental Education Level")
axes[2].tick_params(axis='x', rotation=90)
st.pyplot(fig)


st.subheader("Multivariate Analysis")
st.markdown("#### Heatmap")
fig, ax = plt.subplots(figsize=(6,5))
sns.heatmap(filtered_df[["math_score", "reading_score", "writing_score"]].corr(), ax=ax)
st.pyplot(fig)

st.markdown("#### Grouped Bar Chart")
st.markdown("##### Average Scores by Ethnicity")
avg_scores = filtered_df.groupby("ethnic_group")[["math_score","reading_score","writing_score"]].mean().reset_index()
fig = px.bar(avg_scores, x="ethnic_group", y=["math_score","reading_score","writing_score"],
             barmode="group", labels={"value":"Average Score","ethnic_group":"Ethnicity"}, height=400)
st.plotly_chart(fig)

st.markdown("##### Average Scores by Parental Education")
avg_scores = filtered_df.groupby("parent_education")[["math_score","reading_score","writing_score"]].mean().reset_index()
fig = px.bar(avg_scores, x="parent_education", y=["math_score","reading_score","writing_score"],
             barmode="group", labels={"value":"Average Score","parent_education":"Parent Education"}, height=400)
st.plotly_chart(fig)

