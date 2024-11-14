from flask import Flask, request, jsonify
import json
import os
import difflib
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Load the knowledge base from the JSON file
def load_knowledge_base(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {"contexts": []}
    else:
        return {"contexts": []}

def save_knowledge_base(file_path, knowledge_base):
    with open(file_path, 'w') as file:
        json.dump(knowledge_base, file, indent=4)

def find_answer(knowledge_base, question, threshold=0.6):
    question_length = len(question)
    for context in knowledge_base["contexts"]:
        for stored_question in context["questions"]:
            length_similarity = abs(len(stored_question) - question_length) / max(len(stored_question), question_length)
            if length_similarity < threshold:
                string_similarity = difflib.SequenceMatcher(None, stored_question, question).ratio()
                if string_similarity >= threshold:
                    return random.choice(context["answers"])
    return None

def add_question(knowledge_base, context_name, question, answer):
    for context in knowledge_base["contexts"]:
        if context["context"].lower() == context_name.lower():
            context["questions"].append(question)
            context["answers"].append(answer)
            save_knowledge_base('data.json', knowledge_base)
            return
    # If context does not exist, create a new one
    knowledge_base["contexts"].append({
        "context": context_name,
        "questions": [question],
        "answers": [answer]
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
    context = data.get('context').lower()
    question = data.get('question').lower()
    answer = data.get('answer')
    
    add_question(knowledge_base, context, question, answer)
    return jsonify({'message': 'Thank you! I\'ve learned something new.'})

if __name__ == '__main__':
    app.run(debug=True)