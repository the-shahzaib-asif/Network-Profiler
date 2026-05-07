# fingerprint.py
# Requirement FR-4: Fingerprint Generation

def generate_fingerprint(url, features, behavior_label):
    return {
        "target_url": url,
        "classification": behavior_label,
        "protocol_stats": [{"name": k, "count": v} for k, v in features["protocol_counts"].items()],
        "time_series": features.get("time_series", []),
        "histogram_stats": [{"range": k, "count": v} for k, v in features["histogram_counts"].items()],
        "summary": {
            "total_packets": features["total_packets"],
            "total_bytes": features["total_bytes"],
            "mean_packet_size": features["mean_packet_size"],
            "max_packet_size": features["max_packet_size"],
            "unique_ips": features["unique_ips_count"]
        }
    }