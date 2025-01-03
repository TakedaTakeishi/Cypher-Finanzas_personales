import sys
import os
from os import path
# Usamos dirname para obtener la carpeta padre de la carpeta en la que se encuentra este archivo.
# Guardando la carpeta padre del proyecto en una variable.
# Se usa dos veces para obtener la carpeta padre del proyecto.
raiz = path.dirname(path.dirname(path.abspath(__file__)))
# Agregamos la carpeta padre del proyecto al path de python para poder importar los módulos que se encuentran en ella.
sys.path.append(raiz)


import controladores.Base_Controlador as ctr
from datetime import datetime, timedelta
import locale

# Creamos la variable global para la ruta de los usuarios.
ruta_usuarios = raiz + '/Usuarios.txt'

# -------------------------------------- Funciones -----------------------------------------------

#Los límites pueden tener esta nomeclatura [lim_inf, lim_sup], ejemplos: [None, 5], [1, 5], [1, None] 

def input_validado(texto, opcion, limites = None):
    while True:
        match(opcion):
            case 1:
                try:
                    variable = int(input(texto)) 
                    return variable
                except ValueError:
                    print(">>>¿Es número?>>>")
            case 2:
                try:
                    variable = float(input(texto)) 
                    return variable
                except ValueError:
                    print(">>>¿Es número?>>>")
            case 3:
                variable = input_validado(texto, 1)
                if(limites[0] <= variable <= limites[1]):
                    return True, variable
                else:
                    print(">>>No esta dentro del rango")
                    return False, variable
            case 4:
                #Quitamos saltos de línea y espacios con strip y luego lo convertimos a bool para saber si está vacío o no. Si no está vacío devuelve True.
                t = input(texto)
                if(bool(t.strip())):
                    return t
                else:
                    print(">>>No puede ser vacío")
            case 5:
                Nombre = input_validado(texto,4) 
                if not(Nombre[0].isalpha()):
                    print(">>>El primer caracter debe ser letra")
                elif all(c.isalnum() or ' ' for c in Nombre):
                    # print(">>>Entrada correcta...")
                    return Nombre
                else:
                    print(">>>¿Es alfanumérico?")
            
            
def submenu(texto_titulo, texto_eleccion, lista_opciones):
    valido = False
    while not valido:
        i = 1
        print(f"\n----------< {texto_titulo.upper()} >----------")
        for opcion in lista_opciones:
            print(f'{i}. {opcion}')
            i+=1
        print('0. Salir')
        valido, eleccion = input_validado(f"{texto_eleccion}:\nR: ", 3, (0,i-1))
    return eleccion
                    
def submenu_obligatorio(texto_titulo, texto_eleccion, lista_opciones):
    valido = False
    while not valido:
        i = 1
        print(f"\n----------< {texto_titulo.upper()} >----------")
        for opcion in lista_opciones:
            print(f'{i}. {opcion}')
            i+=1
        valido, eleccion = input_validado(f"{texto_eleccion}:\nR: ", 3, (0,i-1))
    return eleccion
   
def es_bisiesto(anio):
    if (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0):
        return True
    else:
        return False

def eleccion(Pregunta):
    while True:
        choice = input(f"\n{Pregunta} (s/n)\nR: ")
        if (choice.upper() == 'S' or choice.upper() == 'N'):
            if choice.upper() == 'S':
                return True
            elif choice.upper() == 'N':
                return False
        print('>>>Opción inválida, intenta otra vez.')

def fecha_ingresar() -> str:
    anio=mes=dia=0
    while anio <= 0:
        anio = input_validado("Ingresa el año: ", 1)
        if anio <= 0:
            print(">>>El año no es válido")

    while 0>=mes or mes>12:
        mes = input_validado("Ingresa el mes: ", 1)
        if 0>=mes or mes>12:
            print(">>>El mes no es válido")

    while dia <= 0 or dia > 31:
        dia  = input_validado("Ingrese el dia: ", 1)
        if mes in [4, 6, 9, 11] and (dia <= 0 or dia > 30):
            print(">>>El día no es válido para este mes")
            dia = 0
        elif mes == 2:
            if es_bisiesto(anio):  
                if dia <= 0 or dia > 29:
                    print(">>>El día no es válido para febrero en un año bisiesto")
                    dia = 0
            else:
                if dia <= 0 or dia > 28:
                    print(">>>El día no es válido para febrero")
                    dia = 0
        elif dia <= 0 or dia > 31:
            print(">>>El día no es válido para este mes")
            dia = 0
    return f"{anio:04d}-{mes:02d}-{dia:02d}"
        

        
def fecha_Inicial():
    fecha_hora_actual = datetime.now().date()
    print(".:Fecha a iniciar analisis:.")
    while True:
        entered_date_str = fecha_ingresar()
        entered_date = datetime.strptime(entered_date_str, "%Y-%m-%d").date()
        if entered_date <= fecha_hora_actual:
            break
        else:
            print(">>>La fecha no puede ser mayor a la fecha actual")
    return entered_date_str
   
def fecha_Final(Fecha_operacion):
    while True:
        print("Ingrese una fecha de finalizacion:")
        fecha = fecha_ingresar()
        var = ctr.fecha_compara(fecha,Fecha_operacion)
        if var < 0:
            print(">>>Debe ser una fecha futura al día de la operación")
        else:
            return fecha




def fecha_Seleccionar(cursor):
    # En esta parte se tiene que obtener los años en los que hay registros
    Anios = ctr.obtener_Anios(cursor)
    if len(Anios) > 1:
        eleccion = submenu_obligatorio('Elegir año', 'Elección', Anios)
        anio = Anios(eleccion-1)
    else:
        anio = Anios
    #  Despues se tienen que obtener los meses 
    Meses = ctr.obtener_Meses(cursor, anio)
    if len(Meses) > 1:
        eleccion = submenu_obligatorio('Elegir mes', 'Elección', Meses)
        mes = Meses(eleccion-1)
    else:
        mes = Meses
    Dias = ctr.obtener_Dias(cursor, mes, anio)
    if len(Dias) > 1:
        eleccion = submenu_obligatorio('Elegir dia','Elección', Dias)
        dia = Dias(eleccion-1)
    else:
        dia = Dias
    Fecha = f"{anio:04d}-{mes:02d}-{dia:02d}"
    Dia_ID = ctr.fecha_Dia_ID(cursor, Fecha)
    return Fecha, Dia_ID
        
#Que va a pedir y como

def usuario_Crear(): 
    while True:
        Nombre = input_validado("Dame el nombre del usuario: ", 4) 
        if not(Nombre[0].isalnum()):
            print(">>>El primer caracter debe ser letra o número.")
        elif all(c.isalnum() or c == '-' or '_' for c in Nombre) and ' ' not in Nombre:
            print("Nombre correcto...")
            break
        else:
            print(">>>No debe tener espacios")
    return Nombre

def usuario_Asigna(ruta, Nombre):

    with open(ruta, 'a', encoding="utf-8") as file:
        usuario = Nombre + '\n'
        file.write(usuario)


#def fecha_



def usuarios_Uno(file_path):
    with open(file_path, 'r') as file:
        # Leer la primera línea (y descartarla)
        file.readline()
        # Leer la segunda línea
        second_line = file.readline()
        
        # Verificar si la segunda línea está vacía o contiene solo espacios en blanco
        if second_line.strip() == '':
            return True
        else:
            return False

def usuario_Nuevo():
    ruta = raiz + '/Usuarios.txt'
    Nombre = usuario_Crear()
    usuario_Asigna(ruta, Nombre)
    Fecha = fecha_Inicial()
    Base, cursor = ctr.base_Inicializar(1, Nombre, Fecha)
    return Base, cursor, Nombre

def usuario_Nombre(ruta, fila):
    with open(ruta, 'r', encoding="utf-8") as file:
        Nombre = file.readlines()[fila-1]
    return Nombre.strip()
    
def usuarios_Elegir(Usuarios_Max):
    ruta = raiz + '/Usuarios.txt'
    while True:
        print()
        opcion = int(input("Elije el número de usuario: "))
        if (0 < opcion <= Usuarios_Max):
            Usuario = usuario_Nombre(ruta, opcion)
            return Usuario
        print("Valor inválido")



def usuarios_menu():
    print("Elije usuario:")
    ruta = raiz + '/Usuarios.txt'
    file_object = open(ruta, "r", encoding="utf-8")
    # Loop over and print each line in the file object.
    i = 0
    for string in file_object:
        i += 1
        print(f'{i}. {string}', end='')
    #Enviamos i para saber el número máximo de usuarios.
    return i

def usuario_leer(ruta, file):
    if path.getsize(ruta) > 0:
        #Para saber si tenemos más de un usuario comprobamos
        if (usuarios_Uno(ruta)):
            Nombre = file.readlines()[0]
        else:
            Nombre = usuarios_Elegir(usuarios_menu())
        Base, cursor = ctr.base_Inicializar(2, Nombre)
    else:
        print("\n >>>No hay usuario creado, crea uno nuevo<<< \n")
        Base, cursor, Nombre = usuario_Nuevo()
    return Base, cursor, Nombre

def usuario_Iniciar():
#     ruta = path.realpath('Usuarios.txt')
#     print(f'La ruta de usuarios txt es: {ruta}')
    ruta = raiz + '/Usuarios.txt'
    # Si existe leemos si no escribimos y creamos
    if (os.path.exists(ruta)):
        with open(ruta,'r') as file:
             
            Base, cursor, Nombre = usuario_leer(ruta, file)    
    else:
        with open(ruta,'w') as file: 
            
            Base, cursor, Nombre = usuario_leer(ruta, file) 
    return Base, cursor, Nombre.strip()



def delete_line(file_path, line_number):
    # Leer todas las líneas del archivo
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Verificar que la línea a eliminar existe
    if line_number < 1 or line_number > len(lines):
        raise IndexError(">>>El número de línea está fuera del rango.")
    
    # Eliminar la línea deseada (restar 1 porque las listas son 0-indexadas)
    del lines[line_number - 1]

    # Escribir las líneas restantes de nuevo al archivo
    with open(file_path, 'w') as file:
        file.writelines(lines)


def usuarios_Borrar(Usuarios_Max, Base, cursor, Usuario):
    print("0. Cancelar proceso")
    ruta = raiz + '/Usuarios.txt'
    borrado = False
    while True:
        opcion = input_validado("\nElige el número de usuario a eliminar: ",1)
        if (0 < opcion <= Usuarios_Max):
            Nombre = usuario_Nombre(ruta, opcion) #Verificar si existe el usuario.
            delete_line(ruta, opcion)
            Base_nombre = Nombre + ".db"
            Path = ctr.usuarios_Dir(Base_nombre)
            if (Nombre == Usuario):
                base_Cerrar(Base, cursor)
                borrado = True
            os.remove(Path) #Verificar si existe la base.
            print("Usuario borrado...")
            return borrado
        elif(opcion == 0):
            print("Proceso cancelado...")
            break
        print(">>>Valor inválido") #Tener una opción para cancelar la operación.

def input_rubro():
    if eleccion('¿Quieres ingresar rubro?'):
        return input_validado('Ingresa el rubro: ', 5)

'''
def datos_Menu():
    valido = False
    while(not valido):
        print("\n Dime que tipo de operación quieres ingresar.")
        print("----------OPERACIONES----------\n")
        print("1. Operación simple")
        print("2. Operación recurrente")
        valido, eleccion = input_validado("Elige que opción quieres:\nR: ", 3, (1,2)) 
    return eleccion
'''

def dato_Intervalo_Tipo(fecha):
    eleccion = submenu('Intervalos', 'Elije el intervalo de repetición', ('Anual', 'Mensual', 'Semanal', 'Dias'))

    match (eleccion):
        case 0: return None
        case 1:                             #YYYY-MM-DD
            print(f'La operación se repetirá cada {fecha[-2:]} del mes {fecha[5:7]} de cada año' )
            if(es_bisiesto(int(fecha[:4])) and int(fecha[-2:]) == 29):
                return 'Fin del mes de febrero'
            else:       
                return 'Anual' #Verificar lo del día bisiesto
        case 2:                        
            dia = int(fecha[-2:])
            if dia > 28:
                while True:       
                    print(f'No todos los meses tienen {dia} días. ¿Quieres que se repita al final del mes o cada 28?')
                    mes = int(input('''1. Fin de mes
                                    \n2. Cada 28'''))
                    if(1 <= mes <= 2):
                        break
                if mes == 1:
                    return 'Fin de mes'
                else:
                    return 'Cada 28'
            else:
                print(f'La operación se repetirá el día {dia} de cada mes')
                return 'Mensual'
        case 3:
            print(f'La operación se repetirá este día de cada semana')
            return 'Semanal'
        case 4:
            while True:
                Dias = input('Dime cada cuantos días se repetirá (por ejemplo 28): ')
                if (Dias.isnumeric()):
                    num_Dias = int(Dias)
                    if(num_Dias > 0):
                        return num_Dias
                    else:
                        print("¿Es mayor a cero?")
                else:
                    print("¿Es número?")
                print(">>>Entráda no válida")
        case _: 
            return None

def dato_Intervalo_Codificacion(Tipo):
    if (type(Tipo) is int or type(Tipo) is None):
        return Tipo
    elif(Tipo == 'Semanal'):
        return 7
    elif(Tipo == 'Mensual'):
        return -1
    elif(Tipo == 'Fin del mes de febrero'):
        return -2
    elif(Tipo == 'Cada 28'):
        return -3
    elif(Tipo == 'Fin de mes'):
        return -4
    elif (Tipo == 'Anual'):
        return -5


def printOperacion(concepto, monto, rubro, intervalo, fecha_final, intereses):
    print(f'Concepto:\t{concepto}')
    print(f'Monto:\t\t${monto}')
    if(rubro is not None):
        print(f'rubro:\t\t{rubro}')
    if(intervalo is not None):
        print(f'intervalo:\t{intervalo}')
    if(fecha_final is not None):
        print(f'fecha_final:\t{fecha_final}')
    if(intereses is not None):
        print(f'intereses:\t{intereses}%')
    print()

def print_Operaciones(Operaciones):
    i = 1
    for tupla in Operaciones:
        print(f'\n\tOperación: {i}')
                        #concepto, monto, rubro, intervalo, fecha_final, intereses
        printOperacion(tupla[0], tupla[1], tupla[2], tupla[3], tupla[4], tupla[5])
        i = i + 1

def Operacion_input(Fecha, Op):
    #Verificar datos
    concepto =  input_validado("Ingresa el concepto: ", 5)
    monto = input_validado("Ingresa el monto: ", 2)
    rubro = None
    intervalo =  None
    fecha_final = None
    intereses = None
    if Op == 2:
        intervalo =  dato_Intervalo_Codificacion(dato_Intervalo_Tipo(Fecha))
        if (intervalo is None):
            choice = 1
            rubro = input_rubro()
        else:
            rubro = input_validado("Ingresa el Rubro: ", 5) 
            if eleccion('¿Tiene fecha de finalización?'):
                fecha_final = fecha_Final(Fecha)
                
            if eleccion('¿Cuenta con intereses?'):
                porcentaje = input_validado("¿Cuál es el porcentaje?: ", 2)
                intereses = porcentaje / 100    
    
    else:
        rubro = input_rubro() 
    
    return [concepto, monto, rubro, intervalo, fecha_final, intereses]

def operacion_Modificar(lista, Fecha):
    opciones = ('Concepto', 'Monto', 'Rubro', 'Intervalo', 'Fecha final' ,'Intereses')
    while True:
        # 'Concepto', 'Monto', 'Rubro', 'Intervalo', 'Fecha final' ,'Intereses'
        printOperacion(lista[0], lista[1], lista[2], lista[3], lista[4], lista[5])
        if(lista[3] is not None):
            opcion = submenu('Cambiar algun Dato','¿Que dato quieres cambiar?',opciones)
        else:
            opcion = submenu('Cambiar algun Dato','¿Que dato quieres cambiar?',opciones[:-3])
        match(opcion):
            case 0: break
            case 1: lista[0] = input_validado("Ingresa el concepto: ", 4)
            case 2: lista[1] = input_validado("Ingresa la monto: ", 2)
            case 3: lista[2] = input_validado("Ingrese el rubro: ",5)
            case 4: lista[3] = dato_Intervalo_Codificacion(dato_Intervalo_Tipo(Fecha))
            case 5:
                lista[4] = fecha_Final(Fecha)
            
            case 6: 
                porcentaje = input_validado("¿Cuál es el porcentaje?: ", 2)
                lista[5] = porcentaje / 100
        printOperacion(lista[0], lista[1], lista[2], lista[3], lista[4], lista[5]) # Cambio
        return lista



def operacion_Elegir_Modificar(Modificaciones, Operaciones, Fecha):
    while True:
        #concepto, monto, rubro, intervalo, fecha_final, intereses
        print_Operaciones(Operaciones)
        # Obtenemos las montos que identifican a cada operación
        opciones = []
        for tupla in Operaciones:
            opciones.append(tupla[0])    
        tupla = submenu(f'Operaciones del dia {Fecha}', '¿Cuál quieres modificar?', opciones)
        if tupla == 0:
            break      
        lista = list(Operaciones[tupla-1])
        # Cuando queremos modificar, para reutilizar el código, lo haremos de dos maneras, una parte por parte y otra volviéndola a hacer
        opciones_modificacion = ('Modificar una parte de la operación', 'Cambiarlo todo')
        while True:
            seleccion = submenu('Modificando operacion', '¿Que modificar?', opciones_modificacion)
            match seleccion:
                case 0: break
                case 1:
                    lista_nueva = operacion_Modificar(lista, Fecha)
                case 2:
                    choice = submenu(f'Cambiando : {lista[0]}', '¿A que tipo de operación la deseas cambiar?', ('Simple', 'Recurrente') )
                    if choice != 0:
                        if(choice == 1):
                            lista_nueva = Operacion_input(Fecha,1)
                        else:
                            lista_nueva = Operacion_input(Fecha,2)
            
            cambiar = True
            for i, mod in enumerate(Modificaciones):
                # Si Modificaciones está vacío, agregamos la nueva tupla
                if not Modificaciones:
                    Modificaciones.append(tuple(lista_nueva + lista[-3:]))
                    cambiar = False
                    break
                # Si el TRANSACCION_ID coincide, actualizamos la tupla
                elif lista[-3] == mod[-3]:
                    Modificaciones[i] = tuple(lista_nueva + lista[-3:])
                    cambiar = False
                    break
            # Si no se encontró una coincidencia, se agrega la nueva tupla
            if cambiar: 
                Modificaciones.append(tuple(lista_nueva + lista[-3:]))

def operacion(Base, cursor, Dia_ID, Fecha):
    Operaciones = []
    operacion = 0
    while True:
        opciones = ('Registrar movimiento', 'Mostrar movimiento', 'Borrar movimiento', 'Modificar movimiento', 'Subir movimientos a la base de datos')
        opcion = submenu(f"Menu Ingreso Fecha: {Fecha}", 'Elige que deseas hacer', opciones)
        match opcion:
            case 0: return operacion
            case 1:
                while True:
                    choice = submenu('Movimiento', '¿Qué tipo de operación quieres?', ('Simple', 'Recurrente') )
                    if choice == 0:
                        break
                    Tupla = tuple(Operacion_input(Fecha, choice))
                    Operaciones.append(Tupla)
            case 2:
                print_Operaciones(Operaciones)
            case 3:
                opciones = []
                for tupla in Operaciones:
                    opciones.append(tupla[0])    
                opcion = submenu('Borrar', '¿Cuál quieres borrar?', opciones)
                
                if opcion !=0 and eleccion(f'¿Seguro que quieres borrar: {opciones[opcion-1]}'):
                    Operaciones.pop(opcion-1)
            case 4:
                opciones = []
                for tupla in Operaciones:
                    opciones.append(tupla[0])    
                tupla = submenu('Modificación', '¿Cuál quieres cambiar?', opciones)
                if tupla !=0:
                    Tupla = Operaciones[tupla-1]
                    lista = list(Tupla)
                    Operaciones[tupla-1] = tuple(operacion_Modificar(lista, Fecha))
                        
                    
            case 5:
                #Si esta vacío no ingresa.
                if bool(Operaciones) is False:
                    print('>>>No hay operaciones para ingresar')
                else:
                    for Tupla in Operaciones:
                        ctr.insertOperation(Base, cursor, Dia_ID, Tupla[0],Tupla[1],Tupla[2],Tupla[3],Tupla[4],Tupla[5])      
                    # Si deseamos que el usuario pueda guardar varias veces la misma operación u operaciones entonces debemos quitar o modificar la línea de abajo que es la que reinicia todo.
                    operacion += len(Operaciones)
                    Operaciones = []



def modificar(Base, cursor, Dia_ID, Fecha):
    Operaciones = ctr.obtener_Transacciones(Base, cursor, Dia_ID) # Verificar si existe o no Transacciones.
    # [(CONCEPTO, MONTO, TIPO, INTERVALO, FECHA_FINAL, INTERESES, TRANSACCION_ID, OPERACION_ID, INFO_ID)]
    Modificaciones = []
    modificacion = 0
    while True:      
        opciones = ('Elejir operación a modificar', 'Mostrar modificaciones', 'Borrar modificación', 'Editar modificación', 'Guardar modificaciones')
        opcion = submenu(f"Menu Modificación Operaciones de {Fecha}: ", 'Elige que deseas hacer', opciones)
        match opcion:
            case 0: return modificacion
            case 1:
                operacion_Elegir_Modificar(Modificaciones, Operaciones, Fecha)                           
            case 2:
                print_Operaciones(Modificaciones)            
            case 3:
                opciones = []
                for tupla in Modificaciones:
                    opciones.append(tupla[0])    
                opcion = submenu('Borrar', '¿Cuál quieres borrar?', opciones)
                if opcion != 0 and eleccion(f'¿Seguro que quieres borrar: {opciones[opcion-1]}'):
                    Modificaciones.pop(opcion-1)
            case 4:
                opciones = []
                for tupla in Modificaciones:
                    opciones.append(tupla[0])    
                tupla = submenu('Modificación', '¿Cuál quieres cambiar?', opciones)
                if tupla != 0:
                    Tupla = Modificaciones[tupla-1]
                    lista = list(Tupla)
                    Modificaciones[tupla-1] = tuple(operacion_Modificar(lista, Fecha))
                            
            case 5:
                #Si esta vacío no actualiza.
                if bool(Modificaciones) is False:
                    print('>>>No hay Modificaciones para ingresar')
                else:
                    for Tupla in Modificaciones:
                        ctr.updateOperacion(Base, cursor, Tupla)
                    modificacion += len(Modificaciones)
                    Modificaciones = []


def DL(fecha) -> str:
    """
    Convierte una fecha a formato legible en español: [día] DD de Mes del YYYY
    
    Args:
        fecha: Puede ser str en formato 'YYYY-MM-DD' o un objeto datetime
        
    Returns:
        str: Fecha formateada en español, ej: '[Lun] 1 de Enero del 2024'
        
    Raises:
        ValueError: Si el formato de fecha es inválido
    """
    # Diccionario para traducir días y meses
    dias = {
        'Mon': 'Lun', 'Tue': 'Mar', 'Wed': 'Mié',
        'Thu': 'Jue', 'Fri': 'Vie', 'Sat': 'Sáb', 'Sun': 'Dom'
    }
    
    meses = {
        'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo',
        'April': 'Abril', 'May': 'Mayo', 'June': 'Junio',
        'July': 'Julio', 'August': 'Agosto', 'September': 'Septiembre',
        'October': 'Octubre', 'November': 'Noviembre', 'December': 'Diciembre'
    }
    
    try:
        # Convertir a datetime si es string
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d') if isinstance(fecha, str) else fecha
        
        # Formatear fecha
        fecha_txt = fecha_obj.strftime('[%a] %d de %B del %Y')
        
        # Traducir día y mes
        for eng, esp in dias.items():
            fecha_txt = fecha_txt.replace(eng, esp)
        for eng, esp in meses.items():
            fecha_txt = fecha_txt.replace(eng, esp)
        
        # Eliminar ceros iniciales en días
        fecha_txt = fecha_txt.replace(' 0', ' ')
        
        return fecha_txt
        
    except (ValueError, AttributeError) as e:
        raise ValueError(f"Formato de fecha inválido. Debe ser 'YYYY-MM-DD' o datetime: {str(e)}")
        
# ------------------------------------- Datos ingresar -----------------------------------------------------
def actualizar_diario(Base, cursor, fecha_objeto):
    # 1. Insertar movimientos recurrentes
    ctr.insertar_recurrencias(Base, cursor, fecha_objeto.strftime('%Y-%m-%d'))
    
    # 2. Calcular y actualizar saldo del día
    fecha_actual = fecha_objeto.strftime('%Y-%m-%d')
    dia_id = ctr.ID_de_fecha(cursor, fecha_actual)
    
    # Obtener la suma de todos los movimientos del día
    cursor.execute('''
        SELECT COALESCE(SUM(i.MONTO), 0)
        FROM Transacciones t
        JOIN Info_transacciones i ON t.INFO_ID = i.INFO_ID
        WHERE t.DIA_ID = ?
    ''', (dia_id,))
    saldo_dia = cursor.fetchone()[0]
    
    # Obtener saldo anterior
    if dia_id > 1:
        cursor.execute('SELECT SALDO FROM Diario WHERE DIA_ID = ?', (dia_id - 1,))
        saldo_anterior = cursor.fetchone()[0]
    else:
        saldo_anterior = 0
    
    # Actualizar saldo del día
    cursor.execute('''
        UPDATE Diario 
        SET DIA_SALDO = ?,
            SALDO = ? + ?
        WHERE DIA_ID = ?
    ''', (saldo_dia, saldo_anterior, saldo_dia, dia_id))
    
    Base.commit()
    
    # 3. Actualizar estadísticas con el nuevo saldo
    ctr.actualizar_estadisticas(Base, cursor, fecha_objeto)


def datos_Ingresar(Base, cursor): #Cuando el tipo es 1 se regresa con intervalo, 0 sin intervalo
    ultimo_dia, Dia_ID = ctr.fecha_Max(cursor)
    ultimo_dia_txt = DL(ultimo_dia)
    print(f"El último día es: {ultimo_dia_txt}")
    dia_Hoy_objeto = datetime.now().date()
    dia_Hoy_str = dia_Hoy_objeto.strftime('%Y-%m-%d')
    print(f'Haciendo la diferencia entre: {dia_Hoy_str} y {ultimo_dia}.')
    diferencia = ctr.fecha_compara(dia_Hoy_str,ultimo_dia)
    print(f'La diferencia es: {diferencia}')
    ctr.generarDias(Base, cursor, ultimo_dia, diferencia)
    if diferencia <= 0:
        operacion(Base,cursor, Dia_ID, ultimo_dia)
    elif diferencia == 1:  
        operacion(Base,cursor, Dia_ID, ultimo_dia)
        actualizar_diario(Base, cursor, dia_Hoy_objeto)
    else:
        fecha_objeto = datetime.strptime(ultimo_dia, '%Y-%m-%d').date()
        # Pregunta si quieres ingresar dia por día o pasar. Luego para cada dia pregunta si para ese día hay datos que ingresar.  
        if eleccion(f'.:Han pasado {diferencia} días >> ¿Quieres ingresar datos para esos días?'):
            
            for _ in range(diferencia):
                fecha_objeto += timedelta(days=1)
                fecha_actual_str = fecha_objeto.strftime('%Y-%m-%d')
                fecha_actual_txt = DL(fecha_objeto)
                actualizar_diario(Base, cursor, fecha_objeto)
                # TODO: tener la opción de saltarte varias fechas.
                if eleccion(f'Para la fecha {fecha_actual_txt} ¿Quieres ingresar datos?'):
                    Dia_id_N = ctr.ID_de_fecha(cursor,fecha_actual_str)
                    operacion(Base,cursor, Dia_id_N, fecha_actual_str)

        else:
            for _ in range(diferencia):
                fecha_objeto += timedelta(days=1)
                actualizar_diario(Base, cursor, fecha_objeto)
    
def datos_Modificar(Base, cursor):
    #Para conocer hasta el día en que se pueden hacer cambios.
    _, Dia_ID_Max = ctr.fecha_Max(cursor)
    Fecha, Dia_ID = fecha_Seleccionar(cursor) #YYYY-MM-DD
    Dia_ID_Inicio = Dia_ID
    Num_Operaciones = 0
    
    while True:
        opcion = submenu(f'Modificar el {Fecha}', '¿Qué deseas realizar?', ('Agregar operaciones', 'Modificar alguna operación', 'Cambiar día'))
        # Usamos Num_Operaciones para ver cuántas actualizaciones de saldos se realizarán.
        match opcion:
            case 0: break
            case 1: 
                Num_Operaciones += operacion(Base, cursor, Dia_ID, Fecha)                           
            case 2: 
                Num_Operaciones += modificar(Base, cursor, Dia_ID, Fecha) # En construcción
            case 3: 
                Fecha, Dia_ID = fecha_Seleccionar(Base,cursor) # En construcción
                if Num_Operaciones == 0:
                    Dia_ID_Inicio = Dia_ID
                elif Dia_ID < Dia_ID_Inicio:
                    Dia_ID_Inicio = Dia_ID

    # Antes de actualizar los saldos y para que no se actualicen de manera innecesaria.
    if Num_Operaciones != 0 and Dia_ID_Inicio != Dia_ID_Max:          
        ctr.updateSaldos(Base, cursor, Dia_ID_Inicio, Dia_ID_Max)


def base_Cerrar(Base, cursor):
    Base.commit()
    cursor.close()
    Base.close()
    print("Base cerrada...")
    
def datos_Mostrar(cursor):
    while True:
        opciones = ('Todo', 'Transacciones', 'Info transacciones', 'Rubros', 'Flujo', 'Diario', 'Semanal', 'Mensual', 'Anual')
        opcion = submenu('Mostrar DATOS','¿Que tabla quieres que muestre?', opciones)
        match(opcion):
            case 0:
                break
            case 1:
                ctr.printAll(cursor)
            case 2:
                ctr.printTransacciones(cursor)
            case 3:
                ctr.printInfo_trasacciones(cursor)
            case 4:
                ctr.printRubro(cursor)
            case 5:
                ctr.printFlujo(cursor)
            case 6:
                ctr.printDiario(cursor)
            case 7:
                ctr.printSemanal(cursor)
            case 8:
                ctr.printMensual(cursor)
            case 9:
                ctr.printAnual(cursor)
            case _:
                print(">>>Opción no valida")

   
# -------------------------------------- Menu -----------------------------------------------
def menu():
    Base, cursor, Usuario = usuario_Iniciar()
    while True:
        print("<----------  MENU  ---------->\n")
        print("1. Registrar movimiento")
        print("2. Mostrar movimiento")
        print("3. Modificar movimiento")
        print("4. Quitar/restaurar histórico")
        # TODO Poner las operaciones de usuario en un apartado
        print("5. Cambiar de usuario")
        print("6. Crear nuevo Usuario")
        print("7. Borrar un usuario")
        print("0. Salir")
        opcion = input_validado("Elige la opcion que quieres:\nR: ", 1)

        match(opcion):
            case 0:
                break
            case 1:
                datos_Ingresar(Base, cursor)
            case 2:
                print('--En construccion')
                datos_Mostrar(cursor)
            case 3:
                print('En construccion')
                datos_Modificar(Base, cursor)
            case 4:
                pass
            case 5:
                base_Cerrar(Base, cursor)
                Usuario = usuarios_Elegir(usuarios_menu())         
                Base, cursor = ctr.base_Inicializar(2, Usuario)
            case 6:
                Base, cursor, Usuario = usuario_Nuevo() 
            case 7:
                if (usuarios_Borrar(usuarios_menu(), Base, cursor, Usuario)):
                    Base, cursor, Usuario = usuario_Iniciar()
            case _:
                print(">>>No existe esa operacion")
    base_Cerrar(Base, cursor)
    
#=============================================================================================================
#                                          === MAIN ===
#=============================================================================================================

menu()

#=============================================================================================================
#                                          === A realizar ===
#=============================================================================================================

#TODO Meter datos de prueba para probar el trigger Actualizador_Monto
#TODO  Hacer la función para actualizar operaciones con intervalo Operaciones_Intervalo
#TODO  Hacer la función operación_Modificar() que quita los registros de modo que ya no activos, se usan los triggers para actualizar los saldos automáticamente si es que se actualiza la columna estado.
#TODO  Hacer un submenú para los rubros y dejarte elegir.

# No prioritarios ----------------------------------------------------------------------------------------------------------------------------

#TODO  Cambiar la impresión de tablas para que se muestren sólo las operaciones activas.
#TODO  Hacer la validación: monto no debe ser cero
#TODO  Buscar una manera de que las fechas en español salgan bien.
#TODO  Hacer que el porcentaje tenga un % para el ingreso del dato sin que el usuario lo ponga. input('Porcentaje (%)': )    Porcentaje: %

# ERRORES ------------------------------------------------------------------------------------------------------------------------------------

