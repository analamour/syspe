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


$(document).ready(function() {
    $('#clientes').change(function() {
        var clienteId = $(this).val();
        $.get('/get_pedidos/' + clienteId, function(data) {
            $('#pedidos').empty();
            data.forEach(function(pedido) {
                $('#pedidos').append('<option value="' + pedido.id + '">' + pedido.descripcion + '</option>');
            });
        });
    });
});
