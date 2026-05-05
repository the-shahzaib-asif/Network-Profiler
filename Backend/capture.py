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
    #web hitt
    threading.Thread(target=generate_traffic, args=(url,)).start()

    print(f"[*] Starting packet capture for {duration} seconds on IP {target_ip}...")
    
    # Packets sniff 
    try:
        packets = sniff(timeout=duration)
    except Exception as e:
        print(f"Sniffing error: {e}")
       # (safeguard)
        packets = sniff(timeout=duration)

    #save to pcap file
    wrpcap(filename, packets)
    print(f"[*] Capture complete. Saved {len(packets)} packets to {filename}")
    
    return filename