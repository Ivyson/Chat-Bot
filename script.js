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
    userMessageElement.textContent = `${userInput}`;
    userMessageElement.style.backgroundColor = 'red';
    userMessageElement.style.color = "white";
    userMessageElement.style.height = '2vw';
    userMessageElement.style.textAlign = 'right';
    userMessageElement.style.paddingRight = "10px"
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
        botMessageElement.textContent = `${data.response}`;
        botMessageElement.style.backgroundColor = 'blue';
        botMessageElement.style.color = "white";
        botMessageElement.style.height = '2vw';
        botMessageElement.style.textAlign = 'left';
        

        if (data.response === "I don't know the answer. Please teach me.") {
            // teachBot(userInput);
            botMessageElement.textContent = `I did not understand Your question, I am yet to be updated..`;

        }
        messageContainer.appendChild(botMessageElement);
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
function teach(){
    return ""
}