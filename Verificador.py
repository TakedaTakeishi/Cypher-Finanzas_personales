from pathlib import Path
import Base_Controlador as ctr
from os import path
from datetime import datetime

# ---------------------------------------------------------------------
# def diferencia(str_fin, str_inicio,tipo):

#     query = f"""
#     SELECT (strftime('%{tipo}', '{str_fin}') - strftime('%{tipo}', '{str_inicio}'));
#     """
#     cursor.execute(query)
#     fetchedData = cursor.fetchall()  
#     return fetchedData[0][0]
# ---------------------------------------------------------------------



'''
def Verificador_1(Archivo):
    
    if os.path.exists(Archivo):
        print("La archivo existe.")
        return True
    else:
        print("La archivo no existe.")
        return False


def Verificador_2(Archivo):
    file_path = Path(Archivo)
    if file_path.exists():
        print("El archivo existe.")
    else:
        print("El archivo no existe.")



ruta_absoluta = os.path.realpath('Base_Nombres.txt')

print("Ruta absoluta con ralpath: {}".format(ruta_absoluta))


with open(ruta_absoluta, 'r') as file:  #En el futuro hay que hacer una función para reguntar qué base acceder.
    nom = file.readlines()[0]
    print(nom)
print(type(nom))
Nombre_Base = nom.strip()
Verificador_1(Nombre_Base)
Verificador_2(Nombre_Base)

print("****" + Nombre_Base + "******")
print("Mandando como texto")

Verificador_1('bases.db')
Verificador_2('bases.db')

'''

'''
 # Create the file object.
 # Give the correct filename with path in the following line.

ruta = os.path.realpath('Usuarios.txt')
file_object = open(ruta, "r", encoding="utf-8")
# Loop over and print each line in the file object.
i = 0
for string in file_object:
    i += 1
    print(f'{i}. {string}', end='')

print(i)
'''

'''
from datetime import datetime

# Obtener la fecha y hora actual
fecha_hora_actual = datetime.now()

# Extraer solo la fecha
fecha_actual = fecha_hora_actual.date()

# Extraer solo el día
dia_actual = fecha_hora_actual.day
dia_actuald = fecha_hora_actual.month
año = fecha_hora_actual.year

print(f"Fecha y hora actual: {fecha_hora_actual}")
print(f"Fecha actual: {fecha_actual}")
print(f"Día actual: {dia_actual}")
print(dia_actuald)
print(año)
'''

def fecha_Inicial():
    anio=mes=dia=0
    fecha_hora_actual = datetime.now()

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





def usuario_Asigna(ruta, Nombre):
    with open(ruta, 'a') as file:
        Usuario = Nombre + '\n'
        file.write(Usuario)


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

def usuarios_Elegir(Usuarios_Max):
    ruta = path.realpath('Usuarios.txt')
    while True:
        print()
        opcion = int(input("Elije el número de usuario: "))
        if (opcion <= Usuarios_Max and opcion > 0):
            with open(ruta, 'r') as file:
                Usuario = file.readlines()[opcion-1]
            return Usuario
        print("Valor inválido")


def menu_Usuarios():
    print("Elije usuario:")
    ruta = path.realpath('Usuarios.txt')
    file_object = open(ruta, "r", encoding="utf-8")
    # Loop over and print each line in the file object.
    i = 0
    for string in file_object:
        i += 1
        print(f'{i}.{string}', end='')
    Usuario = usuarios_Elegir(i)
    return Usuario
        


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


def usuario_Iniciar():
    ruta = path.realpath('Usuarios.txt')
    with open(ruta,'r') as file: 
        if path.getsize(ruta) > 0:
            if (usuarios_Uno(ruta)):
                Nombre = file.readlines()[0]                
            else:
                Nombre = menu_Usuarios()           
            Base, cursor = ctr.base_Inicializar(2, Nombre)
        else:
            print("No hay usuario creado, crea uno nuevo.")
            Nombre = usuario_Crear()
            usuario_Asigna(ruta, Nombre)
            Fecha = fecha_Inicial()
            Base, cursor = ctr.base_Inicializar(1, Nombre, Fecha)

    return Base, cursor

base, cursor = usuario_Iniciar()

def fecha_Ultima(cursor):
    cursor.execute("""SELECT MAX(FECHA) FROM Diario""")
    fetchedData = cursor.fetchall()[0][0]
    return fetchedData


print(fecha_Ultima(cursor))