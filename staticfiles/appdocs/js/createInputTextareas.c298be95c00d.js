// Create textarea inputs for ECUAPASS document forms (e.g. "txt00", "txt01"
// Textarea properties are given in the input parameters JSON file

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
				textarea.setAttribute (restriction, restriction);
			});
		}

		inputsContainer.appendChild (textarea);
		textAreas.push (textarea);
	});

	return (textAreas);
}

