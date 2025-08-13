

crear_cuenta = input('Si desea crear la cuenta ingrese "S" para si o "N" para no: ').strip().upper()
datos_usuario = {}
match crear_cuenta:
    case 'S':
        print('Creacion de la cuenta')
        nombre = input('Ingrese el nombre: ')
        cc = int(input('Digite la cedula sin puntos y sin espacios...ejm: 1097066225: '))
        email = input('Ingrese el email: ')
        contacto = int(input('Ingrese su numero telefonico: '))

        contact = {'contacto': contacto}
        emails = {'email': email}
        user = {'nombre': nombre}
        cedula = {'cedula':  cc}
        datos_usuario.update(user)
        datos_usuario.update(cedula)
        datos_usuario.update(emails)
        datos_usuario.update(contact)
        print(datos_usuario)
