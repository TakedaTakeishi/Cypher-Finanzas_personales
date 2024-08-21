import sqlite3 as sql
import Base_Creacion as bc
from urllib.request import pathname2url
import os
import re
import string
from pathlib import Path
import pathlib
from os import path
from datetime import datetime, timedelta



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
    cursor.execute(Diario, (None,Fecha,0,0,0,0,0,0,0))
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
    VALUES(?, ? );'''
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
    
    cursor.execute('''SELECT *
                    FROM Rubro
                    WHERE UPPER(TIPO) = "{}"'''.format(Tipo))
    fetchedData = cursor.fetchall()[0][0]
    
    return fetchedData
        
    '''
                CREATE TABLE Rubro(
                        RUBRO_ID    integer NOT NULL
                        ,TIPO       text    NOT NULL
                        ,CONSTRAINT RUBRO_ID_PK PRIMARY KEY (RUBRO_ID AUTOINCREMENT)
                        );
    '''



def insertInfo_transaccciones(Base, cursor, Concepto, Monto, Rubro = None):
    Info_Transacciones = '''INSERT INTO Info_transacciones
    VALUES(?, ?, ?, ?);'''
    if(Rubro):
        Rubro_id = insertRubro(cursor, Rubro)
    else:
        Rubro_id = None
    cursor.execute(Info_Transacciones, (None, Concepto, Monto, Rubro_id)) #Falta verificar el rubro_id de rubro
    Base.commit()

    #Retornamos el ID
    cursor.execute('''SELECT MAX(INFO_ID)
                        FROM Info_Transacciones''')
    fetchedData = cursor.fetchall()[0][0]
    print(f"La última operación de Info_transacciones es: {fetchedData}")
    return fetchedData

    '''
                CREATE TABLE Info_transacciones(
                        INFO_ID     integer  NOT NULL
                        ,CONCEPTO   text     NOT NULL
                        ,CANTIDAD   numeric  NOT NULL
                        ,RUBRO_ID   integer
                        ,CONSTRAINT I_ID_IT_PK PRIMARY KEY(INFO_ID AUTOINCREMENT)
                        ,CONSTRAINT INFO_RUBRO_R_ID_FK FOREIGN KEY (RUBRO_ID) REFERENCES Rubro (RUBRO_ID)
    '''

def insertTransacciones(Base, cursor, Operacion_ID, Fecha_hora, Info_ID, Dia_ID):
    Transacciones = '''INSERT INTO Transacciones
    VALUES(?, ? ,?, ?, ?);'''
    cursor.execute(Transacciones, (None, Operacion_ID, Fecha_hora, Info_ID, Dia_ID))
    Base.commit()
    """
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
    """
         
    

def insertFlujo(Base, cursor, Intervalo = None, Fecha_final = None, Intereses = None):
    Flujo = '''INSERT INTO Flujo
    VALUES(?, ?, ?, ?);'''
    cursor.execute(Flujo, (None, Intervalo, Fecha_final, Intereses))
    Base.commit()

    cursor.execute('''SELECT MAX(OPERACION_ID)
                        FROM Flujo''')
    fetchedData = cursor.fetchall()[0][0]
    print(f"La última operación de Flujo es: {fetchedData}")
    return fetchedData

    '''
            CREATE TABLE Flujo(
                        OPERACION_ID    integer NOT NULL
                        ,INTERVALO      numeric
                        ,FECHA_FINAL    date
                        ,INTERESES      numeric
                        ,CONSTRAINT O_ID_PK PRIMARY KEY(OPERACION_ID,TRANSACCION_ID)
                    );

    '''

#=============================================================================================================
#                                          ===Insertar un Dato===
#=============================================================================================================

# Función para insertar fechas en la tabla
def insertar_fechas(cursor, fecha_inicio, num_dias):
    fecha_actual = datetime.strptime(fecha_inicio, '%Y-%m-%d')
    for i in range(num_dias):
        print(i)
        fecha_actual += timedelta(days=1)
        cursor.execute('INSERT INTO Diario (FECHA) VALUES (?)', (fecha_actual.strftime('%Y-%m-%d'),))

#ctr.insertOperation(Base, cursor, Dia_ID, concepto,cantidad,rubro,intervalo,fecha_final,intereses)

def insertOperation(Base, cursor, Dia_ID, Concepto, Monto, Rubro = None, Intervalo = None, Fecha_final = None, Intereses = None):
    Operacion_ID = insertFlujo(Base, cursor, Intervalo, Fecha_final, Intereses)
    Info_ID = insertInfo_transaccciones(Base, cursor, Concepto, Monto, Rubro)
    
    Fecha_hora = datetime.now()
    print(f"La fecha y hora actual es: {Fecha_hora}")
    insertTransacciones(Base, cursor, Operacion_ID, Fecha_hora, Info_ID, Dia_ID)

def generarDias(Base, cursor, fecha_inicio, num_dias):
    fecha_actual = datetime.strptime(fecha_inicio, '%Y-%m-%d')
    for _ in range(num_dias):
        fecha_actual += timedelta(days=1)
        cursor.execute('INSERT INTO Diario (FECHA) VALUES (?)', (fecha_actual.strftime('%Y-%m-%d'),))
    Base.commit()    

#=============================================================================================================
#                                          === Modificar Tablas ===
#=============================================================================================================

def updateSaldos(Base, cursor, Dia_ID_Inicio, Dia_ID_Final):
    for Dia_ID in range(Dia_ID_Inicio, Dia_ID_Final):
        cursor.execute(
        f'''
            UPDATE Diario
                SET SALDO = DIA_SALDO + COALESCE((SELECT SALDO FROM Diario WHERE DIA_ID = {Dia_ID}), 0)
                WHERE DIA_ID = {Dia_ID} + 1
                AND EXISTS (SELECT 1 FROM Diario WHERE DIA_ID = {Dia_ID} + 1);
        
        '''
        )
    Base.commit()
                            




def modifTransacc():
    Transacciones = '''UPDATE Transacciones
                        SET '''

#=============================================================================================================
#                                          === IMPRESIONES ===
#=============================================================================================================

def printDiario(cursor):
    print("\n--------Imprimiendo Info Diario:")
    cursor.execute('''SELECT *
                        FROM Diario''')                 
    fetchedData = cursor.fetchall()
    for i in fetchedData:
        print(i)

def printSemanal(cursor):
    print("\n--------Imprimiendo Info Semanal:")
    cursor.execute('''SELECT *
                        FROM Semanal''')                 
    fetchedData = cursor.fetchall()
    for i in fetchedData:
        print(i)

def printMensual(cursor):
    print("\n--------Imprimiendo Info Mensual:")
    cursor.execute('''SELECT *
                        FROM Mensual''')                 
    fetchedData = cursor.fetchall()
    for i in fetchedData:
        print(i)

def printAnual(cursor):
    print("\n--------Imprimiendo Info Anual:")
    cursor.execute('''SELECT *
                        FROM Anual''')                 
    fetchedData = cursor.fetchall()
    for i in fetchedData:
        print(i)

def printRubro(cursor):
    print("\n--------Imprimiendo los Rubros:")
    cursor.execute('''SELECT *
                    FROM Rubro''')
    fetchedData = cursor.fetchall()
    for i in fetchedData:
        print(f'\t{i[0]}.-{i[1]}')


def printInfo_trasacciones(cursor):
    print("\n--------Imprimiendo Info Transacciones:")
    cursor.execute('''SELECT *
                        FROM Info_transacciones''')                 
    fetchedData = cursor.fetchall()
    for i in fetchedData:
        print(i)

def printTransacciones(cursor):
    print("\n--------Imprimiendo Transacciones:")
    cursor.execute('''SELECT *
                    FROM Transacciones''')
    fetchedData = cursor.fetchall()
    for i in fetchedData:
        print(i)

    
def printFlujo(cursor):
    print("\n--------Imprimiendo Flujos:")
    cursor.execute('''SELECT *
                    FROM Flujo''')
    fetchedData = cursor.fetchall()
    for i in fetchedData:
        print(i)

def printAll(cursor):
    printTransacciones(cursor)
    printInfo_trasacciones(cursor)
    printRubro(cursor)
    printFlujo(cursor)
    printDiario(cursor)
    printSemanal(cursor)
    printMensual(cursor)
    printAnual(cursor)

#=============================================================================================================
#                                          === Obtener datos ===
#=============================================================================================================
def obtener_Transacciones(Base, cursor, Dia_ID):
    cursor.execute(f'''SELECT T.TRANSACCION_ID, I.INFO_ID, I.CONCEPTO, I.MONTO, I.RUBRO_ID, R.TIPO
                      FROM Transacciones T 
                      JOIN Info_Transacciones I ON T.INFO_ID = I.INFO_ID  
                      LEFT JOIN RUBRO R ON I.RUBRO_ID = R.RUBRO_ID
                      WHERE T.DIA_ID = {Dia_ID}''')
    return cursor.fetchall()

def obtener_Anios(Base, cursor):
    valores  = cursor.execute('''SELECT FECHA FROM Diario''')

#=============================================================================================================
#                                          === CREACION DE USUARIO Y BASES ===
#=============================================================================================================

def modifTransacc():
    Transacciones = '''INSERT INTO Transacciones
    VALUES(?, ? ,?, ?, ?);'''

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

def base_Fecha():   
    regular = False
    s = ""
    while(not regular):
        s = input("Dame la fecha inicial en formato YYYY-MM-DD: ") #DD-MM-YYYY
        #s = año + '-' + mes + '-' + dia
        regular = bool(re.match(r'^\d{4}-\d{2}-\d{2}$',s)) #Hacer un validador de días, meses y años para la interfaz: le toca a Salazar
        if(regular != True):
            print("Formato incorrecto, vuelve a intentarlo.")
        else:
            if validar_fecha(s) == False:      
                print("Fecha está en el futuro, vuelva a intentarlo.")
                regular = False
            else:
                print(f"Fecha aceptada, la base inicia el: {s}")
    return s
'''

'''
def diferencia(cursor, str_fin, str_inicio, tipo):

    query = f'''
    SELECT (strftime('%{tipo}', '{str_fin}') - strftime('%{tipo}', '{str_inicio}'));
    '''
    cursor.execute(query)
    fetchedData = cursor.fetchall()  
    return fetchedData[0][0]

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
def fecha_Max(cursor):
    cursor.execute("""SELECT MAX(FECHA) FROM Diario""")
    Fecha = cursor.fetchall()[0][0]
    cursor.execute("""SELECT MAX(DIA_ID) FROM Diario""")
    Dia_ID = cursor.fetchall()[0][0]
    return Fecha, Dia_ID

def fecha_Dia_ID(cursor, Fecha):
    cursor.execute(f'''SELECT DIA_ID FROM Diario
                      WHERE FECHA = "{Fecha}"''')
    Dia_ID = cursor.fetchall()[0][0]
    print(f'El día ID de {Fecha} es {Dia_ID}.')
    return Dia_ID


def datos_Semana(cursor):
    pass
    cursor.execute()
