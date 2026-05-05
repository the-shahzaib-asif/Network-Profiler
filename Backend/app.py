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

## BASE Funontion
def get_website_stats(url, filename):
    target_ip = get_ip_from_url(url)
    if not target_ip:
        raise Exception(f"Invalid URL. IP address not found for {url}!")

    capture_traffic(target_ip, url, duration=10, filename=filename)
    features = extract_features(filename)
    
    traffic_type = "Static / Simple Webpage"
    if features["total_bytes"] > 200000 or features["max_packet_size"] > 1400:
         traffic_type = "Streaming / Heavy Media"
    elif features["unique_ips_count"] >= 10:
         traffic_type = "Social Media / Complex Site"

    return {
        "target_url": url,
        "classification": traffic_type,
        "protocol_stats": [{"name": k, "count": v} for k, v in features["protocol_counts"].items()],
        "time_series": [
            {"time": "3s", "bytes": features["total_bytes"] // 3},
            {"time": "6s", "bytes": (features["total_bytes"] // 3) * 2},
            {"time": "10s", "bytes": features["total_bytes"]}
        ],
        "histogram_stats": [{"range": k, "count": v} for k, v in features["histogram_counts"].items()],
        "summary": {
            "total_packets": features["total_packets"],
            "total_bytes": features["total_bytes"],
            "mean_packet_size": features["mean_packet_size"],
            "max_packet_size": features["max_packet_size"],
            "unique_ips": features["unique_ips_count"]
        }
    }


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


## Compare ENd Point-
@app.route('/api/compare', methods=['POST'])
def compare_traffic():
    data = request.get_json(force=True, silent=True)
    url1 = data.get('url1')
    url2 = data.get('url2')

    if not url1 or not url2:
        return jsonify({"error": "Enter Both Link!!!"}), 400

    print(f"Starting comparison: {url1} vs {url2}")

    
    result1 = get_website_stats(url1, "traffic1.pcap")
    result2 = get_website_stats(url2, "traffic2.pcap")

    return jsonify({
        "status": "success",
        "website1": {"url": url1, "data": result1},
        "website2": {"url": url2, "data": result2}
    }), 200
if __name__ == '__main__':
    app.run(debug=True, port=5000)



    ##.\venv\Scripts\activate