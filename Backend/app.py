from flask import Flask, request, jsonify
from flask_cors import CORS
import urllib.parse
import socket
from capture import capture_traffic
from extract import extract_features
from classify import get_behavior_label      # Nayi file import ki
from fingerprint import generate_fingerprint # Nayi file import ki

app = Flask(__name__)
CORS(app)

def get_ip_from_url(url):
    try:
        domain = urllib.parse.urlparse(url).netloc
        domain = domain.split(':')[0]
        if not domain:
            domain = url
        return socket.gethostbyname(domain)
    except Exception as e:
        return None

def get_website_stats(url, filename):
    target_ip = get_ip_from_url(url)
    if not target_ip:
        raise Exception(f"Invalid URL. IP address not found for {url}!")

    # 1. Packet Capture (FR-2)
    capture_traffic(target_ip, url, duration=10, filename=filename)
    
    # 2. Extract Features (FR-3)
    features = extract_features(filename)
    if not features:
        raise Exception("Failed to extract features or no packets captured.")
    
    # 3. Classify Behavior (FR-5)
    behavior_label = get_behavior_label(features)
    
    # 4. Generate Fingerprint (FR-4)
    fingerprint_json = generate_fingerprint(url, features, behavior_label)
    
    return fingerprint_json

@app.route('/api/analyze', methods=['POST'])
def analyze_traffic():
    data = request.get_json(force=True, silent=True)
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URl Required!!"}), 400

    try:
        result = get_website_stats(url, "traffic.pcap")
        result["status"] = "success"
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/compare', methods=['POST'])
def compare_traffic():
    data = request.get_json(force=True, silent=True)
    url1 = data.get('url1')
    url2 = data.get('url2')

    if not url1 or not url2:
        return jsonify({"error": "Enter Both Link!!!"}), 400

    try:
        result1 = get_website_stats(url1, "traffic1.pcap")
        result2 = get_website_stats(url2, "traffic2.pcap")

        return jsonify({
            "status": "success",
            "website1": {"url": url1, "data": result1},
            "website2": {"url": url2, "data": result2}
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)



    ##.\venv\Scripts\activate