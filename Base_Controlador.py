import sqlite3 as sql

Base = sql.connect('base_principal.db')
cursor = Base.cursor()

#Plantillas
insertFlujo = """INSERT INTO Flujo
VALUES(?, ? ,?,  ?);"""

insertTransacciones = """INSERT INTO Transacciones
VALUES(?, ? ,?, ?);"""

insertRubro =  """INSERT INTO Rubro
VALUES(?, ? );"""

insertInfo_transacciones = """INSERT INTO Info_transacciones
VALUES(?, ?, ?, ?);"""

insertSemanal = """INSERT INTO SEMANAL
VALUES(?, ?, ?, ?, ?, ?, ?, ?);"""

insertDiario = """INSERT INTO Diario
VALUES(?, ?, ?, ?, ?, ?, ?);"""

insertSemanal = """INSERT INTO Semanal 
VALUES(?, ?, ?, ?, ?, ?, ?, ?);"""

insertMensual = """INSERT INTO Mensual 
VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);"""

insertAnual = """INSERT INTO ANUAL 
VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);"""

#Ingreso de datos
cursor.execute(insertDiario, (None, '2024-07-16',None,None,None,None,None))
cursor.execute(insertDiario, (None, '2024-07-17',None,None,None,None,None))

#Imprimir los datos
cursor.execute("""select * from Diario""" )
fetchedData = cursor.fetchall() #Recupera todos los registros de la consulta
print(fetchedData)

Base.commit()
cursor.close()
Base.close()