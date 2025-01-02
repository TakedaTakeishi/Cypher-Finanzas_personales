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


def fecha_compara(Fecha_principal, Fecha_secundaria):
    if (type(Fecha_principal) is not datetime):
        F_principal = datetime.strptime(Fecha_principal, "%Y-%m-%d")
    if (type(Fecha_secundaria) is not datetime):
        F_secundaria = datetime.strptime(Fecha_secundaria, "%Y-%m-%d")
    if F_principal != F_secundaria:
        return (F_principal - F_secundaria).days
    else:
        return 0

#=============================================================================================================
#                                          === CONSULTAS ===
#=============================================================================================================

def fecha_Max(cursor):
    cursor.execute("""SELECT MAX(FECHA) FROM Diario""")
    Fecha = cursor.fetchall()[0][0]
    cursor.execute("""SELECT MAX(DIA_ID) FROM Diario""")
    Dia_ID = cursor.fetchall()[0][0]
    return Fecha, Dia_ID

def ID_de_fecha(cursor, Fecha):
    cursor.execute(f'''SELECT DIA_ID FROM Diario
                      WHERE FECHA = "{Fecha}"''')
    Dia_ID = cursor.fetchall()[0][0]
    print(f'El día ID de {Fecha} es {Dia_ID}.')
    return Dia_ID

def fecha_de_ID(cursor, Dia_ID):
    cursor.execute(f'''SELECT FECHA FROM Diario
                      WHERE DIA_ID = {Dia_ID}''')
    Fecha = cursor.fetchall()[0][0]
    return Fecha

def datos_Semana(cursor):
    pass
    cursor.execute()

def consulta_intervalos(cursor):
    consulta = '''SELECT OPERACION_ID FROM FLUJO
                WHERE INTERVALO IS NOT NULL'''
    cursor.execute(consulta)
    return cursor.fetchall()

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



def insertInfo_transaccciones(Base, cursor, Concepto, Monto, Rubro = None, Compuesto = None):
    Info_Transacciones = '''INSERT INTO Info_transacciones
    VALUES(?, ?, ?, ?, ?);'''
    if(Rubro):
        Rubro_id = insertRubro(cursor, Rubro)
    else:
        Rubro_id = None
    cursor.execute(Info_Transacciones, (None, Concepto, Monto, Rubro_id, Compuesto)) #Falta verificar el rubro_id de rubro
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

def insertTransacciones(Base, cursor, Operacion_ID, Fecha_hora, Info_ID, Dia_ID, Actualizar = None):
    Transacciones = '''INSERT INTO Transacciones
    VALUES(?, ? ,?, ?, ?, ?);'''
    cursor.execute(Transacciones, (None, Operacion_ID, Fecha_hora, Info_ID, Dia_ID, Actualizar))
    Base.commit()
    """
                  CREATE TABLE Transacciones(
                            TRANSACCION_ID      integer  NOT NULL
                            ,OPERACION_ID       integer  NOT NULL
                            ,FECHA              datetime NOT NULL
                            ,INFO_ID            integer  NOT NULL
                            ,DIA_ID             integer  NOT NULL
                            ,ACTUALIZAR         date     
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

# Para obtener los días que se tienen que sumar
def dato_Intervalo_decodificacion(Codigo, fecha_actual=None):
    """
    Decodifica el intervalo y retorna los días a sumar.
    Args:
        Codigo: El código del intervalo (-5 a 7 o números positivos mayores)
        fecha_actual: Fecha actual para cálculos especiales (formato YYYY-MM-DD)
    Returns:
        int: Número de días a sumar
    """
    from calendar import monthrange
    from datetime import datetime, timedelta

    # Para códigos positivos directos (incluye semanal=7)
    if Codigo > 0:
        return Codigo
    
    # Si no se proporciona fecha_actual, usar la fecha del sistema
    if fecha_actual is None:
        fecha_actual = datetime.now()
    elif isinstance(fecha_actual, str):
        fecha_actual = datetime.strptime(fecha_actual, '%Y-%m-%d')

    match Codigo:
        case -1:  # Mensual
            # Obtener el último día del mes actual
            _, ultimo_dia = monthrange(fecha_actual.year, fecha_actual.month)
            # Si estamos en el último mes del año
            if fecha_actual.month == 12:
                siguiente_fecha = datetime(fecha_actual.year + 1, 1, fecha_actual.day)
            else:
                # Intentar crear la fecha del siguiente mes
                try:
                    siguiente_fecha = datetime(fecha_actual.year, fecha_actual.month + 1, fecha_actual.day)
                except ValueError:
                    # Si el día no existe en el siguiente mes, usar el último día
                    siguiente_fecha = datetime(fecha_actual.year, fecha_actual.month + 1, 1) - timedelta(days=1)
            
            return (siguiente_fecha - fecha_actual).days

        case -2:  # Fin del mes de febrero
            # Calcular días hasta el próximo febrero
            if fecha_actual.month < 2:
                proximo_feb = datetime(fecha_actual.year, 2, 29)
            else:
                proximo_feb = datetime(fecha_actual.year + 1, 2, 29)
            try:
                # Intentar con 29 (año bisiesto)
                return (proximo_feb - fecha_actual).days
            except ValueError:
                # Si no es bisiesto, usar 28
                return (proximo_feb.replace(day=28) - fecha_actual).days

        case -3:  # Cada 28
            return 28

        case -4:  # Fin de mes
            # Calcular días hasta el fin del mes actual
            _, ultimo_dia = monthrange(fecha_actual.year, fecha_actual.month)
            fin_mes = datetime(fecha_actual.year, fecha_actual.month, ultimo_dia)
            if fecha_actual.day == ultimo_dia:
                # Si ya estamos en fin de mes, calcular el siguiente
                if fecha_actual.month == 12:
                    siguiente_fecha = datetime(fecha_actual.year + 1, 1, 31)
                else:
                    _, siguiente_ultimo = monthrange(fecha_actual.year, fecha_actual.month + 1)
                    siguiente_fecha = datetime(fecha_actual.year, fecha_actual.month + 1, siguiente_ultimo)
                return (siguiente_fecha - fecha_actual).days
            return (fin_mes - fecha_actual).days

        case -5:  # Anual
            # Calcular días hasta la misma fecha del próximo año
            try:
                siguiente_fecha = datetime(fecha_actual.year + 1, fecha_actual.month, fecha_actual.day)
            except ValueError:
                # Si es 29 de febrero y el siguiente año no es bisiesto
                siguiente_fecha = datetime(fecha_actual.year + 1, 2, 28)
            return (siguiente_fecha - fecha_actual).days

        case _:
            return None
    

#ctr.insertOperation(Base, cursor, Dia_ID, concepto,cantidad,rubro,intervalo,fecha_final,intereses)
def insertOperation(Base, cursor, Dia_ID, Concepto, Monto, Rubro = None, Intervalo = None, Fecha_final = None, Intereses = None):
    Operacion_ID = insertFlujo(Base, cursor, Intervalo, Fecha_final, Intereses)
    Info_ID = insertInfo_transaccciones(Base, cursor, Concepto, Monto, Rubro)
    
    Fecha_hora = datetime.now()
    print(f"La fecha y hora actual es: {Fecha_hora}")
    fecha = fecha_de_ID(cursor, Dia_ID)
    if Intervalo:
        # Entonces Actualizar es la fecha + el intervalo
        # Aquí necesitamos una función que haga que el intervalo sea un número que podamos sumar a la fecha
        Actualizar = fecha + timedelta(days=dato_Intervalo_decodificacion(Intervalo, fecha))
    else:
        Actualizar = None
    insertTransacciones(Base, cursor, Operacion_ID, Fecha_hora, Info_ID, Dia_ID, Actualizar)

def generarDias(Base, cursor, fecha_inicio, num_dias):
    fecha_actual = datetime.strptime(fecha_inicio, '%Y-%m-%d')
    for _ in range(num_dias):
        fecha_actual += timedelta(days=1)
        cursor.execute('INSERT INTO Diario (FECHA) VALUES (?)', (fecha_actual.strftime('%Y-%m-%d'),))
    Base.commit()    


# Funciones para agregar transacciones recurrentes

# Las que cumplen con la fecha de actualización
def se_actualizan(cursor, intervalos, fecha_str):
    intervalos_lista = [i[0] for i in intervalos]
    # Usamos map para convertir los elementos de intervalos_lista de número a string
    # Luego a eso le aplicamos join para unir los elementos con comas
    consulta =  f'''SELECT TRANSACCION_ID FROM TRANSACCIONES
                    WHERE OPERACION_ID IN ({','.join(map(str, intervalos_lista))})
                    AND ACTUALIZAR = "{fecha_str}"'''
    cursor.execute(consulta)
    return cursor.fetchall()

def agregar_recurrentes(Base, cursor, cumplen, fecha_str):
    id_fecha = ID_de_fecha(cursor, fecha_str)
    for tupla in cumplen:
        consulta = f'''SELECT F.INTERVALO, F.INTERESES, F.FECHA_FINAL, F.OPREACION_ID, T.INFO_ID, I.MONTO, I.COMPUESTO, I.CONCEPTO, D.FECHA, R.RUBRO
                        FROM FLUJO F
                        JOIN TRANSACCIONES T ON F.OPERACION_ID = T.OPERACION_ID
                        JOIN INFO_TRANSACCIONES I ON T.INFO_ID = I.INFO_ID
                        JOIN DIARIO D ON T.DIA_ID = D.DIA_ID
                        LEFT JOIN RUBRO R ON I.RUBRO_ID = R.RUBRO_ID
                        WHERE T.TRANSACCION_ID = {tupla[0]}'''
        cursor.execute(consulta)
        intervalo, intereses, fecha_final, operacion_id, info_id, monto, compuesto, concepto, fecha, rubro = cursor.fetchall()[0]
        if fecha_compara(fecha_str, fecha_final) >= 0:
            actualiza = '''UPDATE FLUJO SET INTERVALO = NULL
                            WHERE OPERACION_ID = {operacion_id}'''
            cursor.execute(actualiza)
        else:
            if intereses:
                if compuesto:
                    nuevo_monto = compuesto * intereses
                    nuevo_compuesto = compuesto + nuevo_monto
                else:
                    nuevo_monto = monto * intereses
                    nuevo_compuesto = monto + nuevo_monto
                nuevo_info_id = insertInfo_transaccciones(Base, cursor, f'Intereses: {concepto}', nuevo_monto, rubro, nuevo_compuesto)
            else:
                nuevo_info_id = info_id

            Actualizar = fecha + timedelta(days=dato_Intervalo_decodificacion(intervalo, fecha))
            Fecha_hora = datetime.now()
            
            insertTransacciones(Base, cursor, operacion_id, Fecha_hora, nuevo_info_id, id_fecha, Actualizar) 
            
        
    Base.commit()

def insertar_recurrencias(Base, cursor, fecha_objeto):
    fecha_str = fecha_objeto.strftime('%Y-%m-%d')
    intervalos = consulta_intervalos(cursor)
    if intervalos:
        cumplen = se_actualizan(cursor, intervalos, fecha_str)
        if cumplen:
            agregar_recurrentes(Base, cursor, cumplen, fecha_str)
# Función para actualizar el promedio, la media y la mediana de un día determinado
def actualizar_estadisticas(Base, cursor, fecha_objeto_anterior):    
    fecha_id = ID_de_fecha(cursor, fecha_objeto_anterior.strftime('%Y-%m-%d'))
    # Obtenemos el saldo del día anterior
    cursor.execute(f'SELECT SALDO FROM DIARIO WHERE DIA_ID = {fecha_id}')
    saldo_anterior = cursor.fetchall()[0][0]
    # Ahora hacemos el promedio con saldo anterior / id del día
    promedio = saldo_anterior / fecha_id
    # Se obtiene la mediana y la moda de todos los días hasta la fecha
    # Pimero los saldos ordenados de menor a mayor
    cursor.execute('SELECT SALDO FROM DIARIO ORDER BY SALDO WHERE DIA_ID <= ?', (fecha_id,))
    saldos = cursor.fetchall()
    # Ahora obtenemos la mediana
    if len(saldos) % 2 == 0:
        mediana = (saldos[len(saldos) // 2 - 1] + saldos[len(saldos) // 2]) / 2
    else:
        mediana = saldos[len(saldos) // 2]
    # Ahora obtenemos la moda
    # Lo hacemos usando conjunto para obtener los valores únicos y luego el valor que más se repite
    moda = max(set(saldos), key=saldos.count)
    # Actualizamos los valores en la tabla en el día correspondiente
    cursor.execute('UPDATE DIARIO SET PROMEDIO = ?, MEDIANA = ?, MODA = ? WHERE DIA_ID = ?', (promedio, mediana, moda, fecha_id))
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

