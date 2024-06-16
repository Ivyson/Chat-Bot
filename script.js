function startNewChat() {
    document.getElementById('messages').innerHTML = '';
}

function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (!userInput.trim()) {
        return;
    }

    const messageContainer = document.getElementById('messages');
    const userMessageElement = document.createElement('div');
    userMessageElement.textContent = `You : ${userInput}`;
    messageContainer.appendChild(userMessageElement);

    fetch('http://127.0.0.1:5000/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        const botMessageElement = document.createElement('div');
        botMessageElement.textContent = `Sam : ${data.response}`;
        messageContainer.appendChild(botMessageElement);

        if (data.response === "I don't know the answer. Please teach me.") {
            teachBot(userInput);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to send message. Please ensure the backend server is running.');
    });

    document.getElementById('user-input').value = '';
}

function teachBot(userQuestion) {
    const answer = prompt("I don't know the answer. Please teach me the correct response or type 'skip' to skip.");
    if (answer && answer.toLowerCase() !== 'skip') {
        fetch('http://127.0.0.1:5000/api/teach', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: userQuestion, answer: answer })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to teach the bot. Please ensure the backend server is running.');
        });
    }
}