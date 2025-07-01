# servidor/servidor_main.py
import socket
import threading
import logging
from datetime import datetime
import os
import csv

PORTA = 5000
HOST = '0.0.0.0'
LIMITE_TEMPERATURA = 38.0
ARQUIVO_CSV = 'registros.csv'
ARQUIVO_SENSORES = 'sensores_autorizados.txt'
sensores_autorizados = set()
leitura_lock = threading.Lock()

# Configurações de log
logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO
)

# Inicializa arquivo de sensores autorizados
def carregar_sensores():
    if not os.path.exists(ARQUIVO_SENSORES):
        logging.warning("Arquivo de sensores autorizados não encontrado.")
        return
    with open(ARQUIVO_SENSORES, 'r') as f:
        for linha in f:
            sensores_autorizados.add(linha.strip())

# Inicializa arquivo CSV
def inicializar_csv():
    if not os.path.exists(ARQUIVO_CSV):
        with open(ARQUIVO_CSV, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["sensor_id", "timestamp", "temperatura"])

# Função para processar conexão de sensor
def lidar_com_sensor(conn, addr):
    logging.info(f"Nova conexao de {addr}")
    with conn:
        while True:
            dados = conn.recv(1024)
            if not dados:
                break
            mensagem = dados.decode().strip()
            try:
                sensor_id, timestamp, temperatura = mensagem.split("|")
                temperatura = float(temperatura)
            except Exception:
                logging.error("Mensagem com formato invalido.")
                continue

            if sensor_id not in sensores_autorizados:
                conn.sendall(b"NAO_AUTORIZADO")
                continue

            # Salvar dados
            with leitura_lock:
                with open(ARQUIVO_CSV, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([sensor_id, timestamp, temperatura])

            # Resposta ao sensor
            if temperatura >= LIMITE_TEMPERATURA:
                conn.sendall(b"AJUSTE")
            else:
                conn.sendall(b"OK")

def iniciar_servidor():
    carregar_sensores()
    inicializar_csv()
    logging.info(f"Servidor escutando em {HOST}:{PORTA}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORTA))
        s.listen()
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=lidar_com_sensor, args=(conn, addr))
            thread.start()

if __name__ == '__main__':
    iniciar_servidor()
