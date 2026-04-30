from scapy.all import rdpcap, IP, TCP, UDP, DNSQR
import statistics
import os

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
        
    stats = {"TCP": 0, "UDP": 0, "DNS": 0, "ICMP": 0, "Other": 0}
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

    for pkt in packets:
        if IP in pkt:
            size = len(pkt)
            total_bytes += size
            packet_sizes.append(size)
            unique_ips.add(pkt[IP].dst)

           
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

            # Protocol counting (Baqi code purana hi hai)
            if pkt.haslayer("DNSQR"):
                 stats["DNS"] += 1
                 try:
                    query_name = pkt[DNSQR].qname.decode('utf-8')
                    dns_queries.add(query_name)
                 except: pass
            elif TCP in pkt:
                stats["TCP"] += 1
            elif UDP in pkt:
                stats["UDP"] += 1
            elif pkt.haslayer("ICMP"):
                stats["ICMP"] += 1
            else:
                stats["Other"] += 1

    # Math calculations
    mean_size = int(statistics.mean(packet_sizes)) if packet_sizes else 0
    max_size = max(packet_sizes) if packet_sizes else 0
    
    return {
        "protocol_counts": stats,
        "total_bytes": total_bytes,
        "total_packets": len(packet_sizes),
        "mean_packet_size": mean_size,
        "max_packet_size": max_size,
        "unique_ips_count": len(unique_ips),
        "dns_queries": list(dns_queries)[:5],
        # 👉 NAYA: Histogram data return karo
        "histogram_counts": histogram_buckets 
    }