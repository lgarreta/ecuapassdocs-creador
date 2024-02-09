function createTextareaInputs (inputParameters) {
	inputParameters.forEach (function (input) {
		console.log (input)
	}
}

//
//function createTextarea(id, className) {
//    var textarea = document.createElement("textarea");
//    textarea.setAttribute("name", id);
//    textarea.setAttribute("id", id);
//    textarea.setAttribute("class", className);
//    return textarea;
//}
//
//// IDs and classes for textareas
//var textareaData = [
//    { id: "txt02", class: "input_permiso" },
//    { id: "txt03", class: "input_permiso" },
//    { id: "txt04", class: "input_general" },
//    { id: "txt05", class: "input_fecha" },
//    { id: "txt06", class: "input_placaPais" },
//    { id: "txt07", class: "input_general" }
//];
//
//// Get the container to append textareas
//var container = document.getElementById("textareasContainer");
//
//// Loop through textareaData and create textareas
//textareaData.forEach(function(data) {
//    var textarea = createTextarea(data.id, data.class);
//    container.appendChild(textarea);
//});
//
