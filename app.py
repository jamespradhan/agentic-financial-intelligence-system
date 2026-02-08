import streamlit as st
import os
from agent import FinancialAgent

# Page Config
st.set_page_config(page_title="Fin-Agent", layout="centered")

st.title("🤖 Agentic Financial Analyst")
st.markdown("Upload a financial report (PDF) and ask complex reasoning questions.")

# Initialize Agent
agent = FinancialAgent()

# 1. File Upload Section
uploaded_file = st.file_uploader("Upload Annual Report", type=["pdf"])

# 2. Query Section
query = st.text_input("Ask a question:", placeholder="e.g., What is the Year-over-Year revenue growth?")

if uploaded_file and query and st.button("Analyze Report"):
    with st.spinner("Agent is reading and reasoning..."):
        # Save temp file for processing
        temp_path = "temp_report.pdf"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        try:
            # Run the Agent
            result = agent.analyze(temp_path, query)
            
            # 3. Display Results
            st.success("Analysis Complete")
            
            # Big Metric Display
            st.markdown(f"### 💡 Answer: {result.answer}")
            
            # Reasoning Dropdown (This shows the "Agentic" nature)
            with st.expander("Show Reasoning Trace (Chain-of-Thought)", expanded=True):
                for item in result.reasoning_path:
                    st.markdown(f"**Step {item.step_number}:** {item.logic}")
            
            # Metadata
            st.caption(f"Confidence: {result.confidence_score*100:.1f}% | Source Page: {result.source_page}")
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            # Cleanup
            if os.path.exists(temp_path):
                os.remove(temp_path)