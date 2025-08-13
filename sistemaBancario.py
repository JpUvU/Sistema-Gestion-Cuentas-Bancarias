import os 
base_de_datos = {}
mov_depoist = 0
def menu_principal():
    print('--------------------------------------')
    print('''      GESTION DE CUENTAS BANCARIAS       
            1: Crear cuenta 
            2: Depositar Dinero
            3: Solicitar Credito
            4: Retirar Dinero
            5: Pago Cuota Credito
            6: Cancelar Cuenta''')
    print('--------------------------------------')


    
def crear_cuenta():

    crear_cuenta = input('Si desea crear la cuenta ingrese "S" para si o "N" para no: ').strip().upper()

    if crear_cuenta == 'S':
        print('Creando la cuenta')
        try:
            nombre = input('Ingrese el nombre: ')
            cc = int(input('Digite la cedula sin puntos y sin espacios...ejm: 1097066225: '))
            email = input('Ingrese el email: ')
            contacto = int(input('Ingrese su numero telefonico: '))
            ubicacion = input('Ingrese la ciudad de residencia: ').strip()
            saldo = int(input('Ingrese el saldo inicial: '))
            tipoCuenta = input('Ingrese si la cuenta sera ahorros o corriente: ').strip()
            saldo_cdt = 0
            SaldocreditoLibreInv = 0


            if tipoCuenta == 'ahorros' or tipoCuenta ==  'corriente':
                datos_usuario = {nombre: {'cedula': cc, 'email': email, 'contacto': contacto, 'ciudad': ubicacion, 'saldo': saldo, 
                                          'productos':{'Tipo': tipoCuenta, 'CDT': saldo_cdt ,'credito libre inversion': SaldocreditoLibreInv}}}

                llave = len(base_de_datos) + 1
                base_de_datos.update({llave: datos_usuario})
            else:
                print('error')
        except ValueError:
            print('Error inesperado, ingresa los datos correctamente...')

        print(base_de_datos)
    else:
        print('saliendo...')


def depositar_saldo():
    user = input('Ingrese nombre del usuario al cual le vas a depositar: ')
    global mov_depoist
    # Recorremos el diccionario principal
    for llave, item in base_de_datos.items():

        nombre_guardado = list(item.keys())[0] 
        datos_usuario = list(item.values())[0] 
        
        # Comparamos el nombre ingresado con el nombre que encontramos
        if user == nombre_guardado:
            saldo_actual = datos_usuario.get('saldo')
            print(f'Saldo actual para {user}: {saldo_actual}')
            
            try:
                monto_a_depositar = int(input(f'Ingrese el saldo a agregar a el sr/sra {user}: '))
                datos_usuario['saldo'] += monto_a_depositar
                print(f'Depósito exitoso. Nuevo saldo para {user}: {datos_usuario["saldo"]}')
                mov_depoist += 1
            except ValueError:
                print("Error: Ingrese un valor numérico válido.")
            return # Salimos de la función una vez que encontramos al usuario

    # Si el bucle termina sin encontrar el usuario
    print('No se ha encontrado el usuario.')



def menu_credito():
    print('--------------------------------------')
    print('''      Consulta del portafolio       
            1: CDT 
            2: Credito libre inversion
            3: Credito de vivienda
            4: Credito para comprar automovil''')
    print('--------------------------------------')



def portafolio():
    menu_credito()
    optionPortafolio = int(input('Ingresa la opcion deseada para proceder: '))

    if optionPortafolio == 1:
         saldo_cdt()
    elif optionPortafolio == 2:
        credit_libre_inversion()
        
        
def saldo_cdt():
    try:
        cedula = int(input('Ingrese la cédula del usuario al que se le abrirá el CDT: '))
        # Recorremos el diccionario principal
        for llave, item in base_de_datos.items():

            # Guardamos la clave principal, es decir el nombre
            nombre_usuario = list(item.keys())[0]
            # Guardamos los valores de la clave principal
            datos_usuario = item[nombre_usuario]
            
            # Para saber si la cedula que nosotros buscamos coincide con los valores guardados en datos_usuario...
            if datos_usuario['cedula'] == cedula:
                print(f'Usuario encontrado: {nombre_usuario}')
                print(f'Saldo actual: {datos_usuario["saldo"]}')

                monto = int(input('Ingrese el monto que desea invertir en el CDT: '))
                if monto > datos_usuario['saldo']:
                    print('Fondos insuficientes para abrir el CDT.')
                    return
                else:
                    datos_usuario['saldo'] -= monto
                    datos_usuario['productos']['CDT'] += monto
                    print(f'CDT creado exitosamente por ${monto}')
                    print(f'Nuevo saldo: {datos_usuario["saldo"]}')
                    print(f'CDT actual: {datos_usuario["productos"]["CDT"]}')
                    return
        print('Usuario no encontrado con esa cédula.')
    except ValueError:
        print('Error: debe ingresar un número de cédula y un monto válidos.')


def credit_libre_inversion():
    try:
        cedula = int(input('Ingrese la cédula del usuario al que se le abrirá crédito de libre inversión: '))

        for llave, item in base_de_datos.items():
            nombre_usuario = list(item.keys())[0]
            datos_usuario = item[nombre_usuario]

            if cedula == datos_usuario['cedula']:
                print(f'Usuario encontrado: {nombre_usuario}')
                print(f'Saldo actual: {datos_usuario["saldo"]}')

                montoAprestar = int(input('Ingresa el monto que vas a solicitar de libre inversión: '))

                # Suponiendo que permites solo un crédito activo por persona
                if datos_usuario['productos']['Credito'] > 0:
                    print('Lo sentimos, ya tienes un crédito activo.')
                else:
                    datos_usuario['productos']['Credito'] += montoAprestar
                    datos_usuario['saldo'] += montoAprestar  # Se suma al saldo
                    print(f'Sr/Sra {nombre_usuario}, su crédito fue aprobado por ${montoAprestar}')
                    print(f'Nuevo saldo: {datos_usuario["saldo"]}')
                    print(f'Crédito actual: {datos_usuario["productos"]["Credito"]}')
                return

        print('Usuario no encontrado con esa cédula.')

    except ValueError:
        print('Error: debe ingresar números válidos para cédula y monto.')


            
while True:
    menu_principal()
    opcion = int(input('Ingrese la opcion a ejecutar: '))
    os.system('cls')
    match opcion:
        case 1:
            crear_cuenta()
        case 2:
            depositar_saldo()
        case 3:
            portafolio()

