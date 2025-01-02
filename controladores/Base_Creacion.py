
## Comienzo del proyecto de Finanzas  
def Creacion_Tablas(Base, cursor):

    #Creación de Entidades de la BD
    cursor.execute("PRAGMA foreign_keys = ON;")
#    cursor.execute("PRAGMA recursive_triggers = on;")
    
    #Borrado de tablas
    cursor.execute("DROP TABLE IF EXISTS Flujo;")
    cursor.execute("DROP TABLE IF EXISTS Transacciones;")
    cursor.execute("DROP TABLE IF EXISTS Info_transacciones;")
    cursor.execute("DROP TABLE IF EXISTS Rubro;")
    cursor.execute("DROP TABLE IF EXISTS Anual;")
    cursor.execute("DROP TABLE IF EXISTS Mensual;")
    cursor.execute("DROP TABLE IF EXISTS Semanal;")
    cursor.execute("DROP TABLE IF EXISTS Diario;")
    
    #Creación de las tablas
    cursor.execute(''' 
                   CREATE TABLE Diario(
                            DIA_ID      integer NOT NULL
                            ,FECHA      date    NOT NULL
                            ,DIA_INGRESO    numeric default 0
                            ,DIA_EGRESO     numeric default 0
                            ,DIA_SALDO      numeric default 0
                            ,SALDO          numeric default 0
                            ,PROMEDIO       numeric default 0
                            ,MEDIANA        numeric default 0
                            ,MODA           numeric default 0
                            ,CONSTRAINT D_ID_PK PRIMARY KEY (DIA_ID AUTOINCREMENT)
                        );
    ''') 
    cursor.execute('''
                    CREATE TABLE Semanal(
                            SEMANA_ID       integer NOT NULL
                            ,SEMANA_INICIO  integer NOT NULL
                            ,SEMANA_FIN     integer
                            ,SEMANA_INGRESO numeric default 0
                            ,SEMANA_EGRESO  numeric default 0
                            ,SEMANA_SALDO   numeric default 0
                            ,SALDO          numeric default 0
                            ,PROMEDIO       numeric default 0
                            ,MEDIANA        numeric default 0
                            ,MODA           numeric default 0
                            ,CONSTRAINT S_ID_PK PRIMARY KEY (SEMANA_ID AUTOINCREMENT)
                            ,CONSTRAINT SEM_DIA_INI_FK FOREIGN KEY (SEMANA_INICIO) REFERENCES Diario (DIA_ID)
                        	,CONSTRAINT SEM_DIA_FIN_FK FOREIGN KEY (SEMANA_FIN)    REFERENCES Diario (DIA_ID)
                        );
    ''') 
    
    cursor.execute('''
                    CREATE TABLE Mensual(
                            MES_ID          integer NOT NULL
                            ,MES_INICIO     integer NOT NULL
                            ,MES_FIN        integer
                            ,MES_INGRESO    numeric default 0 
                            ,MES_EGRESO     numeric default 0
                            ,MES_SALDO      numeric default 0
                            ,SALDO          numeric default 0
                            ,PROMEDIO       numeric default 0 
                            ,MEDIANA        numeric default 0 
                            ,MODA           numeric default 0
                            ,CONSTRAINT M_ID_PK PRIMARY KEY (MES_ID AUTOINCREMENT)
                            ,CONSTRAINT MES_DIA_INI_FK FOREIGN KEY (MES_INICIO)   REFERENCES Diario (DIA_ID)
                            ,CONSTRAINT MES_DIA_FIN_FK FOREIGN KEY (MES_FIN)      REFERENCES Diario (DIA_ID)
                        );
    ''')  
    
    cursor.execute('''
                    CREATE TABLE Anual(
                            ANIO_ID         integer NOT NULL
                            ,ANIO_INICIO    integer NOT NULL
                            ,ANIO_FIN       integer
                            ,ANIO_INGRESO   numeric default 0
                            ,ANIO_EGRESO    numeric default 0
                            ,ANIO_SALDO     numeric default 0 
                            ,SALDO          numeric default 0
                            ,PROMEDIO       numeric default 0
                            ,MEDIANA        numeric default 0
                            ,MODA           numeric default 0
                            ,CONSTRAINT A_ID_PK PRIMARY KEY (ANIO_ID AUTOINCREMENT)
                            ,CONSTRAINT ANUAL_MES_INI_FK FOREIGN KEY (ANIO_INICIO)   REFERENCES Diario (DIA_ID)
                            ,CONSTRAINT ANUAL_MES_FIN_FK FOREIGN KEY (ANIO_FIN)      REFERENCES Diario (DIA_ID)
                        );
    ''') 

    cursor.execute('''
                CREATE TABLE Flujo(
                            OPERACION_ID    integer NOT NULL
                            ,INTERVALO      numeric
                            ,FECHA_FINAL    date
                            ,INTERESES      numeric
                            ,ESTADO         boolean default TRUE
                            ,CONSTRAINT O_ID_PK PRIMARY KEY(OPERACION_ID AUTOINCREMENT) 
                        );
    ''')
    
    
    cursor.execute('''
                    CREATE TABLE Rubro(
                            RUBRO_ID    integer NOT NULL
                            ,TIPO       text    NOT NULL
                            ,CONSTRAINT RUBRO_ID_PK PRIMARY KEY (RUBRO_ID AUTOINCREMENT)
                            );
    ''') 
    
    cursor.execute('''
                    CREATE TABLE Info_transacciones(
                            INFO_ID     integer  NOT NULL
                            ,CONCEPTO   text     NOT NULL
                            ,MONTO      numeric  NOT NULL
                            ,RUBRO_ID   integer
                            ,COMPUESTO  numeric  
                            ,CONSTRAINT I_ID_IT_PK PRIMARY KEY(INFO_ID AUTOINCREMENT)
                            ,CONSTRAINT INFO_RUBRO_R_ID_FK FOREIGN KEY (RUBRO_ID) REFERENCES Rubro (RUBRO_ID)
                        );
    ''')
    # Se utiliza actualizar para guardar la fecha donde actualizar la operación recurrente        
    cursor.execute('''
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
    ''') #La fecha es para la hora y fecha del ingreso del registro de la transacción.
    # TODO: Cambiar los nombres de los constraints
#--------------------------------------TRIGGERS--------------------------------------------
## Pasos para actualizar el saldo según los saldos anteriores

#Primero se actualizan los egresos e ingresos del día dependiendo de las transacciones realizadas
# Se puede hacer más eficiente con un if


    cursor.execute('''
                    
                    CREATE TRIGGER IF NOT EXISTS Dia
                    AFTER INSERT ON Transacciones
                        BEGIN     
                            UPDATE Diario
                            SET 
                                DIA_INGRESO = DIA_INGRESO + COALESCE((SELECT MONTO FROM Info_transacciones
                                                                    WHERE INFO_ID = NEW.INFO_ID AND MONTO > 0), 0)
                                ,DIA_EGRESO = DIA_EGRESO + COALESCE((SELECT MONTO FROM Info_transacciones
                                                                   WHERE INFO_ID = NEW.INFO_ID AND MONTO < 0), 0)
                            WHERE DIA_ID = NEW.DIA_ID;
                        END;
                    ''')

# Se actualiza el saldo del día sumando los nuevos egresos e ingresos
    cursor.execute('''
                    
                    CREATE TRIGGER IF NOT EXISTS Suma_Ingreso_Egreso
                    AFTER UPDATE OF DIA_INGRESO, DIA_EGRESO ON Diario
                        BEGIN
                            
                            UPDATE Diario
                            SET DIA_SALDO = NEW.DIA_INGRESO + NEW.DIA_EGRESO
                            WHERE DIA_ID = NEW.DIA_ID;

                        END;
                    ''')

# Una vez actualizado el saldo del día, sumamos el saldo del día anterior para conformar el nuevo saldo general.
    cursor.execute('''  
                    CREATE TRIGGER IF NOT EXISTS Actualizar_Saldo_Diario
                    AFTER UPDATE OF DIA_SALDO ON Diario
                        BEGIN
                        --No hemos avanzado
                           --Esta parte suma el saldo del día anterior con el nuevo saldo actualizado
                            UPDATE Diario
                            SET SALDO = DIA_SALDO + COALESCE((SELECT SALDO FROM Diario
                                                                    WHERE DIA_ID = (NEW.DIA_ID - 1) ), 0)
                            WHERE DIA_ID = NEW.DIA_ID;
                        END;
                    ''')    

# Ahora creamos los triggers para modificaciones en Info transacciones, actualizamos de manera recursiva los siguientes días, si existen.
# LOS TRIGGER NO SOPORTAN LOS IF EN SQLITE

    cursor.execute('''

                    CREATE TRIGGER IF NOT EXISTS Actualizador_Monto
                    AFTER UPDATE OF MONTO ON Info_Transacciones
                    BEGIN
                        -- Actualizar los valores en Diario
                        UPDATE Diario
                        SET 
                            DIA_INGRESO = DIA_INGRESO +
                                        CASE 
                                            WHEN OLD.MONTO > 0 AND NEW.MONTO > 0 THEN NEW.MONTO - OLD.MONTO
                                            WHEN OLD.MONTO > 0 AND NEW.MONTO < 0 THEN -OLD.MONTO
                                            WHEN OLD.MONTO < 0 AND NEW.MONTO > 0 THEN NEW.MONTO
                                            ELSE 0
                                        END,
                            DIA_EGRESO = DIA_EGRESO +
                                        CASE 
                                            WHEN OLD.MONTO < 0 AND NEW.MONTO < 0 THEN NEW.MONTO - OLD.MONTO
                                            WHEN OLD.MONTO < 0 AND NEW.MONTO > 0 THEN -OLD.MONTO
                                            WHEN OLD.MONTO > 0 AND NEW.MONTO < 0 THEN NEW.MONTO
                                            ELSE 0
                                        END
                        WHERE DIA_ID = (SELECT DIA_ID FROM Transacciones WHERE INFO_ID = NEW.INFO_ID);
                    END;
                    ''')





# Cambios a tener en cuenta
    
    Base.commit()  #Guarda los cambios
   
"""
    cursor.excute('''
                    CREATE TRIGGER IF NOT EXISTS Intervalos
                    AFTER INSERT OF FECHA ON Diario
                        BEGIN
                            --Si existe una fila con intervalo entonces 
                            IF () THEN
                        END;
                    ''')
"""


"""
    cursor.execute('''
                    
                    CREATE TRIGGER IF NOT EXISTS Dia
                    AFTER INSERT ON Transacciones
                        BEGIN     
                            UPDATE Diario
                            SET 
                                DIA_INGRESO = DIA_INGRESO + COALESCE((SELECT MONTO FROM Info_transacciones
                                                                    WHERE INFO_ID = NEW.INFO_ID AND MONTO > 0), 0)
                             
                            ,DIA_EGRESO = DIA_EGRESO + COALESCE((SELECT MONTO FROM Info_transacciones
                                                                   WHERE INFO_ID = NEW.INFO_ID AND MONTO < 0), 0)
                            WHERE DIA_ID = NEW.DIA_ID;
                        END;
                    ''')
"""
# tenemos que tener en cuanta todos los triggerss y las posibles expresiones que se pueden utlizar

