from flask import Flask, jsonify
import psutil
import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return "<h2>Lexicon Health Monitor Active ✅</h2>"

@app.route("/status")
def status():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
    return jsonify({
        "cpu_usage": cpu,
        "memory_usage": memory,
        "uptime": str(uptime)
    })

if __name__ == "__main__":
    app.run(debug=True, port=5004)
