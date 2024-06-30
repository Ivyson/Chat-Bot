'''''
from flask import request, jsonify
from googlesearch import search


def google_search(query, num_results=3):
    search_results = []
    for url in search(query, tld="com", num=num_results, stop=num_results, pause=2):
        search_results.append(url)
    return search_results

def chat():
    user_message = request.json['message']
    try:
        search_results = google_search(user_message)
        if search_results:
            response_message = "Here are some sources I found:\n" + "\n".join(search_results)
        else:
            response_message = "I couldn't find any information. Please try again."
    except Exception as e:
        response_message = f"An error occurred: {e}"

    return jsonify({'message': response_message})

# For manual testing outside the Flask app
if __name__ == '__main__':
    try:
        user_message = input("You: ")
        search_results = google_search(user_message)
        if search_results:
            response_message = "Here are some sources I found:\n" + "\n".join(search_results)
            print(response_message)
        else:
            response_message = "I couldn't find any information. Please try again."
    except Exception as e:
        print(f"An error occurred: {e}")
'''