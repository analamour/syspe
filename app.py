from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
from MySQLdb import IntegrityError
from decimal import Decimal


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
    try:
        cur.execute('DELETE FROM clientes WHERE id_cliente = %s', (id,))
        mysql.connection.commit()
        flash('Cliente eliminado')
    except IntegrityError:
        mysql.connection.rollback()  
        flash('No se puede eliminar el cliente ya que posee pedidos realizados')
    finally:
        cur.close()  
    return redirect(url_for('listadoCliente'))

@app.route('/buscar_cliente', methods=['GET'])
def buscar_cliente():
    razon_social = request.args.get('razon_social', default="", type=str)
    cur = mysql.connection.cursor()

    cur.execute('''
        SELECT 
            id_cliente, 
            razonsocial
        FROM 
            clientes
        WHERE 
            razonsocial LIKE %s
    ''',('%' + razon_social + '%',))


    clientes = cur.fetchall()
    return render_template('listadoCliente.html', clientes=clientes)

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
    cur.execute('''
        SELECT 
            a.id_articulo, a.producto, a.detalle, a.precio, a.stockDisponible, 
            IFNULL(SUM(d.cantidad), 0) as stockVendido, a.rubro,
            (a.stockDisponible - IFNULL(SUM(d.cantidad), 0)) as stockActual
    FROM articulo a
    LEFT JOIN detallesPedido d ON a.id_articulo = d.id_articulo
    GROUP BY a.id_articulo, a.producto, a.detalle, a.precio, a.stockDisponible, a.rubro;
    ''')
    data = cur.fetchall()
    return render_template('inventario.html', articulo=data)



@app.route("/delete_articulo/<string:id_articulo>")
def delete_articulo(id_articulo):
    cur = mysql.connection.cursor()
    try:
        cur.execute('DELETE FROM articulo WHERE id_articulo = %s', (int(id_articulo),))
        mysql.connection.commit()
        flash('Artículo eliminado')
    except IntegrityError:
        mysql.connection.rollback()  # Revertir cualquier cambio si ocurre un error
        flash('No se puede eliminar el artículo ya que está siendo utilizado o referenciado en otro lugar.')
    finally:
        cur.close()  # Cerrar el cursor
    return redirect(url_for('inventario'))


@app.route("/edit_articulo/<id_articulo>")
def get_articulo(id_articulo):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM articulo WHERE id_articulo = %s', (int(id_articulo),))
    data = cur.fetchall()
    return render_template('edit-articulo.html', articulo=data[0])

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


@app.route("/cargarventa", methods=["GET", "POST"])
def cargarventa():
    cur = mysql.connection.cursor()

    if request.method == "POST":
        producto_ids = request.form.getlist('producto_id[]')
        cantidades = request.form.getlist('cantidad[]')

        total_venta = 0
        for producto_id, cantidad in zip(producto_ids, cantidades):
            cur.execute("SELECT precio FROM articulo WHERE id_articulo=%s", (producto_id,))
            precio = cur.fetchone()[0]
            total_venta += precio * int(cantidad)

        # Aquí, después de calcular el total, guardarías la venta en la base de datos.
        # ... código para guardar en BD ...

        # Luego, mostrar una confirmación al usuario
        return render_template('confirmacion.html', total=total_venta)

    else:  # Si es GET
        cur.execute('SELECT id_cliente, razonsocial FROM clientes')  # Obteniendo clientes
        clientes_data = cur.fetchall()
        cur.execute('SELECT id_articulo, producto, precio FROM articulo WHERE stockDisponible > 0')
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
        cur.execute("SELECT stockDisponible, stockVendido FROM articulo WHERE id_articulo=%s", (codigoarticulo,))
        cantidadDisponibleActual, cantidadVendidaActual = cur.fetchone()
        print("Stock Disponible actual:", cantidadDisponibleActual)
        print("Stock Vendido actual:", cantidadVendidaActual)

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
                WHERE id_articulo =%s;
            """, (disponible, vendido, codigoarticulo))
            
            mysql.connection.commit()
            flash('Stock actualizado')
        return redirect(url_for('inventario'))
    
@app.route("/consultarPedido")
def consultarPedido():
    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT 
            p.id_pedido, 
            p.fecha_pedido,
            p.precio_final,
            c.razonsocial,
            d.cantidad,
            d.subtotal,
            a.producto,
            p.id_cliente
         FROM 
            pedidos p
        JOIN 
            Clientes c ON p.id_cliente = c.id_cliente
        LEFT JOIN 
            detallesPedido d ON p.id_pedido = d.id_pedido
        LEFT JOIN 
            articulo a ON d.id_articulo = a.id_articulo
        ORDER BY 
            p.fecha_pedido DESC;        
    ''')
    data = cur.fetchall()
    print(data)
    return render_template('consultarPedido.html', pedidos=data)


@app.route("/edit_pedido/<id>")
def edit_pedido(id):
    cur = mysql.connection.cursor()
    
    # Obtener datos del pedido basado en el ID
    cur.execute('SELECT * FROM pedidos WHERE id_pedido = %s', (id,))
    pedido_data = cur.fetchone()
    
    # Obtener todos los clientes
    cur.execute('SELECT id_cliente, razonsocial FROM Clientes')
    clientes = cur.fetchall()
    
    return render_template('edit-pedido.html', pedido=pedido_data, clientes=clientes)


@app.route("/delete_pedido/<id>")
def delete_pedido(id):
    cur = mysql.connection.cursor()
    try:
        # Primero eliminar detalles
        cur.execute('DELETE FROM detallespedido WHERE id_pedido = %s', (id,))
        # Luego eliminar el pedido
        cur.execute('DELETE FROM pedidos WHERE id_pedido = %s', (id,))
        mysql.connection.commit()
        flash('Pedido eliminado correctamente!')
    except Exception as e:
        mysql.connection.rollback()
        flash('Error al eliminar el pedido: ' + str(e))
    return redirect(url_for('consultarPedido'))


@app.route('/update_pedido/<id>', methods=['POST'])
def update_pedido(id):
    if request.method == 'POST':
        id_cliente = request.form['clienteSeleccionado']  # O el nombre del campo que corresponda
        
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE pedidos
            SET id_cliente = %s
            WHERE id_pedido = %s
        """, (id_cliente, id))
        
        mysql.connection.commit()
        flash('pedido actualizado correctamente!')
        return redirect(url_for('consultarPedido'))



@app.route("/detalle_pedido/<id_pedido>")
def detalle_pedido(id_pedido):
    cur = mysql.connection.cursor()

    # Obtener detalles del pedido basado en el ID
    cur.execute('''
        SELECT 
            p.id_pedido, 
            p.fecha_pedido,
            p.precio_final,
            c.razonsocial,
            d.cantidad,
            d.subtotal,
            a.producto,
            a.precio
        FROM 
            pedidos p
        JOIN 
            Clientes c ON p.id_cliente = c.id_cliente
        JOIN 
            detallesPedido d ON p.id_pedido = d.id_pedido
        JOIN 
            articulo a ON d.id_articulo = a.id_articulo
        WHERE 
            p.id_pedido = %s;
    ''', (id_pedido,))
    
    detalles = cur.fetchall()
    
    #  para calcular el total
    total = sum([detalle[5] for detalle in detalles])
    # Pasa el total a la plantilla
    return render_template('detalle-pedido.html', detalles=detalles, total=total)

@app.route('/buscar', methods=['GET'])
def buscar_pedidos():
    nombre_cliente = request.args.get('nombre_cliente', default="", type=str)
    id_pedido = request.args.get('id_pedido', default="", type=str)
    cur = mysql.connection.cursor()

    # Consulta SQL
    cur.execute('''
        SELECT 
            p.id_pedido, 
            p.fecha_pedido, 
            c.razonsocial
        FROM 
            pedidos p
        JOIN 
            Clientes c ON p.id_cliente = c.id_cliente
        WHERE 
            c.razonsocial LIKE %s AND p.id_pedido LIKE %s
    ''', ('%' + nombre_cliente + '%', '%' + id_pedido + '%',))

    pedidos = cur.fetchall()
    return render_template('consultarPedido.html', pedidos=pedidos)




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

@app.route('/get_pedidos/<int:id_cliente>')
def get_pedidos(id_cliente):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM pedido WHERE id_cliente = %s', [id_cliente])
    pedidos = cur.fetchall()
    return jsonify(pedidos)

@app.route('/crear_pedido', methods=['POST'])
def crear_pedido():
    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        producto_ids = request.form.getlist('producto_id[]')
        cantidades = request.form.getlist('cantidad[]')

        # Validaciones básicas
        if not cliente_id or not producto_ids or not cantidades:
            flash('Faltan datos en el formulario.')
            return redirect(url_for('cargarventa'))

        if len(producto_ids) != len(cantidades):
            flash('La cantidad de productos y cantidades no coincide.')
            return redirect(url_for('cargarventa'))

        try:
            cur = mysql.connection.cursor()

            # Crear un nuevo pedido (sin precio_unitario)
            cur.execute("""
                INSERT INTO pedidos (fecha_pedido, precio_final, id_cliente) 
                VALUES (NOW(), 0, %s);
            """, (cliente_id,))
            
            pedido_id = cur.lastrowid  # Obtener el ID del último registro insertado
            
            total_pedido = 0
            for producto_id, cantidad in zip(producto_ids, cantidades):
                cur.execute("SELECT precio FROM articulo WHERE id_articulo=%s", (producto_id,))
                precio_unitario = cur.fetchone()[0]
                subtotal = precio_unitario * Decimal(cantidad)
                total_pedido += subtotal
                
                # Insertar en detallesPedido
                cur.execute("""
                    INSERT INTO detallesPedido (id_pedido, id_articulo, cantidad, subtotal) 
                    VALUES (%s, %s, %s, %s);
                """, (pedido_id, producto_id, cantidad, subtotal))
                
            # Actualizar el precio total del pedido
            cur.execute("""
                UPDATE pedidos 
                SET precio_final = %s 
                WHERE id_pedido = %s;
            """, (total_pedido, pedido_id))
            
            # Reducir el stock del artículo
            cur.execute("""
                UPDATE articulo 
                SET stockDisponible = stockDisponible - %s 
                WHERE id_articulo = %s;
            """, (cantidad, producto_id))

            mysql.connection.commit()
            flash('Pedido creado con éxito.')
            
        except Exception as e:
            # Aquí se maneja la excepción, en caso de que algo falle.
            mysql.connection.rollback()  # Deshacer los cambios en caso de un error
            flash('Hubo un error al crear el pedido: ' + str(e))

        return redirect(url_for('consultarPedido'))
      

if __name__ == '__main__':
    app.run(port=3000, debug=True)
