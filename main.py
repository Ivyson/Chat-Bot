import json
import os
import difflib

# Load the knowledge base from the JSON file
def load_knowledge_base(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {"questions": []}
    else:
        return {"questions": []}

# Save the knowledge base to the JSON file
def save_knowledge_base(file_path, knowledge_base):
    with open(file_path, 'w') as file:
        json.dump(knowledge_base, file, indent=4)

# Find the answer to a question
def find_answer(knowledge_base, question, threshold=0.6):
    questions = [entry["question"] for entry in knowledge_base["questions"]]
    closest_matches = difflib.get_close_matches(question, questions, n= 1, cutoff=threshold)
    
    if closest_matches:
        best_match = closest_matches[0]
        for entry in knowledge_base["questions"]:
            if entry["question"].lower() == best_match.lower():
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
        question = input("You: ")
        if question.lower() == 'exit':
            break
        
        answer = find_answer(knowledge_base, question)
        if answer:
            print(f"Sam: {answer}")
        else:
            answer = input("I don't know the answer. Please teach me or skip this by typing skip :) : ")
            if answer.lower() == 'skip':
                continue
            else:
                add_question(knowledge_base, question, answer)
                save_knowledge_base(file_path, knowledge_base)
                print("Thank you! I've learned something new.")

if __name__ == "__main__":
    run_bot()
