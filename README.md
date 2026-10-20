# LLM APIs: Your First AI Application

AI Engineering Bootcamp · Module 1 class materials

## Notebooks

| File | What it covers |
|---|---|
| `01_first_llm_call.ipynb` | First call, tokens and latency, messages, temperature, Gemini and Groq, prompts |
| `02_reliability_and_logging.ipynb` | Retries with back-off, safe failure demo, logging to JSON Lines |
| `03_classwork_ask_tool.ipynb` | Classwork: build the "Ask" tool step by step |
| `04_assignment_model_comparison.ipynb` | Assignment: compare two models on 5 questions |

## Setup (VS Code)

1. Install the **Python** and **Jupyter** extensions in VS Code.
2. Open this folder in VS Code (File > Open Folder).
3. Create and activate a virtual environment in the VS Code terminal:
   - Windows: `python -m venv .venv` then `.venv\Scripts\activate`
   - macOS / Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
4. Install packages: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and add your API keys:
   - Gemini: https://aistudio.google.com
   - Groq: https://console.groq.com
6. Open `01_first_llm_call.ipynb`, click **Select Kernel** (top right), and choose `.venv`.
7. Run cells with **Shift + Enter**.

## Rules

- Never commit `.env` or share your API keys.
- Free-tier prompts may be used by providers to improve their models. Don't send personal or confidential data.

---

## Assignment 2 · Model Comparison Report

**Topic:** Python programming fundamentals  
**Models:** Gemini (`GEMINI_MODEL` from `.env`) vs Groq (`GROQ_MODEL` from `.env`), temperature 0.2.  
**Method:** Five test questions were run against each model. Responses were assessed against the answer key in `04_assignment_model_comparison.ipynb`. Full results, including answers, token counts, latency, errors, and ratings, are recorded in [`results.csv`](results.csv).

### Test questions

1. In Python, what is the difference between a list and a tuple?
2. What does the `self` parameter in a Python class method refer to?
3. Write a one-line expression for the squares of even numbers 0–9.
4. What is the output of `print(type([]) is list)`?
5. Explain the difference between `==` and `is` in Python.

### Results

| Metric | Gemini (`gemini-3.8-flash`) | Groq (`openai/gpt-oss-20b`) |
|---|---:|---:|
| Correct answers | 0 | 5 |
| Partly correct answers | 0 | 0 |
| Wrong / failed answers | 5 | 0 |
| API errors | 5 | 0 |
| Average latency (s) | N/A | 0.86 |
| Average output tokens | N/A | 121 |

**Important limitation:** All five Gemini requests failed after retries with timeout/rate-limit errors, so Gemini did not return answers that could be evaluated. The five Gemini rows are marked `wrong` for the assignment's rating summary because no usable answer was returned; this should not be interpreted as evidence that Gemini's answers were factually incorrect. Gemini's latency and output-token averages are unavailable. Groq answered all five questions correctly; its average latency was approximately 0.86 seconds and average output length was approximately 121 tokens.

### Which model would I choose, and why?

Based on the results collected in this run, I would choose Groq for this Python fundamentals task because it successfully answered all five questions correctly. Its average latency was about 0.86 seconds, and its responses used an average of 121 output tokens. Gemini's requests all failed with timeout or rate-limit errors, so I could not compare its answer quality, speed, or verbosity fairly. I would retest Gemini after resolving the API errors before making a final quality comparison between the two models.
