function containsOnlyNumbers(cadena){
    return /^\d+$/.test(cadena)
}

function validarCuit() {
    cuit = document.getElementById("cuit").value
    if (cuit.length === 11 && containsOnlyNumbers(cuit)===true) {
        console.log("Cuit correcto")
    } else {
        console.log("Cuit invalido")
        document.getElementById("cuit").value=""
        let element = document.createElement('label')
        let texto = document.createTextNode('Cuit invalido')
        element.appendChild(texto)
        document.getElementById("cuitAlert").appendChild(element)
    }
}

function limpiarAlertaCuit(){
    alertaLabel = document.getElementById("cuitAlert");
    alertaLabel.removeChild(alertaLabel.firstElementChild);
}