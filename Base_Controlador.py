import sqlite3 as sql
import Base_Creacion as bc
import Base_Insercion as bi
from urllib.request import pathname2url
import os



#---------------------------------------------------------------------

#Verificar si existe la base de datos
    
    #Si no existe la crea usando Base_Creacion en el día especificado

    #Y sólo se ejecuta una vez

    #Devuelve verdadero si se creo correctamente

#---------------------------------------------------------------------
insertDiario = """INSERT INTO Diario
VALUES(?, ?, ?, ?, ?, ?, ?);"""

def verificar_base_de_datos(Nombre_Base):
    if os.path.exists(Nombre_Base):
        print("La base de datos existe.")
        return True
    else:
        print("La base de datos no existe.")
        return False


# ---------------------------------------------------------------------------------------------------------------
# Necesitamos una función para comparar la fecha actual con la ingresada de modo que no se ponga una fecha futura.
# Mejorar los comentarios.
# ---------------------------------------------------------------------------------------------------------------

def Inicializar_Base(Nombre_ini, ruta_absoluta):
    #Verificamos para evitar sobreescribir una base ya creada
    Verificacion = verificar_base_de_datos(Nombre_ini)
    
    if Verificacion == False:
        Nombre_Base =  input("Dame el nombre de la nueva base: ") #Hay que considerar excepciones
        Nombre_Base += '.db'
        Fecha = input("Dame la fecha inicial en formato YYYY-MM-DD: ")
        with open(ruta_absoluta, 'a') as file:
            Nombre = Nombre_Base + '\n'
            file.write(Nombre)
    
        Base = sql.connect(Nombre_Base)
        cursor = Base.cursor()
        
        # Llamamos a la funcion creacion por que la ruta no existe entonces se tiene que crear una nueva base con las tablas

        bc.Creacion_Tablas(Fecha,Base,cursor)

        cursor.execute(insertDiario, (None,Fecha,None,None,None,None,None))
        Base.commit()
        print("La base ha sido creada")
    else:
        print("Conectando a {}" .format(Nombre_ini))
        
        # Primera conexión a la base.    
        Base = sql.connect(Nombre_ini)
        cursor = Base.cursor()
    return Base, cursor

# --------------------------------------------------------------------- 
# Fecha:'YYYY-MM-DD'
# os.path.realpath se ejecuta para darnos las ruta completa de el nombre que esta en ella
# ---------------------------------------------------------------------


ruta_absoluta = os.path.realpath('Base_Nombres.txt')

print("Ruta absoluta:{}".format(ruta_absoluta))

with open(ruta_absoluta, 'r') as file:
    Nombre_Base = file.readlines()[0]
    
    print(Nombre_Base)
Base, cursor = Inicializar_Base(Nombre_Base,ruta_absoluta)



# ---------------------------------------------------------------------

# ---------------------------------------------------------------------



#Cerrando la base y guardando cambios
Base.commit()
cursor.close()
Base.close()