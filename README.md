# LLM APIs: Your First AI Application

AI Engineering Bootcamp · Module 1 class materials

## Notebooks

| File | What it covers |
|---|---|
| 01_first_llm_call.ipynb | First call, tokens and latency, messages, temperature, Gemini and Groq, prompts |
| 02_reliability_and_logging.ipynb | Retries with back-off, safe failure demo, logging to JSON Lines |
| 03_classwork_ask_tool.ipynb | Classwork: build the "Ask" tool step by step (all tasks completed) |
| 04_assignment_model_comparison.ipynb | Assignment: compare two models on 5 questions |
| ask.py | The finished "Ask" tool from notebook 03 (supports `--provider groq`) |

## Setup (VS Code)

1. Install the **Python** and **Jupyter** extensions in VS Code.
2. Open this folder in VS Code (File > Open Folder).
3. Create and activate a virtual environment in the VS Code terminal:
   - Windows: `python -m venv .venv` then `.venv\Scripts\activate`
   - macOS / Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
4. Install packages: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and paste your keys:
   - Gemini: https://aistudio.google.com (Get API key)
   - Groq: https://console.groq.com (API Keys)
6. Open `01_first_llm_call.ipynb`, click **Select Kernel** (top right) and choose `.venv`.
7. Run cells with **Shift + Enter**.

## Rules

- Never commit `.env` or share your keys.
- Free-tier prompts may be used by providers to improve their models. Don't send personal or confidential data.

---

## Assignment 2 · Model Comparison Report

**Topic:** Python programming fundamentals
**Models:** Gemini (`gemini-3.8-flash`) vs Groq (`openai/gpt-oss-20b`), temperature 0.2
**Method:** 5 test questions, each with one objectively correct answer (answer key in the notebook). Every answer rated *correct*, *partly correct* or *wrong* against the key. Full data in [`results.csv`](results.csv).

### Test questions

1. In Python, what is the difference between a list and a tuple?
2. What does the `self` parameter in a Python class method refer to?
3. Write a one-line expression for the squares of even numbers 0–9.
4. What is the output of `print(type([]) is list)`?
5. Explain the difference between `==` and `is` in Python.

### Results

| Metric | Gemini (gemini-3.8-flash) | Groq (openai/gpt-oss-20b) |
|---|---|---|
| Correct | 4 | 5 |
| Partly correct | 0 | 0 |
| Wrong | 1 | 0 |
| Errors | 1 | 0 |
| Avg latency (s) | 12.71 | 0.53 |
| Avg tokens out | 56 | 128 |

*Gemini's "wrong" is an error row: Q4 hit the free-tier rate limit, all 3 retries
(2s, 4s, 8s back-off) failed, and no answer was produced — recorded by the
notebook's error handling. Every answer Gemini did return was correct.*

### Which model would I choose, and why?

I would choose **Groq**. Both models answered every question they completed
correctly (Groq 5/5, Gemini 4/4), so on pure answer quality they tie — but Groq
delivered those answers in an average of 0.53s versus Gemini's 12.71s, roughly
24× faster, and it completed all 5 calls with zero errors while Gemini's 4th
call was lost to rate limiting even after retries. Groq's answers are more
verbose (128 vs 56 average tokens out), but for a study-assistant use case that
extra explanation is useful rather than harmful. Speed and reliability win here:
for this topic, **Groq** is the better choice; I'd only reconsider Gemini if
answer depth on harder questions mattered more than latency, or on a paid tier
where its rate limits wouldn't bite.
