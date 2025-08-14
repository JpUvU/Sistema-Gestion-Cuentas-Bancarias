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
            6: Cancelar Cuenta
            7: Salir del sistema''')
    print('--------------------------------------')
import uuid

def generar_id():
    return str(uuid.uuid4())[:8]  # ID único corto
    
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
            SaldoCreditoLibreInv = 0
            SaldoCreditoVivienda = 0
            saldoCreditoAutomovil = 0
            deudaCredito = 0

            if tipoCuenta == 'ahorros' or tipoCuenta ==  'corriente':
                datos_usuario = {nombre: {'cedula': cc, 'email': email, 'contacto': contacto, 'ciudad': ubicacion, 'saldo': saldo,'deuda': deudaCredito, 
                                          'productos':{ generar_id():{'Tipo': tipoCuenta}, generar_id():{'CDT': saldo_cdt} , generar_id():{'credito libre inversion': SaldoCreditoLibreInv},
                                            generar_id():{'credito vivienda: ': SaldoCreditoVivienda}, generar_id():{'credito automovil': saldoCreditoAutomovil}}}}

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



def menu_credito():
    print('--------------------------------------')
    print('''      Consulta del portafolio       
            1: CDT 
            2: Credito libre inversion
            3: Credito de vivienda
            4: Credito para comprar automovil
            5: Historial de productos''')
    print('--------------------------------------')



def portafolio():
    menu_credito()
    optionPortafolio = int(input('Ingresa la opcion deseada para proceder: '))

    if optionPortafolio == 1:
         saldo_cdt()
    elif optionPortafolio == 2:
        credit_libre_inversion()
    elif optionPortafolio == 3:
        credit_vivienda()
    elif optionPortafolio == 4:
        credit_automovil()
    elif optionPortafolio == 5:
        historial_productos()
        
        
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
                if monto > datos_usuario['saldo'] or datos_usuario['saldo'] < 0:
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

                # Verificamos si tiene deuda activa
                if datos_usuario['deuda'] > 0:
                    print(f'No puedes abrir otro crédito sr/sra {nombre_usuario} . Tienes deuda activa.')
                    return
                montoAprestar = int(input('Ingresa el monto que vas a solicitar: '))
                datos_usuario['productos']['credito libre inversion'] += montoAprestar
                datos_usuario['saldo'] += montoAprestar
                datos_usuario['deuda'] += montoAprestar
                print(f'Su crédito fue aprobado por ${montoAprestar}')
                print(f'Nuevo saldo: {datos_usuario["saldo"]}')
                print(f'Deuda actual: {datos_usuario["deuda"]}')
                return

        print('Usuario no encontrado con esa cédula.')

    except ValueError:
        print('Error: debe ingresar números válidos para cédula y monto.')


def credit_vivienda():
    try:
        cedula = int(input('Ingrese la cédula del usuario al que se le abrirá crédito de vivienda: '))

        for llave, item in base_de_datos.items():
            nombre_usuario = list(item.keys())[0]
            datos_usuario = item[nombre_usuario]

            if cedula == datos_usuario['cedula']:
                print(f'Usuario encontrado: {nombre_usuario}')
                print(f'Saldo actual: {datos_usuario["saldo"]}')

                if datos_usuario['deuda'] > 0:
                    print('No puedes abrir otro crédito. Tienes deuda activa.')
                    return

                montoAprestar = int(input('Ingresa el monto que vas a solicitar: '))
                datos_usuario['productos']['credito vivienda'] += montoAprestar
                datos_usuario['saldo'] += montoAprestar
                datos_usuario['deuda'] += montoAprestar
                print(f'Su crédito de vivienda fue aprobado por ${montoAprestar}')
                print(f'Nuevo saldo: {datos_usuario["saldo"]}')
                print(f'Deuda actual: {datos_usuario["deuda"]}')
                return

        print('Usuario no encontrado con esa cédula.')

    except ValueError:
        print('Error: debe ingresar números válidos para cédula y monto.')

def credit_automovil():
    try:
        cedula = int(input('Ingrese la cédula del usuario al que se le abrirá crédito de automovil: '))

        for llave, item in base_de_datos.items():
            nombre_usuario = list(item.keys())[0]
            datos_usuario = item[nombre_usuario]

            if cedula == datos_usuario['cedula']:
                print(f'Usuario encontrado: {nombre_usuario}')
                print(f'Saldo actual: {datos_usuario["saldo"]}')

                if datos_usuario['deuda'] > 0:
                    print('No puedes abrir otro crédito. Tienes deuda activa.')
                    return

                montoAprestar = int(input('Ingresa el monto que vas a solicitar: '))
                datos_usuario['productos']['credito automovil'] += montoAprestar
                datos_usuario['saldo'] += montoAprestar
                datos_usuario['deuda'] += montoAprestar
                print(f'Su crédito de automovil fue aprobado por ${montoAprestar}')
                print(f'Nuevo saldo: {datos_usuario["saldo"]}')
                print(f'Deuda actual: {datos_usuario["deuda"]}')
                return

        print('Usuario no encontrado con esa cédula.')

    except ValueError:
        print('Error: debe ingresar números válidos para cédula y monto.')


def retirar_saldo():
    user = input('Ingrese nombre del usuario al cual le vas a retirar saldo: ')
    
    for llave, item in base_de_datos.items():
        nombre_guardado = list(item.keys())[0] 
        datos_usuario = list(item.values())[0] 
        
        if user == nombre_guardado:
            saldo_actual = datos_usuario["saldo"]
            print(f'Saldo actual para {user}: {saldo_actual}')
            
            try:
                monto_a_retirar = int(input(f'Ingrese el monto a retirar de {user}: '))
                
                if monto_a_retirar <= 0:
                    print("Error: El monto debe ser mayor que cero.")
                    return
                
                if saldo_actual >= monto_a_retirar:
                    datos_usuario["saldo"] -= monto_a_retirar
                    print(f'Retiro exitoso. Nuevo saldo para {user}: {datos_usuario["saldo"]}')
                else:
                    print('Lo sentimos, no tienes suficiente saldo para poder retirar ese valor.')
            except ValueError:
                print("Error: Ingrese un valor numérico válido.")
            return

    print('No se ha encontrado el usuario.')


def pagar_deuda():
    user = input('Ingrese nombre del usuario al cual le vas a pagar la deuda: ')
    
    for llave, item in base_de_datos.items():
        nombre_guardado = list(item.keys())[0] 
        datos_usuario = list(item.values())[0] 
        
        if user == nombre_guardado:
            saldo_actual = datos_usuario.get("saldo", 0)
            deuda_actual = datos_usuario.get("deuda", 0)

            print(f'Saldo actual: {saldo_actual}')
            print(f'Deuda actual: {deuda_actual}')
            
            try:
                monto_a_pagar = int(input(f'Ingrese el monto a pagar de {user}: '))
                
                if monto_a_pagar <= 0:
                    print("Error: El monto debe ser mayor que cero.")
                    return
                
                if saldo_actual < monto_a_pagar:
                    print("Error: No tienes saldo suficiente para pagar esa cantidad.")
                    return

                if deuda_actual <= 0:
                    print("El usuario no tiene deudas.")
                    return

                # Si el monto es mayor que la deuda, solo pagamos lo que se debe
                pago_real = min(monto_a_pagar, deuda_actual)

                # Restar al saldo y a la deuda
                datos_usuario["saldo"] -= pago_real
                datos_usuario["deuda"] -= pago_real

                print(f'Pago exitoso. Nuevo saldo: {datos_usuario["saldo"]}, Nueva deuda: {datos_usuario["deuda"]}')
                
                if monto_a_pagar > deuda_actual:
                    print(f'Se intentó pagar más de la deuda. Solo se descontó {pago_real}. El resto se mantiene en el saldo.')

                # Revisar si la deuda quedó en cero
                if datos_usuario["deuda"] == 0:
                    print('🎉 Felicitaciones, no tienes ninguna deuda por el momento.')
            
            except ValueError:
                print("Error: Ingrese un valor numérico válido.")
            return

    print('No se ha encontrado el usuario.')


def cancelar_cuenta():
    user = input('Ingrese nombre del usuario que quiere cancelar la cuenta: ')
    
    for llave, item in list(base_de_datos.items()):  # Usamos list() para evitar errores al borrar mientras iteramos
        nombre_guardado = list(item.keys())[0] 
        
        if nombre_guardado == user:
            confirmar_cancelacion = input('Estas seguro que deseas cancelar la cuenta "S" para si "N" para no: ').strip().upper()
            if confirmar_cancelacion == 'S':
                base_de_datos.pop(llave)  # Elimina toda la entrada del usuario
                print(f'✅ La cuenta de {user} se ha cancelado con éxito.')
                break
            else:
                print('❌ Cacncelaste la eliminacion...')
                break
    else:
        print('❌ No se ha encontrado el usuario.')

    print(base_de_datos)

def historial_productos():
    try:
        cedula_buscar = int(input("Ingrese la cédula del usuario: "))
        
        for llave, item in base_de_datos.items():
            nombre_usuario = list(item.keys())[0]
            datos_usuario = item[nombre_usuario]
            
            if datos_usuario['cedula'] == cedula_buscar:
                print(f"\n📄 Historial de productos de {nombre_usuario} (Cédula: {cedula_buscar})")
                print("-" * 50)
                
                productos = datos_usuario['productos']
                
                for id_producto, info_producto in productos.items():
                    # info_producto es un diccionario con un solo par clave-valor
                    nombre_prod = list(info_producto.keys())[0]
                    valor_prod = list(info_producto.values())[0]
                    print(f"🆔 ID: {id_producto}")
                    print(f"📌 Producto: {nombre_prod}")
                    print(f"💰 Valor/Monto: {valor_prod}")
                    print("-" * 50)
                return
        
        print("❌ No se encontró un usuario con esa cédula.")
    except ValueError:
        print("❌ Error: La cédula debe ser un número.")



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
        case 4:
            retirar_saldo()
        case 5:
            pagar_deuda()
        case 6:
            cancelar_cuenta()
        case 7:
            print('🚪 Has salido del sistema. Hasta la proxima 👋🏻')
            break