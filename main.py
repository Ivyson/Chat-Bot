from flask import Flask, request, jsonify
import json
import os
from flask_cors import CORS
from flask import abort 
import random
import nltk
import google.generativeai as genai
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import difflib
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)
# Define the model
generation_config = {
    "temperature": 1,
    "top_p": 1,
    "top_k": 64,
    "max_output_tokens": 2000,
    "response_mime_type": "text/plain",
}
system_instruction = "Use the given Documents to Answer all of the following questions"
model = genai.GenerativeModel(
    model_name='models/gemini-1.5-flash',
    generation_config=generation_config,
    system_instruction=system_instruction,
    tools='code_execution'
)
history = []  
# Download required NLTK data files
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

app = Flask(__name__)
# Allow all origins for testing purposes, or specify the correct origin if known
CORS(app, resources={r"/api/*": {"origins": ["http://127.0.0.1:5000", "http://127.0.0.1:5500"]}})

 

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

def preprocess_text(text):
    # Tokenize the text into words
    words = word_tokenize(text.lower())
    # Remove stopwords
    words = [word for word in words if word not in stopwords.words('english')]
    # Perform lemmatization
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return ' '.join(words)

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

# @app.route('/api/chat', methods=['POST'])
# def chat():
#     # knowledge_base = load_knowledge_base('data.json')
#     data = request.get_json()
#     user_message = data.get('message')
#     # print(data)
    
#     # Search the knowledge base first
#     # answer = find_answer(knowledge_base, user_message)
#     answer = model.generate_content(user_message,tools='code_execution')
#      # Store the conversation history
#     history.append({"role": "user", "parts": [user_message]})
#     history.append({"role": "model", "parts": [answer.text]})
#     if not answer:
#         response = "No answer found for your question"
#         return jsonify({'response': response})
#     else:
#         # resonse = "The answer was found"
#         return jsonify({'response': answer })
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')
    chat_session = model.start_chat(
            history=history
        )

    try:
        history.append({"role": "user", "parts": [user_message]})
        answer = model.generate_content(user_message, tools='code_execution')
        history.append({"role": "model", "parts": [answer.text]})
        chat_session = model.start_chat(
            history=history
        )
        return jsonify({'response': answer.text})
    except Exception as e:
        # Handle any error that occurs during the model's generation call
        return jsonify({'error': f"Error generating content: {str(e)}"}), 500

    
@app.route('/api/botstat', methods=['POST'])
def botstats():
    return jsonify({"message": 'Running'})

@app.route('/api/teach', methods=['POST'])
def teach():
    knowledge_base = load_knowledge_base('data.json')
    data = request.get_json()
    context = data.get('context', '').strip().lower()  # Validate and sanitize context
    question = data.get('question', '').strip().lower()  # Validate and sanitize question
    answer = data.get('answer', '')  # No need to sanitize answer here

    if not context or not question:
        abort(400, 'Invalid request: Context or question is missing or empty')

    add_question(knowledge_base, context, question, answer)
    return jsonify({'message': 'Thank you! I\'ve learned something new.'})


if __name__ == '__main__':
    app.run(debug=True)