import sqlite3 as sql
import Base_Creacion as bc
import Base_Insercion as bi
from urllib.request import pathname2url
import os
import re
import string
from pathlib import Path
import pathlib
from os import path



#                        Consideraciones                          
#---------------------------------------------------------------------
#Verificar si existe la base de datos
    #Si no existe la crea usando Base_Creacion en el día especificado

    #Y sólo se ejecuta una vez

    #Devuelve verdadero si se creo correctamente
#---------------------------------------------------------------------

# --------------------------------------------------------------------- 
# Fecha:'YYYY-MM-DD'
# os.path.realpath se ejecuta para darnos las ruta completa de el nombre que esta en ella
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------
# Necesitamos una función para comparar la fecha actual con la ingresada de modo que no se ponga una fecha futura.
# Mejorar los comentarios.
# ---------------------------------------------------------------------------------------------------------------


# ------------------------------------------INSERSIONES----------------------------------------------------------

def insertDiario(Base, cursor, Fecha):
    Diario = """INSERT INTO Diario
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    cursor.execute(Diario, (None,Fecha,None,None,None,None,None,None,None))
    Base.commit()
    ''' 
                CREATE TABLE Diario(
                        DIA_ID      integer NOT NULL
                        ,FECHA      date    NOT NULL
                        ,DIA_INGRESO    numeric
                        ,DIA_EGRESO     numeric
                        ,DIA_SALDO      numeric
                        ,SALDO          numeric
                        ,PROMEDIO       numeric
                        ,MEDIANA        numeric
                        ,MODA           numeric
                        ,CONSTRAINT D_ID_PK PRIMARY KEY (DIA_ID AUTOINCREMENT)
                    );
    '''

def insertRubro(Base, cursor, Rubro):
    Rubro =  '''INSERT INTO Rubro
    VALUES(?, ? );'''
    cursor.execute(Rubro,(None,Rubro)) #Hay que validar si ya existe un rubro
    Base.commit()
    '''
                CREATE TABLE Rubro(
                        RUBRO_ID    integer NOT NULL
                        ,TIPO       text    NOT NULL
                        ,CONSTRAINT RUBRO_ID_PK PRIMARY KEY (RUBRO_ID AUTOINCREMENT)
                        );
    '''


def insertInfo_transaccciones(Base, cursor, Concepto, Cantidad, Rubro = None):
    Info_Transacciones = '''INSERT INTO Info_transacciones
    VALUES(?, ?, ?, ?);'''
    cursor.execute(Info_Transacciones, (None, Concepto, Cantidad, Rubro)) #Falta verificar el rubro_id de rubro
    Base.commit()
    '''
                CREATE TABLE Info_transacciones(
                        INFO_ID     integer  NOT NULL
                        ,CONCEPTO   text     NOT NULL
                        ,CANTIDAD   numeric  NOT NULL
                        ,RUBRO_ID   integer
                        ,CONSTRAINT I_ID_IT_PK PRIMARY KEY(INFO_ID AUTOINCREMENT)
                        ,CONSTRAINT INFO_RUBRO_R_ID_FK FOREIGN KEY (RUBRO_ID) REFERENCES Rubro (RUBRO_ID)
    '''
    
def insertTransacciones(Base, cursor, Fecha_hora, Info_ID, Dia_ID):
    Transacciones = '''INSERT INTO Transacciones
    VALUES(?, ? ,?, ?);'''
    cursor.execute(Transacciones, (Fecha_hora, Info_ID, Dia_ID))
    Base.commit()
    '''
                CREATE TABLE Transacciones(
                        TRANSACCION_ID      integer  NOT NULL
                        ,FECHA              datetime NOT NULL
                        ,INFO_ID            integer  NOT NULL
                        ,DIA_ID             integer  NOT NULL
                        ,CONSTRAINT T_D_T_PK PRIMARY KEY(TRANSACCION_ID AUTOINCREMENT)
                        ,CONSTRAINT TRANSAC_INFO_ID_FK FOREIGN KEY (INFO_ID)   REFERENCES Info_transacciones (INFO_ID)
                        ,CONSTRAINT TRANSAC_DIA_ID_FK  FOREIGN KEY (DIA_ID)    REFERENCES Diario (DIA_ID)
                    );
    '''


def insertFlujo(Base, cursor, Transaccion_ID, Intervalo = None, Intereses = None, Fecha_final = None):
    Flujo = '''INSERT INTO Flujo
    VALUES(?, ?, ?, ?, ?);'''
    cursor.execute(Flujo, (None,Transaccion_ID, Intervalo, Intereses, Fecha_final))
    Base.commit()
    '''
            CREATE TABLE Flujo(
                        OPERACION_ID    integer NOT NULL
                        ,TRANSACCION_ID integer NOT NULL
                        ,INTERVALO      numeric
                        ,INTERESES      numeric
                        ,FECHA_FINAL    date
                        ,CONSTRAINT O_ID_PK PRIMARY KEY(OPERACION_ID,TRANSACCION_ID)
                        ,CONSTRAINT FLUJ_TRANS_ID_FK FOREIGN KEY (TRANSACCION_ID)   REFERENCES Transacciones (TRANSACCION_ID)  
                    );
    '''

# --------------------------------------------CREACIÓN DE USUARIOS Y BASES------------------------------------------------------------
def nombre_BD(Nombre):
    Nombre_Base = Nombre.strip() + ".bd"
    return Nombre_Base


def verificar_BD(Nombre):
    if os.path.exists(nombre_BD(Nombre)):
        print("La base de datos existe.")
        return True
    else:
        print("La base de datos no existe.")
        return False



def base_Fecha():
    '''while(True):
        s = input("Dame la fecha inicial en formato YYYY-MM-DD: ") #DD-MM-YYYY
        #Dime que año es: 2040
        regular = bool(re.match(r'^\d{4}-\d{2}-\d{2}$',s)) #Hacer un validador de días, meses y años.
        if(regular == True):
            print("Fecha inicial: " + s)
            break
        print("Formato incorrecto, vuelve a intentarlo.")'''
    
    regular = False
    while(not regular):
        s = input("Dame la fecha inicial en formato YYYY-MM-DD: ") #DD-MM-YYYY
        #s = año + '-' + mes + '-' + dia
        regular = bool(re.match(r'^\d{4}-\d{2}-\d{2}$',s)) #Hacer un validador de días, meses y años para la interfaz: le toca a Salazar
        if(regular != True):
            print("Formato incorrecto, vuelve a intentarlo.")
    print("Fecha inicial: " + s)
    return s



def usuarios_Dir(Base_Nombre):
    current_directory = Path.cwd()
    folder_name = 'BD'
    target_folder = current_directory / folder_name
    if not target_folder.exists():
        target_folder.mkdir()
        print(f"La carpeta ha sido creada: {target_folder}")
        
    archivo = target_folder / Base_Nombre
    print(f"Ruta de la base: {archivo}")
    return archivo

def base_Inicializar(Opcion, Nombre, Fecha = None): #Opción 1 para crear base y 2 para conectarse directamente.
    Base_Nombre = Nombre.strip() + ".db"                                               
    #Si no existe una base de datos, entonces se debe crea.
    archivo_en_carpeta = usuarios_Dir(Base_Nombre)
    Base = sql.connect(archivo_en_carpeta)
    cursor = Base.cursor()
    match Opcion:
        case 1:
            #Por estar vacia 
            bc.Creacion_Tablas(Base, cursor)
            insertDiario(Base, cursor, Fecha)
            # cursor.execute(insertDiario, (None,Fecha,None,None,None,None,None,None,None)) #Se debe sustituir por Base_Insercion
            print("La base ha sido creada")
        case 2:
            print("Conectando a {}" .format(Base_Nombre))    

    #Para no tener que cerrar la conexión la devolvemos
    return Base, cursor



#----------------------------CONSULTAS----------------------------
def fecha_Ultima(cursor):
    cursor.execute("""SELECT MAX(FECHA) FROM Diario""")
    fetchedData = cursor.fetchall()[0][0]
    return fetchedData

def datos_Semana(cursor):
    pass
    cursor.execute()