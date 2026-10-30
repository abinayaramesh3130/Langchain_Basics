import csv
from pathlib import Path
from datetime import datetime

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "dataset"
MODEL_NAME = "llama3.2"

llm = ChatOllama(model=MODEL_NAME, temperature=0.2)

PROMPTS = {
    "general": ChatPromptTemplate.from_template(
        "You are a helpful college assistant. Answer clearly and simply. "
        "If details are not provided, say the student should contact the college office. "
        "Question: {question}"
    ),
    "admission": ChatPromptTemplate.from_template(
        "You are a college admission assistant. Explain admission-related steps in simple numbered points. "
        "Do not invent dates, fees, eligibility rules, or document requirements. "
        "If information is missing, direct the student to the admission office. Student query: {question}"
    ),
    "library": ChatPromptTemplate.from_template(
        "You are a library assistant. Give practical, polite guidance about library services. "
        "Do not invent opening hours, borrowing limits, or fines. If exact policy is unknown, "
        "ask the student to check with the librarian. Student query: {question}"
    ),
    "examination": ChatPromptTemplate.from_template(
        "You are an examination office assistant. Explain exam procedures clearly. "
        "Never invent exam dates, attendance rules, or hall-ticket details. "
        "Direct the student to official college notices for exact information. Student query: {question}"
    ),
    "fees_support": ChatPromptTemplate.from_template(
        "You are a student support assistant. Give safe, practical guidance about fees, scholarships, "
        "certificates, and student services. Do not invent amounts, deadlines, or payment links. "
        "Recommend the relevant college office for official details. Student query: {question}"
    )
}

# LangChain chains use prompt | model | output parser.
from langchain_core.output_parsers import StrOutputParser
output_parser = StrOutputParser()

chatbot_chains = {name: prompt | llm | output_parser for name, prompt in PROMPTS.items()}

summary_prompt = ChatPromptTemplate.from_template(
    "Summarize the following text in 4 simple bullet points:\n\n{text}"
)
summary_chain = summary_prompt | llm | output_parser

qa_prompt = ChatPromptTemplate.from_template(
    "Answer the question using only the context below. "
    "If the answer is not in the context, say that the information is not available.\n\n"
    "Context: {context}\nQuestion: {question}"
)
qa_chain = qa_prompt | llm | output_parser

def save_response(query, response, template_name):
    path = DATA_DIR / "chatbot_responses.csv"
    new_file = not path.exists() or path.stat().st_size == 0
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["query_id", "user_query", "response", "template_used"])
        writer.writerow([datetime.now().isoformat(timespec="seconds"), query, response, template_name])

def save_chain_result(chain_name, input_text, output_text):
    path = DATA_DIR / "chain results.csv"
    new_file = not path.exists() or path.stat().st_size == 0
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["chain_name", "input_text", "output_text"])
        writer.writerow([chain_name, input_text, output_text])

def ask_college_bot(question, template_name="general"):
    if template_name not in chatbot_chains:
        template_name = "general"
    answer = chatbot_chains[template_name].invoke({"question": question})
    save_response(question, answer, template_name)
    return answer

def summarize_text(text):
    result = summary_chain.invoke({"text": text})
    save_chain_result("summarization", text, result)
    return result

def answer_from_context(context, question):
    result = qa_chain.invoke({"context": context, "question": question})
    save_chain_result("question_answering", question, result)
    return result

def main():
    print("COLLEGE ASSISTANT CHATBOT (LangChain + Ollama)")
    print("Type 'exit' to stop.")
    print("Templates: general, admission, library, examination, fees_support")
    while True:
        question = input("\nYou: ").strip()
        if question.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye!")
            break
        if not question:
            continue
        template_name = input("Choose template (press Enter for general): ").strip().lower() or "general"
        if template_name not in PROMPTS:
            print("Unknown template. Using general.")
            template_name = "general"
        try:
            print("\nChatbot:", ask_college_bot(question, template_name))
        except Exception as e:
            print("Error connecting to Ollama. Check that Ollama is running and the model is installed.")
            print("Details:", e)

if __name__ == "__main__":
    main()
