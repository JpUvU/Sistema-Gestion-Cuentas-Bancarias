import os 
base_de_datos = {}

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
            Saldocredito = 0

            if tipoCuenta == 'ahorros' or tipoCuenta ==  'corriente':
                datos_usuario = {nombre: {'cedula': cc, 'email': email, 'contacto': contacto, 'ciudad': ubicacion, 'saldo': saldo, 'Tipo': tipoCuenta, 'Credito': Saldocredito }}

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
            except ValueError:
                print("Error: Ingrese un valor numérico válido.")
            return # Salimos de la función una vez que encontramos al usuario

    # Si el bucle termina sin encontrar el usuario
    print('No se ha encontrado el usuario.')


def solicitar_credito():
    pass


while True:
    menu_principal()
    opcion = int(input('Ingrese la opcion a ejecutar: '))
    os.system('cls')
    match opcion:
        case 1:
            crear_cuenta()
        case 2:
            depositar_saldo()

