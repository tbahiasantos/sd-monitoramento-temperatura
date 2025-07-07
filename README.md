# 🌡️ Monitoramento Distribuído de Temperatura com Sensores Simulados

Projeto acadêmico da disciplina **Sistemas Distribuídos** (CEFET-MG, 2025/1), com foco em comunicação cliente-servidor via sockets TCP, visualização em tempo real com Flask e controle inteligente de sensores.

---

## 🧩 Estrutura do Projeto

```
SD_Monitoramento_Temperatura/
├── cliente/
│   ├── cliente_sensor.py           # Simulador de sensor individual com controle por tendência
│   ├── iniciar_sensores.py         # Executa múltiplos sensores em paralelo
├── servidor/
│   ├── servidor_main.py            # Servidor TCP: gerencia sensores e comanda ajustes
│   ├── servidor_web.py             # Painel web com Flask + API
│   └── templates/
│       └── index.html              # Interface web com gráfico, alertas e status por sensor
├── sensores_autorizados.txt       # Lista de sensores permitidos
├── registros.csv                  # Banco de dados local com histórico das leituras
├── README.md
```

---

## 🚀 Execução

### 1. Inicie o servidor TCP

```bash
python servidor/servidor_main.py
```

### 2. Inicie o painel web

```bash
python servidor/servidor_web.py
```

Acesse: [http://localhost:8000](http://localhost:8000)

### 3. Inicie os sensores simulados

```bash
python cliente/iniciar_sensores.py
```

---

## 🛠️ Funcionalidades

- 🔁 Comunicação TCP em tempo real com sensores simulados
- 📊 Painel web com **gráfico em tempo real** (sem precisar recarregar)
- 🖥️ **Tabela de status** com cores dinâmicas por faixa de temperatura:
  - Azul (≤ 20 °C), Verde (≤ 23 °C), Amarelo (≤ 25 °C), Laranja (≤ 27 °C), Vermelho (> 27 °C)
- 🧠 Controle inteligente:
  - Servidor envia comando `AJUSTE` para sensores em estado crítico
- ❤️ Animação de heartbeat ativo
- ⚠️ Alertas recentes exibidos na interface
- 💾 Persistência local de leituras em `registros.csv`

---

## 📋 Requisitos

- Python 3.8+
- Bibliotecas:
  - `flask`
  - `pandas`

Instale com:

```bash
pip install flask pandas
```

---

## 📚 Créditos

Desenvolvido por **Thiago Lima Bahia Santos**  
Disciplina **Sistemas Distribuídos** – CEFET-MG (1º semestre de 2025)

---