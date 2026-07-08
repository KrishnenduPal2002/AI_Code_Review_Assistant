# 🧠 AI Code Review Assistant

An AI-powered code review tool that analyzes your code and returns a structured, professional review — bugs, readability issues, best practices, time complexity,
an overall quality score, and a fully refactored version — all through a clean, custom-styled Streamlit interface.

Built with **LangChain**, **OpenAI (GPT-4o-mini)**, **Pydantic**, and **Streamlit**, with a deterministic static-analysis layer (Pyflakes) to catch mechanical bugs the LLM might miss.

---

## ✨ Features

- 🐞 **Bug detection** — combines LLM reasoning with static analysis (Pyflakes) for reliable results
- 📖 **Readability suggestions** — actionable feedback on naming, structure, and clarity
- ✅ **Best practice checks** — flags violations of language/framework conventions
- ⏱️ **Time complexity estimate** — Big-O analysis of the submitted code
- 💯 **Quality score (0–100)** — color-coded overall rating with a short summary
- 🛠️ **Fully refactored code** — a cleaned-up, corrected version you can copy directly
- 📄 **Auto-generated documentation** — docstrings and explanations for the refactored code
- 🎨 **Polished UI** — dark, glassmorphic Streamlit interface with tabbed results

---

## 🗂️ Project Structure

```
ai-code-review-assistant/
├── agent.py            # LLM client setup (ChatOpenAI)
├── models.py            # CodeReview Pydantic schema (structured output)
├── parser.py             # PydanticOutputParser bound to CodeReview
├── prompts.py            # Review prompt template
├── static_checks.py      # Deterministic static analysis (Pyflakes)
├── reviewer.py            # Orchestrates the LangChain pipeline + static checks
├── app.py                  # Streamlit UI
├── requirements.txt
├── .env.example
└── README.md
```

## 🧩 How it works

1. Code is submitted through the Streamlit UI.
2. A LangChain pipeline (`prompt | llm | parser`) sends the code to GPT-4o-mini
   with a structured-output prompt built from a Pydantic schema (`CodeReview`).
3. For Python code, `static_checks.py` runs Pyflakes to catch undefined names,
   unused imports, and similar mechanical issues.
4. Static-analysis findings are merged into the LLM's bug list, and the final
   structured result is rendered in the UI across tabs: **Findings**,
   **Refactored Code**, **Documentation**, and **Complexity**.

---

## 🛣️ Roadmap / Ideas

- [ ] Support for multi-file / repository-level reviews
- [ ] Diff view between original and refactored code
- [ ] Review history saved per session
- [ ] Additional static analyzers for other languages (e.g. ESLint for JS/TS)

---
