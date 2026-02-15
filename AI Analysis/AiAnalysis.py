import pandas as pd
import plotly.express as px
import streamlit as st
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

class LogicAgent:
    def __init__(self, df):
        self.df = df
        self.cols = df.columns
        self.num_cols = df.select_dtypes(include=['number']).columns.tolist()
        self.cat_cols = df.select_dtypes(include=['object']).columns.tolist()

    def answer_question(self, query):
        query = query.lower()
        
        # Rule 1: High-level summary
        if "summary" in query or "overview" in query:
            return f"This dataset has {len(self.df)} rows and {len(self.cols)} columns. Key metrics: {self.df.describe().to_string()}"
        
        # Rule 2: Detecting Trends (Time Series)
        if "trend" in query or "time" in query:
            date_col = self.df.select_dtypes(include=['datetime', 'object']).columns[0]
            fig = px.line(self.df, x=date_col, y=self.num_cols[0], title="Automated Trend Analysis")
            return fig
        
        # Rule 3: Comparisons
        if "compare" in query or "versus" in query:
            fig = px.bar(self.df, x=self.cat_cols[0], y=self.num_cols[0], title="Automated Comparison")
            return fig

        return "I understand the data, but please use keywords like 'summary', 'trend', or 'compare'."

# --- Desktop Interface ---
st.set_page_config(layout="wide")
st.title("🖥️ Pro Data Analyst Desktop (No-AI Edition)")

file = st.file_uploader(r"C:\Users\Admin\Data Analysis\BMW sales data (2010-2024).csv", type=['csv', 'xlsx'])

if file:
    df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
    agent = LogicAgent(df)
    
    tab1, tab2 = st.tabs(["Quick Q&A", "Full Desktop Analysis"])
    
    with tab1:
        query = st.text_input("Ask a question (e.g., 'Give me a summary' or 'Show trend')")
        if query:
            result = agent.answer_question(query)
            if isinstance(result, str): st.write(result)
            else: st.plotly_chart(result)

    with tab2:
        st.write("### Generating Professional Desktop Report...")
        pr = ProfileReport(df, explorative=True)
        st_profile_report(pr)