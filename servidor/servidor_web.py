"""
servidor_web.py

Servidor Flask responsável por exibir o painel de temperatura com:
- Status dos sensores (Ativo, Inativo, Crítico)
- Gráfico das últimas leituras por sensor
- Alertas recentes de temperatura crítica
- Monitoramento de falhas via heartbeat (timeout de 10 segundos)

Autor: Thiago Bahia
Projeto: SD_Monitoramento_Temperatura
Data: 2025-07-06
"""

from flask import Flask, render_template, jsonify
import pandas as pd
import os
import json
from datetime import datetime

app = Flask(__name__)

# Configurações gerais
ARQUIVO_CSV = "registros.csv"
ARQUIVO_SENSORES = "sensores_autorizados.txt"
TEMP_CRITICA = 27.0
LIMITE_INATIVO = 10  # segundos

def carregar_sensores() -> list[str]:
    """
    Carrega os sensores autorizados do arquivo de configuração.

    Retorna:
        Lista de IDs de sensores autorizados.
    """
    if not os.path.exists(ARQUIVO_SENSORES):
        return []
    with open(ARQUIVO_SENSORES, "r") as f:
        return [linha.strip() for linha in f if linha.strip()]

def carregar_dados() -> pd.DataFrame:
    """
    Carrega os registros de temperatura do arquivo CSV em um DataFrame.

    Retorna:
        DataFrame com colunas ['sensor_id', 'timestamp', 'temperatura']
    """
    if not os.path.exists(ARQUIVO_CSV):
        return pd.DataFrame(columns=['sensor_id', 'timestamp', 'temperatura'])

    try:
        df = pd.read_csv(ARQUIVO_CSV)
        if 'temperatura' not in df.columns:
            df = pd.read_csv(ARQUIVO_CSV, header=None, names=['sensor_id', 'timestamp', 'temperatura'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df = df.dropna(subset=['sensor_id', 'timestamp', 'temperatura'])
        return df
    except Exception:
        return pd.DataFrame(columns=['sensor_id', 'timestamp', 'temperatura'])

def preparar_dados():
    """
    Processa os dados para exibição no painel (tabela, gráfico e alertas).

    Retorna:
        info_sensores (list): dados para a tabela de status
        alertas (list): lista de alertas recentes
        grafico (dict): dados para plotagem do gráfico
    """
    sensores = carregar_sensores()
    df = carregar_dados()
    agora = datetime.now()

    info_sensores = []
    alertas = []
    grafico = {}

    for sensor in sensores:
        registros = df[df['sensor_id'] == sensor].copy()
        registros.sort_values(by='timestamp', inplace=True)

        if registros.empty:
            # Sensor ainda sem leitura registrada
            info_sensores.append({
                'id': sensor,
                'last_temp': 'N/A',
                'last_time': 'N/A',
                'status': 'Inativo'
            })
            grafico[sensor] = {'temps': [], 'times': []}
            continue

        ultima = registros.iloc[-1]
        try:
            temp = float(ultima['temperatura'])
        except ValueError:
            temp = 0.0

        tempo = ultima['timestamp']
        tempo_desde_ultima = (agora - tempo).total_seconds()

        if tempo_desde_ultima > LIMITE_INATIVO:
            status = "Inativo"
        elif temp > TEMP_CRITICA:
            status = "Crítico"
        else:
            status = "Ativo"

        info_sensores.append({
            'id': sensor,
            'last_temp': f"{temp:.2f}",
            'last_time': tempo.strftime("%Y-%m-%d %H:%M:%S"),
            'status': status
        })

        ultimos = registros.tail(20)
        grafico[sensor] = {
            'temps': [round(float(t), 2) for t in ultimos['temperatura']],
            'times': ultimos['timestamp'].dt.strftime("%H:%M:%S").tolist()
        }

    # Coleta os 5 alertas mais recentes
    alertas_df = df[df['temperatura'] > TEMP_CRITICA].sort_values(by='timestamp', ascending=False).head(5)
    for _, row in alertas_df.iterrows():
        alertas.append({
            'sensor': row['sensor_id'],
            'temp': f"{float(row['temperatura']):.2f}",
            'time': row['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        })

    return info_sensores, alertas, grafico

@app.route("/")
def index():
    """
    Rota principal. Renderiza o painel HTML.
    """
    sensores, alertas, grafico = preparar_dados()
    return render_template("index.html",
                           sensors_info=sensores,
                           alerts_info=alertas,
                           initial_data_json=json.dumps(grafico))

@app.route("/dados")
def dados_api():
    """
    Rota de API usada para atualizar o painel dinamicamente via JavaScript.
    """
    sensores, alertas, grafico = preparar_dados()
    return jsonify({
        'sensors': sensores,
        'alerts': alertas,
        'chart_data': grafico
    })

@app.route("/health")
def health():
    """
    Rota de verificação de saúde do servidor (para automações).
    """
    return "OK", 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
