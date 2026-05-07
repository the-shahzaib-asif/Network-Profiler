

def get_behavior_label(features):
    traffic_type = "Static / Simple Webpage"
    
    # Rule 1: Streaming (High volume, large packets)
    if features["total_bytes"] > 500000 and features["mean_packet_size"] > 800:
        traffic_type = "Streaming / Heavy Media"
        
    # Rule 2: Social Media (Many unique IPs connected)
    elif features["unique_ips_count"] >= 10:
        traffic_type = "Social Media / Complex Site"
        
    # Rule 3: API-Heavy (Small packets, lots of requests)
    elif features["mean_packet_size"] < 300 and features["total_packets"] > 50:
        traffic_type = "API-Heavy"
        
    return traffic_type