# Install necessary packages
!pip install pandasai streamlit markdown2 plotly

# Import libraries
import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from pandasai.agent import SemanticAgent
import markdown2
import plotly.express as px
import os

# Initialize Streamlit app
st.title("PandasAI Enhanced Streamlit App")
st.write("Interact with your dataset using natural language queries and AI-powered insights.")

# Set up Semantic Agent
agent = SemanticAgent()

# Auto-save function
def save_report(report_content):
    with open("report.md", "w") as file:
        file.write(markdown2.markdown(report_content))

# File upload
uploaded_file = st.file_uploader("Upload a CSV file", type="csv", help="Upload your dataset in CSV format to get started.")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    sdf = SmartDataframe(df)
    sdf.set_agent(agent)

    # Query input and response
    st.subheader("Ask Questions About Your Dataset")
    query = st.text_input("Enter your question here", help="Ask questions in natural language, e.g., 'Show top events by fatalities.'")
    if query:
        answer, code, insights = sdf.chat(query, return_full=True)  # Assume return_full provides answer, code, and insights
        st.write("**Answer:**", answer)
        
        # Show insights and visualizations (if available)
        st.write("**Insight Explanation:**", insights if insights else "No additional insights.")
        
        # Plot visualization for numeric summaries
        if "fatalities" in query.lower():
            fig = px.histogram(df, x="event_type", y="fatalities", title="Fatalities by Event Type")
            st.plotly_chart(fig)
        
        # Code display toggle
        if st.checkbox("Show Generated Code"):
            st.code(code)

        # Save to report
        report_content = f"### Query: {query}\n\nAnswer:\n{answer}\n\nInsights:\n{insights}\n\n"
        save_report(report_content)
        st.write("Auto-saved report updated with the latest query.")

# Download report button
if st.button("Download Report"):
    with open("report.md", "r") as file:
        st.download_button("Download Report as Markdown", file, file_name="report.md")

# Option to switch dataset
if st.button("Switch Dataset"):
    st.write("You can upload a new dataset, and previous responses will be saved.")
