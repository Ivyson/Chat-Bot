# Chat - Bot Application
This project is a simple chatbot built using Flask and NLTK. The chatbot uses a knowledge base stored in a JSON file to answer user questions. If the answer is not found in the knowledge base, it performs a Google search and returns the top search results.

## Features
 - Load and save knowledge base from a JSON file
 - Preprocess text (tokenization, stopword removal, lemmatization)
 - Find answers using Levenshtein string similarity
 - Add new questions and answers to the knowledge base
 - Perform Google searches and return results
 - REST API endpoints to interact with the chatbot and manage the knowledge base
## Requirements
- Python 3.6+
- Flask
- Flask-CORS
- python-Levenshtein
- NLTK
- googlesearch-python
- requests
- beautifulsoup4
## Installation
1. To clone the repo to your local machine, You can either perform the following tasks
     - download the zip version of this repository by <a href="https://github.com/Ivyson/Chat-Bot/archive/refs/heads/main.zip">Clicking Here!</a>
     - Navigate through your terminal and enter : ``` git clone https://github.com/Ivyson/Chat-Bot.git```