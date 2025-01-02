import sqlite3 as sql
from . import Base_Creacion as bc
from urllib.request import pathname2url
import os
import sys
from os import path
import re
from pathlib import Path
from datetime import datetime, timedelta

# Obtenemos la ruta raíz del proyecto
raiz = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(raiz)

# Definimos la carpeta donde se guardarán las bases de datos
BD_DIR = path.join(raiz, 'base_datos')

# Creamos la carpeta BD si no existe
if not path.exists(BD_DIR):
    os.makedirs(BD_DIR)

#=============================================================================================================
#                                          === INSERCIONES ===
#=============================================================================================================
#No hemos avanzado con el proyecto
def insertFecha(Base, cursor, Fecha):
    Diario = """INSERT INTO Diario
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    cursor.execute(Diario, (None,Fecha,0,0,0,0,0,0,0))

    Base.commit()

    Semanal = """INSERT INTO Semanal
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    cursor.execute(Semanal, (None,1,None,0,0,0,0,0,0,0))

    Mensual = """INSERT INTO Mensual
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    cursor.execute(Mensual, (None,1,None,0,0,0,0,0,0,0))

    Base.commit()
    Anual = """INSERT INTO Anual
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    cursor.execute(Anual, (None,1,None,0,0,0,0,0,0,0))

    Base.commit()
'''
INSERT INTO Diario VALUES (Null,'2023-07-23',0,0,0,0,0,0,0);
INSERT INTO Semanal VALUES (Null,'2023-07-23',Null,0,0,0,0,0,0,0);
INSERT INTO Mensual VALUES (Null,'2023-07-23',Null,0,0,0,0,0,0,0);
INSERT INTO Anual VALUES (Null,'2023-07-23',Null,0,0,0,0,0,0,0);

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
    
    cursor.execute('''SELECT RUBRO_ID
                    FROM Rubro
                    WHERE UPPER(TIPO) = "{}"'''.format(Tipo))
   
    return cursor.fetchall()[0][0]
        
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
    VALUES(?, ?, ?, ?, ?);'''
    cursor.execute(Flujo, (None, Intervalo, Fecha_final, Intereses, None))
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

def updateOperacion (Base, cursor, Tupla):
    # [(CONCEPTO, MONTO, TIPO, INTERVALO, FECHA_FINAL, INTERESES, TRANSACCION_ID, OPERACION_ID, INFO_ID)]                         
    CONCEPTO, MONTO, TIPO, INTERVALO, FECHA_FINAL, INTERESES, TRANSACCION_ID, OPERACION_ID, INFO_ID = Tupla[0], Tupla[1], Tupla[2], Tupla[3], Tupla[4], Tupla[5], Tupla[6], Tupla[7], Tupla[8]
    cursor.execute(f'''
                UPDATE Transacciones
                SET FECHA = {datetime.now}
                WHERE TRANSACCION_ID = {TRANSACCION_ID}
                ''')    
    # Para comprobar que exista un rubro
    if TIPO:
        RUBRO_ID = insertRubro(cursor, TIPO)
    else:
        RUBRO_ID = None
    
    cursor.execute(f'''
            UPDATE Info_transacciones
            SET 
                CONCEPTO  = {CONCEPTO}    
                ,MONTO    = {MONTO}
                ,RUBRO_ID = {RUBRO_ID}

            WHERE INFO_ID = {INFO_ID}
            ''') # Se puede mejorar la eficiencia, haciendo que si el monto ha permanecido igual entonces no acualice monto para no encender algunos triggers.   

    # Sólo en caso de que se se tenga intervalo
    if INTERVALO:
        cursor.execute(f'''
                    UPDATE Flujo
                    SET 
                        INTERVALO    = {INTERVALO}
                        ,FECHA_FINAL = {FECHA_FINAL}   
                        ,INTERESES   = {INTERESES}

                    WHERE OPERACION_ID = {OPERACION_ID}
                    ''')
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
                                #concepto, monto, rubro, intervalo, fecha_final, intereses
    cursor.execute(f'''SELECT I.CONCEPTO, I.MONTO, R.TIPO, O.INTERVALO, O.FECHA_FINAL, O.INTERESES, T.TRANSACCION_ID, T.OPERACION_ID, I.INFO_ID
                      FROM Transacciones T 
                      JOIN Info_Transacciones I ON T.INFO_ID = I.INFO_ID
                      JOIN Flujo O ON T.OPERACION_ID = O.OPERACION_ID
                      LEFT JOIN RUBRO R ON I.RUBRO_ID = R.RUBRO_ID
                      WHERE T.DIA_ID = {Dia_ID}''')
    return cursor.fetchall()

def obtener_Anios(cursor):
    cursor.execute('''SELECT D.FECHA
                      FROM Diario D
                      JOIN Anual A ON D.DIA_ID = A.ANIO_INICIO;
                      ''')
    fetchedData = cursor.fetchall()
    anios = []
    # fectchedData = [(2023-02-01,), (2024-01-01,), (2025-01-01,)]
    for tupla in fetchedData:
        anios.append(tupla[0][:4])
    return anios

def obtener_Meses(cursor, anio):
    cursor.execute(f'''SELECT D.FECHA 
                       FROM Mensual M
                       JOIN Diario D ON M.MES_INICIO = D.DIA_ID
                       WHERE strftime('%Y', D.FECHA) = '{anio}';
                        ''')
    fetchedData = cursor.fetchall()
    meses = []
    # fectchedData = [(2023-02-01,), (2024-01-01,), (2025-01-01,)]
    for tupla in fetchedData:
    # Extrae el mes de la fecha
        mes = tupla[0][5:7]  # '02', '01', '11'
    # Elimina el cero inicial si existe
        meses.append(mes.lstrip('0'))
    return meses


def obtener_Dias(cursor, mes, anio):
    cursor.execute(f'''SELECT FECHA
                       FROM Diario
                       WHERE strftime('%Y', FECHA) = '{anio}'
                       AND  strftime('%m', FECHA) = '{mes}';
                   ''')
    fetchedData = cursor.fetchall()
    dias = []
    # fectchedData = [(2023-02-01,), (2024-01-01,), (2025-01-01,)]
    for tupla in fetchedData:
        dia = tupla[0][-2:]
        dias.append(dia.lstrip('0'))
    return dias
#=============================================================================================================
#                                          === CREACION DE USUARIO Y BASES ===
#=============================================================================================================

def modifTransacc(): # ¿Este es útil?
    Transacciones = '''INSERT INTO Transacciones
    VALUES(?, ? ,?, ?, ?);'''

def nombre_BD(Nombre):
    # Ahora retornamos sólo el nombre del archivo
    return f"{Nombre.strip()}.db"

def verificar_BD(Nombre):
    # Construimos la ruta completa usando path.join
    ruta_bd = path.join(BD_DIR, nombre_BD(Nombre))
    if path.exists(ruta_bd):
        print("La base de datos existe.")
        return True
    else:
        print("La base de datos no existe.")
        return False

def usuarios_Dir(Base_Nombre):
    # Simplemente retornamos la ruta completa de la base de datos
    return path.join(BD_DIR, Base_Nombre)

def base_Inicializar(Opcion, Nombre, Fecha = None): #Opción 1 para crear base y 2 (o cualquiera realmente) para conectarse directamente.
    
    Base_Nombre = Nombre.strip() + ".db"                                               
    #Si no existe una base de datos, entonces se debe crea.
    archivo_en_carpeta = usuarios_Dir(Base_Nombre)
    Base = sql.connect(archivo_en_carpeta)
    cursor = Base.cursor()
    match Opcion:
        case 1:
            #Por estar vacia 
            bc.Creacion_Tablas(Base, cursor)
            insertFecha(Base, cursor, Fecha)
            # cursor.execute(insertDiario, (None,Fecha,None,None,None,None,None,None,None)) #Se debe sustituir por Base_Insercion
            print("La base ha sido creada")
    print("\t.::Conectando a {}::." .format(Base_Nombre))   


    #Para no tener que cerrar la conexión la devolvemos
    return Base, cursor

#=============================================================================================================
#                                          === CONSULTAS ===
#=============================================================================================================

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
