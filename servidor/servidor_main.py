import socket
import threading
import logging
from datetime import datetime
import os

HOST = 'localhost'
PORT = 5000
LIMITE_TEMPERATURA = 38.0
ARQUIVO_REGISTRO = 'registro_temperaturas.csv'
SENSORES_AUTORIZADOS = 'sensores_autorizados.txt'

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

if not os.path.exists(ARQUIVO_REGISTRO):
    with open(ARQUIVO_REGISTRO, 'w') as f:
        f.write('sensor_id,timestamp,temperatura\n')

with open(SENSORES_AUTORIZADOS, 'r') as f:
    sensores_validos = {linha.strip() for linha in f if linha.strip()}

def salvar_csv(sensor_id, timestamp, temperatura):
    with open(ARQUIVO_REGISTRO, 'a') as f:
        f.write(f"{sensor_id},{timestamp},{temperatura:.1f}\n")

def lidar_com_cliente(conexao, endereco):
    logging.info(f"Nova conexão de {endereco}")
    while True:
        try:
            dados = conexao.recv(1024).decode()
            if not dados:
                break
            sensor_id, timestamp, temperatura = dados.strip().split('|')
            if sensor_id not in sensores_validos:
                logging.warning(f"Sensor não autorizado: {sensor_id}")
                continue
            temperatura = float(temperatura)
            salvar_csv(sensor_id, timestamp, temperatura)
            logging.info(f"{sensor_id} {timestamp}: {temperatura:.1f}°C")
            if temperatura > LIMITE_TEMPERATURA:
                logging.warning(f"ALERTA: {sensor_id} registrou {temperatura:.1f}°C em {timestamp}")
        except Exception as e:
            logging.error(f"Erro ao processar dados de {endereco}: {e}")
            break
    conexao.close()
    logging.info(f"Conexão encerrada com {endereco}")

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen()
    logging.info(f"Servidor ouvindo em {HOST}:{PORT}")
    while True:
        conexao, endereco = servidor.accept()
        threading.Thread(target=lidar_com_cliente, args=(conexao, endereco), daemon=True).start()

if __name__ == '__main__':
    iniciar_servidor()