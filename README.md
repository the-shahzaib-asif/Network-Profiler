# Network Fingerprint Generator and Behavioral Profiler

## 1. Project Overview
This project is a specialized network analysis tool designed to perform non-intrusive behavioral profiling of web traffic. By analyzing packet-level metadata such as size, timing, and protocol distribution, the system generates a unique digital fingerprint for any target URL. The core objective is to classify encrypted traffic patterns (HTTPS) using side-channel telemetry without the need for packet decryption.

## 2. Technical Architecture

### Data Ingestion Module (`capture.py`)
- **Mechanism**: Implements a multi-threaded sniffing engine using the Scapy library.
- **Serialization**: Captures raw network frames and archives them in industry-standard PCAP format.
- **Thread Management**: Utilizes the `threading` module to synchronize the HTTP request generation with the packet capturing process, ensuring the capture of the initial TCP handshake.

### Statistical Extraction Module (`extract.py`)
- **Metric Calculation**: Extracts quantitative data including total byte count, mean packet size (MPS), and unique destination IP counts.
- **Protocol Analysis**: Inspects Layer 3 (IP) and Layer 4 (TCP/UDP) headers to determine the protocol distribution.
- **Bucketization**: Categorizes packet sizes into specific byte ranges to analyze payload density.

### Classification Engine (`classify.py`)
- **Heuristic Framework**: Implements a rule-based decision engine to categorize traffic behavior based on the following thresholds:
    - **Streaming**: High volume (>500KB) and large average packet size (>800 bytes).
    - **Social/Complex**: High entropy in destination IPs (>10 unique connections).
    - **API-Heavy**: High frequency of small control packets (<300 bytes average).

### Presentation Layer (React + Vite)
- **State Management**: Uses React hooks for asynchronous data fetching and UI state updates.
- **Visualization**: Implements Recharts for dynamic rendering of throughput timelines and protocol distribution charts.

## 3. Directory Structure
```text
Network_Profiler/
├── Backend/
│   ├── app.py              # Flask REST API & Orchestration
│   ├── capture.py          # Scapy Sniffing Logic
│   ├── extract.py          # Feature Extraction
│   ├── classify.py         # Behavioral Logic
│   ├── fingerprint.py      # JSON Schema Generation
│   └── requirements.txt    # Python Dependencies
├── Frontend/
│   ├── src/                # React Components & Logic
│   ├── package.json        # Node.js Dependencies
│   └── vite.config.js      # Build Configuration
└── README.md
