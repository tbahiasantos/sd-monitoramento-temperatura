# cliente/cliente_sensor.py
import socket
import time
import random
import sys
from datetime import datetime

HOST = 'localhost'
PORTA = 5000
INTERVALO = 2  # segundos

def simular_temperatura(temp_atual):
    # Aumenta ou diminui até ±0.5°C
    return round(temp_atual + random.uniform(-0.5, 0.5), 2)

def ajustar_temperatura(temp_atual):
    # Reduz temperatura de forma forçada
    return round(temp_atual - random.uniform(0.8, 1.5), 2)

def sensor(sensor_id):
    temperatura = random.uniform(35.0, 37.0)  # Temperatura inicial

    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORTA))
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                mensagem = f"{sensor_id}|{timestamp}|{temperatura:.2f}"
                s.sendall(mensagem.encode())
                resposta = s.recv(1024).decode()
                print(f"[{sensor_id}] Enviado: {mensagem}")
                print(f"[{sensor_id}] Resposta: {resposta}")

                if resposta == "AJUSTE":
                    temperatura = ajustar_temperatura(temperatura)
                    print(f"[{sensor_id}] Ajustando temperatura para {temperatura}°C\n")
                elif resposta == "NAO_AUTORIZADO":
                    print(f"[{sensor_id}] Sensor não autorizado no servidor.")
                    break
                else:
                    temperatura = simular_temperatura(temperatura)

                time.sleep(INTERVALO)

        except Exception as e:
            print(f"[{sensor_id}] Falha na conexão: {e}")
            time.sleep(5)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python cliente_sensor.py sensor_ID")
        sys.exit(1)

    sensor_id = sys.argv[1]
    sensor(sensor_id)
