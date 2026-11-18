import os
import random
import time

import requests

API_URL = os.environ.get("API_URL", "http://api:5000/datos")
INTERVAL = float(os.environ.get("INTERVAL", "5"))
SENSOR_ID = os.environ.get("SENSOR_ID", "sensor_01")


def generar_lectura():
    temperatura = round(random.uniform(20, 40), 1)
    humedad = round(random.uniform(40, 90), 1)
    return {"sensor_id": SENSOR_ID, "temperatura": temperatura, "humedad": humedad}


if __name__ == "__main__":
    while True:
        lectura = generar_lectura()
        try:
            r = requests.post(API_URL, json=lectura, timeout=5)
            print(f"Enviado: {lectura} -> {r.status_code}", flush=True)
        except requests.exceptions.RequestException as e:
            print(f"API no disponible todavia: {e}", flush=True)
        time.sleep(INTERVAL)