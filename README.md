# 🌡️ Monitoramento Distribuído de Temperatura com Sensores Simulados

Projeto acadêmico da disciplina **Sistemas Distribuídos** (CEFET-MG, 2025/1), com foco em comunicação cliente-servidor via sockets TCP, visualização em tempo real com Flask e controle de sensores inteligentes.

---

## 🧩 Estrutura do Projeto

```
SD_Monitoramento_Temperatura/
├── cliente/
│   ├── cliente_sensor.py           # Simulador de sensor individual
├── servidor/
│   ├── servidor_main.py            # Servidor TCP para receber leituras
│   ├── servidor_web.py             # Painel web em Flask
│   └── templates/
│       └── index.html              # Interface HTML com gráfico e tabelas
├── iniciar_sensores.py            # Executa múltiplos sensores em paralelo
├── sensores_autorizados.txt       # Lista de sensores permitidos
├── registros.csv                  # Banco de dados CSV gerado em tempo de execução
```

---

## 🚀 Execução

### 1. Inicie o servidor TCP

```bash
python servidor/servidor_main.py
```

### 2. Inicie o painel web (Flask)

```bash
python servidor/servidor_web.py
```

Acesse: [http://localhost:8000](http://localhost:8000)

### 3. Inicie os sensores

```bash
python iniciar_sensores.py
```

---

## 🛠️ Funcionalidades

- 🔁 Comunicação em tempo real com sockets TCP
- 📈 Painel gráfico com atualização automática (sem precisar recarregar a página)
- 🔥 Detecção de superaquecimento com controle automático de temperatura
- ⚠️ Registro de alertas e última leitura por sensor
- 🧪 Execução paralela de múltiplos sensores via subprocesso
- 📝 Armazenamento local em `registros.csv` para auditoria

---

## 📋 Requisitos

- Python 3.8+
- Bibliotecas:
  - `flask`
  - `pandas`
  - `chart.js` (via CDN)

Instale com:

```bash
pip install flask pandas
```

---

## 📚 Créditos

Desenvolvido por **Thiago Lima Bahia Santos**  
Disciplina **Sistemas Distribuídos** – CEFET-MG (1º semestre de 2025)

---
