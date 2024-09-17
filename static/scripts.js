// Fetch the current queue when the page loads
window.onload = function() {
    getQueue();
}

// Function to get the current queue from the server
function getQueue() {
    fetch('/get-queue')
        .then(response => response.json())
        .then(data => {
            const queueList = document.getElementById('queueList');
            queueList.innerHTML = '';  // Clear existing list

            // Loop through the queue and add it to the UI
            data.forEach((item, index) => {
                const listItem = document.createElement('li');
                listItem.className = 'queue-item';
                listItem.innerHTML = `${index + 1}. ${item.name}
                    <button class="remove-btn" onclick="removeFromQueue('${item.name}')">Remove</button>`;
                queueList.appendChild(listItem);
            });
        });
}

// Function to add a name to the queue
function addToQueue() {
    const userName = document.getElementById('userName').value.trim();

    if (userName) {
        fetch('/add-to-queue', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'name': userName })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                getQueue();  // Refresh queue
                document.getElementById('userName').value = '';  // Clear input field
            }
        });
    } else {
        alert('Please enter a name.');
    }
}

// Function to clear the queue
function clearQueue() {
    fetch('/clear-queue', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                getQueue();  // Refresh queue
            }
        });
}

// Function to remove single entry in queue
function removeFromQueue(userName) {
    fetch('/remove-from-queue', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'name': userName })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                getQueue();  // Refresh queue
            }
        });
}

document.getElementById('userName').addEventListener('keydown', function(event) {
    if (event.key === 'Enter'){
        document.getElementById("addButton").click();
    }
});