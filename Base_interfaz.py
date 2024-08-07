import Base_Controlador as ctr
from os import path
from datetime import datetime
import os


#Que va a pedir y como

def usuario_Crear(): 
    while True:
        Nombre = input("Dame el nombre del usuario: ")
        if Nombre == "":
            print("Debe contener al menos una letra o número.")
        elif not(Nombre[0].isalnum()):
            print("El primer caracter debe ser letra o número.")
        elif all(c.isalnum() or c == '-' or '_' for c in Nombre) and ' ' not in Nombre:
            print("Nombre correcto")
            break
        else:
            print("No debe tener espacios")
    return Nombre

def usuario_Asigna(ruta, Nombre):
    with open(ruta, 'a') as file:
        Usuario = Nombre + '\n'
        file.write(Usuario)

def fecha_Inicial():
    anio=mes=dia=0
    fecha_hora_actual = datetime.now()
    print(".:Fecha a iniciar analisis:.")
    while True:
        while anio<=0:
            anio=int(input("Ingresa el año: "))
            if anio<=0:
                print("El año no es válido")

        while 0>=mes or mes>12:
            mes=int(input("Ingresa el mes: "))
            if 0>=mes or mes>12:
                print("El mes no es válido")

        while dia <= 0 or dia > 31:
            dia = int(input("Ingresa el día: "))
            if mes in [4, 6, 9, 11] and (dia <= 0 or dia > 30):
                print("El día no es válido para este mes")
                dia = 0
            elif mes == 2:
                if (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0):  
                    if dia <= 0 or dia > 29:
                        print("El día no es válido para febrero en un año bisiesto")
                        dia = 0
                else:
                    if dia <= 0 or dia > 28:
                        print("El día no es válido para febrero")
                        dia = 0
            elif dia <= 0 or dia > 31:
                print("El día no es válido para este mes")
                dia = 0
        entered_date_str = f"{anio:04d}-{mes:02d}-{dia:02d}"
        entered_date = datetime.strptime(entered_date_str, "%Y-%m-%d")
        if entered_date<=fecha_hora_actual:
            break
        else:
            print("La fecha no puede ser mayor a la fecha actual")
            anio=mes=dia=0
    return entered_date_str



def usuarios_Uno(file_path):
    with open(file_path, 'r') as file:
        # Leer la primera línea (y descartarla)
        first_line = file.readline()
        # Leer la segunda línea
        second_line = file.readline()
        
        # Verificar si la segunda línea está vacía o contiene solo espacios en blanco
        if second_line.strip() == '':
            return True
        else:
            return False
'''        
def contar_lineas(archivo):
    with open(archivo, 'r') as f:
        contenido = f.read()
    lineas = contenido.splitlines()
    return len(lineas)
'''

def usuario_Nuevo():
    ruta = path.realpath('Usuarios.txt')
    Nombre = usuario_Crear()
    usuario_Asigna(ruta, Nombre)
    Fecha = fecha_Inicial()
    Base, cursor = ctr.base_Inicializar(1, Nombre, Fecha)
    return Base, cursor, Nombre

def usuario_Nombre(ruta, fila):
    with open(ruta, 'r') as file:
        Nombre = file.readlines()[fila-1]
    return Nombre.strip()
    
def usuarios_Elegir(Usuarios_Max):
    ruta = path.realpath('Usuarios.txt')
    while True:
        print()
        opcion = int(input("Elije el número de usuario: "))
        if (opcion <= Usuarios_Max and opcion > 0):
            Usuario = usuario_Nombre(ruta, opcion)
            return Usuario
        print("Valor inválido")



def usuarios_menu():
    print("Elije usuario:")
    ruta = path.realpath('Usuarios.txt')
    file_object = open(ruta, "r", encoding="utf-8")
    # Loop over and print each line in the file object.
    i = 0
    for string in file_object:
        i += 1
        print(f'{i}.{string}', end='')
    #Enviamos i para saber el número máximo de usuarios.
    return i
        

def usuario_Iniciar():
    ruta = path.realpath('Usuarios.txt')
    with open(ruta,'r') as file: 
        if path.getsize(ruta) > 0:
            #Para saber si tenemos más de un usuario comprobamos
            if (usuarios_Uno(ruta)):
                Nombre = file.readlines()[0]                
            else:
                Nombre = usuarios_Elegir(usuarios_menu())          
            Base, cursor = ctr.base_Inicializar(2, Nombre)
        else:
            print("No hay usuario creado, crea uno nuevo.")
            Base, cursor, Nombre = usuario_Nuevo()
    return Base, cursor, Nombre.strip()



def delete_line(file_path, line_number):
    # Leer todas las líneas del archivo
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Verificar que la línea a eliminar existe
    if line_number < 1 or line_number > len(lines):
        raise IndexError("El número de línea está fuera del rango.")
    
    # Eliminar la línea deseada (restar 1 porque las listas son 0-indexadas)
    del lines[line_number - 1]

    # Escribir las líneas restantes de nuevo al archivo
    with open(file_path, 'w') as file:
        file.writelines(lines)


def usuarios_Borrar(Usuarios_Max, Base, cursor, Usuario):
    ruta = path.realpath('Usuarios.txt')
    borrado = False
    while True:
        print()
        opcion = int(input("Elige el número de usuario a eliminar: "))
        if (opcion <= Usuarios_Max and opcion > 0):
            Nombre = usuario_Nombre(ruta, opcion) #Verificar si existe el usuario.
            delete_line(ruta, opcion)
            Base_nombre = Nombre + ".db"
            Path = ctr.usuarios_Dir(Base_nombre)
            # print(f"El usuario actual es: {Usuario}")
            # print(f"El nombre elegido es: {Nombre}")
            if (Nombre == Usuario):
                base_Cerrar(Base, cursor)
                borrado = True
            os.remove(Path) #Verificar si existe la base.
            print("Usuario borrado.")
            return borrado
        print("Valor inválido") #Tener una opción para cancelar la operación.




def datos_Ingresar(cursor, tipo ): #Cuando el tipo es 1 se regresa con intervalo, 0 sin intervalo
    pass
    if ctr.diferencia(datetime.now(), ctr.fecha_Ultima(cursor),'d')>=1:
        while True:
            choice=int(input("1-Informacion del dia(con intervalo) \n2-Informacion del dia(sin intervalo)"))
            if choice ==1 :
                concepto =  input("Ingresa el concepto: ")
                cantidad=   float(input("Ingresa la cantidad: "))
                rubro=      input("Ingresa el rubro: ")
                intereses=  float(input("Ingresa los intereses: "))
                intervalo=  int(input("Ingresa el intervalo en dias: "))
                fecha_final=ctr.base_Fecha()


def base_Cerrar(Base, cursor):
    Base.commit()
    cursor.close()
    Base.close()
    print("Base cerrada...")   
    

      

# menu---------------------------
# nombre
# nombre
# nombre
#elije el numero de usuario 
# Quieres Crear otro usuario?

def menu():
    Base, cursor, Usuario = usuario_Iniciar()
    while True:
        print("----------MENU----------\n")
        print("1. Ingresar Dato")
        print("2. Mostrar Datos")
        print("3. Modificar Datos")
        print("4. Cambiar de usuario")
        print("5. Crear nuevo Usuario")
        print("6. Borrar un usuario")
        print("0. Salir")
        opcion = int(input("Elige que opcion quieres:\nR:"))

        match(opcion):
            case 0:
                break
            case 1:
                datos_Ingresar(cursor)
            # case 2:
            #     #datos_Mostrar(cursor)

            # case 3:
            #     datos_Modificar()
            case 4:
                base_Cerrar(Base, cursor)
                Usuario = usuarios_Elegir(usuarios_menu())         
                Base, cursor = ctr.base_Inicializar(2, Usuario)
            case 5:
                base_Cerrar(Base, cursor)    
                Base, cursor, Usuario = usuario_Nuevo() 
            case 6:
                if (usuarios_Borrar(usuarios_menu(), Base, cursor, Usuario)):
                    Base, cursor, Usuario = usuario_Iniciar()
            case _:
                print("No existe esa operacion")
    base_Cerrar(Base, cursor)


#---------------------------------- MAIN -----------------------------------

menu()

# Probar el borrado, creación y cambio de usuarios.