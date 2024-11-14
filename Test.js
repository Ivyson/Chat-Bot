// fetch("http://127.0.0.1:5000/api/botstat", {
//     method: "POST",
//     headers: {
//         "Content-Type": "application/json"
//     },
//     body: JSON.stringify({})
// })
// .then(response => response.json())
// .then(data => console.log("Server Response:", data))
// .catch(error => console.error("Error connecting to the server:", error));
// Function to send a message to the backend
function sendMessage() {
    // const userInput = document.getElementById('user-input').value;
    // if (!userInput.trim()) {
    //     return;
    // }
    // const messageContainer = document.getElementById('messages');

    // // Create and style the user message element
    // const userMessageElement = document.createElement('div');
    // userMessageElement.innerText = `${userInput}`;
    // userMessageElement.style.color = "white";
    // userMessageElement.style.height = '2vw';
    // userMessageElement.style.textAlign = 'right';
    // userMessageElement.style.paddingRight = "10px";
    // userMessageElement.style.marginTop = "10px";
    // userMessageElement.style.borderBottom = "1px solid grey";
    // messageContainer.appendChild(userMessageElement);

    // Send the user message to the backend
    fetch('http://127.0.0.1:5000/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: "Hi, How are you" })
    })
    .then(response => {
        console.log(response.status);
        // console.log(response.text);
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
      console.log(data.response);
      

    })
    .catch(error => {
        console.error('Error : Something went wrong', error);
        alert('Failed to send message. Please ensure the backend server is running.',error);
    });

    document.getElementById('user-input').value = '';
}