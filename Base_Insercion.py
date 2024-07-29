#Plantillas
# #Ingreso de datos
# cursor.execute(insertDiario, (None, '2024-07-16',None,None,None,None,None))
# cursor.execute(insertDiario, (None, '2024-07-17',None,None,None,None,None))

# #Imprimir los datos
# cursor.execute('''select * from Diario''' )
# fetchedData = cursor.fetchall() #Recupera todos los registros de la consulta
# print(fetchedData)

# Funciones
#Recibe una fecha y devuelve FALSO o VERDADERO, para decir si se creo o no.

#Función general para insertar cosas


def insertDiario(cursor,Fecha):
    Diario = '''INSERT INTO Diario
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);'''
    cursor.execute(Diario, (None,Fecha,None,None,None,None,None,None,None))
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
    
    Rubro =  '''INSERT INTO Rubro
    VALUES(?, ? );'''
    cursor.execute(Rubro, (None,rubro)) #Hay que validar si ya existe un rubro

    '''
                CREATE TABLE Rubro(
                        RUBRO_ID    integer NOT NULL
                        ,TIPO       text    NOT NULL
                        ,CONSTRAINT RUBRO_ID_PK PRIMARY KEY (RUBRO_ID AUTOINCREMENT)
                        );
    '''


def insertInfo_transaccciones(cursor, Concepto, Cantidad, Rubro = None):
    Info_Transacciones = '''INSERT INTO Info_transacciones
    VALUES(?, ?, ?, ?);'''
    cursor.execute(Info_Transacciones, (None, Concepto, Cantidad, Rubro)) #Falta verificar el rubro_id de rubro
   
    '''
                CREATE TABLE Info_transacciones(
                        INFO_ID     integer  NOT NULL
                        ,CONCEPTO   text     NOT NULL
                        ,CANTIDAD   numeric  NOT NULL
                        ,RUBRO_ID   integer
                        ,CONSTRAINT I_ID_IT_PK PRIMARY KEY(INFO_ID AUTOINCREMENT)
                        ,CONSTRAINT INFO_RUBRO_R_ID_FK FOREIGN KEY (RUBRO_ID) REFERENCES Rubro (RUBRO_ID)
    '''
    
def insertTransacciones(cursor, Fecha_hora, Info_ID, Dia_ID):
    Transacciones = '''INSERT INTO Transacciones
    VALUES(?, ? ,?, ?);'''
    cursor.execute(Transacciones, (None, Fecha_hora, Info_ID, Dia_ID))
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


def insertFlujo(cursor, Transaccion_ID, Intervalo = None, Intereses = None, Fecha_final = None):
    Flujo = '''INSERT INTO Flujo
    VALUES(?, ?, ?, ?, ?);'''
    cursor.execute(Flujo, (None,Transaccion_ID, Intervalo, Intereses, Fecha_final))

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
    
"""
def insertSemanal():
    insertSemanal = '''INSERT INTO Semanal 
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
def insertMensual():
    insertMensual = '''INSERT INTO Mensual 
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
def insertAnual():
    insertAnual = '''INSERT INTO ANUAL 
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
"""
