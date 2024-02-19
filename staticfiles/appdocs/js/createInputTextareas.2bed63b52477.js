// Create textarea inputs for ECUAPASS document forms (e.g. "txt00", "txt01"
// Textarea properties are given in the input parameters file (JSON)

function createInputTextareas (inputsParameters, inputsContainer) {
	var textAreas = [];
	Object.keys (inputsParameters).forEach (key => {
		let input = inputsParameters [key]; 

		var textarea = document.createElement("textarea");
		textarea.setAttribute("name", key);
		textarea.setAttribute("id", key);
		textarea.setAttribute("class", input ["class"]);

		// Restrictions like "hidden" or "readonly"
		if ("restrictions" in input) {
			input ["restrictions"].forEach (restriction => {
				if (restriction.includes ("color")) {
					let color = restriction.split ("=")[1]
					textarea.style.color = color
				}else {
					textarea.setAttribute (restriction, restriction);
				}
			});
		}

		// Set onBlur to listen when user leaves out a textarea
		textarea.addEventListener ('blur', function (event) {
			//id = this.id
			console.log ("--id:")
		}

		inputsContainer.appendChild (textarea);
		textAreas.push (textarea);
	});

	return (textAreas);
}

