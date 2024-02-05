
function loadInputParameters () {
    // Fetch JSON data using AJAX
	let jsonData;
    fetch('{% static "appdocs/json/cartaporte_input_parameters.json" %}')
        .then(response => response.json())
        .then(data => {
            // Assign JSON data to the variable
            jsonData = data;
            console.log(jsonData); // Optional: Log the data to the console
			return (jsonData)
        })
        .catch(error => console.error('Error fetching JSON:', error));
}

