import sqlite3 as sql
from . import Base_Creacion as bc
import os
import sys
from os import path
from datetime import datetime, timedelta
from calendar import monthrange

# Obtenemos la ruta raíz del proyecto
raiz = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(raiz)

# Definimos la carpeta donde se guardarán las bases de datos
BD_DIR = path.join(raiz, 'base_datos')

# Creamos la carpeta BD si no existe
if not path.exists(BD_DIR):
    os.makedirs(BD_DIR)


def fecha_compara(Fecha_primaria, Fecha_secundaria):
    F_primaria = datetime.strptime(Fecha_primaria, "%Y-%m-%d").date()
    F_secundaria = datetime.strptime(Fecha_secundaria, "%Y-%m-%d").date()
    diferencia = (F_primaria - F_secundaria).days
    return diferencia

#=============================================================================================================
#                                          === CONSULTAS ===
#=============================================================================================================
def calcular_saldo_dia(cursor, dia_id):
# Obtener la suma de todos los movimientos del día
    cursor.execute('''
        SELECT COALESCE(SUM(i.MONTO), 0)
        FROM Transacciones t
        JOIN Info_transacciones i ON t.INFO_ID = i.INFO_ID
        WHERE t.DIA_ID = ?
    ''', (dia_id,))
    return cursor.fetchone()[0]

def calcular_saldo_anterior(cursor, dia_id):
    if dia_id > 1:
        cursor.execute('SELECT SALDO FROM Diario WHERE DIA_ID = ?', (dia_id - 1,))
        saldo_anterior = cursor.fetchone()[0]
    else:
        saldo_anterior = 0
    return saldo_anterior

def actualizar_saldo_diario(cursor, dia_id: int, saldo_dia: int, saldo_anterior: int):
    # Actualizar saldo del día
    cursor.execute('''
        UPDATE Diario 
        SET DIA_SALDO = ?,
            SALDO = ? + ?
        WHERE DIA_ID = ?
    ''', (saldo_dia, saldo_anterior, saldo_dia, dia_id))

def fecha_Max(cursor):
    cursor.execute('''SELECT MAX(FECHA), MAX(DIA_ID)
                    FROM Diario''')
    fetchedData = cursor.fetchall()
    # Retornamos la fecha y el ID
    return fetchedData[0][0], fetchedData[0][1]

def ID_de_fecha(cursor, fecha_str: str):
    cursor.execute('''SELECT DIA_ID
                    FROM Diario
                    WHERE FECHA = ?''', (fecha_str,))
    # Usamos fetchone para obtener un solo resultado
    resultado = cursor.fetchone()
    if resultado is None:
        raise ValueError(f"No se encontró ningún ID para la fecha {fecha_str}")
    return resultado[0]

def fecha_de_ID(cursor, Dia_ID):
    cursor.execute('''SELECT FECHA 
                    FROM Diario
                    WHERE DIA_ID = ?''', (Dia_ID,))
    resultados = cursor.fetchall()
    if not resultados:
        raise ValueError(f"No se encontró ninguna fecha para el ID {Dia_ID}")
    fecha_str = resultados[0][0]
    return datetime.strptime(fecha_str, "%Y-%m-%d").date()

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
         
    

def insertFlujo(Base, cursor, Intervalo = None, Fecha_final = None, Intereses = None, Estado = True):
    Flujo = '''INSERT INTO Flujo
    VALUES(?, ?, ?, ?, ?);'''
    cursor.execute(Flujo, (None, Intervalo, Fecha_final, Intereses, Estado))
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
    fecha_actual = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
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
        fecha_actual = datetime.now().date()
    elif isinstance(fecha_actual, str):
        fecha_actual = datetime.strptime(fecha_actual, '%Y-%m-%d').date()

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

def ultimo_dia_mes(fecha_actual: datetime.date):
    """
    Determina si la fecha dada es el último día del mes.
    Args:
        fecha_actual: Fecha a evaluar
    Returns:
        bool: True si es el último día del mes, False en caso contrario
    """
    

def generarDias(Base, cursor, fecha_inicio: str, num_dias: int):
    """
    Genera los días desde la fecha de inicio hasta la fecha de inicio + num_dias. Además si este día es fin de
    semana, mes o año, se generan los registros correspondientes en las tablas semanales, mensuales y anuales.
    Args:
        Base: Conexión a la base de datos
        cursor: Cursor de la base de datos
        fecha_inicio: Fecha de inicio en formato YYYY-MM-DD
        num_dias: Número de días a generar
    Returns:
        None (la base se actualiza directamente)
    """
    fecha_actual = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()

        
    for _ in range(num_dias):
        fecha_actual += timedelta(days=1)
        cursor.execute('INSERT INTO Diario (FECHA) VALUES (?)', (fecha_actual.strftime('%Y-%m-%d'),))
        # Si es inicio de semana, mes o año, insertar en las tablas correspondientes
        if fecha_actual.day == 1:
            # Es inicio de mes
            cursor.execute('INSERT INTO Mensual (MES_INICIO) VALUES (?)', (fecha_actual.strftime('%Y-%m-%d'),))
            # El día es el último día del mes
            if ultimo_dia_mes(fecha_actual):
                cursor.execute('INSERT INTO Mensual (MES_FINAL) VALUES (?)', (fecha_actual.strftime('%Y-%m-%d'),))  


        if fecha_actual.month == 1:
            # Es inicio de año
            cursor.execute('INSERT INTO Anual (ANIO_INICIO) VALUES (?)', (fecha_actual.strftime('%Y-%m-%d'),))
    Base.commit()    


# -------------- Funciones para agregar actualizaciones de operaciones --------------
def es_fin_de(fecha: datetime) -> dict:
    """
    Determina si una fecha es fin de semana, mes o año
    
    Args:
        fecha: datetime object
    Returns:
        dict: Diccionario indicando si es fin de cada periodo
    """
    # Obtener el último día del mes actual
    ultimo_dia_mes = monthrange(fecha.year, fecha.month)[1]
    
    return {
        'semana': fecha.weekday() >= 5,  # 5=Sábado, 6=Domingo
        'mes': fecha.day == ultimo_dia_mes,
        'año': fecha.month == 12 and fecha.day == 31
    }


# Función para actualizar la información de las tablas diario, semanal, mensual y anual
def actualizar_periodos_financieros(Base, cursor, fecha_objeto):
    """
    Actualiza la información de las tablas diario, semanal, mensual y anual con los datos del intervalo
    Args:
        Base: Conexión a la base de datos
        cursor: Cursor de la base de datos
        fecha_objeto: Fecha de la actualización en formato datetime.date
    Returns:
        None (la base se actualiza directamente)

    """
    # Primero veamos si la fecha es inicio de semana, mes o año
    

def actualizar_diario(Base, cursor, fecha_objeto):
    # 1. Insertar movimientos recurrentes
    insertar_recurrencias(Base, cursor, fecha_objeto.strftime('%Y-%m-%d'))
    
    # 2. Calcular y actualizar saldo del día
    fecha_actual = fecha_objeto.strftime('%Y-%m-%d')
    dia_id = ID_de_fecha(cursor, fecha_actual)
    
    # Obtener saldo del día
    saldo_dia = calcular_saldo_dia(cursor, dia_id)
    
    # Obtener saldo anterior
    saldo_anterior = calcular_saldo_anterior(cursor, dia_id)
    
    # Actualizar saldo del día
    actualizar_saldo_diario(cursor, dia_id, saldo_dia, saldo_anterior)
    
    Base.commit()
    
    # 3. Actualizar estadísticas con el nuevo saldo
    actualizar_estadisticas(Base, cursor, fecha_objeto)

# Las que cumplen con la fecha de actualización
def se_actualizan(cursor, intervalos, fecha_str):
    intervalos_lista = [i[0] for i in intervalos]
    print(f"\nBuscando operaciones que se actualizan en {fecha_str}")
    print(f"Operaciones con intervalo: {intervalos_lista}")
    
    # Modificamos la consulta para usar strftime y comparar solo las fechas
    consulta = '''SELECT T.TRANSACCION_ID, T.ACTUALIZAR, F.INTERVALO, I.CONCEPTO 
                 FROM TRANSACCIONES T
                 JOIN FLUJO F ON T.OPERACION_ID = F.OPERACION_ID
                 JOIN INFO_TRANSACCIONES I ON T.INFO_ID = I.INFO_ID
                 WHERE F.OPERACION_ID IN ({})
                 AND date(T.ACTUALIZAR) = ?
                 AND F.ESTADO = TRUE'''.format(','.join(['?'] * len(intervalos_lista)))
    
    try:
        cursor.execute(consulta, intervalos_lista + [fecha_str])
        resultados = cursor.fetchall()
        print("\nTransacciones encontradas:")
        for r in resultados:
            print(f"ID: {r[0]}, Fecha actualización: {r[1]}, Intervalo: {r[2]}, Concepto: {r[3]}")
        return resultados
    except Exception as e:
        print(f"Error en la consulta: {e}")
        print(f"Consulta ejecutada: {consulta}")
        print(f"Parámetros: {intervalos_lista + [fecha_str]}")
        return []

def agregar_recurrentes(Base, cursor, cumplen, fecha_str):

    id_fecha = ID_de_fecha(cursor, fecha_str)
    print(f"\nProcesando {len(cumplen)} transacciones recurrentes para fecha {fecha_str}")
    
    for tupla in cumplen:
        consulta = f'''SELECT F.INTERVALO, F.INTERESES, F.FECHA_FINAL, F.OPERACION_ID, T.INFO_ID, I.MONTO, I.COMPUESTO, I.CONCEPTO, R.TIPO
                        FROM FLUJO F
                        JOIN TRANSACCIONES T ON F.OPERACION_ID = T.OPERACION_ID
                        JOIN INFO_TRANSACCIONES I ON T.INFO_ID = I.INFO_ID
                        JOIN DIARIO D ON T.DIA_ID = D.DIA_ID
                        LEFT JOIN RUBRO R ON I.RUBRO_ID = R.RUBRO_ID
                        WHERE T.TRANSACCION_ID = {tupla[0]}'''
        cursor.execute(consulta)
        resultado = cursor.fetchall()[0]
        intervalo, intereses, fecha_final, operacion_id, info_id, monto, compuesto, concepto, rubro = resultado
        
        # Verificar si la operación debe terminar, es mayor a 1 para que se ejecute en la fecha final
        if fecha_final is not None and fecha_compara(fecha_str, fecha_final) >= 1:
            # Actualizar para marcar que la operación recurrente ha terminado
            cursor.execute('UPDATE FLUJO SET INTERVALO = NULL WHERE OPERACION_ID = ?', (operacion_id,))
        else:
            if intereses:
                if compuesto:
                    nuevo_monto = compuesto * intereses
                    nuevo_compuesto = compuesto + nuevo_monto
                else:
                    nuevo_monto = monto * intereses
                    nuevo_compuesto = monto + nuevo_monto
                nuevo_info_id = insertInfo_transaccciones(Base, cursor, concepto, nuevo_monto, rubro, nuevo_compuesto)
            else:
                nuevo_info_id = info_id
            # Como todos cumplen que se actualizan hoy, entonces podemos usar fecha_str
            Actualizar = datetime.strptime(fecha_str, '%Y-%m-%d').date() + timedelta(days=dato_Intervalo_decodificacion(intervalo, fecha_str))
            Fecha_hora = datetime.now()
            
            insertTransacciones(Base, cursor, operacion_id, Fecha_hora, nuevo_info_id, id_fecha, Actualizar) 
            
        
    Base.commit()

def insertar_recurrencias(Base, cursor, fecha_str: str):
    print(f"\nBuscando recurrencias para fecha: {fecha_str}")
    
    intervalos = consulta_intervalos(cursor)
    print(f"Total de operaciones con intervalo: {len(intervalos)}")

    # Ejecutar diagnóstico
    diagnostico_recurrencias(cursor, fecha_str)
    
    if intervalos:
        cumplen = se_actualizan(cursor, intervalos, fecha_str)
        if cumplen:
            agregar_recurrentes(Base, cursor, cumplen, fecha_str)
        else:
            print("No hay operaciones para actualizar en esta fecha")
    else:
        print("No hay operaciones recurrentes configuradas")

# Función para actualizar el promedio, la media y la mediana de un día determinado
def actualizar_estadisticas(Base, cursor, fecha_objeto):    
    fecha_id = ID_de_fecha(cursor, fecha_objeto.strftime('%Y-%m-%d'))
    
    # Obtener todos los saldos hasta la fecha actual
    cursor.execute('SELECT SALDO FROM DIARIO WHERE DIA_ID <= ? ORDER BY SALDO', (fecha_id,))
    saldos = [row[0] for row in cursor.fetchall()]
    
    if not saldos:
        return
        
    # Calcular estadísticas
    promedio = sum(saldos) / len(saldos)
    
    # Mediana
    if len(saldos) % 2 == 0:
        mediana = (saldos[len(saldos)//2 - 1] + saldos[len(saldos)//2]) / 2
    else:
        mediana = saldos[len(saldos)//2]
    
    # Moda
    from collections import Counter
    moda = Counter(saldos).most_common(1)[0][0]
    
    # Actualizar estadísticas
    cursor.execute('''
        UPDATE DIARIO 
        SET PROMEDIO = ?,
            MEDIANA = ?,
            MODA = ?
        WHERE DIA_ID = ?
    ''', (promedio, mediana, moda, fecha_id))
    
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

def diagnostico_recurrencias(cursor, fecha_str):
    """Función para diagnosticar por qué no se encuentran las recurrencias"""
    print("\n=== Diagnóstico de Recurrencias ===")
    
    # 1. Verificar todas las operaciones con intervalo
    cursor.execute("""
        SELECT F.OPERACION_ID, F.INTERVALO, F.FECHA_FINAL, F.ESTADO,
               T.ACTUALIZAR, I.CONCEPTO
        FROM FLUJO F
        JOIN TRANSACCIONES T ON F.OPERACION_ID = T.OPERACION_ID
        JOIN INFO_TRANSACCIONES I ON T.INFO_ID = I.INFO_ID
        WHERE F.INTERVALO IS NOT NULL
    """)
    operaciones = cursor.fetchall()
    
    print(f"\nOperaciones recurrentes encontradas: {len(operaciones)}")
    for op in operaciones:
        print(f"""
        Operación ID: {op[0]}
        - Intervalo: {op[1]}
        - Fecha final: {op[2]}
        - Estado: {op[3]}
        - Próxima actualización: {op[4]}
        - Concepto: {op[5]}
        """)
    
    # 2. Verificar específicamente las actualizaciones para la fecha dada
    cursor.execute("""
        SELECT COUNT(*) 
        FROM TRANSACCIONES 
        WHERE ACTUALIZAR = ?
    """, (fecha_str,))
    count = cursor.fetchone()[0]
    print(f"\nActualizaciones programadas para {fecha_str}: {count}")


# ========================================================================================
#                                         === Obtener Datos ===
# ========================================================================================

def obtener_datos_mensuales(cursor):
    """Obtiene datos mensuales de transacciones."""
    query = '''
        SELECT 
            strftime('%Y-%m', d.FECHA) as YearMonth,
            SUM(CASE WHEN i.MONTO > 0 THEN i.MONTO ELSE 0 END) as Ingresos,
            SUM(CASE WHEN i.MONTO < 0 THEN ABS(i.MONTO) ELSE 0 END) as Egresos,
            SUM(i.MONTO) as Saldo
        FROM Diario d
        LEFT JOIN Transacciones t ON d.DIA_ID = t.DIA_ID
        LEFT JOIN Info_transacciones i ON t.INFO_ID = i.INFO_ID
        GROUP BY strftime('%Y-%m', d.FECHA)
        ORDER BY YearMonth
    '''
    cursor.execute(query)
    return cursor.fetchall()

def obtener_datos_categorias(cursor):
    """Obtiene datos por categoría (rubro)."""
    query = '''
        SELECT 
            r.TIPO,
            SUM(CASE WHEN i.MONTO > 0 THEN i.MONTO ELSE 0 END) as Ingresos,
            SUM(CASE WHEN i.MONTO < 0 THEN ABS(i.MONTO) ELSE 0 END) as Egresos
        FROM Info_transacciones i
        LEFT JOIN Rubro r ON i.RUBRO_ID = r.RUBRO_ID
        GROUP BY r.TIPO
    '''
    cursor.execute(query)
    return cursor.fetchall()

def obtener_datos_diarios(cursor):
    """Obtiene datos diarios."""
    query = '''
        SELECT 
            d.FECHA,
            SUM(CASE WHEN i.MONTO > 0 THEN i.MONTO ELSE 0 END) as Ingresos,
            SUM(CASE WHEN i.MONTO < 0 THEN ABS(i.MONTO) ELSE 0 END) as Egresos,
            d.SALDO
        FROM Diario d
        LEFT JOIN Transacciones t ON d.DIA_ID = t.DIA_ID
        LEFT JOIN Info_transacciones i ON t.INFO_ID = i.INFO_ID
        GROUP BY d.FECHA
        ORDER BY d.FECHA
    '''
    cursor.execute(query)
    return cursor.fetchall()