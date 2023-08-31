from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de MySQL 
app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"] = '123'
app.config["MYSQL_DB"] = 'syspe'
mysql = MySQL(app)

# Configuración
app.secret_key = 'mysecretkey'

# MODULO CLIENTES
@app.route("/")
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes')
    data = cur.fetchall()
    return render_template('index.html', contacts=data)

@app.route("/altaCliente")
def altaCliente():
    return render_template('altaCliente.html')

@app.route("/listadoCliente")
def listadoCliente():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes')
    data = cur.fetchall()
    return render_template('listadoCliente.html', clientes=data)

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
        cur.execute('INSERT INTO clientes (razonsocial, nombrefantsia, telefono, cuit, direccion, mail) VALUES (%s, %s, %s, %s, %s,%s )', (razonsocial, nombrefantsia, telefono, cuit, direccion, mail))
        mysql.connection.commit()
        flash("Cliente agregado")
        return redirect(url_for('altaCliente'))

@app.route("/edit/<id>")
def get_cliente(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes WHERE id_cliente = %s', (id,))
    data = cur.fetchall()
    return render_template('edit-contact.html', cliente=data[0])

@app.route('/update/<id>', methods=['POST'])
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
        nombrefantsia = %s,
        telefono = %s,
        cuit = %s,
        direccion = %s,
        mail = %s
    WHERE id_cliente = %s
    """, (razonsocial, nombrefantsia, telefono, cuit, direccion, mail, id))
        mysql.connection.commit()
        flash('Cliente modificado')
        return redirect(url_for('listadoCliente'))

@app.route("/delete/<string:id>")
def delete_cliente(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM clientes WHERE id_cliente = %s', (id,))
    mysql.connection.commit()
    flash('Cliente eliminado')
    return redirect(url_for('listadoCliente'))

# MODULO ARTICULOS
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
        cur.execute('INSERT INTO articulo (producto, comentario, precio, stockVendido, stockDisponible, rubro) VALUES (%s, %s, %s, %s, %s, %s)', (producto, detalles, precio, 0, cantidad, rubro))
        mysql.connection.commit()
        flash("articulo agregado")
        return redirect(url_for('altaProducto'))

@app.route("/inventario")
def inventario():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM articulo')
    data = cur.fetchall()
    return render_template('inventario.html', articulo=data)

@app.route("/delete_articulo/<string:id_articulo>")
def delete_articulo(id_articulo):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM articulo WHERE id_articulo = %s', (int(id_articulo),))
    mysql.connection.commit()
    flash('articulo eliminado')
    return redirect(url_for('inventario'))

@app.route("/edit_articulo/<id_articulo>")
def get_articulo(id_articulo):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM articulo WHERE id_articulo = %s', (int(id_articulo),))
    data = cur.fetchall()
    return render_template('edit-product.html', articulo=data[0])

@app.route('/update_articulo/<id_articulo>', methods = ['POST'])
def update_articulo(id_articulo):
    if request.method == 'POST':
        producto = request.form['producto']
        comentario = request.form['comentario']
        precio = request.form['precio']
        stockDisponible = request.form['stockDisponible']
        stockVendido = request.form['stockVendido']
        rubro = request.form['rubro']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE articulo
            SET producto = %s,
                comentario = %s,
                precio = %s,
                stockDisponible = %s,
                stockVendido = %s,
                rubro = %s
            WHERE id_articulo = %s
        """,  (producto, comentario, precio, stockDisponible, stockVendido, rubro, id_articulo))   
  
        mysql.connection.commit()
        flash('articulo modificado')
        return redirect(url_for('inventario'))


#MODULO VENTAS

@app.route("/cargarventa")
def cargarventa():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id_cliente, razonsocial FROM clientes')  # Obteniendo clientes
    clientes_data = cur.fetchall()
    cur.execute('SELECT id_articulo, producto FROM articulo WHERE stockDisponible > 0')
    articulo_data = cur.fetchall()
    return render_template('cargarventa.html', articulo=articulo_data, clientes=clientes_data)

@app.route("/cargarstock")
def cargarstock():
    cur = mysql.connection.cursor()
    cur.execute ('SELECT id_articulo, producto FROM articulo')
    data = cur.fetchall()
    return render_template('cargarstock.html', articulo = data)


@app.route('/restar_stock_vendido', methods=['POST'])
def restar_stock_vendido():
    if request.method == 'POST':
        cliente_id = request.form.get('clienteSeleccionado')
        cantVentaForm = request.form.get('cantidadVendido')
        codigoarticulo = request.form.get('codigoarticulo')
        if not all([cliente_id, cantVentaForm, codigoarticulo]):
            flash('Faltan datos en el formulario.')
            return redirect(url_for('cargarventa'))
        cur = mysql.connection.cursor()
        cur.execute("SELECT stockDisponible, stockVendido FROM articulo WHERE id=%s", (codigoarticulo,))
        cantidadDisponibleActual, cantidadVendidaActual = cur.fetchone()
        cantidadVendidaForm = int(cantVentaForm)
        if cantidadVendidaForm > cantidadDisponibleActual:
            flash(f'La cantidad ingresada supera al stock disponible')
        else:
            disponible = cantidadDisponibleActual - cantidadVendidaForm
            vendido = cantidadVendidaActual + cantidadVendidaForm
            cur.execute("""
                UPDATE articulo
                SET stockDisponible =%s,
                stockVendido = %s
                WHERE id =%s;
            """, (disponible, vendido, codigoarticulo))
            mysql.connection.commit()
            flash('Stock actualizado')
        return redirect(url_for('inventario'))

@app.route("/consultarPedido")
def consultarPedido():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM detallesPedido')
    data = cur.fetchall()
    return render_template('consultarPedido.html', pedidos = data)

@app.route("/edit_pedido/<id>")
def edit_pedido(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Pedidos WHERE id = %s', (id,))
    pedido_data = cur.fetchall()
    cur.execute('SELECT * FROM DetallesPedido WHERE pedido_id = %s', (id,))
    detalles_pedido = cur.fetchall()
    return render_template('edit_pedido.html', pedido=pedido_data[0])

@app.route('/update_pedido/<id>', methods=['POST'])
def update_pedido(id):
    if request.method == 'POST':
        id_cliente = request.form['id_cliente']
        # Captura otros datos del formulario si los agregas, como fecha, etc.
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE Pedidos
            SET id_cliente = %s
            WHERE id = %s
        """, (id_cliente, id))
        mysql.connection.commit()
        flash('Pedido actualizado correctamente!')
        return redirect(url_for('consultarPedido'))

@app.route('/agregar_stock_ingresado', methods=['POST'])
def agregar_stock_ingresado():
    if request.method == 'POST':
        codigoarticulo = request.form['codigoarticulo']
        print("EL CODIGO articulo ES ",codigoarticulo)
        cantIngresoForm = request.form['cantidad']
        cur = mysql.connection.cursor()
        cur.execute(f"select stockDisponible from articulo where id_articulo={codigoarticulo}")
        cantidadDisponibleActual = cur.fetchall()
        disponible = int(cantidadDisponibleActual[0][0]) + int(cantIngresoForm)
        cur.execute("""
            UPDATE articulo
            SET stockDisponible = %s
            WHERE id_articulo = %s;
        """, (disponible, codigoarticulo))
        mysql.connection.commit()
        flash('Stock actualizado')
        return redirect(url_for('inventario'))

        

if __name__ == '__main__':
    app.run(port=3000, debug=True)
