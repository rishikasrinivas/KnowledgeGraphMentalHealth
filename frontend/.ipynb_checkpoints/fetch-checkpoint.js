async function fetchData() {
    try {
        const response = await fetch('/get_results'); // Adjust the URL as necessary

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        
        

        const outputElement = document.getElementById('output');
        outputElement.innerHTML = JSON.stringify(data, null, 2); // Display the data
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

document.getElementById('fetchButton').addEventListener('click', fetchData);