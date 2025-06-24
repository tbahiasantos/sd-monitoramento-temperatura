import socket
import time
import random
from datetime import datetime
import sys

HOST = 'localhost'
PORT = 5000
SENSOR_ID = sys.argv[1] if len(sys.argv) > 1 else 'sensor_001'

def gerar_temperatura():
    return round(random.uniform(35.0, 40.0), 1)

def conectar():
    while True:
        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente.connect((HOST, PORT))
            print(f"[SENSOR] {SENSOR_ID} conectado.")
            return cliente
        except:
            print("[ERRO] Tentando reconectar...")
            time.sleep(2)

cliente = conectar()

try:
    while True:
        temperatura = gerar_temperatura()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        mensagem = f"{SENSOR_ID}|{timestamp}|{temperatura}"
        try:
            cliente.send(mensagem.encode())
        except:
            print("[ERRO] Reconectando...")
            cliente = conectar()
        time.sleep(2)
except KeyboardInterrupt:
    print("[SENSOR] Encerrando conexão.")
    cliente.close()