"""
cliente_sensor.py

Cliente TCP simulando um sensor de temperatura em uma baia de servidor.
Envia periodicamente dados de temperatura ao servidor central e reage a comandos recebidos.

Autor: Thiago Bahia
Projeto: SD_Monitoramento_Temperatura
Data: 2025-07-06
"""

import socket
import time
import random
import sys
from datetime import datetime

# Configurações da conexão
SERVIDOR = 'localhost'
PORTA = 5000
INTERVALO_ENVIO = 2  # segundos
LIMITE_CRITICO = 27.0  # Referência local; controle principal é do servidor

def gerar_temperatura(temp_atual, tendencia):
    """
    Gera uma nova temperatura com base na tendência atual e ruído aleatório.
    Pode alterar a tendência com 10% de chance.

    Parâmetros:
        temp_atual (float): temperatura anterior
        tendencia (int): -1 (esfriando), 0 (estável), 1 (esquentando)

    Retorna:
        nova_temp (float), nova_tendencia (int)
    """
    if random.random() < 0.2:  # 20% de chance de alterar tendência (antes era 10%)
        tendencia = random.choice([-1, 0, 1])

    variacao = random.uniform(0.3, 0.9) * tendencia  # aumento da variação
    ruido = random.uniform(-0.3, 0.5)                # ruído levemente positivo
    nova_temp = temp_atual + variacao + ruido
    nova_temp = max(18.0, min(nova_temp, 40.0))
    return round(nova_temp, 2), tendencia

def executar_sensor(sensor_id):
    """
    Conecta ao servidor e inicia o envio periódico de leituras de temperatura.

    Parâmetros:
        sensor_id (str): identificador único do sensor
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVIDOR, PORTA))
        print(f"[{sensor_id}] Conectado ao servidor {SERVIDOR}:{PORTA}")
    except Exception as e:
        print(f"[{sensor_id}] Erro ao conectar: {e}")
        return

    temp = random.uniform(23.0, 26.0)  # Temperatura inicial
    tendencia = 0

    try:
        while True:
            temp, tendencia = gerar_temperatura(temp, tendencia)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            mensagem = f"{sensor_id}|{timestamp}|{temp}"
            sock.sendall(mensagem.encode())

            try:
                resposta = sock.recv(1024).decode()
            except (ConnectionResetError, BrokenPipeError):
                print(f"[{sensor_id}] Conexão perdida com o servidor.")
                break

            print(f"[{sensor_id}] Enviado: {mensagem}")
            print(f"[{sensor_id}] Resposta: {resposta}")

            if resposta == "OFF":
                print(f"[{sensor_id}] Desligado por superaquecimento.")
                break
            elif resposta == "AJUSTE":
                tendencia = -1  # Faz a temperatura cair
            elif resposta == "OK":
                print(f"[{sensor_id}] Temperatura dentro do limite.")

            time.sleep(INTERVALO_ENVIO)

    except KeyboardInterrupt:
        print(f"\n[{sensor_id}] Interrompido manualmente.")

    finally:
        sock.close()
        print(f"[{sensor_id}] Conexão encerrada.")

if __name__ == "__main__":
    sensor_id = sys.argv[1] if len(sys.argv) > 1 else input("Digite o ID do sensor: ").strip()
    executar_sensor(sensor_id)
