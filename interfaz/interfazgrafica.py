#Importaciones
import customtkinter as ctk
import os
from PIL import ImageTk, Image
import bd.base_datos as sqlbd

# ---> Rutas
#Carpeta principal
carpeta_principal = os.path.dirname(__file__)
#.\proyecto-bd\bd\interfaz
carpeta_imagenes = os.path.join(carpeta_principal, "imagenes")
#.\proyecto-bd\bd\interfaz\imagenes

# Objeto para manejar bases de datos MySQL
base_datos = sqlbd.BaseDatos(**sqlbd.acceso_bd)

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

class Login:
    def __init__(self):
        # Creación de la ventana principal
        self.root = ctk.CTk() #Instancia
        self.root.title("Programación Fácil - Proyecto de bases de datos") #Titulo
        self.root.iconbitmap(os.path.join(carpeta_imagenes, "")) #Icono
        self.root.geometry("400x500") #Tamaño de la ventana
        self.root.resizable(False,False) #Bloqueo de redimensión de ventana

        # Contenido de la ventana principal
        # Carga de la imagen
        logo = ctk.CTkImage(
            light_image=Image.open((os.path.join(carpeta_imagenes, "Syspe.png"))), # Imagen modo claro
            dark_image=Image.open((os.path.join(carpeta_imagenes, "Syspe.png"))), # Imagen modo oscuro
            size=(250, 250)) # Tamaño de las imágenes
        
        # Etiqueta para mostrar la imagen
        etiqueta = ctk.CTkLabel(master=self.root,
                               image=logo,
                               text="")
        etiqueta.pack(pady=15)

        # Campos de texto
        # Usuario
        ctk.CTkLabel(self.root, text="Usuario").pack()
        self.usuario = ctk.CTkEntry(self.root)
        self.usuario.insert(0, "Ej:Laura")
        self.usuario.bind("<Button-1>", lambda e: self.usuario.delete(0, 'end'))
        self.usuario.pack()

        # Contraseña
        ctk.CTkLabel(self.root, text="Contraseña").pack()
        self.contrasena = ctk.CTkEntry(self.root)
        self.contrasena.insert(0, "*******")
        self.contrasena.bind("<Button-1>", lambda e: self.contrasena.delete(0, 'end'))
        self.contrasena.pack()

        # Botón de envío
        ctk.CTkButton(self.root, text="Entrar", command=self.validar).pack(pady=10)

        # Bucle de ejecución
        self.root.mainloop()
        
    # Función para validar el login
    def validar(self):
        obtener_usuario = self.usuario.get()
        obtener_contrasena = self.contrasena.get()
        # Verifica si el valor que tiene el usuario o la contraseña o ambos no coinciden
        if obtener_usuario != "Amira" or obtener_contrasena != "1234":
            # En caso de tener ya un elemento "info_login" (etiqueta) creado, lo borra
            if hasattr(self, "info_login"):
                self.info_login.destroy()
            # Crea esta etiqueta siempre que el login sea incorrecto
            self.info_login = ctk.CTkLabel(self.root, text="Usuario o contraseña incorrectos.")
            self.info_login.pack()
        else:
            # En caso de tener ya un elemento "info_login" (etiqueta) creado, lo borra
            if hasattr(self, "info_login"):
                self.info_login.destroy()
            # Crea esta etiqueta siempre que el login sea correcto
            self. info_login = ctk.CTkLabel(self.root, text=f"Hola, {obtener_usuario}. Espere unos instantes...")
            self.info_login.pack()
            # Se destruye la ventana de login
            self.root.destroy()
            # Se instanacia la ventana de opciones del programa
            ventana_opciones = VentanaOpciones()

class FuncionesPrograma:
    def ventana_verclientes(self):
        ventana = VerClientes()
        
    def ventana_ingresarcliente(self):
        #self.root.destroy()
        ventana = IngresarCliente()
        
    def ventana_modificarcliente(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para modificar los datos de un cliente")
        
    def ventana_verpedidos(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana que muestra los registros de los pedidos")
        
    def ventana_ingresarpedido(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para ingresar un nuevo pedido")
        
    def ventana_modificarpedido(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para modificar los datos de un pedido")
    
    def ventana_verproductos(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana que muestra los registros de los productos")
        
    def ventana_ingresarproducto(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para ingresar un nuevo producto")
        
    def ventana_modificarproducto(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para modificar los datos de un producto")
        
objeto_funciones = FuncionesPrograma()  
           
class VentanaOpciones:
    botones = {'Ver clientes': objeto_funciones.ventana_verclientes, 
               'Ingresar nuevo cliente': objeto_funciones.ventana_ingresarcliente, 
               'Modificar clientes': objeto_funciones.ventana_modificarcliente, 
               'Ver pedidos': objeto_funciones.ventana_verpedidos, 
               'Ingresar nuevo pedido': objeto_funciones.ventana_ingresarpedido,
               'Modificar pedido': objeto_funciones.ventana_modificarpedido, 
               'Ver productos': objeto_funciones.ventana_verproductos, 
               'Ingresar nuevo producto': objeto_funciones.ventana_ingresarproducto, 
               'Modificar producto': objeto_funciones.ventana_modificarproducto}
    
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Opciones para trabajar con bases de datos.")

        #Contador para la posición de los botones
        contador = 0

        # Crea los botones y establece su texto
        for texto_boton in self.botones:
            button = ctk.CTkButton(
                master=self.root,
                text=texto_boton,
                height=25,
                width=200,
                command=self.botones[texto_boton]
            )
            button.grid(row=contador//3, column=contador%3, padx=5, pady=5)
        
            # Incrementa el contador
            contador += 1
        self.root.mainloop()

#class VerPedidos:
class VerClientes:
    def __init__(self):
        self.root = ctk.CTkToplevel()
        self.root.title("Listado de todos los clientes")
        
        # Crea el frame y añádelo a la ventana
        marco = ctk.CTkFrame(self.root)
        marco.pack(padx=10, pady=10)
        
        self.marco2 = ctk.CTkFrame(marco, width=300)
        self.marco2.grid(row=0,column=0)
    
        
        contador = 0
        
        resultado = base_datos.consulta("SELECT * FROM primerapruebasyspe.clientes")
        for registro in resultado:
            label = ctk.CTkLabel(
                master=marco,
                text=registro,
                height=25,
                width=200,
            )
            label.grid(row=contador//7, column=contador%7, padx=5, pady=5)

        #print(total_registros)
        #self.info_login.pack()
        
        self.root.mainloop()
#class VerProductos:
#class IngresarPedido:

class IngresarCliente:
    def __init__(self):
        self.root = ctk.CTkToplevel()
        self.root.title("Ingrese aquí los datos del nuevo cliente: ")
        
        #Campo de texto para ingresar razon social
        ctk.CTkLabel(self.root, text="Razón social").pack()
        self.razonsocial = ctk.CTkEntry(self.root, width=400)
        self.razonsocial.insert(0,"")
        self.razonsocial.bind("<Button-1>", lambda e: self.razonsocial.delete(0, 'end'))
        self.razonsocial.pack()
        
        #Campo de texto para ingresar nombre de fantasía
        ctk.CTkLabel(self.root, text="Nombre de fantasía").pack()
        self.nombrefantasia = ctk.CTkEntry(self.root, width=400)
        self.nombrefantasia.insert(0,"")
        self.nombrefantasia.bind("<Button-1>", lambda e: self.nombrefantasia.delete(0, 'end'))
        self.nombrefantasia.pack()
        
        #Campo de texto para ingresar telefono
        ctk.CTkLabel(self.root, text="Telefono").pack()
        self.telefono = ctk.CTkEntry(self.root, width=400)
        self.telefono.insert(0,"")
        self.telefono.bind("<Button-1>", lambda e: self.telefono.delete(0, 'end'))
        self.telefono.pack()
        
        #Campo de texto para ingresar CUIT
        ctk.CTkLabel(self.root, text="CUIT").pack()
        self.CUIT = ctk.CTkEntry(self.root, width=400)
        self.CUIT.insert(0,"")
        self.CUIT.bind("<Button-1>", lambda e: self.CUIT.delete(0, 'end'))
        self.CUIT.pack()
        
        #Campo de texto para ingresar direccion
        ctk.CTkLabel(self.root, text="Direccion").pack()
        self.direccion = ctk.CTkEntry(self.root, width=400)
        self.direccion.insert(0,"")
        self.direccion.bind("<Button-1>", lambda e: self.direccion.delete(0, 'end'))
        self.direccion.pack()
        
        #Campo de texto para ingresar E-mail
        ctk.CTkLabel(self.root, text="E-mail", width=400).pack()
        self.email = ctk.CTkEntry(self.root, width=400)
        self.email.insert(0,"")
        self.email.bind("<Button-1>", lambda e: self.email.delete(0, 'end'))
        self.email.pack()
        
        ctk.CTkButton(self.root, text="Guardar", command=self.guardarCliente).pack(pady=20)

        self.root.mainloop()
        
    def guardarCliente(self):
        obtener_razonsocial = self.razonsocial.get()
        obtener_nombrefantasia = self.nombrefantasia.get()
        obtener_telefono = self.telefono.get()
        obtener_CUIT = self.CUIT.get()
        obtener_direccion = self.direccion.get()
        obtener_email = self.email.get()
        # Verifica si el valor que tiene el usuario o la contraseña o ambos no coinciden
        if obtener_razonsocial == "" or obtener_nombrefantasia == "" or obtener_telefono == "" or obtener_CUIT == "" or obtener_direccion == "" or obtener_email == "":
            # En caso de tener ya un elemento "info_login" (etiqueta) creado, lo borra
            if hasattr(self, "chequearCamposCompletos"):
                self.chequearCamposCompletos.destroy()
            # Crea esta etiqueta siempre que algun campo este vacio
            self.chequearCamposCompletos = ctk.CTkLabel(self.root, text="Debe completar todos los datos para poder ingresar un nuevo usuario.\n Intentelo nuevamente")
            self.chequearCamposCompletos.pack()
        else:
            # En caso de que todos los campos esten completos, lo ingresa en la bd y lo hace saber
            if hasattr(self, "chequearCamposCompletos"):
                self.chequearCamposCompletos.destroy()
               
            # Guardo los datos ingresados en un diccionario (es lo que voy a pasar como parametro para cargar en la bd)
            nuevo_registro = [{"razon_social":obtener_razonsocial,
                              "nombre_fantasia": obtener_nombrefantasia,
                              "telefono": obtener_telefono,
                              "CUIT": obtener_CUIT,
                              "direccion": obtener_direccion,
                              "email": obtener_email}]
                
            # Carga los datos en la base de datos
            #print(nuevo_registro)
            base_datos.insertar_registro("primerapruebasyspe", "clientes", nuevo_registro)
            # Crea esta etiqueta siempre que los campos esten completos
            self.chequearCamposCompletos = ctk.CTkLabel(self.root, text=f"Usuario {obtener_nombrefantasia} ingresado exitosamente.")
            self.chequearCamposCompletos.pack()

#class IngresarProducto:
#class ModificarPedido:
#class ModificarCliente:
#class ModificarProducto:


