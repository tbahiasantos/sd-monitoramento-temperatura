# cliente/iniciar_sensores.py
import subprocess
import time

sensores = [
    "sensor_001",
    "sensor_002",
    "sensor_003",
    "sensor_004",
    "sensor_005"
]

for sensor in sensores:
    subprocess.Popen(["python", "cliente_sensor.py", sensor], cwd="cliente")
    print(f"Iniciado: {sensor}")
    time.sleep(1)
