# 🧠 AI Interview Questions & Answers Generator

This project is a **LangChain-based tool** that generates **interview questions and answers** dynamically based on user input. It leverages the power of OpenAI's GPT models to simulate intelligent Q&A generation, ideal for technical interviews, HR rounds, or practice sessions.

---

## 🚀 Features

- Generates interview questions from any pdf that you give to the model.
- Provides intelligent answers using LangChain + LLM
- Easy to extend with custom prompts or models

---

## 🛠️ Tech Stack

- 🐍 Python
- 🧠 [LangChain](https://www.langchain.com/)
- 🦾 OpenAI GPT (via API)
- 📁 `.env` for secret management

---

## ⚙️ Installation

```bash
# 1. Clone the repo
git clone https://github.com/Sudharshansirikonda/AI_Interview_ques_ans_Generator.git
cd AI_Interview_ques_ans_Generator

# 2. (Optional) Create and activate a virtual environment
conda create -n langchain-env python=3.10 -y
conda activate langchain-env

# 3. Install dependencies
pip install -r requirements.txt
