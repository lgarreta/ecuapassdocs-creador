// Functions for autocomplete in document forms

// Create autocomplete for an entity
function createAutocomplete (entity) {
	let inputSelector = entity.inputSelector
	let sourceUrl     = entity.sourceUrl
	
	$(inputSelector).autocomplete({
		// List of autocomplete options
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
		position: { my: "left top", at: "center top", collision: "none" }, // Customize the position
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
		// Empresas
		let empresaInputs = getTextAreasByClassName ("input_empresa")
		empresaInputs.forEach (inputName => {
			createAutocomplete(new AutoComplete (inputName, 'opciones-empresa')) 
		});
	
		let lugarInputs = getTextAreasByClassName ("input_lugar")
		lugarInputs.forEach (inputName => {
			createAutocomplete(new AutoComplete (inputName, 'opciones-lugar' )) 
		});
	}else if (documentType == "manifiesto") {
		console.log ("-- Autocomplet for manifiesto")

		let cartaporteInput = document.getElementById("txt28")    // field cartaporte   
		createAutocomplete(new AutoCompleteCartaporte (cartaporteInput, "opciones-cartaporte")) 

		let vehiculoInputs = getTextAreasByClassName ("input_placaPais")
		vehiculoInputs.forEach (inputName => {
			createAutocomplete(new AutoCompletePlacaPais (inputName, 'opciones-vehiculo')) 
		});

		let conductorInputs = getTextAreasByClassName ("input_conductor")
		conductorInputs.forEach (inputName => {
			createAutocomplete(new AutoCompleteConductor (inputName, 'opciones-conductor')) 
		});
	}
}

//----------------------------------------------------------------------
//---------------- Autocomplet for "cartaporte" ------------------------
//----------------------------------------------------------------------
class AutoComplete {
	// Init with input element and source URL
	constructor (inputSelector, sourceUrl) {
		console.log ("-- on constructor --");
		let inputId = "#" + inputSelector
		this.inputSelector = inputSelector;
		this.sourceUrl     = sourceUrl;
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

//-- Autocomplet for "cartaporte" ------------------------
class AutoCompleteCartaporte extends AutoComplete {
	// When an item is selected, populate the textarea 
	onItemSelected (ui) {
		let index = ui.item.value.split (".")[0]
		let text = this.fullData [index]["itemText"]
		let values = text.split ("||");
		
		document.getElementById("txt28").value   = values [0]  // Cartaporte
		document.getElementById("txt29").value   = values [1]  // Descripcion
		document.getElementById("txt30").value   = values [2]  // Cantidad
		document.getElementById("txt31").value   = values [3]  // Marca
		document.getElementById("txt32_1").value = values [4]  // Peso bruto
		document.getElementById("txt32_3").value = values [5]  // Peso neto
		document.getElementById("txt33_1").value = values [6]  // Otra medida
		document.getElementById("txt34").value   = values [7]  // INCONTERMS
		document.getElementById("txt32_2").value = values [8]  // Peso bruto total. NO CALCULADO
		document.getElementById("txt32_4").value = values [9]  // Peso neto total. NO CALCULADO
		document.getElementById("txt33_2").value = values [10] // Otra medida total. NO CALCULADO
	}
}

//-- AutoComplete for Vehiculo inputs
class AutoCompletePlacaPais extends AutoComplete {
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

//-- Autocomplete Conductor inputs
class AutoCompleteConductor extends AutoComplete {
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
