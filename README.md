# Week 10 - LangChain Basics

## Project
College Assistant Chatbot using LangChain Prompt Templates and Chains with a local Ollama model.

## Folder structure
```text
LangChain_Basics/
├── dataset/
│   ├── prompts.csv
│   ├── user queries.csv
│   ├── chatbot_responses.csv
│   └── chain results.csv
├── notebook/
│   └── Week10_LangChain_Basics.ipynb
├── langchain_chatbot.py
├── requirements.txt
└── README.md
```

## 1. Requirements
- Python 3.10 or newer
- Ollama installed and running
- A model downloaded in Ollama (this project uses `llama3.2`)

If the model is not installed, open PowerShell and run:
```powershell
ollama pull llama3.2
```

## 2. Create and activate a virtual environment (PowerShell)
```powershell
python -m venv venv
.env\Scripts\Activate.ps1
```

If activation is blocked, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.env\Scripts\Activate.ps1
```

## 3. Install packages
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Run the chatbot
Make sure Ollama is running. Then:
```powershell
python langchain_chatbot.py
```
Choose one of these prompt templates: `general`, `admission`, `library`, `examination`, `fees_support`. Press Enter to use `general`. Type `exit` to stop.

## 5. Run the Jupyter Notebook
From the project folder:
```powershell
jupyter notebook
```
Open `notebook/Week10_LangChain_Basics.ipynb` and run the cells in order. The notebook tests 20 queries, displays the responses, tests all five prompt templates, and demonstrates summarization and question-answering chains. The 20-query test can take time because each question is sent to the local model.

## 6. Three chains
1. College chatbot chain: prompt template -> Ollama model -> string output.
2. Summarization chain: summarizes supplied text.
3. Question-answering chain: answers from supplied context only.

## 7. CSV output
- `prompts.csv`: five reusable prompt templates.
- `user queries.csv`: 20 test questions.
- `chatbot_responses.csv`: chatbot questions and generated answers.
- `chain results.csv`: summarization and question-answering outputs.

The CSV files are created with headers. Generated answers are added when you run the chatbot or notebook.

## 8. Week 9 vs Week 10 comparison
| Week 9 chatbot | Week 10 chatbot |
|---|---|
| Directly sends user input to Ollama | Uses LangChain components |
| Prompt is generally written inside Python code | Uses reusable prompt templates |
| Model call and program logic are closely connected | Prompt, model and output are arranged as a chain |
| Adding new tasks requires more manual code | Separate chains can be created for different tasks |
| Basic chatbot structure | Modular structure that can later be extended for RAG |

## Notes
- This is a starter college assistant. It does not contain official college data, so it must not be treated as a source for actual fees, deadlines, exam dates, or policies.
- If your Week 9 Ollama model has a different name, change `MODEL_NAME` in `langchain_chatbot.py`.
- LangChain's current Ollama integration uses `ChatOllama` from `langchain_ollama` and runnable chains such as `prompt | llm | output_parser`.
