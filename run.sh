#Install The required Dependencies
pip install -r requirements.txt
# Downloads the required NLTK files 
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"