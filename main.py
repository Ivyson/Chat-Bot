import json
import os

# Load the knowledge base from the JSON file
def load_knowledge_base(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        return {"questions": []}

# Save the knowledge base to the JSON file
def save_knowledge_base(file_path, knowledge_base):
    with open(file_path, 'w') as file:
        json.dump(knowledge_base, file, indent=4)

# Find the answer to a question
def find_answer(knowledge_base, question):
    for entry in knowledge_base["questions"]:
        if entry["question"].lower() == question.lower():
            return entry["answer"]
    return None

# Add a new question and answer to the knowledge base
def add_question(knowledge_base, question, answer):
    knowledge_base["questions"].append({
        "question": question,
        "answer": answer
    })

# Main function to run the bot
def run_bot():
    file_path = 'data.json'
    knowledge_base = load_knowledge_base(file_path)

    while True:
        question = input("Ask a question (or type 'exit' to quit): ")
        if question.lower() == 'exit':
            break
        
        answer = find_answer(knowledge_base, question)
        if answer:
            print(f"Answer: {answer}")
        else:
            answer = input("I don't know the answer. Please teach me: ")
            add_question(knowledge_base, question, answer)
            save_knowledge_base(file_path, knowledge_base)
            print("Thank you! I've learned something new.")

if __name__ == "__main__":
    run_bot()
