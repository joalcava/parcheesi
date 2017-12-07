import select
import socket
import pickle

from parques import Parques

conexiones = []
usuarios = []
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
turno = 1
parques = None
jugando = False
juego_finalizado = False
colores_disponibles = {
    1: "ROJO",
    2: "AMARILLO",
    3: "AZUL",
    4: "VERDE"
}

def enviar_mensaje_a_todos(message):
    print('\nse inicia el envio de datos.')
    for _socket in conexiones:
        if _socket != server_socket:
            try:
                _socket.send(message)
                print("datos enviados a: ", _socket)
            except:
                _socket.close()
                conexiones.remove(_socket)
                print("error enviando datos a: ", _socket)
    print('envio de datos terminado.\n')


def nuevo_jugador(cliente):
    mensaje = "Bienvenido\n" \
              "A continuacion ingrese: nombre de usuario y color " \
              "en ese orden y separado por comas.\n" \
              "ingrese el numero del color en base a la siguiente lista:\n" \
              "Colores disponibles:\n" + str(colores_disponibles)

    cliente.send(bytes(mensaje, 'utf-8'))
    datos = cliente.recv(1024).decode('utf-8').split(",")

    if len(datos) != 2:
        cliente.send(b"datos con formato incorrecto. intente de nuevo")
        return False

    if int(datos[1]) not in colores_disponibles.keys():
        cliente.send(b"color incorrecto. intente de nuevo")
        return False
    cliente.send(b"ok, todo bien, todo bonito.")
    pos = len(usuarios) + 1
    nombre = datos[0]
    color = int(datos[1])
    jugador = (nombre, color, pos)
    usuarios.append(jugador)
    del(colores_disponibles[color])
    return True


def iniciar_juego():
    print('iniciando juego...')
    parques = Parques(usuarios)
    print('...juego iniciado')
    for cliente in conexiones:
        if cliente != server_socket:
            cliente.send(b'Su turno')
            cliente.recv(1024).decode('utf-8').split(",")

def preguntar_iniciar():
    aceptados = 0
    for cliente in conexiones:
        if cliente != server_socket:
            cliente.send(b"desea iniciar el juego? [si/no].")
            respuesta = cliente.recv(1024).decode('utf-8')
            if respuesta == "si":
                aceptados += 1
    if aceptados == len(usuarios):
        enviar_mensaje_a_todos(b"ok")
        return True
    return False


def procesar_datos(datos):
    pass


if __name__ == '__main__':

    server_socket.bind(("localhost", 5000))
    server_socket.listen(20)
    conexiones.append(server_socket)

    while not juego_finalizado:
        read_sockets, write_sockets, error_sockets = select.select(conexiones, [], [])

        for _socket in read_sockets:

            # Nueva conexion
            if _socket == server_socket:

                nuevo_socket, addr = server_socket.accept()
                print('atendiendo conexion entrante.')
                if len(conexiones) > 5:
                    nuevo_socket.send(b"El juego esta lleno, intenta mas tarde.")
                    break
                if jugando:
                    nuevo_socket.send(b"\nya se esta jugando una partida. intente mas tarde\n")
                    break

                resultado = nuevo_jugador(nuevo_socket)
                if resultado:
                    enviar_mensaje_a_todos(b"se unio un nuevo jugador")
                    conexiones.append(nuevo_socket)
                    if len(usuarios) >= 2:
                        resultado = preguntar_iniciar()
                        if resultado:
                            iniciar_juego()
                        else:
                            enviar_mensaje_a_todos(b"juego no iniciado, un integrante quiere esperar.")
            # Datos recibidos de un cliente
            else:
                try:
                    data = _socket.recv(4096)
                    procesar_datos(data)
                    if juego_finalizado:
                        break
                except:
                    print("Un cliente desconectado")
                    conexiones.remove(_socket)
                    _socket.close()
                    continue
    server_socket.close()