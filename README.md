# 🤖 DualAgent AI

> **Multi-Agent Writer & Editor — Two specialized AI agents working together to produce refined content.**

DualAgent AI is a **multi-agent content generation application** built with Python, Streamlit, Groq API, and Llama 3.3 70B.

The system uses two specialized agents in a sequential workflow: a **Writer Agent** generates the initial draft, while an **Editor/Critic Agent** reviews, improves, and refines that draft into a polished final output.

Built as part of the **NeuroFive Solutions Generative AI & Prompt Engineering Internship — Week 4: Multi-Agent Basics**.

---

## 🖥️ Application Preview

<table>
<tr>
<td width="50%" align="center">

### ✍️ Agent 1 — Writer Output

<img src="Agent%20Prompt%20Outputs/Agent%201%20Output.png" width="100%" height="520" alt="Agent 1 Writer Output">

</td>
<td width="50%" align="center">

### 🧠 Agent 2 — Editor Output

<img src="Agent%20Prompt%20Outputs/Agent%202%20Output.png" width="100%" height="520" alt="Agent 2 Editor Output">

</td>
</tr>

<tr>
<td width="50%" align="center">

### 🖥️ Main UI

<img src="Agent%20Prompt%20Outputs/Main%20UI.png" width="100%" height="520" alt="DualAgent AI Main UI">

</td>
<td width="50%" align="center">

### ✨ Final Refined Output

<img src="Agent%20Prompt%20Outputs/Final%20Output.png" width="100%" height="520" alt="Final Refined Output">

</td>
</tr>
</table>

---

## 🚀 How It Works

```text
User Topic
    │
    ▼
✍️ Writer Agent
Creates the initial draft
    │
    ▼
🧠 Editor / Critic Agent
Reviews and improves the draft
    │
    ▼
✨ Refined Final Output
    │
    ▼
🔍 Improvement Analysis
```

The key aspect of the system is that **Agent 2 directly receives Agent 1's generated output**, allowing the agents to collaborate sequentially.

---

## 🤖 Agents

### ✍️ Writer Agent

Responsible for creating the initial draft based on the user's:

* Topic
* Content type
* Tone
* Desired length

The Writer focuses exclusively on **content creation** rather than self-critique.

### 🧠 Editor / Critic Agent

Receives the Writer's draft and improves it by focusing on:

* Clarity
* Structure
* Grammar
* Flow
* Professional tone
* Repetition
* Overall readability

It also reports the **key improvements made** during the editing stage.

---

## ✨ Features

* 🤖 **Two-Agent Architecture** — Specialized Writer and Editor agents
* 🔄 **Sequential Orchestration** — Agent 1's output becomes Agent 2's input
* 📝 **Multiple Content Types** — Article, LinkedIn Post, Report, Explainer
* 🎯 **Configurable Tone** — Professional, Educational, Persuasive
* 📏 **Flexible Length** — Short, Medium, Detailed
* 📊 **Draft vs Refined Comparison** — View the original and improved versions
* 🔍 **Improvement Analysis** — Understand what the Editor changed
* 📈 **Session Analytics** — Track generations and successful runs
* 🎨 **Modern Streamlit UI** — Dark, portfolio-oriented interface
* 🔐 **Environment-Based API Security** — Credentials stored outside source code

---

## 🔄 Multi-Agent Pipeline

The application implements a simple but practical agent orchestration pattern:

| Stage | Agent          | Responsibility                     |
| ----- | -------------- | ---------------------------------- |
| 01    | ✍️ Writer      | Generate the initial content draft |
| 02    | 🧠 Editor      | Review and improve the draft       |
| 03    | ✨ Final Output | Present the refined content        |
| 04    | 🔍 Analysis    | Highlight the improvements made    |

This architecture demonstrates how specialized agents can divide responsibilities instead of relying on a single prompt-response interaction.

---

## 🧪 Testing

The pipeline was tested with **two different professional topics** to verify that the Writer → Editor workflow works across multiple content-generation scenarios.

### Test 01 — AI Agents & Software Development

**Content Type:** LinkedIn Post
**Tone:** Professional
**Length:** Medium

The system generated an initial LinkedIn draft through the Writer Agent and then passed it to the Editor Agent for refinement.

### Test 02 — Retrieval-Augmented Generation

**Content Type:** LinkedIn Post
**Tone:** Professional
**Length:** Medium

The same two-agent pipeline was executed on a second AI-focused topic to evaluate consistency across different inputs.

### Editor Improvements Observed

The Editor Agent primarily improved:

* Content structure
* Sentence clarity
* Professional tone
* Flow and transitions
* Repetition
* Overall readability

---

## 🛠️ Tech Stack

| Category      | Technologies            |
| ------------- | ----------------------- |
| Language      | Python                  |
| UI            | Streamlit               |
| LLM API       | Groq API                |
| Model         | Llama 3.3 70B Versatile |
| Configuration | python-dotenv           |
| Styling       | Custom CSS              |

---

## 📁 Project Structure

```text
DualAgent-AI/
│
├── app.py
├── Agent Prompt Outputs/
│   ├── Agent 1 Output.png
│   ├── Agent 2 Output.png
│   ├── Final Output.png
│   └── Main UI.png
│
├── .gitignore
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Waariha-Asim/DualAgent-AI.git
cd DualAgent-AI
```

### 2. Create a Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install streamlit groq python-dotenv
```

### 4. Configure the API Key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

The application loads the key using `python-dotenv`:

```python
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
```

The `.env` file is excluded from Git through `.gitignore`.

### 5. Run the Application

```bash
streamlit run app.py
```

---

## 👩‍💻 Author

### Waariha Asim

**AI Engineer | AI Automation Engineer**


> **DualAgent AI — Two specialized agents. One refined result.**
