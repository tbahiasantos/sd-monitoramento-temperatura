# servidor/servidor_web.py
from flask import Flask, render_template, jsonify
import pandas as pd
import os

ARQUIVO_CSV = 'registros.csv'
app = Flask(__name__)

def carregar_dados():
    if not os.path.exists(ARQUIVO_CSV):
        return pd.DataFrame(columns=["sensor_id", "timestamp", "temperatura"])
    return pd.read_csv(ARQUIVO_CSV)

@app.route('/')
def index():
    df = carregar_dados()

    # Últimas leituras por sensor
    ultimos = df.sort_values("timestamp").groupby("sensor_id").tail(1).sort_values("sensor_id")

    # Leituras críticas
    alertas = df[df["temperatura"] >= 38.0].sort_values("timestamp", ascending=False).head(10)

    # Status dos sensores (simples)
    status_sensores = {}
    for sensor in df["sensor_id"].unique():
        ult_temp = df[df["sensor_id"] == sensor].sort_values("timestamp").iloc[-1]["temperatura"]
        status_sensores[sensor] = "CRITICO" if ult_temp >= 38.0 else "OK"

    # Dados para o gráfico
    dados_sensores = {}
    for sensor in df["sensor_id"].unique():
        df_sensor = df[df["sensor_id"] == sensor].sort_values("timestamp").tail(20)
        dados_sensores[sensor] = {
            "temperaturas": df_sensor["temperatura"].tolist(),
            "timestamps": df_sensor["timestamp"].tolist()
        }

    return render_template("index.html",
                           ultimos=ultimos.to_dict(orient="records"),
                           alertas=alertas.to_dict(orient="records"),
                           status_sensores=status_sensores,
                           dados_sensores=dados_sensores)

@app.route('/dados')
def dados():
    return jsonify(success=True)  # apenas para trigger do reload

if __name__ == '__main__':
    app.run(debug=True, port=8000)
