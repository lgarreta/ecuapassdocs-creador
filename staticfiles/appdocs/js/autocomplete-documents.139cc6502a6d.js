// Functions for autocomplete in document forms

// Create autocomplete for an entity
function createAutocomplete (entity) {
	let inputSelector = entity.inputSelector
	let sourceUrl     = entity.sourceUrl
	
	$(inputSelector).autocomplete({
		source: function (request, response) {
			$.ajax({ url: sourceUrl, dataType: 'json', data: { query: request.term},

				beforeSend: function (xhr, settings) {
					// Include the CSRF token in the request headers
					xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
				},

				success: function (data) {
					responseData = entity.onAjaxSuccess (data)
					response (responseData)
				}
			});
		},
		minLength: 2, 
		select: function (event, ui) {
			entity.onItemSelected (ui)
			// Prevent the default behavior of filling the input with the selected value
			return false;
		}
	});
}

// Return array of selected textAreas according to className
function getTextAreasByClassName (className) {
	let selectedTextAreas = []
	textAreas.forEach (textArea => {
		if (textArea.className.includes (className)) {
			selectedTextAreas.push (textArea)
		}
	});
	return (selectedTextAreas);
}

// Set autocomplete for document according to doc type
// Doc types: "cartaporte", "manifiesto", "declaración
function setAutocompleteForDocument (documentType) {
	if (documentType == "cartaporte") {
		console.log ("-- Autocomplet for cartaporte")
		let empresaInputs = getTextAreasByClassName ("input_empresa")
		empresaInputs.forEach (inputName => {
			createAutocomplete(new AutoCompleteEmpresa (inputName)) 
		});
	}else if (documentType == "manifiesto") {
		console.log ("-- Autocomplet for manifiesto")

		let vehiculoInputs = getTextAreasByClassName ("input_placaPais")
		vehiculoInputs.forEach (inputName => {
			createAutocomplete(new AutoCompletePlacaPais (inputName)) 
		});

		let conductorInputs = getTextAreasByClassName ("input_conductor")
		conductorInputs.forEach (inputName => {
			createAutocomplete(new AutoCompleteConductor (inputName)) 
		});
	}
}

//----------------------------------------------------------------------
//---------------- Autocomplet for "manifiesto" ------------------------
//----------------------------------------------------------------------

// Autocomplete class for Empresa inputs
class AutoCompleteEmpresa {
	constructor (inputSelector) {
		let inputId = "#" + inputSelector
		this.inputSelector = inputSelector;
		this.sourceUrl     = "opciones-empresa/"
		this.fullData = null;
	}

	// When ajax query is succesfull, set items
	onAjaxSuccess (data) {
		this.fullData = data;
		let flatData = [];
		for (let i=0; i < data.length; i++) {
			flatData.push (data[i] ["itemLine"])
		}
		return flatData;
	}

	// When an item is selected, populate the textarea 
	onItemSelected (ui) {
		let index = ui.item.value.split (".")[0]
		let text = this.fullData [index]["itemText"]
		$(this.inputSelector).val (text);
	}
}

//----------------------------------------------------------------------
//---------------- Autocomplet for "manifiesto" ------------------------
//----------------------------------------------------------------------

// Autocomplete class for Vehiculo inputs
class AutoCompletePlacaPais {
	constructor (inputSelector) {
		let inputId        = "#" + inputSelector
		this.inputSelector = inputSelector;
		this.sourceUrl     = "opciones-vehiculo/"
		this.fullData      = null;
	}

	// When ajax query is succesfull, set items
	onAjaxSuccess (data) {
		this.fullData = data;
		let flatData = [];
		for (let i=0; i < data.length; i++) {
			flatData.push (data[i] ["itemLine"])
		}
		return flatData;
	}

	// When an item is selected, populate the textarea 
	onItemSelected (ui) {
		let index = ui.item.value.split (".")[0]
		let text = this.fullData [index]["itemText"]
		let values = text.split ("||");
		let input = this.inputSelector
		if (input.id === "txt06") {
			document.getElementById("txt04").value = values [0]
			document.getElementById("txt05").value = values [1]
			document.getElementById("txt06").value = values [2]
			document.getElementById("txt07").value = values [3]
		}else {
			document.getElementById("txt09").value = values [0]
			document.getElementById("txt10").value = values [1]
			document.getElementById("txt11").value = values [2]
			document.getElementById("txt12").value = values [3]
		}
	}
}

// Autocomplete class for Conductor inputs
class AutoCompleteConductor {
	constructor (inputSelector) {
		let inputId        = "#" + inputSelector
		this.inputSelector = inputSelector;
		this.sourceUrl     = "opciones-conductor/"
		this.fullData      = null;
	}

	// When ajax query is succesfull, set items
	onAjaxSuccess (data) {
		this.fullData = data;
		let flatData = [];
		for (let i=0; i < data.length; i++) {
			flatData.push (data[i] ["itemLine"])
		}
		return flatData;
	}

	// When an item is selected, populate the textarea 
	onItemSelected (ui) {
		let index = ui.item.value.split (".")[0]
		let text = this.fullData [index]["itemText"]
		let values = text.split ("||");
		let input = this.inputSelector
		if (input.id === "txt13") {
			document.getElementById("txt13").value = values [0]
			document.getElementById("txt14").value = values [1]
			document.getElementById("txt15").value = values [2]
			document.getElementById("txt16").value = values [3]
			document.getElementById("txt17").value = values [4]
		}else {
			document.getElementById("txt18").value = values [0]
			document.getElementById("txt19").value = values [1]
			document.getElementById("txt20").value = values [2]
			document.getElementById("txt21").value = values [3]
			document.getElementById("txt22").value = values [4]
		}
	}
}
