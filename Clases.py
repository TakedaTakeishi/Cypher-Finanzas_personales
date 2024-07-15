import sqlite3 as sql

## Comienzo del proyecto de Finanzas  
print("Con esto comienza el proyecto")

Base = sql.connect('base_principal.db')

cursor = Base.cursor()

#Creación de Entidades de la BD

cursor.execute("""
            CREATE TABLE Flujo(
                        OPERACION_ID    integer NOT NULL
                        ,TRANSACCION_ID integer NOT NULL
                        ,INTERVALO      numeric
                        ,INTERESES      numeric
                        ,CONSTRAINT O_ID_PK PRIMARY KEY(OPERACION_ID)
                        ,CONSTRAINT T_ID_PK PRIMARY KEY(TRANSACCION_ID)
                    );
""")

cursor.execute("""
                CREATE TABLE Transacciones(
                        TRANSACCION_ID      integer  NOT NULL
                        ,FECHA              date     NOT NULL
                        ,INFO_ID            integer  NOT NULL
                        ,DIA_ID             integer  NOT NULL
                        ,CONSTRAINT T_ID_T_PK PRIMARY KEY(TRANSACCION_ID)
                        ,CONSTRAINT D_ID_T_PK PRIMARY KEY(DIA_ID)
                    );
""") 
 
cursor.execute("""
                CREATE TABLE Info_transacciones(
                        INFO_ID     integer  NOT NULL
                        ,COCEPTO    date     NOT NULL
                        ,CANTIDAD   numeric  NOT NULL
                        ,RUBRO_ID   integer
                        ,CONSTRAINT I_ID_IT_PK PRIMARY KEY(INFO_ID)
                    );
""")                  
cursor.execute("""
                CREATE TABLE Rubro(
                        RUBRO_ID    integer NOT NULL
                        ,TIPO       text    NOT NULL
                        ,CONSTRAINT RUBRO_ID_PK PRIMARY KEY (RUBRO_ID)
                    );
""")   

cursor.execute(""" 
               CREATE TABLE Diario(
                        DIA_ID      integer NOT NULL
                        ,FECHA      date    NOT NULL
                        ,DIA_SALDO  numeric
                        ,SALDO      numeric
                        ,PROMEDIO   numeric
                        ,MEDIANA    numeric
                        ,MODA       numeric
                        ,CONSTRAINT D_ID_PK PRIMARY KEY (DIA_ID)
                    );
""") 

cursor.execute("""
                CREATE TABLE SEMANAL(
                        SEMANA_ID       integer NOT NULL
                        ,SEMANA_INICIO  date    NOT NULL
                        ,SEMANA_FIN     date    NOT NULL
                        ,SEMANA_SALDO   numeric NOT NULL
                        ,SALDO          numeric NOT NULL
                        ,PROMEDIO       numeric NOT NULL
                        ,MEDIANA        numeric NOT NULL
                        ,MODA           numeric NOT NULL
                        ,CONSTRAINT S_ID_PK PRIMARY KEY (SEMANA_ID)
                    );
""") 

cursor.execute("""
                CREATE TABLE MENSUAL(
                        MES_ID          integer NOT NULL
                        ,MES_INICIO     date    NOT NULL
                        ,MES_FIN        date    NOT NULL
                        ,MES_SALDO      numeric NOT NULL
                        ,SALDO          numeric NOT NULL
                        ,PROMEDIO       numeric NOT NULL 
                        ,MEDIANA        numeric NOT NULL 
                        ,MODA           numeric NOT NULL
                        ,CONSTRAINT M_ID_PK PRIMARY KEY (MES_ID)
                    );
""")  

cursor.execute("""
                CREATE TABLE ANUAL(
                        ANIO_ID         integer NOT NULL
                        ,ANIO_INICIO    date    NOT NULL
                        ,ANIO_FIN       date    NOT NULL
                        ,ANIO_SALDO    numeric NOT NULL 
                        ,SALDO          numeric NOT NULL
                        ,PROMEDIO       numeric NOT NULL
                        ,MEDIANA        numeric NOT NULL
                        ,MODA           numeric NOT NULL
                        ,CONSTRAINT A_ID_PK PRIMARY KEY (ANIO_ID)
                    );
""")   
Base.commit()

cursor.execute("""
            ALTER TABLE CONSTRAINT 
""")

insertFlujo = """INSERT INTO Flujo
VALUES(?, ? ,? ,? );"""

insertTransacciones = """INSERT INTO Transacciones
VALUES(?, ? ,? ,? );"""

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

cursor.execute(insertFlujo, (1, 1, 205, 0.5))
cursor.execute("""select * from Flujo""" )
fetchedData = cursor.fetchall() #Recupera todos los registros de la consulta
print(fetchedData)


Base.commit()
cursor.close()
Base.close()