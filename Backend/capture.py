import threading
import requests
import time
from scapy.all import sniff, wrpcap

def generate_traffic(url):
    time.sleep(1) # Thora delay taake sniff pehle shuru ho jaye
    try:
        requests.get(url, timeout=5)
    except:
        pass

def capture_traffic(target_ip, url, duration=10, filename="traffic.pcap"):
    # Background mein website ko hit karna
    threading.Thread(target=generate_traffic, args=(url,)).start()

    print(f"[*] Starting packet capture for {duration} seconds on IP {target_ip}...")
    
    # Packets sniff karna
    try:
        packets = sniff(timeout=duration)
    except Exception as e:
        print(f"Sniffing error: {e}")
        # Agar filter ka masla ho toh baghair filter ke open sniff karo (safeguard)
        packets = sniff(timeout=duration)

    # FR-2 Requirement: Packets ko .pcap file mein save karna
    wrpcap(filename, packets)
    print(f"[*] Capture complete. Saved {len(packets)} packets to {filename}")
    
    return filename