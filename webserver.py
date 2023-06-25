from flask import Flask, jsonify
from threading import Thread
import json
app = Flask('')
JSONFILE = "test.json" #Replace with file name same in Main.py
def get_ips_content():
    with open(JSONFILE) as file:
        content = json.load(file)
    return content

@app.route('/')
def home():
    ips_content = get_ips_content()
    return jsonify(ips_content)

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
