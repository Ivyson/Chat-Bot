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
1. To clone the repo to your local machine, You can perform <b> ONE <b> of the following tasks :
     - download the zip version of this repository by <a href="https://github.com/Ivyson/Chat-Bot/archive/refs/heads/main.zip">Clicking Here!</a> Or,
     - Navigate through your terminal and enter : ``` git clone https://github.com/Ivyson/Chat-Bot.git``` then ``` cd Chat-Bot ```
2. Create a virtual enviroment(Optional)
    - ### On Windows
     -Using CMD
     - ``` python -m venv venv && .\venv\Scripts\activate ```
    - ### On MacOS and Linux
     - ``` python3 -m venv venv ``` then ``` source venv/bin/activate ```
3. Install the dependencies
1. Ensure that your current location in your terminal is ``` Chat-Bot ```, You can confirm this by typing ``` pwd ``` in your terminal, If you are indeed in that location then you may proceed to the next step.
2. Install all the required dependencies for this application to run by running the following script: ``` pip install -r requirements.txt ``` . Even easier, if your systems security allows this, you can run a bash file ``` run.sh ``` and it will ensure that everything is done for you, it will even run the python script for you.
 - If the security of your system does not allow running the ``` run.sh ``` file then, after installing the dependencies, ensure that you run the ``` main.py ``` file by entering ``` python main.py ``` on your terminal.