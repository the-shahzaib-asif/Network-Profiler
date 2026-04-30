import React from 'react';


const SummaryCard = ({ summary,classification }) => {
      const trafficType = classification ? classification : "Unknown Traffic";

  return (
  <div id="analysis">
     <div id="classficationType"> <h2>Type: {trafficType}</h2></div>
         <div id="chartSummary">
          <h3>Network Fingerprint Summary</h3>
           <ul style={{ listStyleType: 'none', padding: 0, lineHeight: '1.8' }}>
            <li><strong>Total Packets:</strong> {summary.total_packets}</li>
           <li><strong>Total Bytes:</strong> {summary.total_bytes} bytes</li>
           <li><strong>Mean Packet Size:</strong> {summary.mean_packet_size} bytes</li>
         <li><strong>Max Packet Size:</strong> {summary.max_packet_size} byte</li>
         <li><strong>Unique IPs Contacted:</strong> {summary.unique_ips}</li>
         </ul>
</div>
      
</div>
  );
};

export default SummaryCard;