from flask import Flask, request, jsonify
from flask_cors import CORS
from scapy.all import sniff, IP, TCP, UDP
import urllib.parse
import socket
import threading
import requests
import time

app = Flask(__name__)
CORS(app) 

@app.route('/api/analyze', methods=['POST'])
def analyze_traffic():
    print("---------------------------------")
    data = request.get_json(force=True, silent=True)
    
    if not data or 'url' not in data:
        return jsonify({"error": "Data mein URL nahi mila!"}), 400

    url = data.get('url')
    print(f"Success! URL recieved : {url}")
    
    
    dummy_network_data = {
        "status": "success",
        "target_url": url,
        "protocol_stats": [
            {"name": "TCP", "count": 450},
            {"name": "UDP", "count": 120},
            {"name": "HTTP", "count": 300},
            {"name": "HTTPS", "count": 850}
        ],
        "time_series": [
            {"time": "1s", "bytes": 1024},
            {"time": "2s", "bytes": 2048},
            {"time": "3s", "bytes": 1500},
            {"time": "4s", "bytes": 3000},
            {"time": "5s", "bytes": 2500}
        ]
    }

    print("Sending Dummy Network Data to frontend...")
    print("---------------------------------")
    
    return jsonify(dummy_network_data), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)

## .\venv\Scripts\activate

