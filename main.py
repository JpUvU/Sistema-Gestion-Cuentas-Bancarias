from datetime import datetime
import os
import uuid 
from database import guardar_datos, cargar_datos

ARCHIVO_DATOS = "base_de_datos.json"
base_de_datos = cargar_datos()

def menu_principal():
    print('--------------------------------------')
    print('''      GESTION DE CUENTAS BANCARIAS       
            1: Crear cuenta 
            2: Depositar Dinero
            3: Solicitar Credito
            4: Retirar Dinero
            5: Pago Cuota Credito
            6: Cancelar Cuenta
            7: Historial de productos
            8: Historial de movimientos
            9: Salir del sistema''')
    print('--------------------------------------')

def generar_id():
    return str(uuid.uuid4())[:8]  # ID único corto
    
def crear_cuenta():
    crear_cuenta = input('Si desea crear la cuenta ingrese "S" para si o "N" para no: ').strip().upper()

    if crear_cuenta == 'S':
        print('Creando la cuenta')
        try:
            nombre = input('Ingrese el nombre: ').strip()
            cc = int(input('Digite la cédula sin puntos y sin espacios... ejm: 1097066225: '))
            email = input('Ingrese el email: ').strip()
            contacto = int(input('Ingrese su número telefónico: '))
            ubicacion = input('Ingrese la ciudad de residencia: ').strip()
            saldo = int(input('Ingrese el saldo inicial: '))
            tipoCuenta = input('Ingrese si la cuenta será ahorros o corriente: ').strip().lower()
            saldo_cdt = 0
            SaldoCreditoLibreInv = 0
            SaldoCreditoVivienda = 0
            saldoCreditoAutomovil = 0
            deudaCredito = 0

            # 🔎 Validaciones de unicidad
            for _, item in base_de_datos.items():
                nombre_existente = list(item.keys())[0]
                datos_existentes = item[nombre_existente]

                if datos_existentes['cedula'] == cc:
                    print("❌ Error: Ya existe un usuario con esa cédula.")
                    return
                if nombre_existente.lower() == nombre.lower():
                    print("❌ Error: El nombre de usuario ya está registrado.")
                    return
                if datos_existentes['contacto'] == contacto:
                    print("❌ Error: El número de teléfono ya está registrado.")
                    return
                if datos_existentes['email'].lower() == email.lower():
                    print("❌ Error: El correo electrónico ya está registrado.")
                    return

            # ✅ Si pasa las validaciones, se crea la cuenta
            if tipoCuenta in ('ahorros', 'corriente'):
                datos_usuario = {
                    nombre: {
                        'cedula': cc,
                        'email': email,
                        'contacto': contacto,
                        'ciudad': ubicacion,
                        'saldo': saldo,
                        'deuda': deudaCredito,
                        'productos': {
                            generar_id(): {'Tipo': tipoCuenta},
                            generar_id(): {'CDT': saldo_cdt},
                            generar_id(): {'credito libre inversion': SaldoCreditoLibreInv},
                            generar_id(): {'credito vivienda': SaldoCreditoVivienda},
                            generar_id(): {'credito automovil': saldoCreditoAutomovil}
                        },
                        'movimientos': {}
                    }
                }

                llave = len(base_de_datos) + 1
                base_de_datos.update({llave: datos_usuario})
                print(f"✅ Cuenta creada exitosamente para {nombre}")
            else:
                print('❌ Error: Tipo de cuenta inválido. Debe ser "ahorros" o "corriente".')

        except ValueError:
            print('❌ Error inesperado, ingresa los datos correctamente...')

    else:
        print('Saliendo...')


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
                registrar_movimiento(datos_usuario, "Depósito", monto_a_depositar)
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
            4: Credito para comprar automovil''')
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
        
def saldo_cdt():
    try:
        cedula = int(input('Ingrese la cédula del usuario al que se le abrirá el CDT: '))
        
        for llave, item in base_de_datos.items():
            nombre_usuario = list(item.keys())[0]
            datos_usuario = item[nombre_usuario]
            
            if datos_usuario['cedula'] == cedula:
                print(f'Usuario encontrado: {nombre_usuario}')
                print(f'Saldo actual: {datos_usuario["saldo"]}')

                monto = int(input('Ingrese el monto que desea invertir en el CDT: '))
                
                if monto > datos_usuario['saldo'] or datos_usuario['saldo'] <= 0:
                    print('Fondos insuficientes para abrir el CDT.')
                    return
                
                # Buscar el producto "CDT" por su ID
                for id_prod, prod_info in datos_usuario['productos'].items():
                    if "CDT" in prod_info:
                        prod_info["CDT"] += monto
                        break

                datos_usuario['saldo'] -= monto

                print(f'CDT creado exitosamente por ${monto}')
                print(f'Nuevo saldo: {datos_usuario["saldo"]}')
                # Mostrar CDT actualizado
                for id_prod, prod_info in datos_usuario['productos'].items():
                    if "CDT" in prod_info:
                        print(f'CDT actual: {prod_info["CDT"]}')
                        break
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
                    print(f'No puedes abrir otro crédito sr/sra {nombre_usuario}. Tienes deuda activa.')
                    return

                montoAprestar = int(input('Ingresa el monto que vas a solicitar: '))

                # Buscar el producto "credito libre inversion" por su ID
                for id_prod, prod_info in datos_usuario['productos'].items():
                    if "credito libre inversion" in prod_info:
                        prod_info["credito libre inversion"] += montoAprestar
                        break

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

                # Buscar el producto "credito vivienda" por su ID
                for id_prod, prod_info in datos_usuario['productos'].items():
                    if "credito vivienda" in prod_info:
                        prod_info["credito vivienda"] += montoAprestar
                        break

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
        cedula = int(input('Ingrese la cédula del usuario al que se le abrirá crédito de automóvil: '))

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

                # Buscar el producto "credito automovil" por su ID
                for id_prod, prod_info in datos_usuario['productos'].items():
                    if "credito automovil" in prod_info:
                        prod_info["credito automovil"] += montoAprestar
                        break

                datos_usuario['saldo'] += montoAprestar
                datos_usuario['deuda'] += montoAprestar

                print(f'Su crédito de automóvil fue aprobado por ${montoAprestar}')
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
                    registrar_movimiento(datos_usuario, "Retiro", -monto_a_retirar)
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
                registrar_movimiento(datos_usuario, "pago deuda", pago_real)

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
        cedula_buscar = int(input("Ingrese la cédula del usuario para consultar: "))
        
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

def registrar_movimiento(datos_usuario, tipo, valor):
    id_mov = generar_id()
    datos_usuario["movimientos"][id_mov] = {
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "hora": datetime.now().strftime("%H:%M:%S"),
        "tipo": tipo,
        "valor": valor,
        "saldo_resultante": datos_usuario["saldo"]
    }

def historial_movimientos():
    try:
        cedula_buscar = int(input("Ingrese la cédula del usuario para ver el historial de movimientos: "))
        
        for llave, item in base_de_datos.items():
            nombre_usuario = list(item.keys())[0]
            datos_usuario = item[nombre_usuario]
            
            if datos_usuario['cedula'] == cedula_buscar:
                print(f"\n📜 Historial de movimientos de {nombre_usuario}")
                print("-" * 60)
                
                if not datos_usuario["movimientos"]:
                    print("📌 No hay movimientos registrados.")
                    return
                
                for id_mov, info in datos_usuario["movimientos"].items():
                    print(f"🆔 ID: {id_mov}")
                    print(f"📅 Fecha: {info['fecha']} ⏰ Hora: {info['hora']}")
                    print(f"📌 Tipo: {info['tipo']}")
                    print(f"💰 Valor: {info['valor']}")
                    print(f"💳 Saldo después: {info['saldo_resultante']}")
                    print("-" * 60)
                return
        
        print("❌ No se encontró un usuario con esa cédula.")
    except ValueError:
        print("❌ Error: La cédula debe ser un número.")



# --- Punto de entrada del programa ---
if __name__ == "__main__":
    while True:
        menu_principal()
        try:
            opcion = int(input('Ingrese la opcion a ejecutar: '))
        except ValueError:
            print("❌ Opción inválida, ingrese un número.")
            continue

        os.system('cls')
        match opcion:
            case 1:
                crear_cuenta()
                guardar_datos(base_de_datos)
            case 2:
                depositar_saldo()
                guardar_datos(base_de_datos)
            case 3:
                portafolio()
                guardar_datos(base_de_datos)
            case 4:
                retirar_saldo()
                guardar_datos(base_de_datos)
            case 5:
                pagar_deuda()
                guardar_datos(base_de_datos)
            case 6:
                cancelar_cuenta()
                guardar_datos(base_de_datos)
            case 7:
                historial_productos()
            case 8:
                historial_movimientos()
            case 9:
                print('🚪 Has salido del sistema. Hasta la próxima 👋🏻')
                break