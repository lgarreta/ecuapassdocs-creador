async function loadInputParameters (parametersFile) {
	try {
		// Fetch JSON data using AJAX
		//fetch('{% static "appdocs/json/cartaporte_input_parameters.json" %}')
		const response = await fetch(parametersFile);
		const jsonData = await response.json ();
		console.log (">>> jsonData:", jsonData); // Optional: Log the data to the console
		return (jsonData);
	}catch (error) {
		console.error('Error fetching JSON:', error);
		return null;
	}
}

