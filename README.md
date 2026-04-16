# 🎙️Voice AI Agent (Local Automation Assistant)

An intelligent **Voice-Based Local AI Agent** that can understand user commands (via audio or text), interpret intent, and execute tasks such as file creation, code generation, and text processing — all locally and safely.

---

##  Features

*  **Voice Input Support** (Record or Upload Audio)
*  **Speech-to-Text using Whisper**
*  **Intent Detection using LLM**
*  **Local Task Execution Engine**
*  **Safe File Handling in `output/` Directory**
*  **Code Generation & Auto-Saving**
*  **Streamlit Interactive UI**

---

##  Architecture Overview

```
User Input (Voice/Text)
        ↓
Speech-to-Text (Whisper)
        ↓
Intent Detection (LLM)
        ↓
Task Router
   ├── File Operations
   ├── Code Generation
   └── Text Processing
        ↓
Execution Engine
        ↓
Output (Saved in /output folder + UI Display)
```

---

##  Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **Speech Recognition:** Whisper
* **AI/NLP:** LLM (OpenAI / Groq)
* **File Handling:** OS Module

---

## 📁 Project Structure

```
├── app.py                 # Main Streamlit Application
├── output/               # All generated files (SAFE ZONE)
├── utils/                # Helper functions (optional)
├── requirements.txt
└── README.md
```

---

##  Safety Design

To prevent accidental system modifications:

* ✅ All generated files are restricted to the `output/` directory
* ❌ No direct access to system-critical paths
*  Controlled execution environment

---

##  Usage

1. Open the Streamlit UI
2. Choose input method:

   * Upload Audio 🎧
   * Record Voice 🎤
3. Give commands like:

   * "Create a Python file for sorting"
   * "Summarize this text"
   * "Generate a login page code"
4. Output will:

   * Be displayed in UI
   * Saved inside `/output` folder

---

##  Example Commands

*  "Create a folder and add a file"
*  "Generate Python code for binary search"
*  "Summarize this paragraph"

---
##  Future Improvements

*  Real-time voice streaming
*  Plugin-based tool system
*  Web automation support
*  Mobile-friendly UI

---
