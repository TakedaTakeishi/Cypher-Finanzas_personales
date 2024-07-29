

def fecha_Ultima(cursor):
    cursor.execute("""SELECT MAX(FECHA) FROM Diario""")
    fetchedData = cursor.fetchall()[0][0]
    return fetchedData

