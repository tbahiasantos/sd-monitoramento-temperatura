# Monitoramento Distribuído de Temperatura 🌡️

Este projeto foi desenvolvido como parte da disciplina de **Sistemas Distribuídos** do curso de Engenharia de Computação (CEFET-MG). A aplicação simula um sistema de monitoramento de sensores de temperatura distribuídos em diferentes clientes, comunicando-se com um servidor central via sockets.

## 📦 Estrutura do Projeto

```

SD\_Monitoramento\_Temperatura/
├── cliente/
│   └── cliente\_sensor.py           # Script do cliente simulando sensores
├── servidor/
│   ├── servidor\_main.py            # Servidor TCP para receber dados
│   ├── servidor\_web.py             # Interface web com Flask
│   ├── sensores\_autorizados.txt    # Lista de sensores autorizados
│   └── templates/
│       └── index.html              # Página HTML da interface web
├── dados.csv                       # Arquivo de persistência das leituras
└── README.md

````

## ⚙️ Funcionalidades

- Envio periódico de dados de temperatura de clientes para o servidor
- Autenticação de sensores via lista autorizada
- Armazenamento das leituras em arquivo `.csv`
- Interface web com Flask para monitoramento em tempo real
- Registro de logs das interações e falhas

## 🚀 Como Executar

### Pré-requisitos

- Python 3.9 ou superior
- Bibliotecas: `Flask`

Instale as dependências:

```bash
pip install flask
````

### 1. Inicie o servidor TCP

```bash
python servidor/servidor_main.py
```

### 2. Inicie o servidor web (em outro terminal)

```bash
python servidor/servidor_web.py
```

Acesse no navegador: [http://localhost:5000](http://localhost:5000)

### 3. Execute o cliente simulador

```bash
python cliente/cliente_sensor.py
```

> Você pode executar múltiplos clientes em paralelo com diferentes IDs.

## 🛡️ Segurança e Tolerância a Falhas

* Apenas sensores com IDs autorizados no arquivo `sensores_autorizados.txt` conseguem enviar dados.
* O servidor lida com falhas de conexão e mensagens inválidas sem interrupções.
* Logs são registrados para depuração e rastreabilidade.

## 📁 Persistência

As leituras de temperatura são registradas no arquivo `dados.csv` com:

* Timestamp
* ID do sensor
* Valor da temperatura

## 👨‍💻 Autor

Thiago Bahia
Projeto acadêmico — CEFET-MG — 2025/1
