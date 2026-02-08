# Agentic Financial Intelligence System 🤖📊

Document Reasoning Agent powered by Large Language Models (LLMs).

## 🚀 Executive Summary

This project is an Agentic System designed to perform zero-shot reasoning on complex financial reports (Balance Sheets, P&L, Risk Disclosures). Unlike traditional RAG pipelines that simply retrieve text, this agent utilizes Chain-of-Thought (CoT) prompting to "read," "reason," and "synthesize" answers from disjointed sections of a PDF.

### Key Engineering Highlights:

Latency Optimization: Implements state-aware caching to reduce follow-up query time by 90%.

Reasoning Engine: Uses structured "Reasoning Traces" to explain how an answer was derived, ensuring auditability.

Type Safety: Enforces strict JSON schemas with Pydantic to ensure reliable downstream API integration.

## 🏗️ System Architecture

The system decouples the Heavy Lifting (File I/O) from the Intelligence (Inference) layer to ensure a snappy user experience.

1. Ingestion Layer: Asynchronously uploads and processes large PDFs, polling for `ACTIVE` status to prevent timeouts.

2. Caching Layer: Stores the processed file handle in `st.session_state`, mimicking a persistent WebSocket connection.

3. Reasoning Engine: A custom `FinancialAgent` class that orchestrates the Gemini 2.5 Flash model to perform multi-step deduction.

4. Presentation Layer: A Streamlit dashboard that visualizes the "Thought Process" and validates Source Citations.

## ✨ Key Features

### 1. 🧠 Agentic "Chain-of-Thought" Reasoning

Instead of a black-box answer, the agent breaks down its logic.
- Search: Scans the entire document for relevant tables and figures.

- Synthesize: Merges information found across multiple pages into a coherent summary.

- Reason: Executes logical deductions or calculations explicitly within the reasoning path.

### 2. ⚡ Latency-Optimized "Stateful" Caching

- Problem: Re-uploading large documents for every interaction is slow and inefficient.

- Solution: The app uploads the file once. The file handle is cached in the session.

- Impact: Follow-up questions take <2 seconds (vs. 10+ seconds for re-upload).

### 3. 🔍 Multi-Page Source Citation
Financial data is often fragmented. The agent tracks and cites every page used to construct its final response, allowing for quick verification.

## ⚡ Installation & Usage

### Prerequisites

- Python 3.12+
- A Google Gemini API Key
- `uv` package manager (recommended)

### 1. Clone & Setup

```
git clone [https://github.com/yourusername/agentic-financial-intelligence-system.git](https://github.com/yourusername/agentic-financial-intelligence-system.git)
cd agentic-financial-intelligence-system

# Install dependencies using uv
uv sync
```

### 2. Configure Environment

Create a `.env` file in the root directory and add your API key:
```
GEMINI_API_KEY="your_actual_api_key_here"
```

### 3. Run the Agent
```
uv run streamlit run app.py
```

## 📖 User Guide: How to Run the Demo

Once the application is running, follow this workflow to demonstrate the system's capabilities:

- Upload & Cache: Open the sidebar and upload a complex PDF (e.g., an Annual Report). The system will process it once and cache it.

- Ask Reasoning Questions: Enter questions like "What is the Year-over-Year revenue growth?" or "Summarize the primary risk factors mentioned."

- Audit the Agent: Expand the "Show Reasoning Trace" section to see exactly how the agent derived its answer and review the cited page numbers.