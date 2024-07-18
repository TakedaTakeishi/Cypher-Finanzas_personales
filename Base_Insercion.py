#Plantillas
# #Ingreso de datos
# cursor.execute(insertDiario, (None, '2024-07-16',None,None,None,None,None))
# cursor.execute(insertDiario, (None, '2024-07-17',None,None,None,None,None))

# #Imprimir los datos
# cursor.execute("""select * from Diario""" )
# fetchedData = cursor.fetchall() #Recupera todos los registros de la consulta
# print(fetchedData)

# Funciones
#Recibe una fecha y devuelve FALSO o VERDADERO, para decir si se creo o no.


def insertFlujo():
    insertFlujo = """INSERT INTO Flujo
    VALUES(?, ? ,?,  ?);"""

def insertTransacciones():
    insertTransacciones = """INSERT INTO Transacciones
    VALUES(?, ? ,?, ?);"""

def insertRubro():
    insertRubro =  """INSERT INTO Rubro
    VALUES(?, ? );"""

def insertInfo_transaccciones():
    insertInfo_transacciones = """INSERT INTO Info_transacciones
    VALUES(?, ?, ?, ?);"""

def insertSemanal():
    insertSemanal = """INSERT INTO SEMANAL
    VALUES(?, ?, ?, ?, ?, ?, ?, ?);"""

def insertDiario():
    insertDiario = """INSERT INTO Diario
    VALUES(?, ?, ?, ?, ?, ?, ?);"""

def insertSemanal():
    insertSemanal = """INSERT INTO Semanal 
    VALUES(?, ?, ?, ?, ?, ?, ?, ?);"""
def insertMenusal():
    insertMensual = """INSERT INTO Mensual 
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);"""
def insertAnual():
    insertAnual = """INSERT INTO ANUAL 
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);"""

#Función general para insertar cosas
def insertar_datos():
    pass