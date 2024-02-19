// Functions for autocomplete in cartaporte documents


// Create autocomplete for an entity
function createAutocomplete (entity) {
	inputSelector = entity.inputSelector
	sourceUrl     = entity.sourceUrl
	
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

function setAutocompleteForDocument (documentType) {
	if (documentType == "cartaporte") {
		empresaInputs = getTextAreasByClassName ("input_empresa")
		empresaInputs.forEach (inputName => {
			createAutocomplete(new AutoCompleteEmpresa (inputName)) 
		});
	}
}
