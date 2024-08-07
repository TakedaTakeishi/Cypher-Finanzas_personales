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
from datetime import datetime



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

def insertRubro(cursor, rubro):
    Tipo = str.upper(rubro)
    Rubro =  '''INSERT INTO Rubro
    VALUES(?, ?);'''
    cursor.execute('''SELECT TIPO
                        FROM Rubro
                        WHERE UPPER(TIPO) = "{}"'''.format(Tipo))
    fetchedData = cursor.fetchall()
    print(fetchedData)
    #Veamos que no existe el rubro cuando está vacío
    if(not bool(fetchedData)):
        print("El rubro no existe, creando uno.")
        cursor.execute(Rubro, (None,Tipo))
    else:
        print("El rubro ya existe.")
        
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
    if(Rubro):
        Rubro_id = insertRubro(cursor, Rubro)
    else:
        Rubro_id = None
    cursor.execute(Info_Transacciones, (None, Concepto, Cantidad, Rubro_id)) #Falta verificar el rubro_id de rubro
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
    VALUES(?, ? ,?, ?, ?);'''
    cursor.execute(Transacciones, (Fecha_hora, Info_ID, Dia_ID))
    Base.commit()

    '''
    CREATE TABLE Transacciones(
                            TRANSACCION_ID      integer  NOT NULL
                            ,OPERACION_ID       integer  NOT NULL
                            ,FECHA              datetime NOT NULL
                            ,INFO_ID            integer  NOT NULL
                            ,DIA_ID             integer  NOT NULL
                            ,CONSTRAINT T_D_T_PK PRIMARY KEY(TRANSACCION_ID AUTOINCREMENT)
                            ,CONSTRAINT TRANSAC_INFO_ID_FK FOREIGN KEY (INFO_ID)   REFERENCES Info_transacciones (INFO_ID)
                            ,CONSTRAINT TRANSAC_DIA_ID_FK  FOREIGN KEY (DIA_ID)    REFERENCES Diario (DIA_ID)
                            ,CONSTRAINT TRANSAC_OPE_ID_FK  FOREIGN KEY (OPERACION_ID) REFERENCES Flujo (OPERACION_ID)
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
                        ,INTERVALO      numeric
                        ,INTERESES      numeric
                        ,FECHA_FINAL    date
                        ,CONSTRAINT O_ID_PK PRIMARY KEY(OPERACION_ID,TRANSACCION_ID) 
                    );
    '''

#--------------------------------------------CREACIÓN DE USUARIOS Y BASES------------------------------------------------------------
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



# def base_Fecha():
    
#     regular = False
#     while(not regular):
#         s = input("Dame la fecha inicial en formato YYYY-MM-DD: ") #DD-MM-YYYY
#         #s = año + '-' + mes + '-' + dia
#         regular = bool(re.match(r'^\d{4}-\d{2}-\d{2}$',s)) #Hacer un validador de días, meses y años para la interfaz: le toca a Salazar
#         if(regular != True):
#             print("Formato incorrecto, vuelve a intentarlo.")
#         else:
#             if validar_fecha(s)== False:
                
#     #print("Fecha inicial: " + s)
#     return s

def validar_fecha(fecha):#Te regresa verdadero si el string fecha es una fecha corrrecta y no esta en el futuro
    anio = int(fecha[:4])
    mes = int(fecha[5:7])
    dia = int(fecha[8:10])
    fecha_hora_actual = datetime.now()

    
    if anio<=0:
        return False
    if mes<=0 or mes>12:
        return False
    if mes in [4, 6, 9, 11] and (dia <= 0 or dia > 30):
                return False
    elif mes == 2:
        if (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0):  
            if dia <= 0 or dia > 29:
                return False
        else:
            if dia <= 0 or dia > 28:
                return False
    elif dia <= 0 or dia > 31:
        return False
    
    entered_date = datetime.strptime(fecha, "%Y-%m-%d")
    if entered_date<=fecha_hora_actual:
        return True
    else:
        return False

def usuarios_Dir(Base_Nombre):
    current_directory = Path.cwd()
    folder_name = 'BD'
    target_folder = current_directory / folder_name
    if not target_folder.exists():
        target_folder.mkdir()
        print(f"La carpeta ha sido creada: {target_folder}")
        
    archivo_ruta = target_folder / Base_Nombre
    #print(f"Ruta de la base: {archivo_ruta}")
    return archivo_ruta

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
    print("\t.::Conectando a {}::." .format(Base_Nombre))   


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