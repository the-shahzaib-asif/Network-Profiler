from scapy.all import rdpcap, IP, TCP, UDP, DNSQR
import statistics
import os
import math

def extract_features(pcap_file):
    print(f"[*] Extracting features from {pcap_file}...")
    if not os.path.exists(pcap_file) or os.path.getsize(pcap_file) == 0:
        print("[!] Error: PCAP file is missing or empty.")
        return None

    try:
        packets = rdpcap(pcap_file)
    except Exception as e:
        print("Error reading pcap:", e)
        return None
        
    if len(packets) == 0:
        return None

    stats = {"HTTPS": 0, "HTTP": 0, "TCP": 0, "UDP": 0, "DNS": 0}
    total_bytes = 0
    packet_sizes = []
    unique_ips = set()
    dns_queries = set()

    histogram_buckets = {
        "0-100": 0,
        "101-500": 0,
        "501-1000": 0,
        "1001-1500": 0,
        "1501+": 0
    }

    start_time = float(packets[0].time)
    timeline_dict = {i: 0 for i in range(11)}

    for pkt in packets:
        current_second = math.floor(float(pkt.time) - start_time)

        if IP in pkt:
            size = len(pkt)
            total_bytes += size
            packet_sizes.append(size)
            unique_ips.add(pkt[IP].dst)

            if current_second <= 10:
                timeline_dict[current_second] += size

            if size <= 100:
                histogram_buckets["0-100"] += 1
            elif 101 <= size <= 500:
                histogram_buckets["101-500"] += 1
            elif 501 <= size <= 1000:
                histogram_buckets["501-1000"] += 1
            elif 1001 <= size <= 1500:
                histogram_buckets["1001-1500"] += 1
            else:
                histogram_buckets["1501+"] += 1

            if pkt.haslayer("DNSQR"):
                 stats["DNS"] += 1
                 try:
                    query_name = pkt[DNSQR].qname.decode('utf-8')
                    dns_queries.add(query_name)
                 except: pass
            elif TCP in pkt:
                if pkt[TCP].dport == 443 or pkt[TCP].sport == 443:
                    stats["HTTPS"] += 1
                elif pkt[TCP].dport == 80 or pkt[TCP].sport == 80:
                    stats["HTTP"] += 1
                else:
                    stats["TCP"] += 1
            elif UDP in pkt:
                stats["UDP"] += 1

    mean_size = int(statistics.mean(packet_sizes)) if packet_sizes else 0
    max_size = max(packet_sizes) if packet_sizes else 0
    
    clean_stats = {k: v for k, v in stats.items() if v > 0}
    
    time_series_data = [{"time": f"{sec}s", "bytes": timeline_dict[sec]} for sec in range(11)]
    
    return {
        "protocol_counts": clean_stats,
        "total_bytes": total_bytes,
        "total_packets": len(packet_sizes),
        "mean_packet_size": mean_size,
        "max_packet_size": max_size,
        "unique_ips_count": len(unique_ips),
        "dns_queries": list(dns_queries)[:5],
        "histogram_counts": histogram_buckets,
        "time_series": time_series_data 
    }