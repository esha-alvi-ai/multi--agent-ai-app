# ui/streamlit_app.py

import streamlit as st
import sys
import os
import traceback

# Adjust Python path so we can import main
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from main import run_pipeline
from logger.logger import setup_logger

logger = setup_logger()

st.set_page_config(page_title="Multi-Agent AI App", layout="wide")

st.title("🤖 Multi-Agent AI App")
st.write("An AI pipeline that runs Planner → Writer → Sanitizer → Summarizer and more using a task graph executor.")

# Sidebar options
st.sidebar.header("⚙️ Settings")
tone = st.sidebar.selectbox("Tone", ["professional", "casual", "funny", "neutral"])
length = st.sidebar.selectbox("Length", ["short", "medium", "long"])

# Main input
topic = st.text_area("📝 Enter your topic or idea", height=150)

if st.button("🚀 Run Multi-Agent Pipeline"):
    if not topic.strip():
        st.warning("Please enter a topic before running.")
    else:
        with st.spinner("Running the multi-agent pipeline..."):
            try:
                # Call main pipeline function
                output = run_pipeline(
                    topic=topic,
                    tone=tone,
                    length=length
                )

                # Show full pipeline output
                if isinstance(output, dict):
                    if "final_article" in output:
                        st.subheader("📜 Final Article")
                        st.write(output["final_article"])
                    if "summary" in output:
                        st.subheader("📌 Summary")
                        st.write(output["summary"])
                    if "plan" in output:
                        st.subheader("🧠 Planner Output")
                        st.write(output["plan"])
                else:
                    st.subheader("📜 Pipeline Output")
                    st.write(output)

            except Exception as e:
                logger.error(f"Error in Streamlit app: {e}")
                st.error(f"An error occurred: {e}")
                st.text(traceback.format_exc())
