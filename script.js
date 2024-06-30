// Function to clear the chat messages
function startNewChat() {
    document.getElementById('messages').innerHTML = '';
}

let scroller = document.getElementsByClassName("main-page")[0];

// Function to send a message to the backend
function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (!userInput.trim()) {
        return;
    }
    const messageContainer = document.getElementById('messages');

    // Create and style the user message element
    const userMessageElement = document.createElement('div');
    userMessageElement.textContent = `${userInput}`;
    userMessageElement.style.color = "white";
    userMessageElement.style.height = '2vw';
    userMessageElement.style.textAlign = 'right';
    userMessageElement.style.paddingRight = "10px";
    userMessageElement.style.marginTop = "10px";
    userMessageElement.style.borderBottom = "1px solid grey";
    messageContainer.appendChild(userMessageElement);

    // Send the user message to the backend
    fetch('http://127.0.0.1:5000/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        const botMessageElement = document.createElement('div');
        botMessageElement.textContent = `${data.response}`;
        botMessageElement.style.color = "white";
        botMessageElement.style.height = '100%';
        botMessageElement.style.paddingLeft = "10px";
        botMessageElement.style.borderBottom = "1px solid grey";
        botMessageElement.style.marginTop = "10px";
        botMessageElement.style.textAlign = 'left';

        if (data.response === "I don't know the answer. Please teach me.") {
            teachBot(userInput);
        }
        messageContainer.appendChild(botMessageElement);

        // Scroll to the bottom of the chat container
        scroller.scrollTo({
            top: scroller.scrollHeight,
            behavior: 'smooth'
        });

    })
    .catch(error => {
        console.error('Error :', error);
        alert('Failed to send message. Please ensure the backend server is running.');
    });

    document.getElementById('user-input').value = '';
}

// Function to teach the bot when it doesn't know the answer
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

document.addEventListener('keydown', (event) => {
    if (event.key == 'Enter') {
        sendMessage();
    }
});

async function checkstatus() {
    try {
        let response = await fetch('http://127.0.0.1:5000/api/botstat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: "hello" })
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        let data = await response.json();
        return data.message;
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}

// Function to animate and check the bot status
async function animate() {
    let statsbar = document.getElementsByClassName('status-bar')[0];
    let stats = await checkstatus();
    if (!stats) {
        statsbar.textContent = "Offline";
        statsbar.style.display = 'flex';
        statsbar.style.backgroundColor = 'red';
        document.getElementById('user-input').style.display = 'none';
    } else {
        statsbar.textContent = "Online";
        statsbar.style.display = 'flex';
        statsbar.style.backgroundColor = 'green';
        document.getElementById('user-input').style.display = 'flex';
    }

    window.requestAnimationFrame(animate);
}

// Call checkstatus once to ensure it's working
checkstatus();

// Use requestAnimationFrame to repeatedly check the bot status
animate();