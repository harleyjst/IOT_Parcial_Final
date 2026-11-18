import csv
import os
from datetime import datetime

from flask import Flask, jsonify, request

app = Flask(__name__)

CSV_FILE = os.environ.get("CSV_FILE", "datos_iot.csv")
HEADER = ["fecha", "sensor_id", "temperatura", "humedad"]


def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            csv.writer(f).writerow(HEADER)


@app.route("/")
def home():
    return "Servidor IoT funcionando correctamente"


@app.route("/datos", methods=["POST"])
def recibir_datos():
    data = request.get_json(silent=True)
    if not data or not all(k in data for k in ("sensor_id", "temperatura", "humedad")):
        return jsonify({"error": "JSON invalido"}), 400

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CSV_FILE, "a", newline="") as f:
        csv.writer(f).writerow(
            [fecha, data["sensor_id"], data["temperatura"], data["humedad"]]
        )
    return jsonify({"status": "ok"}), 201


if __name__ == "__main__":
    init_csv()
    app.run(host="0.0.0.0", port=5000)