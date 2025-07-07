"""
iniciar_sensores.py

Script para iniciar múltiplos sensores de temperatura em processos separados.
Cada sensor simula uma baia de servidor e se comunica com o servidor central via TCP.

Autor: Thiago Bahia
Projeto: SD_Monitoramento_Temperatura
Data: 2025-07-06
"""

import subprocess
import os
import time
import sys
import logging

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%H:%M:%S'
)

def iniciar_sensor(sensor_id):
    """
    Inicia um processo subprocesso com o sensor especificado.

    Parâmetros:
        sensor_id (str): identificador do sensor (ex: baia_01)
    
    Retorna:
        subprocess.Popen: objeto do processo iniciado
    """
    caminho = os.path.join("cliente", "cliente_sensor.py")
    if not os.path.exists(caminho):
        logging.error(f"Arquivo {caminho} não encontrado.")
        return None

    return subprocess.Popen(['python', caminho, sensor_id])

if __name__ == "__main__":
    sensores = [
        "baia_01", "baia_02", "baia_03", "baia_04", "baia_05", "baia_superaquecida"
    ]

    # Alternativa para leitura externa:
    # with open("sensores_autorizados.txt") as f:
    #     sensores = [linha.strip() for linha in f if linha.strip()]

    processos = []

    logging.info("Iniciando sensores...")

    for sensor in sensores:
        processo = iniciar_sensor(sensor)
        if processo:
            processos.append(processo)
            logging.info(f"Sensor {sensor} iniciado.")
        else:
            logging.warning(f"Falha ao iniciar sensor {sensor}.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Encerrando sensores...")
        for p in processos:
            p.terminate()
        for p in processos:
            p.wait()
        logging.info("Todos os sensores foram encerrados.")
