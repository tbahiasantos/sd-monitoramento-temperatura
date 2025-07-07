"""
servidor_main.py

Servidor central TCP responsável por receber e processar leituras de sensores
de temperatura instalados em baias de servidores. Valida sensores autorizados,
registra dados em arquivo CSV e responde com comandos de controle térmico.

Autor: Thiago Bahia
Projeto: SD_Monitoramento_Temperatura
Data: 2025-07-06
"""

import socket
import threading
import logging
import os
from datetime import datetime

# Configurações gerais do servidor
HOST = '0.0.0.0'
PORTA = 5000
ARQUIVO_CSV = "registros.csv"
ARQUIVO_SENSORES = "sensores_autorizados.txt"
TEMP_CRITICA = 27.0

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def inicializar_csv():
    """
    Cria o arquivo CSV de registros se ele ainda não existir.
    """
    if not os.path.exists(ARQUIVO_CSV):
        with open(ARQUIVO_CSV, "w") as f:
            f.write("sensor_id,timestamp,temperatura\n")
        logging.info(f"Arquivo {ARQUIVO_CSV} criado.")

def carregar_sensores_autorizados():
    """
    Lê os sensores autorizados a se conectar, a partir do arquivo de texto.

    Retorna:
        set: conjunto de IDs de sensores autorizados
    """
    if not os.path.exists(ARQUIVO_SENSORES):
        logging.warning("Arquivo de sensores autorizados não encontrado.")
        return set()

    with open(ARQUIVO_SENSORES, "r") as f:
        sensores = {linha.strip() for linha in f if linha.strip()}

    logging.info(f"Sensores autorizados carregados: {sorted(sensores)}")
    return sensores

def registrar_leitura(sensor_id, timestamp, temperatura):
    """
    Registra a leitura de temperatura no arquivo CSV.

    Parâmetros:
        sensor_id (str): identificador do sensor
        timestamp (str): data e hora da leitura
        temperatura (float): valor da temperatura
    """
    with open(ARQUIVO_CSV, "a") as f:
        f.write(f"{sensor_id},{timestamp},{temperatura:.2f}\n")

def tratar_conexao(conexao, endereco, sensores_autorizados):
    """
    Lida com uma conexão de sensor individual.

    Parâmetros:
        conexao (socket): conexão TCP ativa com o sensor
        endereco (tuple): endereço IP do sensor
        sensores_autorizados (set): conjunto com IDs permitidos
    """
    try:
        while True:
            dados = conexao.recv(1024).decode()
            if not dados or '|' not in dados:
                conexao.sendall(b"ERRO")
                break

            partes = dados.strip().split("|")
            if len(partes) != 3:
                conexao.sendall(b"ERRO")
                continue

            sensor_id, timestamp, temperatura_str = partes

            if sensor_id not in sensores_autorizados:
                logging.warning(f"Sensor {sensor_id} não autorizado. Conexão encerrada.")
                conexao.sendall(b"NAO_AUTORIZADO")
                break

            try:
                temperatura = float(temperatura_str)
            except ValueError:
                conexao.sendall(b"ERRO")
                logging.warning(f"Temperatura inválida recebida de {sensor_id}: {temperatura_str}")
                continue

            registrar_leitura(sensor_id, timestamp, temperatura)
            logging.info(f"Leitura de {sensor_id}: {temperatura:.2f} °C em {timestamp}")

            if temperatura > TEMP_CRITICA:
                conexao.sendall(b"AJUSTE")
                logging.warning(f"{sensor_id} em temperatura crítica: {temperatura:.2f} °C")
            else:
                conexao.sendall(b"OK")

    except Exception as e:
        logging.error(f"Erro ao tratar conexão de {endereco}: {e}")
    finally:
        conexao.close()
        logging.info(f"Conexão encerrada com {endereco}")

def iniciar_servidor():
    """
    Inicia o servidor TCP, escutando conexões de sensores em threads separadas.
    """
    inicializar_csv()
    sensores_autorizados = carregar_sensores_autorizados()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.bind((HOST, PORTA))
        servidor.listen()
        logging.info(f"Servidor escutando em {HOST}:{PORTA}")

        while True:
            conexao, endereco = servidor.accept()
            threading.Thread(
                target=tratar_conexao,
                args=(conexao, endereco, sensores_autorizados),
                daemon=True,
                name=f"SensorThread-{endereco}"
            ).start()

if __name__ == "__main__":
    iniciar_servidor()
