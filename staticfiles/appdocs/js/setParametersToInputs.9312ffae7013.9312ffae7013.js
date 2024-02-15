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

