// Enable or disalble buttons from nav bar in document form

function enableDisableDocButtons (enableFlag) {
	if (enableFlag === "ENABLE") {
		document.getElementById("pdf_original_btn").removeAttribute("disabled");
		document.getElementById("pdf_copia_btn").removeAttribute("disabled");
		document.getElementById("pdf_clonar_btn").removeAttribute("disabled");
		document.getElementById("pdf_paquete_btn").removeAttribute("disabled");
	}else {
		document.getElementById("pdf_original_btn").setAttribute("disabled", "disabled");
		document.getElementById("pdf_copia_btn").setAttribute("disabled", "disabled");
		document.getElementById("pdf_clonar_btn").setAttribute("disabled", "disabled");
		document.getElementById("pdf_paquete_btn").setAttribute("disabled", "disabled");
	}
}

