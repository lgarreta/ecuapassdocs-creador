function setParametersToInputs (textAreas, inputParameters, handleInput) {
	// Set restrictions and styles for each input textarea
	textAreas.forEach (function (textArea) {
		const input = inputsParameters [textArea.id];
		textArea.value = input ["value"]
		textArea.style.fontSize  = input["fontSize"];
		textArea.style.textAlign = input ["align"];
		textArea.style.position = "absolute";

		textArea.style.left   = input ["x"]  + "px";
		textArea.style.top    = input ["y"]  + "px";
		textArea.style.width  = input ["width"]  + "px";
		textArea.style.height = input ["height"] + "px";
		st = textArea.style
		console.log (">>> input", st.left, st.top, st.width, st.height);

		textArea.addEventListener ('input', handleInput);
	});
}

// Control max number of lines and chars according to className
function handleInput (event) {
	textArea = event.target;
	convertToUpperCase (textArea);

	MAXLINES = inputsParameters [textArea.id]["maxLines"];
	//MAXCHARS = inputsParameters [textArea.id]["maxChars"] * 3.6;
	MAXCHARS = inputsParameters [textArea.id]["maxChars"];

	// Control maximum number of chars
	//lines = pdf.splitTextToSize (textArea.value, MAXCHARS);
	//textArea.value = lines.join("\n");
	var lines = textArea.value.split('\n');

	for (var i = 0; i < lines.length; i++) {
		if (lines[i].length > MAXCHARS) {
			// Truncate the line to the maximum allowed characters
			var remainingChars = lines[i].substring(MAXCHARS);
			lines[i] = lines[i].substring(0, MAXCHARS);
			// Move the remaining characters to the next line
			lines.splice(i + 1, 0, remainingChars);
		}
	}
	// Join the modified lines and set the textarea value
	textArea.value = lines.join('\n');			

	// Control maximum number of lines
	text = textArea.value;
	lines = text.split('\n'); 
	if (lines.length > MAXLINES) 
		textArea.value = lines.slice (0, MAXLINES).join('\n');
}

// Save the current cursor position
function convertToUpperCase (textArea) {
	var start = textArea.selectionStart;
	var end = textArea.selectionEnd;
	// Convert the text to uppercase and set it back to the textArea
	textArea.value = textArea.value.toUpperCase();
	// Restore the cursor position
		textArea.setSelectionRange(start, end);
}

