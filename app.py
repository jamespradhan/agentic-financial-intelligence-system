import streamlit as st
import os
from agent import FinancialAgent

st.set_page_config(page_title="Fin-Agent", layout="wide")

st.title("⚡ Agentic Financial Analyst")
st.markdown("### Enterprise-Grade Document Reasoning System")

# --- SESSION STATE INITIALIZATION ---
# This ensures the agent and file persist across button clicks
if "agent" not in st.session_state:
    st.session_state.agent = FinancialAgent()

if "cached_file" not in st.session_state:
    st.session_state.cached_file = None

if "cached_file_name" not in st.session_state:
    st.session_state.cached_file_name = None

# --- SIDEBAR: FILE UPLOAD ---
with st.sidebar:
    st.header("1. Document Upload")
    uploaded_file = st.file_uploader("Upload Annual Report (PDF)", type=["pdf"])

    if uploaded_file:
        # Only process if it's a NEW file
        if st.session_state.cached_file_name != uploaded_file.name:
            with st.spinner("Uploading and Processing PDF (One-time)..."):
                # Save temp file
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Upload to Gemini and CACHE the result
                try:
                    st.session_state.cached_file = st.session_state.agent.upload_file(temp_path)
                    st.session_state.cached_file_name = uploaded_file.name
                    st.success("File Processed & Cached!")
                except Exception as e:
                    st.error(f"Error: {e}")
                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
        else:
            st.success("Using Cached File ✅")

# --- MAIN AREA: ANALYSIS ---
st.header("2. Financial Analysis")

if st.session_state.cached_file:
    query = st.text_input("Ask a question about the report:", 
                         placeholder="e.g., What is the Year-over-Year revenue growth and where is it mentioned?")
    
    if query and st.button("Analyze Report"):
        with st.spinner("Agent is thinking..."):
            try:
                # Pass the CACHED file object to the agent
                result = st.session_state.agent.analyze(st.session_state.cached_file, query)
                
                # Display Answer
                st.markdown("### 💡 Answer")
                st.info(result.answer)
                
                # Display Reasoning (Chain-of-Thought)
                with st.expander("Show Reasoning Trace (Chain-of-Thought)", expanded=False):
                    for item in result.reasoning_path:
                        st.markdown(f"**Step {item.step_number}:** {item.logic}")
                
                # Display Sources
                if result.source_pages:
                    st.caption(f"📚 **Sources found on pages:** {', '.join(map(str, result.source_pages))}")
                st.caption(f"🎯 **Confidence Score:** {result.confidence_score * 100:.1f}%")
                
            except Exception as e:
                st.error(f"Analysis Failed: {e}")
else:
    st.info("Please upload a PDF document in the sidebar to begin.")