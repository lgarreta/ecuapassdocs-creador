
// Handle the event went user leaves out a textares

function handleBlurForTextareas (idTextarea, textareas, document_type) {
	if (document_type == "cartaporte") {
		console.log ("-- Handling blur for cartaporte")
		if (idTextarea == "txt06") {
			textareas ["txt07"].value = textareas ["txt06"].value
			textareas ["txt19"].value = textareas ["txt06"].value
		}
	}
}
