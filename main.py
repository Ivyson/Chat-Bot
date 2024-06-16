from flask import Flask, request, jsonify
import json
import os
import difflib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

def save_knowledge_base(file_path, knowledge_base):
    with open(file_path, 'w') as file:
        json.dump(knowledge_base, file, indent=4)

def find_answer(knowledge_base, question, threshold=0.6):
    questions = [entry["question"] for entry in knowledge_base["questions"]]
    closest_matches = difflib.get_close_matches(question, questions, n=1, cutoff=threshold)
    
    if closest_matches:
        best_match = closest_matches[0]
        for entry in knowledge_base["questions"]:
            if entry["question"].lower() == best_match.lower():
                return entry["answer"]
    return None

def add_question(knowledge_base, question, answer):
    knowledge_base["questions"].append({
        "question": question,
        "answer": answer
    })
    save_knowledge_base('data.json', knowledge_base)

@app.route('/api/chat', methods=['POST'])
def chat():
    knowledge_base = load_knowledge_base('data.json')
    data = request.get_json()
    user_message = data.get('message').lower()
    
    answer = find_answer(knowledge_base, user_message)
    if answer:
        response_message = answer
    else:
        response_message = "I don't know the answer. Please teach me."
    
    return jsonify({'response': response_message})

@app.route('/api/teach', methods=['POST'])
def teach():
    knowledge_base = load_knowledge_base('data.json')
    data = request.get_json()
    question = data.get('question').lower()
    answer = data.get('answer')
    
    add_question(knowledge_base, question, answer)
    return jsonify({'message': 'Thank you! I\'ve learned something new.'})

if __name__ == '__main__':
    app.run(debug=True)
