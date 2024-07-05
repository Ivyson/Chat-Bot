from flask import Flask, request, jsonify
import json
import os
import Levenshtein
from flask_cors import CORS
import random
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from googlesearch import search
import requests
from bs4 import BeautifulSoup

# Download required NLTK data files
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

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

def preprocess_text(text):
    # Tokenize the text into words
    words = word_tokenize(text.lower())
    # Remove stopwords
    words = [word for word in words if word not in stopwords.words('english')]
    # Perform lemmatization
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return ' '.join(words)

def find_answer(knowledge_base, question, similarity_threshold=0.5):
    best_match = None
    highest_similarity = 0

    preprocessed_question = preprocess_text(question)

    for context in knowledge_base["contexts"]:
        for stored_question in context["questions"]:
            preprocessed_stored_question = preprocess_text(stored_question)
            # Calculate string similarity using Levenshtein distance
            string_similarity = Levenshtein.ratio(preprocessed_stored_question, preprocessed_question)
            if string_similarity > highest_similarity and string_similarity >= similarity_threshold:
                highest_similarity = string_similarity
                best_match = random.choice(context["answers"])

    return best_match

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

def google_search(query, num_results=1):
    search_results = []
    for url in search(query, tld="com", num=num_results, stop=num_results, pause=1):
        search_results.append(url)
    return search_results

def fetch_page_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except requests.RequestException:
        return None

def extract_text_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    for script in soup(['script', 'style']):
        script.decompose()
    return ' '.join(soup.stripped_strings)


def search_google_and_extract(query, num_results=1):
    urls = google_search(query, num_results)
    return urls  # Return only the URLs


@app.route('/api/chat', methods=['POST'])
def chat():
    knowledge_base = load_knowledge_base('Assets/data.json')
    data = request.get_json()
    user_message = data.get('message').lower()
    
    # Search the knowledge base first
    answer = find_answer(knowledge_base, user_message)
    
    if not answer:
        # If no answer found in the knowledge base, search Google
        search_results = search_google_and_extract(user_message)
        if search_results:
            response_message = "Here are some sources I found:\n" + "\n".join(search_results)
        else:
            response_message = "I couldn't find any information. Please try again."
    else:
        response_message = answer
    
    return jsonify({'response': response_message})
    

@app.route('/api/botstat', methods=['POST'])
def botstats():
    return jsonify({"message": "Running"})
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