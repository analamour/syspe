import mysql.connector


#conexion con la base de datos
acceso_bd = {"host" : "localhost",
             "user" : "root"
#             "database" : "cursoprogramacionfacilprueba"
             }

class BaseDatos: #nos permitirá usar esta función para CUALQUIER conexión a la bd
    def __init__(self, **kwargs):
        self.conector = mysql.connector.connect(**kwargs) #espera que se le pase un diccionario con los datos de la conexión a la bd
        self.cursor = self.conector.cursor()  #creamos el cursor en el INICIADOR para que lo puedan usar todos los métodos
        self.host = kwargs["host"]
        self.usuario =kwargs ["user"]
        self.conexion_cerrada = False
        print("Se abrió la conexión con el servidor.")
        
    ## DECORADORES
        
    # Metodo decorador para el reporte de bases de datos en el servidor
    def reporte_bd(funcion_parametro):
        def interno(self, nombre_bd):
            funcion_parametro(self, nombre_bd)
            print("Estas son las bases de datos que tiene el servidor:")
            BaseDatos.mostrar_bd(self) 
        return interno 
    
    def conexion(funcion_parametro):
        def interno(self, *args, **kwargs):
            try:
                if self.conexion_cerrada:
                    self.conector = mysql.connector.connect(
                        host = self.host,
                        user = self.usuario
                    )
                    self.cursor = self.conector.cursor()
                    self.conexion_cerrada = False
                    print("Se abrio la conexión con el servidor.")
                #Se llama a la funcion externa
                funcion_parametro(self, *args, **kwargs)
            except:
                #Se informa de un error en la llamada
                print("Ocurrió un error con la llamada.")
            finally:
                if self.conexion_cerrada:
                    pass
                else:
                    #Cerramos el cursor y la conexión
                    self.cursor.close()
                    self.conector.close()
                    print("Se cerró la conexión con el servidor.")
                    self.conexion_cerrada=True
            return self.resultado
        return interno 
    
    # Decorador para comprobar si existe una base de datos
    def comprueba_bd(funcion_parametro):
        def interno(self, nombre_bd, *args):
            # Verifica si la base de datos existe en el servidor
            sql = f"SHOW DATABASES LIKE '{nombre_bd}'"
            self.cursor.execute(sql)
            resultado = self.cursor.fetchone()
            
            # Si la base de datos no existe, muestra un mensaje de error
            if not resultado:
                print(f'La base de datos {nombre_bd} no existe.')
                return
            # Ejecuta la función decorada y devuelve el resultado
            return funcion_parametro(self, nombre_bd, *args)
        return interno
     
    ## CONSULTAS SQL 
    # Hace una consulta 
    @conexion          
    def consulta(self,sql): #sql es la instrucción sql que ejecutaremos
        try:
            self.cursor.execute(sql)
            #return self.cursor
            print("Esta es la salida de la instruccion que has ejecutado")
            self.resultado = self.cursor.fetchall() #podemos usar fecthone o fetchmany(CANTIDAD) según la cantidad de registros que queremos mostrar
        except:
            print("Ocurrio un error. Revisa la instrucción SQL.")
    
    # Muestra todas las bases de datos del servidor
    @conexion
    def mostrar_bd(self):
        try:
            self.cursor.execute("SHOW DATABASES")
            resultado = self.cursor.fetchall()
            for bd in resultado:
                print(f"-{bd[0]}")
        except:
            print("No se pudieron obtener las bases de datos. Comprueba la conexión con el servidor.")
    
    # Elimina una base de datos        
    @conexion
    @reporte_bd #llama al decorador
    @comprueba_bd
    def eliminar_bd(self, nombre_bd):
        self.cursor.execute(f"DROP DATABASE {nombre_bd}")
        print(f"Se elimino la base de datos {nombre_bd} correctamente")
    
            
    # Creacion de una base de datos
    @conexion
    @reporte_bd #llama al decorador
    def crear_bd(self, nombre_bd):
        try:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {nombre_bd};") # --> si ya está creada y lo volvemos a ejecutar, va a tirar ERROR
            print(f"Se creó correctamente la base de datos {nombre_bd} o ya estaba creada")
        except:
            print(f"Ocurrió un error al crear la base de datos {nombre_bd}. Intentelo de nuevo")
            
    # Creacion de una TABLA
    @conexion
    @comprueba_bd
    def crear_tabla(self, nombre_bd, nombre_tabla, columnas):
        try:
            #String para guardar el string con las columnas y tipos de datos
            columnas_string=""
            #Se itera la lista que se le pasa como argumento (CADA DICCIONARIO)
            for columna in columnas:
            #formamos el string con nombre, tipo y longitud 
                columnas_string += f"{columna['name']} {columna['type']} ({columna['length']})"
                #Si es clave primaria, auto_increment o no admite valores nulos, lo AÑADE al string
                if columna['primary_key']:
                    columnas_string+=" PRIMARY KEY"
                if columna['auto_increment']:
                    columnas_string+=" AUTO_INCREMENT"
                if columna['not_null']:
                    columnas_string+=" NOT NULL"
                #Hace un salto de línea después de cada diccionario
                columnas_string+=" ,\n"
            #Elimina al final del string el salto de línea y la coma
            columnas_string = columnas_string[:-2]
            #Le indica que base de datos utilizar
            self.cursor.execute(f"USE {nombre_bd}")
            #Se crea la tabla juntando la instrucción SQL con el string generado
            sql = f"CREATE TABLE {nombre_tabla} ({columnas_string});"
            #Se ejecuta la instrucción
            self.cursor.execute(sql)
            #Imprime el mensaje
            print(f"Tabla {nombre_tabla} creada exitosamente.")
        except:
            print("Ocurrió un error al intentar crear la tabla.")
        
    # Eliminar una tabla
    @conexion
    @comprueba_bd 
    def eliminar_tabla(self, nombre_bd, nombre_tabla):
        try:
            self.cursor.execute(f"USE {nombre_bd}")
            self.cursor.execute(f"DROP TABLE {nombre_tabla}")
            print(f"Tabla {nombre_tabla} eliminada exitosamente.")
        except:
            print(f"No se pudo eliminar la tabla {nombre_tabla} de la base de datos {nombre_bd}")
        
    #Metodo para mostrar las tablas de una base de datos
    @conexion
    @comprueba_bd   
    def mostrar_tablas(self, nombre_bd):
        # Se selecciona la base de datos
        self.cursor.execute(f"USE {nombre_bd};")
        # Realiza la consulta para mostrar las tablas de la base de datos actual
        self.cursor.execute("SHOW TABLES")
        resultado = self.cursor.fetchall()
        # Comprueba si la base de datos tiene tablas o no
        if resultado==[]:
            print(f"No hay tablas creadas en la base de datos {nombre_bd}.")
        else:
            # Se informa de que se están obteniendo las tablas
            print("Aquí tienes el listado de las tablas de la base de datos:")
            # Recorre los resultados y los muestra por pantalla
            for tabla in resultado:
                print(f"-{tabla[0]}.")
    
    @conexion
    @comprueba_bd
    def mostrar_columnas(self, nombre_bd, nombre_tabla):
        self.cursor.execute(f"USE {nombre_bd}")
        try:
            # Realiza la consulta para mostrar las columnas de la tabla especificada
            self.cursor.execute(f"SHOW COLUMNS FROM {nombre_tabla}")
            resultado = self.cursor.fetchall()
            
            # Se informa de que se están obteniendo las columnas
            print(f"Aquí tienes el listado de las columnas de la tabla '{nombre_tabla}':")
            # Recorre los resultados y los muestra por pantalla
            for columna in resultado:
               not_null = "No admite valores nulos." if columna[2]=="NO" else "Admite valores nulos"
               primary_key = "Es clave primaria." if columna[3]=="PRI" else ""
               foreign_key = "Es clave externa." if columna[3]=="MUL" else ""
               print(f"-{columna[0]} ({columna[1]}) {not_null} {primary_key} {foreign_key}")

        except:
            print("Ocurrió un error. Comprueba el nombre de la tabla.")
              

    # Método para insertar registros en una tabla
    @conexion
    @comprueba_bd
    def insertar_registro(self, nombre_bd, nombre_tabla, registro):
        self.cursor.execute(f"USE {nombre_bd}")

        if not registro:  # Si la lista está vacía
            print("La lista de registro está vacía.")
            return
    
        # Obtener las columnas y los valores de cada diccionario
        columnas = []
        valores = []
        for registro in registro:
            columnas.extend(registro.keys())
            valores.extend(registro.values())
        #print(columnas)
        #print(valores)

        # Convertir las columnas y los valores a strings
        columnas_string = ''
        for columna in columnas:
            columnas_string += f"{columna}, "
        columnas_string = columnas_string[:-2]  # Quitar la última coma y espacio

        valores_string = ''
        for valor in valores:
            valores_string += f"'{valor}', "
        valores_string = valores_string[:-2]  # Quitar la última coma y espacio

        # Crear la instrucción de inserción
        sql = f"INSERT INTO {nombre_tabla} ({columnas_string}) VALUES ({valores_string})"
        self.cursor.execute(sql)
        self.conector.commit()
        print("Registro añadido a la tabla.")
        
    # Método para eliminar registros con una condición
    @conexion
    @comprueba_bd
    def eliminar_registro(self, nombre_bd, nombre_tabla, condiciones):
        try:
            # Se selecciona la base de datos
            self.cursor.execute(f"USE {nombre_bd}")
            # Se crea la instrucción de eliminación
            sql = f"DELETE FROM {nombre_tabla} WHERE {condiciones}"
            # Se ejecuta y confirma
            self.cursor.execute(sql)
            self.conector.commit()
            print("Registros eliminados.")
        except:
            print("Error al intentar borrar registros en la tabla.")
        
    # Método para eliminar TODOS los registro de una tabla
    @conexion
    @comprueba_bd
    def vaciar_tabla(self, nombre_bd, nombre_tabla):
        try:
            self.cursor.execute(f"USE {nombre_bd}")
            # Se borran todos los registros de una tabla
            sql = f"TRUNCATE TABLE {nombre_tabla}"
            self.cursor.execute(sql)
            self.conector.commit()
            print("Se han borrado todos los registros de la tabla.")
        except:
            print("Error al intentar borrar los registros de la tabla.")

     # Método para actualizar registros en una tabla
    @conexion
    @comprueba_bd
    def actualizar_registro(self, nombre_bd, nombre_tabla, columnas, condiciones):
        try:
          	# Se selecciona la base de datos
            self.cursor.execute(f"USE {nombre_bd}")

            # Crear la instrucción de actualización
            sql = f"UPDATE {nombre_tabla} SET {columnas} WHERE {condiciones}"
            # Se ejecuta la instrucción de actualización y se hace efectiva
            self.cursor.execute(sql)
            self.conector.commit()
            print("Se actualizó el registro correctamente.")
        except:
            print("Ocurrió un error al intentar actualizar el registro.")