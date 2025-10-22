import socket
import json

def mostrar_menu():
    print(\n--- Men de Calificaciones ---)
print(1. Agregar calificacin)
    print(2. Buscar por ID)
    print(3. Actualizar calificacin)
    print(4. Listar todas)
print(5. Eliminar por ID)
    print(6. Salir)
    return input(Elija opcin: )

def enviar_comando(comando):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    client_socket.send(comando.encode('utf-8'))
    respuesta = client_socket.recv(1024).decode('utf-8')
    client_socket.close()
    return json.loads(respuesta)