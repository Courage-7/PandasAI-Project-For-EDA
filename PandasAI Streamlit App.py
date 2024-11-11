# Install necessary packages
!pip install pandasai streamlit markdown2 plotly

# Install necessary packages
!pip install pandasai streamlit markdown2 plotly

# Import necessary libraries
import streamlit as st
import pandas as pd
import markdown2
import plotly.express as px
import os

# Import PandasAI and initialize agents
from pandasai import SmartDataframe
from pandasai.ee.agents.semantic_agent import SemanticAgent, JudgeAgent

# Initialize Streamlit app
st.title("Enhanced PandasAI Streamlit App")
st.write("Chat with your dataset using AI, and generate insights and visualizations with ease.")

# API Key input
st.sidebar.subheader("API Key Configuration")
api_key = st.sidebar.text_input("Enter your PandasAI API key", type="password", help="Your API key is required to connect to PandasAI.")
if api_key:
    os.environ['PANDASAI_API_KEY'] = api_key
else:
    st.warning("Please enter your API key to proceed.")

# Initialize agents (only if API key is provided)
if api_key:
    semantic_agent = SemanticAgent()
    judge_agent = JudgeAgent()
    
    # File upload section
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv", help="Upload a dataset in CSV format.")
    if uploaded_file is not None:
        # Load the dataset
        df = pd.read_csv(uploaded_file)
        sdf = SmartDataframe(df)
        sdf.set_agent(semantic_agent)

        # Query input and response
        st.subheader("Ask Questions About Your Dataset")
        query = st.text_input("Enter your question here", help="Ask natural language questions like 'Show top events by fatalities.'")
        
        # Display the answer, code, and insights
        if query:
            answer, code, insights = sdf.chat(query, return_full=True)  # Assume `return_full` provides answer, code, and insights
            
            st.write("**Answer:**", answer)
            st.write("**Insight Explanation:**", insights if insights else "No additional insights.")

            # Display code upon request
            if st.checkbox("Show Generated Code"):
                st.code(code)
            
            # Generate visualizations based on the query
            if "fatalities" in query.lower():
                fig = px.histogram(df, x="event_type", y="fatalities", title="Fatalities by Event Type")
                st.plotly_chart(fig)
            
            # Auto-save query results to report
            report_content = f"### Query: {query}\n\nAnswer:\n{answer}\n\nInsights:\n{insights}\n\n"
            save_report(report_content)
            st.write("Auto-saved report with the latest query.")

    # Report download option
    if st.button("Download Report"):
        with open("report.md", "r") as file:
            st.download_button("Download Report as Markdown", file, file_name="report.md")

    # Dataset switching feature
    if st.button("Switch Dataset"):
        st.write("Upload a new dataset to begin a fresh session. Previous responses are saved in the report.")

# Function for report auto-save
def save_report(report_content):
    with open("report.md", "w") as file:
        file.write(markdown2.markdown(report_content))
