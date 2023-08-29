from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# conección Mysql 
app.config ["MYSQL_HOST"] = 'localhost'
app.config ["MYSQL_USER"] = 'root'
app.config ["MYSQL_PASSWORD"] = '123'
app.config ["MYSQL_DB"] = 'syspe'
mysql = MySQL(app)


#configuracion
app.secret_key = 'mysecretkey'


#MODULO CLIENTES
@app.route("/")
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes')
    data = cur.fetchall()
    return render_template('index.html', contacts = data)
    

@app.route("/altaCliente")
def altaCLiente():
    return render_template('altaCliente.html')


@app.route("/listadoCliente")
def listadoCliente():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes')
    data = cur.fetchall()
    return render_template('listadoCliente.html', clientes = data)

@app.route("/add_cliente", methods=['POST'])
def add_cliente():
    if request.method == 'POST':
        razonsocial = request.form['razonsocial']
        nombrefantsia = request.form['nombrefantsia']
        telefono = request.form['telefono']
        cuit = request.form['cuit']
        direccion = request.form['direccion']
        mail = request.form['mail']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO clientes (razonsocial, nombrefantsia, telefono, cuit, direccion, mail) VALUES (%s, %s, %s, %s, %s,%s )',(razonsocial, nombrefantsia, telefono, cuit, direccion, mail))
        mysql.connection.commit ()
        flash("Cliente agregado")
        return redirect(url_for('altaCLiente'))
        

@app.route('/altaCliente')
def alta_cliente():
    return render_template('altaCliente.html')

@app.route("/edit/<id>")
def get_cliente(id):
    cur = mysql.connection.cursor()
    cur.execute ('SELECT * FROM clientes WHERE id = %s', (id))
    data = cur.fetchall()
    print(data[0])
    return render_template('edit-contact.html', cliente = data[0])


@app.route('/update/<id>', methods = ['POST'])
def update_clientes(id):
    if request.method == 'POST':
        razonsocial = request.form['razonsocial']
        nombrefantsia = request.form['nombrefantsia']
        telefono = request.form['telefono']
        cuit = request.form['cuit']
        direccion = request.form['direccion']
        mail = request.form['mail']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE clientes
            SET razonsocial = %s,
                nombrefantsia =%s,
                telefono =%s,
                cuit =%s,
                direccion =%s,
                mail =%s
            WHERE id =%s

        """,  (razonsocial, nombrefantsia, telefono, cuit, direccion, mail,id))   
        mysql.connection.commit()
        flash('Cliente modificado')
        return redirect(url_for('listadoCliente'))

@app.route("/delete/<string:id>")
def delete_cliente(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM clientes WHERE id =  {0}'.format(id))
    mysql.connection.commit()
    flash('Cliente eliminado')
    return redirect(url_for('listadoCliente'))

#MODULO PRODUCTOS
@app.route("/altaProducto")
def altaProducto():
    return render_template('altaProducto.html')

@app.route("/add_producto", methods=['POST'])
def add_producto():
    if request.method == 'POST':
        producto = request.form['producto']
        detalles = request.form['detalles']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        rubro = request.form['rubro']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO productos (producto, comentario, precio, stockVendido, stockDisponible, rubro) VALUES (%s, %s, %s, %s, %s,%s )',(producto, detalles, precio, 0, cantidad, rubro))
        mysql.connection.commit ()
        flash("Producto agregado")
        return redirect(url_for('altaProducto'))

@app.route("/inventario")
def inventario():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos')
    data = cur.fetchall()
    return render_template('inventario.html', productos = data)

@app.route("/delete_producto/<string:id>")
def delete_producto(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM productos WHERE id =  {0}'.format(id))
    mysql.connection.commit()
    flash('Producto eliminado')
    return redirect(url_for('inventario'))

@app.route("/edit_producto/<id>")
def get_producto(id):
    cur = mysql.connection.cursor()
    cur.execute ('SELECT * FROM productos WHERE id = %s', (id))
    data = cur.fetchall()
    print(data[0])
    return render_template('edit-product.html', productos = data[0])

@app.route('/update_producto/<id>', methods = ['POST'])
def update_producto(id):
    if request.method == 'POST':
        producto = request.form['producto']
        comentario = request.form['comentario']
        precio = request.form['precio']
        disponible = request.form['stockDisponible']
        vendido = request.form['stockVendido']
        rubro = request.form['rubro']
        precio = request.form ['precio']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE productos
            SET producto = %s,
                comentario = %s,
                precio = %s,
                stockDisponible = %s,
                stockVendido = %s,
                rubro = %s,
                precio =%s
            WHERE id = %s
        """,  (producto, comentario, precio, disponible, vendido, rubro, id))   
  
        mysql.connection.commit()
        flash('Producto modificado')
        return redirect(url_for('inventario'))

@app.route("/cargarventa")
def cargarventa():
    cur = mysql.connection.cursor()
    
    cur.execute('SELECT id, razonsocial FROM clientes')  # Obteniendo clientes
    clientes_data = cur.fetchall()

    cur.execute('SELECT id, producto FROM productos where stockDisponible > 0')
    productos_data = cur.fetchall()

    return render_template('cargarventa.html', productos=productos_data, clientes=clientes_data)


@app.route('/restar_stock_vendido', methods=['POST'])
def restar_stock_vendido():
    if request.method == 'POST':
        cliente_id = request.form.get('clienteSeleccionado')
        producto_seleccionado = request.form.get('codigoProducto')  
        cantVentaForm = request.form.get('cantidadVendido')
        codigoProducto = request.form.get('codigoProducto')

        if not all([cliente_id, producto_seleccionado, cantVentaForm, codigoProducto]):
            flash('Faltan datos en el formulario.')
            return redirect(url_for('cargarventa'))

        cur = mysql.connection.cursor()
        cur.execute("select stockDisponible from productos where id=%s", (codigoProducto,))
        cantidadDisponibleActualTupla = cur.fetchall()
        cantidadDisponibleActual = int(cantidadDisponibleActualTupla[0][0])
        cantidadVendidaForm = int(cantVentaForm)

        if cantidadVendidaForm > cantidadDisponibleActual:
            flash(f'La cantidad ingresada supera al stock disponible')
        else:
            disponible = cantidadDisponibleActual - cantidadVendidaForm
            cur.execute("select stockVendido from productos where id=%s", (codigoProducto,))
            cantidadVendidaActual = cur.fetchall()
            vendido = int(cantidadVendidaActual[0][0]) + int(cantVentaForm)
            cur.execute("""
                UPDATE productos
                SET stockDisponible =%s,
                stockVendido = %s
                WHERE id =%s;
            """, (disponible, vendido, codigoProducto))
            mysql.connection.commit()
            flash('Stock actualizado')

        return redirect(url_for('inventario'))


@app.route("/cargarstock")
def cargarstock():
    cur = mysql.connection.cursor()
    cur.execute ('SELECT id, producto FROM productos')
    data = cur.fetchall()
    return render_template('cargarstock.html', productos = data)

@app.route('/agregar_stock_ingresado', methods = ['POST'])
def agregar_stock_ingresado():
    if request.method == 'POST':
        codigoProducto = request.form['codigoProducto']
        #print("EL CODIGO PRODUCTO ES ",codigoProducto)
        cantIngresoForm = request.form['cantidadIngreso']
        cur = mysql.connection.cursor()
        cur.execute(f"select stockDisponible from productos where id={codigoProducto}")
        cantidadDisponibleActual = cur.fetchall()
        disponible = int(cantidadDisponibleActual[0][0]) + int(cantIngresoForm)
        disponible = str(disponible)
        cur.execute("""
            UPDATE productos
            SET stockDisponible =%s
            WHERE id =%s;
        """,  (disponible, codigoProducto))   
        mysql.connection.commit()
        flash(f'Stock actualizado')
        return redirect(url_for('inventario'))



@app.route('/clienteSeleccionado', methods=['GET', 'POST'])
def clienteSeleccionado():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre FROM clientes")
    clientes = cur.fetchall()
    cur.close()
    return render_template('listadoCliente.html', clientes=clientes)

@app.route("/seleccionarpoducto")
def seleccionarproducto():
    cur = mysql.connection.cursor()
    # Obtener lista de productos
    cur.execute('SELECT id, nombre_producto FROM productos')
    productos = cur.fetchall()
    return render_template('inventario.html', productos=productos)



@app.route('/crear_pedido', methods=['POST'])
def crear_pedido():
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        productos_id = request.form.getlist('producto_id[]')
        cantidades = request.form.getlist('cantidad[]')

        cur = mysql.connection.cursor()

        # Crear el pedido primero
        cur.execute('INSERT INTO Pedidos (cliente_id, fecha_pedido) VALUES (%s, NOW())', (cliente_id,))
        pedido_id = cur.lastrowid  # ID del pedido creado

        # Insertar cada producto en DetallesPedido
        for producto_id, cantidad in zip(productos_id, cantidades):
            cur.execute('INSERT INTO DetallesPedido (pedido_id, producto_id, cantidad) VALUES (%s, %s, %s)', (pedido_id, producto_id, cantidad))

        mysql.connection.commit()
        cur.close()

        flash('Pedido creado con éxito!')
        return redirect(url_for('Index'))  

@app.route("/consultarPedido")
def consultarPedido():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM detallesPedido')
    data = cur.fetchall()
    return render_template('consultarPedido.html', pedidos = data) 


  
if __name__ == '__main__':
    app.run(port = 3000, debug = True)