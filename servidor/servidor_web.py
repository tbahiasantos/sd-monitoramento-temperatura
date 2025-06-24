from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)
CSV_PATH = 'registro_temperaturas.csv'

@app.route('/')
def index():
    if not os.path.exists(CSV_PATH):
        return "Sem dados ainda."
    df = pd.read_csv(CSV_PATH)
    df = df.sort_values(by='timestamp', ascending=False)
    ultimos = df.head(10).to_dict(orient='records')
    alertas = df[df['temperatura'] > 38.0].sort_values(by='timestamp', ascending=False).head(10).to_dict(orient='records')
    return render_template('index.html', ultimos=ultimos, alertas=alertas)

if __name__ == '__main__':
    app.run(debug=True, port=8000)