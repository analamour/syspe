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