from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from MySQLdb import IntegrityError
from decimal import Decimal
from werkzeug.security import generate_password_hash

#Models
from models.ModelUser import ModelUser

#Entities
from models.entities.User import User


app = Flask(__name__)

# Configuración de MySQL 
app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"] = '1234'
app.config["MYSQL_DB"] = 'syspe'
mysql = MySQL(app)

login_manager_app=LoginManager(app)

# Metodo que nos permite obtener los datos del usuario con la sesion iniciada
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(mysql,id)

# Configuración
app.secret_key = 'mysecretkey'

#Modulo LOGIN
@app.route("/")
def welcome():
    if login_user(current_user):
        return redirect(url_for('Index'))
    else:
        return render_template('welcome.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        #print(username)
        #print(password)
        user=User(0, username, password)
        logged_user=ModelUser.login(mysql,user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                print(login_user((current_user)))
                return redirect(url_for('Index'))
            else:
                flash('Invalid password')
                return(render_template('login.html'))
        else:
            flash('User not found')
            return(render_template('login.html'))
    else:
        return(render_template('login.html'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('welcome'))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        direccion = request.form['domicilio']
        cuit = request.form['cuit']
        username= request.form['email']
        password= generate_password_hash(request.form['password'])
        cur = mysql.connection.cursor()
        cur.execute(f'SELECT * FROM usuarios WHERE  username = "{username}"')
        dataMail = cur.fetchone()
        cur.execute(f'SELECT * FROM usuarios WHERE cuit = "{cuit}"')
        dataCuit = cur.fetchone()
        if dataMail != None:
            flash("Direccion de email ya registrada. Debera iniciar sesion para acceder.")
            return render_template('registro.html')
        elif dataCuit != None:
            flash("CUIT ya registrado. Debera iniciar sesion para acceder.")
            return render_template('registro.html')
        else:
            cur.execute(f'INSERT INTO usuarios (username, fullname, password, cuit, direccion) VALUES ("{username}","{nombre} {apellido}","{password}","{cuit}","{direccion}")')
            mysql.connection.commit()
            flash("Nuevo usuario registrado. Inicie sesion para continuar.")
            return redirect(url_for('login'))
    else:
        return render_template('registro.html')

# MODULO CLIENTES
@app.route("/home")
@login_required
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes')
    data = cur.fetchall()
    return render_template('index.html', contacts=data)

@app.route("/altaCliente")
@login_required
def altaCliente():
    return render_template('altaCliente.html')

@app.route("/listadoCliente")
@login_required
def listadoCliente():
    cur = mysql.connection.cursor()
    
    # Consulta para clientes activos
    cur.execute('SELECT * FROM clientes WHERE estado = "activo"')
    clientes_activos = cur.fetchall()
    
    # Consulta para clientes inactivos
    cur.execute('SELECT * FROM clientes WHERE estado = "inactivo"')
    clientes_inactivos = cur.fetchall()
    
    return render_template('listadoCliente.html', activos=clientes_activos, inactivos=clientes_inactivos)


@app.route("/inactivar_cliente/<id>")
@login_required
def inactivar_cliente(id):
    cur = mysql.connection.cursor()
    cur.execute('UPDATE clientes SET estado="inactivo" WHERE id_cliente = %s', (id,))
    mysql.connection.commit()
    flash('Cliente marcado como inactivo')
    return redirect(url_for('listadoCliente'))

@app.route("/activar_cliente/<string:id>")
@login_required
def activar_cliente(id):
    cur = mysql.connection.cursor()
    cur.execute('UPDATE clientes SET estado="activo" WHERE id_cliente = %s', (id,))
    mysql.connection.commit()
    flash('Cliente activado con éxito')
    return redirect(url_for('listadoCliente'))


@app.route("/add_cliente", methods=['POST'])
@login_required
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
@login_required
def get_cliente(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes WHERE id_cliente = %s', (id,))
    data = cur.fetchall()
    return render_template('edit-contact.html', cliente=data[0])

@app.route('/update/<id>', methods=['POST'])
@login_required
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
@login_required
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
@login_required
def buscar_cliente():
    razon_social = request.args.get('razon_social', default="", type=str)
    cur = mysql.connection.cursor()

    cur.execute('''
        SELECT 
            id_cliente, 
            razonsocial,
            nombrefantsia,
            telefono,
            cuit,
            direccion,
            mail
        FROM 
            clientes
        WHERE 
            razonsocial LIKE %s
    ''',('%' + razon_social + '%',))


    clientes = cur.fetchall()
    return render_template('listadoCliente.html', clientes=clientes)

# MODULO ARTICULOS
@app.route("/altaProducto")
@login_required
def altaProducto():
    return render_template('altaProducto.html')

@app.route("/add_producto", methods=['POST'])
@login_required
def add_producto():
    if request.method == 'POST':
        producto = request.form['producto']
        detalle = request.form['detalle']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        estado = "activo" 
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO articulo (producto, detalle, precio, stockVendido, stockDisponible, estado) VALUES (%s, %s, %s, %s, %s, %s)', (producto, detalle, precio, 0, cantidad, estado))
        mysql.connection.commit()
        flash("articulo agregado")
        return redirect(url_for('altaProducto'))
    
@app.route("/inventario")
@login_required
def inventario():
    cur = mysql.connection.cursor()
    
    # Consulta para productos activos
    cur.execute('SELECT * FROM articulo WHERE estado = "activo"')
    productos_activos = cur.fetchall()
    
    # Consulta para productos inactivos
    cur.execute('SELECT * FROM articulo WHERE estado = "inactivo"')
    productos_inactivos = cur.fetchall()
    
    return render_template('inventario.html', activos=productos_activos, inactivos=productos_inactivos)


@app.route("/buscar_producto", methods=["GET"])
@login_required
def buscar_producto():
    producto = request.args.get('producto')
    
    cur = mysql.connection.cursor()
    query = '''
        SELECT 
            a.id_articulo, a.producto, a.detalle, a.precio, a.stockDisponible, 
            IFNULL(SUM(d.cantidad), 0) as stockVendido, 
            (a.stockDisponible - IFNULL(SUM(d.cantidad), 0)) as stockActual
        FROM articulo a
        LEFT JOIN detallesPedido d ON a.id_articulo = d.id_articulo
        WHERE a.producto LIKE %s
        GROUP BY a.id_articulo, a.producto, a.detalle, a.precio, a.stockDisponible;
    '''
    cur.execute(query, ('%' + producto + '%',))
    
    productos_buscados = cur.fetchall()
    productos_activos = [prod for prod in productos_buscados if prod[7] == "activo"]
    productos_inactivos = [prod for prod in productos_buscados if prod[7] == "inactivo"]
    
    return render_template('inventario.html', activos=productos_activos, inactivos=productos_inactivos)


@app.route("/delete_articulo/<string:id_articulo>")
@login_required
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
        cur.close()  
    return redirect(url_for('inventario'))


@app.route("/edit_articulo/<id_articulo>")
@login_required
def get_articulo(id_articulo):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM articulo WHERE id_articulo = %s', (int(id_articulo),))
    data = cur.fetchall()
    return render_template('edit-articulo.html', articulo=data[0])

@app.route("/update_articulo/<id_articulo>", methods=['POST'])
@login_required
def update_articulo(id_articulo):
    detalle = request.form['detalle']
    precio = request.form['precio']
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE articulo
        SET detalle = %s,
        precio = %s
        WHERE id_articulo = %s;
    """, (detalle, precio, id_articulo))
    mysql.connection.commit()
    flash('Artículo actualizado exitosamente')
    return redirect(url_for('inventario'))

@app.route("/listadoProducto")
@login_required
def listadoProducto():
    cur = mysql.connection.cursor()
    
    # Consulta para productos activos
    cur.execute('SELECT * FROM articulo WHERE estado = "activo"')
    productos_activos = cur.fetchall()
    
    # Consulta para productos inactivos
    cur.execute('SELECT * FROM articulo WHERE estado = "inactivo"')
    productos_inactivos = cur.fetchall()
    
    return render_template('inventario.html', activos=productos_activos, inactivos=productos_inactivos)

@app.route('/inactivar_articulo/<id_articulo>')
@login_required
def inactivar_articulo(id_articulo):
    try:
        cur = mysql.connection.cursor()
        cur.execute('UPDATE articulo SET estado="historico" WHERE id_articulo = %s', (id_articulo,))
        mysql.connection.commit()
        flash('Artículo enviado a histórico con éxito', 'success')
    except:
        flash('Hubo un error al enviar el artículo a histórico', 'danger')
    return redirect(url_for('listadoProducto'))

@app.route('/activar_articulo/<id_articulo>')
@login_required
def activar_articulo(id_articulo):
    try:
        cur = mysql.connection.cursor()
        cur.execute('UPDATE articulo SET estado="activo" WHERE id_articulo = %s', (id_articulo,))
        mysql.connection.commit()
        flash('Artículo activado con éxito', 'success')
    except:
        flash('Hubo un error al activar el artículo', 'danger')
    return redirect(url_for('listadoProducto'))

#MODULO VENTAS
@app.route("/cargarventa", methods=["GET", "POST"])
@login_required
def cargarventa():
    cur = mysql.connection.cursor()

    if request.method == "POST":
        producto_ids = request.form.getlist('producto_id[]')
        cantidades = request.form.getlist('cantidad[]')
        id_cliente = request.form.get('id_cliente') 

        total_venta = 0
        for producto_id, cantidad in zip(producto_ids, cantidades):
            cur.execute('SELECT precio, stockDisponible, stockVendido FROM articulo WHERE id_articulo=%s', (producto_id,))
            precio, stockDisponible, stockVendido = cur.fetchone()
            cantidad = int(cantidad)

            if cantidad > stockDisponible:
                flash(f'La cantidad ingresada para el producto {producto_id} supera al stock disponible.')
                return redirect(url_for('cargarventa'))

            # Actualizar stock del producto
            nuevo_stockDisponible = stockDisponible - cantidad
            nuevo_stockVendido = stockVendido + cantidad
            cur.execute("""
                UPDATE articulo
                SET stockDisponible = %s, stockVendido = %s
                WHERE id_articulo = %s
            """, (nuevo_stockDisponible, nuevo_stockVendido, producto_id))

            total_venta += precio * cantidad

        # Guardando el pedido en la base de datos
        cur.execute('''
            INSERT INTO pedidos (id_cliente, fecha_pedido, precio_final, estado) 
            VALUES (%s, NOW(), %s, "pendiente")
        ''', (id_cliente, total_venta))
        mysql.connection.commit()

        return render_template('confirmacion.html', total=total_venta)

    else:  # Si es GET
        # Selecciona solo clientes activos
        cur.execute('SELECT id_cliente, razonsocial FROM clientes WHERE estado = "activo"') 
        clientes_data = cur.fetchall()
        
        # Selecciona solo productos activos con stock disponible
        cur.execute('SELECT id_articulo, producto, precio FROM articulo WHERE stockDisponible > 0 AND estado = "activo"')
        articulo_data = cur.fetchall()
        
        return render_template('cargarventa.html', articulo=articulo_data, clientes=clientes_data)



@app.route("/cargarstock")
@login_required
def cargarstock():
    cur = mysql.connection.cursor()
    cur.execute ('SELECT id_articulo, producto FROM articulo')
    data = cur.fetchall()
    return render_template('cargarstock.html', articulo = data)


@app.route('/restar_stock_vendido', methods=['POST'])
@login_required
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
@login_required
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
            p.id_cliente,
            p.estado
         FROM 
            pedidos p
        JOIN 
            Clientes c ON p.id_cliente = c.id_cliente
        LEFT JOIN 
            detallesPedido d ON p.id_pedido = d.id_pedido
        LEFT JOIN 
            articulo a ON d.id_articulo = a.id_articulo
        ORDER BY 
            p.id_pedido DESC;       
    ''')
    data = cur.fetchall()
    pedidos_preparados = [pedido for pedido in data if pedido[8] == 'preparado']
    pedidos_pendientes = [pedido for pedido in data if pedido[8] == 'pendiente']
    pedidos_anulados = [pedido for pedido in data if pedido[8] == 'anulado' or pedido[8] == 'eliminado']

    return render_template('consultarPedido.html', pedidos_preparados=pedidos_preparados, pedidos_pendientes=pedidos_pendientes, pedidos_anulados=pedidos_anulados)


@app.route("/edit_pedido/<id>")
@login_required
def edit_pedido(id):
    cur = mysql.connection.cursor()
    
    # Obtener datos del pedido basado en el ID
    cur.execute('SELECT * FROM pedidos WHERE id_pedido = %s', (id,))
    pedido_data = cur.fetchone()
    
    # Obtener detalles del pedido
    cur.execute('''
        SELECT d.id_articulo, a.producto, d.cantidad, d.subtotal, a.precio 
        FROM detallesPedido d
        JOIN articulo a ON d.id_articulo = a.id_articulo
        WHERE d.id_pedido = %s;
    ''', (id,))
    detalles = cur.fetchall()
    
    # Obtener todos los clientes
    cur.execute('SELECT id_cliente, razonsocial FROM Clientes')
    clientes = cur.fetchall()
    
    return render_template('edit-pedido.html', pedido=pedido_data, clientes=clientes, detalles=detalles)




@app.route("/delete_pedido/<id>")
@login_required
def delete_pedido(id):
    cur = mysql.connection.cursor()
    try:
        # Cambiamos el estado del pedido a "anulado"
        cur.execute('UPDATE pedidos SET estado = "anulado" WHERE id_pedido = %s', (id,))
        mysql.connection.commit()
        flash('Pedido anulado correctamente!')
    except Exception as e:
        mysql.connection.rollback()
        flash('Error al anular el pedido: ' + str(e))
    return redirect(url_for('consultarPedido'))



@app.route('/update_pedido/<id>', methods=['POST'])
@login_required
def update_pedido(id):
    id_cliente = request.form['clienteSeleccionado']  # O el nombre del campo que corresponda
    
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            UPDATE pedidos
            SET id_cliente = %s
            WHERE id_pedido = %s
        """, (id_cliente, id))
        
        mysql.connection.commit()
        flash('Pedido actualizado correctamente!')
    except Exception as e:
        mysql.connection.rollback()
        flash('Error al actualizar el pedido: ' + str(e))
    finally:
        cur.close()
        
    return redirect(url_for('consultarPedido'))




@app.route("/detalle_pedido/<id_pedido>")
@login_required
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


@app.route('/update_detalle_pedido/<id>', methods=['POST'])
@login_required
def update_detalle_pedido(id):
    # Obtener los datos del formulario
    productos = request.form.getlist('producto[]')
    precios_unitarios = request.form.getlist('precio_unitario[]')
    cantidades = request.form.getlist('cantidad[]')
    subtotales = request.form.getlist('subtotal[]')

    try:
        cur = mysql.connection.cursor()

        # Suponiendo que eliminas todos los detalles y vuelves a insertar para simplificar
        cur.execute("DELETE FROM detallesPedido WHERE id_pedido = %s", [id])

        for producto, precio_unitario, cantidad, subtotal in zip(productos, precios_unitarios, cantidades, subtotales):
            # Aquí debes tener algún identificador para saber qué producto es
            # Insertar el nuevo detalle
            cur.execute("""
                INSERT INTO detallesPedido (id_pedido, id_articulo, cantidad, subtotal) 
                VALUES (%s, %s, %s, %s)
            """, (id, producto, cantidad, subtotal))

            # Suponiendo que debes actualizar el stock de articulo (si eso es parte de tu lógica)
            cur.execute("""
                UPDATE articulo 
                SET stockDisponible = stockDisponible - %s 
                WHERE id_articulo = %s
            """, (cantidad, producto))

        # Actualizar el precio total del pedido
        precio_final = sum([float(subtotal) for subtotal in subtotales])
        cur.execute("""
            UPDATE pedidos
            SET precio_final = %s
            WHERE id_pedido = %s
        """, (precio_final, id))
        
        mysql.connection.commit()
        flash('Detalle del pedido actualizado correctamente!')
    except Exception as e:
        mysql.connection.rollback()
        flash('Error al actualizar el detalle del pedido: ' + str(e))
    finally:
        cur.close()
        
    return redirect(url_for('consultarPedido'))



@app.route('/buscar', methods=['GET'])
@login_required
def buscar_pedidos():
    nombre_cliente = request.args.get('nombre_cliente', default="", type=str)
    id_pedido = request.args.get('id_pedido', default=None, type=str)
    
    query = '''
    SELECT 
        p.id_pedido, 
        p.fecha_pedido,
        p.precio_final,
        c.razonsocial,
        p.id_cliente,
        p.estado
    FROM 
        pedidos p
    JOIN 
        Clientes c ON p.id_cliente = c.id_cliente
    WHERE 
        c.razonsocial LIKE %s
    '''
    
    params = ['%' + nombre_cliente + '%']
    
    if id_pedido:
        query += " AND p.id_pedido = %s"
        params.append(id_pedido)
    
    cur = mysql.connection.cursor()
    cur.execute(query, params)
    
    data = cur.fetchall()  # Obtener los resultados de la consulta
    cur.close()            # Cerrar el cursor

    # Devolver los resultados renderizados en la plantilla
    return render_template('consultarPedido.html', pedidos=data)


 

@app.route("/preparar_pedido/<id>", methods=["GET"])
@login_required
def preparar_pedido(id):
    cur = mysql.connection.cursor()
    try:
        # Cambiar el estado del pedido a "preparado"
        cur.execute('UPDATE pedidos SET estado = "preparado" WHERE id_pedido = %s', (id,))
        mysql.connection.commit()

        # Ahora, puedes obtener los detalles del pedido para imprimir (esto es solo un ejemplo)
        cur.execute('''
            SELECT 
                p.id_pedido, 
                p.fecha_pedido,
                c.razonsocial,
                d.cantidad,
                a.producto,
                a.precio
            FROM 
                pedidos p
            JOIN 
                Clientes c ON p.id_cliente = c.id_cliente
            LEFT JOIN 
                detallesPedido d ON p.id_pedido = d.id_pedido
            LEFT JOIN 
                articulo a ON d.id_articulo = a.id_articulo
            WHERE
                p.id_pedido = %s;
        ''', (id,))
        detalles_pedido = cur.fetchall()

        # Puedes usar estos detalles para renderizar un template específico para impresión
        return render_template('detalle-pedido.html', detalles=detalles_pedido)
    except Exception as e:
        flash('Error al preparar el pedido: ' + str(e))
        return redirect(url_for('consultarPedido'))


@app.route('/pedidos_anulados/<int:id_pedido>', methods=['GET'])
@login_required
def pedidos_anulados(id_pedido):
    cur = mysql.connection.cursor()
    cur.execute('UPDATE pedidos SET estado = "anulado" WHERE id_pedido = %s', (id_pedido,))
    mysql.connection.commit()
    return redirect(url_for('consultarPedido'))

@app.route('/pedidos_pendientes/<int:id_pedido>', methods=['GET'])
@login_required
def pedidos_pendientes(id_pedido):
    cur = mysql.connection.cursor()
    cur.execute('UPDATE pedidos SET estado = "pendiente" WHERE id_pedido = %s', (id_pedido,))
    mysql.connection.commit()
    return redirect(url_for('consultarPedido'))


@app.route('/agregar_stock_ingresado', methods=['POST'])
@login_required
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
@login_required
def get_pedidos(id_cliente):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM pedido WHERE id_cliente = %s', [id_cliente])
    pedidos = cur.fetchall()
    return jsonify(pedidos)

@app.route('/crear_pedido', methods=['POST'])
@login_required
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

def status_401(error):
    return redirect(url_for('welcome'))

def status_404(error):
    return "<h1>Pagina no encontrada</h1>",404    

if __name__ == '__main__':
    app.register_error_handler(401,status_401)
    app.register_error_handler(404,status_404)
    app.run(port=3000, debug=True)
