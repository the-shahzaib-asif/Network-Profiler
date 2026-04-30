from flask import Flask, request, jsonify
from flask_cors import CORS
import urllib.parse
import socket
from capture import capture_traffic
from extract import extract_features

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

@app.route('/api/analyze', methods=['POST'])
def analyze_traffic():
    data = request.get_json(force=True, silent=True)
    url = data.get('url')
    
    target_ip = get_ip_from_url(url)
    if not target_ip:
        return jsonify({"error": "Invalid URL. IP address nahi mila!"}), 400

    # Step 1: Capture traffic
    pcap_filename = capture_traffic(target_ip, url, duration=10, filename="traffic.pcap")

    # Step 2: Extract ALL features
    features = extract_features(pcap_filename)
    if not features:
        return jsonify({"error": "Failed to extract features"}), 500
    traffic_type = "Static / Simple Webpage"
    
    if features["total_bytes"] > 200000 or features["max_packet_size"] > 1400:
         traffic_type = "Streaming / Heavy Media"
    elif features["unique_ips_count"] >= 10:
         traffic_type = "Social Media / Complex Site"

    # Step 3: Frontend ke liye JSON tayyar karna
    protocol_stats = [{"name": k, "count": v} for k, v in features["protocol_counts"].items()]
    
    time_series = [
        {"time": "3s", "bytes": features["total_bytes"] // 3},
        {"time": "6s", "bytes": (features["total_bytes"] // 3) * 2},
        {"time": "10s", "bytes": features["total_bytes"]}
    ]
    histogram_stats = [{"range": k, "count": v} for k, v in features["histogram_counts"].items()]

    return jsonify({
        "status": "success",
        "target_url": url,
        "classification": traffic_type,
        "protocol_stats": protocol_stats,
        "time_series": time_series,
       
        "histogram_stats": histogram_stats, 
        "summary": {
            "total_packets": features["total_packets"],
            "total_bytes": features["total_bytes"],
            "mean_packet_size": features["mean_packet_size"],
            "max_packet_size": features["max_packet_size"],
            "unique_ips": features["unique_ips_count"]
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)



    ##.\venv\Scripts\activate