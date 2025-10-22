import socket
import json
import csv
import os

ARCHIVO_CSV = 'nrcs.csv'

def inicializar_csv():
    if not os.path.exists(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['NRC', 'Materia'])

def buscar_nrc(nrc):
    try:
        with open(ARCHIVO_CSV, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['NRC'] == nrc:
                    return {"status": "ok", "data": row}
            
            return {"status": "not_found", "mensaje": 'NRC no encontrado'}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}

def listar_todas():
    try:
        with open(ARCHIVO_CSV, 'r') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        return {"status": "ok", "data": data}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}

def procesar_comando(comando):
    partes = comando.strip().split('|')
    op = partes[0]

    if op == "BUSCAR_NRC" and len(partes) == 2:
        return buscar_nrc(partes[1])
    elif op == "LISTAR":
        return listar_todas()
    else:
        return {"status": "error", "mensaje": "Comando invalido"}

def manejar_cliente(client_socket, addr):
    print(f"Cliente conectado desde {addr} ")
    try:
        data = client_socket.recv(1024).decode('utf-8')
        if data:
            respuesta = procesar_comando(data)
            client_socket.send(json.dumps(respuesta).encode('utf-8'))
    except Exception as e:
        print(f"Error en hilo: {e}")
    finally:
        client_socket.close()
        print(f"Cliente {addr} desconectado.")

inicializar_csv()
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12346))
server_socket.listen(5) # Cola para mltiples
print("Servidor concurrente escuchando en puerto 12346...")

try:
    while True:
        client_socket, addr = server_socket.accept()
        print(f'Cliente conectado desde {addr}')
        data = client_socket.recv(1024).decode('utf-8')
        if data:
            respuesta = procesar_comando(data)
            client_socket.send(json.dumps(respuesta).encode('utf-8'))
        client_socket.close()
        print('Cliente desconectado.')
except KeyboardInterrupt:
    print('Servidor detenido.')
finally:
    server_socket.close()