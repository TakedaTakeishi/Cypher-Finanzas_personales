import Base_Controlador as ctr
from os import path
from datetime import datetime, timedelta
import os
import locale

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

def fecha_ingresar():
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
    with open(ruta, 'a') as file:
        Usuario = Nombre + '\n'
        file.write(Usuario)

#def fecha_

def fecha_Inicial():
    fecha_hora_actual = datetime.now()
    print(".:Fecha a iniciar analisis:.")
    while True:
        entered_date_str = fecha_ingresar()
        entered_date = datetime.strptime(entered_date_str, "%Y-%m-%d")
        if entered_date <= fecha_hora_actual:
            break
        else:
            print(">>>La fecha no puede ser mayor a la fecha actual")
    return entered_date_str


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
'''        
def contar_lineas(archivo):
    with open(archivo, 'r') as f:
        contenido = f.read()
    lineas = contenido.splitlines()
    return len(lineas)
'''

def usuario_Nuevo():
    ruta = path.realpath('Usuarios.txt')
    Nombre = usuario_Crear()
    usuario_Asigna(ruta, Nombre)
    Fecha = fecha_Inicial()
    Base, cursor = ctr.base_Inicializar(1, Nombre, Fecha)
    return Base, cursor, Nombre

def usuario_Nombre(ruta, fila):
    with open(ruta, 'r') as file:
        Nombre = file.readlines()[fila-1]
    return Nombre.strip()
    
def usuarios_Elegir(Usuarios_Max):
    ruta = path.realpath('Usuarios.txt')
    while True:
        print()
        opcion = int(input("Elije el número de usuario: "))
        if (0 < opcion <= Usuarios_Max):
            Usuario = usuario_Nombre(ruta, opcion)
            return Usuario
        print("Valor inválido")



def usuarios_menu():
    print("Elije usuario:")
    ruta = path.realpath('Usuarios.txt')
    file_object = open(ruta, "r", encoding="utf-8")
    # Loop over and print each line in the file object.
    i = 0
    for string in file_object:
        i += 1
        print(f'{i}. {string}', end='')
    #Enviamos i para saber el número máximo de usuarios.
    return i
        

def usuario_Iniciar():
    ruta = path.realpath('Usuarios.txt')
    with open(ruta,'r') as file: 
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
    ruta = path.realpath('Usuarios.txt')
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
            #Verificar si los días no entran en todos los meses.
            if(int(fecha[5:7]) > 29):
                while True:       
                    print(f'No todos los días tienen {fecha[-2:]} ¿Quieres que se repita al final del mes o cada 28?')
                    mes = int(input('''1. Fin de mes
                                    \n 2. Cada 28'''))
                    if(1 <= mes <= 2):
                        break
                if mes == 1:
                    return 'Fin de mes'
                else:
                    return 'Cada 28'
            else:
                print(f'La operación se repetirá cada: {fecha[5:7]} de cada mes')
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

def dato_Intervalo_Numero(Tipo):
    if (type(Tipo) is int):
        return Tipo
    if (type(Tipo) is None):
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
    print(f'Monto:\t${monto}')
    if(rubro is not None):
        print(f'rubro:\t\t{rubro}')
    if(intervalo is not None):
        print(f'intervalo:\t{intervalo}')
    if(fecha_final is not None):
        print(f'fecha_final:\t{fecha_final}')
    if(intereses is not None):
        print(f'intereses:\t{intereses}%')
    print()
'''
def operacion(Base, cursor, Dia_ID, Fecha):
    while True:
        choice = submenu('Operaciones', '¿Qué tipo de operación quieres?', ('Simple', 'Recurrente') )
        if choice == 0:
            break
        # Verificar los datos.
        concepto =  input_validado("Ingresa el concepto: ", 5)
        if(concepto == 'Cancelar'):
            continue
        monto = input_validado("Ingresa la monto: ", 2)
        rubro = None
        intervalo =  None
        fecha_final = None
        intereses = None
        if choice == 2 :
            intervalo =  dato_Intervalo_Numero(dato_Intervalo_Tipo(Fecha))
            if (intervalo is None):
                choice = 1
                rubro = input_rubro()
            else:
                rubro = input_validado("Ingresa el Rubro: ", 5) 
                if eleccion('¿Tiene fecha de finalización?'):
                    fecha_final = fecha_ingresar()
                    
                if eleccion('¿Cuenta con intereses?'):
                    porcentaje = input_validado("¿Cuál es el porcentaje?: ", 2)
                    intereses = porcentaje / 100    

        else:
            rubro = input_rubro()
                
        opcion = None
        continuar = True
        opciones = ('Concepto','Rubro','Monto','intervalo','Porcentaje','Fecha final')
        while(continuar == True):
            printOperacion(choice, concepto, monto, rubro, intervalo, fecha_final, intereses)
            if(eleccion('¿Desea cambiar algo?')):
                if(choice == 2):
                    opcion = submenu('Cambiar algun Dato','¿Que dato quieres cambiar?',opciones)
                else:
                    opcion = submenu('Cambiar algun Dato','¿Que dato quieres cambiar?',opciones[:-3])
                match(opcion):
                    case 0: break
                    case 1: concepto =  input_validado("Ingresa el concepto: ", 4)
                    case 2: rubro = input_rubro() 
                    case 3: monto = input_validado("Ingresa la monto: ", 2)
                    case 4: intervalo =  dato_Intervalo_Numero(dato_Intervalo_Tipo(Fecha))
                    case 5: 
                        porcentaje = input_validado("¿Cuál es el porcentaje?: ", 2)
                        intereses = porcentaje / 100  
                    case 6: fecha_final = fecha_ingresar()
                
            else: break
        
        if(eleccion('¿Insertar la operación?')):
            ctr.insertOperation(Base, cursor, Dia_ID, concepto,monto,rubro,intervalo,fecha_final,intereses)

        if not eleccion('¿Quieres seguir ingresando más operaciones?'):
            break
'''
def operacion(Base, cursor, Dia_ID, Fecha):
    Operaciones = []
    while True:
        opciones = ('Crear operaciones', 'Mostrar operaciones', 'Borrar operación', 'Modificar operación', 'Guardar operación')
        opcion = submenu(f"Menu Ingreso Fecha: {Fecha}", 'Elige que deseas hacer', opciones)
        match opcion:
            case 0: break
            case 1:
                while True:
                    choice = submenu('Operaciones', '¿Qué tipo de operación quieres?', ('Simple', 'Recurrente') )
                    if choice == 0:
                        break
                    # Verificar los datos.
                    concepto =  input_validado("Ingresa el concepto: ", 5)
                    if(concepto == 'Cancelar'):
                        continue
                    monto = input_validado("Ingresa la monto: ", 2)
                    rubro = None
                    intervalo =  None
                    fecha_final = None
                    intereses = None
                    if choice == 2 :
                        intervalo =  dato_Intervalo_Numero(dato_Intervalo_Tipo(Fecha))
                        if (intervalo is None):
                            choice = 1
                            rubro = input_rubro()
                        else:
                            rubro = input_validado("Ingresa el Rubro: ", 5) 
                            if eleccion('¿Tiene fecha de finalización?'):
                                fecha_final = fecha_ingresar()
                                
                            if eleccion('¿Cuenta con intereses?'):
                                porcentaje = input_validado("¿Cuál es el porcentaje?: ", 2)
                                intereses = porcentaje / 100    
                    
                    else:
                        rubro = input_rubro() 
                    
                    Tupla = (concepto, monto, rubro, intervalo, fecha_final, intereses)
                    Operaciones.append(Tupla)
            case 2:
                i = 1
                for op in Operaciones:
                    print(f'\n\tOperación: {i}')
                    printOperacion(op[0], op[1], op[2], op[3], op[4], op[5])
                    i = i + 1
            case 3:
                i = 0
                opciones = []
                for op in Operaciones:
                    opciones.append(op[0])    
                opcion = submenu('Borrar', '¿Cuál quieres borrar?', opciones)
                
                if opcion !=0 and eleccion(f'¿Seguro que quieres borrar: {opciones[opcion-1]}'):
                    Operaciones.pop(opcion-1)
            case 4:
                i = 0
                opciones = []
                for op in Operaciones:
                    opciones[i].append(op[0])    
                op = submenu('Borrar', '¿Cuál quieres cambiar?', opciones)
                if op !=0 and eleccion(f'¿Seguro que quieres cambiar: {opciones[opcion-1]}'):
                    Tupla = Operaciones[op-1]
                    lista = list(Tupla)
                    opcion = None
                    continuar = True
                    opciones = ('Concepto', 'Monto', 'Rubro', 'Intervalo', 'Fecha final' ,'Intereses')
                    while(continuar == True):
                        # 'Concepto', 'Monto', 'Rubro', 'Intervalo', 'Fecha final' ,'Intereses'
                        printOperacion(lista[0], lista[1], lista[2], lista[3], lista[4], lista[5])
                        if(eleccion('¿Desea cambiar algo?')):
                            if(Tupla[3] is not None):
                                opcion = submenu('Cambiar algun Dato','¿Que dato quieres cambiar?',opciones)
                            else:
                                opcion = submenu('Cambiar algun Dato','¿Que dato quieres cambiar?',opciones[:-3])
                            match(opcion):
                                case 0: break
                                case 1: lista[0] = input_validado("Ingresa el concepto: ", 4)
                                case 2: lista[1] = input_validado("Ingresa la monto: ", 2)
                                case 3: lista[2] = input_rubro()
                                case 4: lista[3] =  dato_Intervalo_Numero(dato_Intervalo_Tipo(Fecha))
                                case 5: lista[4] = fecha_ingresar() # Verificar que la fecha ingresada sea mayor a la actual.
                                case 6: 
                                    porcentaje = input_validado("¿Cuál es el porcentaje?: ", 2)
                                    lista[5] = porcentaje / 100  
                        else: break                   

# ¿Cual quieres borrar?
# 1. Comida para Pepe
# 2. Compra de Carro 
# 3.
# 0. Salir
# remove(choise-1)

# submenu-----------------
# ----------Menu Ingreso <Dia>--------
# 1. datos_ingresar
# 2. Mostrar operaciones
# 3. Borrar operacion
# 4. Modificar operacion
# 5. Guardar operacion
# 6. Salir



def DL(fecha):
    if (type(fecha) is str):
        fecha_objeto = datetime.strptime(fecha, '%Y-%m-%d')
        fecha_txt = fecha_objeto.strftime('[%a] %d de %B del %Y')
    elif (type(fecha) is datetime):
        fecha_txt = fecha.strftime('[%a] %d de %B del %Y')
    fecha_DL= fecha_txt.replace(' 0', ' ')
    return fecha_DL
        
# ------------------------------------- Datos ingresar -----------------------------------------------------



def datos_Ingresar(Base, cursor): #Cuando el tipo es 1 se regresa con intervalo, 0 sin intervalo
    ultimo_dia, Dia_ID = ctr.fecha_Ultima(cursor)
    ultimo_dia_txt = DL(ultimo_dia)
    print(f"El último día es: {ultimo_dia_txt}")
    diferencia = ctr.diferencia(cursor, datetime.now(), ultimo_dia,'d')
    print(f'La diferencia es: {diferencia}')
    ctr.generarDias(Base, cursor, ultimo_dia, diferencia)
    if diferencia <= 1:  
        operacion(Base,cursor, Dia_ID, ultimo_dia)
  
    else:
        #Falta por terminar: Pregunta si quieres ingresar dia por día o pasar. Luego para cada dia pregunta si para ese día hay datos que ingresar.  
        if eleccion(f'.:Han pasado {diferencia} días >> ¿Quieres ingresar datos para esos días?'):
            fecha_objeto = datetime.strptime(ultimo_dia, '%Y-%m-%d')
            
            for _ in range(diferencia):
                fecha_objeto += timedelta(days=1)
                fecha_actual_str = fecha_objeto.strftime('%Y-%m-%d')
                fecha_actual_txt = DL(fecha_objeto)
                if eleccion(f'Para la fecha {fecha_actual_txt} ¿Quieres ingresar datos?'):
                    operacion(Base,cursor, Dia_ID, fecha_actual_str)
    

def base_Cerrar(Base, cursor):
    Base.commit()
    cursor.close()
    Base.close()
    print("Base cerrada...")
    
def menu_mostrar(cursor):
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
    
# --------------------------------------Menu --------------------------------------------------------
def menu():
    #Para no tener que configurar varias veces el tiempo local en su formato, lo hacemos aquí.
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8') #Generalizar dependiendo del sistema en el que corra.
    Base, cursor, Usuario = usuario_Iniciar()
    while True:
        print("----------MENU----------\n")
        print("1. Ingresar Datos")
        print("2. Mostrar Datos")
        print("3. Modificar Datos")
        print("4. Cambiar de usuario")
        print("5. Crear nuevo Usuario")
        print("6. Borrar un usuario")
        print("0. Salir")
        opcion = input_validado("Elige la opcion que quieres:\nR: ", 1)

        match(opcion):
            case 0:
                break
            case 1:
                datos_Ingresar(Base, cursor)
            case 2:
                print('--En construccion')
                menu_mostrar(cursor)
            #     #datos_Mostrar(cursor)
            case 3:
                print('En construccion')
            #     datos_Modificar()
            case 4:
                base_Cerrar(Base, cursor)
                Usuario = usuarios_Elegir(usuarios_menu())         
                Base, cursor = ctr.base_Inicializar(2, Usuario)
            case 5:
                    
                Base, cursor, Usuario = usuario_Nuevo() 
            case 6:
                if (usuarios_Borrar(usuarios_menu(), Base, cursor, Usuario)):
                    Base, cursor, Usuario = usuario_Iniciar()
            case _:
                print(">>>No existe esa operacion")
    base_Cerrar(Base, cursor)
    

#---------------------------------- MAIN -----------------------------------
menu()
# Revisar si se crean el archivo Usuario.txt automáticamente.
# Probar el ingresar datos para recurrentes. (Terminar el menú opción 4 y una función para comparar las fechas.)
# Hacer una validación para cancelar la operacion actual.
# Hacer la función o funciones para comparar fechas sin importar si son objetos (datatime) o strings (estándar).
# Buscar una manera de que las fechas en español salgan bien.
# validar que en concepto y el rubro para que no sean numeros.
# Hacer que el porcentaje tenga un % para el ingreso del dato sin que el usuario lo ponga. input('Porcentaje (%)': )    Porcentaje: %
# Hacer un submenú para los rubros y dejarte elegir.