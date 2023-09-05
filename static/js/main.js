const btnDelete = document.querySelectorAll('.btn-delete')
const btnDeleteProduct = document.querySelectorAll('.btn-delete-product')

if(btnDelete){
   const btnArray = Array.from(btnDelete);
   btnArray.forEach((btn) => {
    btn.addEventListener('click', (e) => {
        if (!confirm('Desea eliminar el cliente')){
            e.preventDefault();
        }
    });
   });
}

if(btnDeleteProduct){
   const btnArray = Array.from(btnDeleteProduct);
   btnArray.forEach((btn) => {
    btn.addEventListener('click', (e) => {
        if (!confirm('Desea eliminar el producto?')){
            e.preventDefault();
        }
    });
   });
}




$(document).ready(function() {  // Asegurarse de que el código se ejecute después de que se haya cargado el DOM.
    $('#clienteSeleccionado').change(function() {
        var clienteId = $(this).val();
        if (clienteId) {  // Solo hacer la solicitud si hay un clienteId seleccionado.
            $.get('/get_pedidos/' + clienteId, function(data) {
                $('#pedidos').empty();  // Vaciar el menú desplegable de pedidos antes de llenarlo nuevamente.
                data.forEach(function(pedido) {
                    // Usar id_pedido como valor y fecha_pedido como descripción en el menú desplegable.
                    $('#pedidos').append('<option value="' + pedido.id_pedido + '">' + pedido.fecha_pedido + '</option>');
                });
            });
        }
    });
});

