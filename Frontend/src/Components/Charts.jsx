import React from 'react';
import { 
  PieChart, Pie, Cell, 
  BarChart, Bar, 
  LineChart, Line, 
  XAxis, YAxis, Tooltip, Legend 
} from 'recharts';

const Charts = ({ protocolData, timelineData, histogramData }) => {
  // Pie chart ke alag alag protocols ke liye colors
  const COLORS = ['#4dabf7', '#51cf66', '#ff6b6b', '#fcc419', '#cc5de8'];

  return (
    <div id="Charts" className="charts-container">
      
      {/* 1. Protocol Pie Chart */}
      <div className="chart-item">
        <h3>1. Protocol Distribution (Pie Chart)</h3>
        <PieChart width={400} height={250}>
          <Pie 
            data={protocolData} 
            dataKey="count" 
            nameKey="name" 
            cx="50%" 
            cy="50%" 
            outerRadius={80} 
            label 
          >
            {protocolData && protocolData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip contentStyle={{ backgroundColor: '#333', border: 'none', borderRadius: '5px', color: '#fff' }} />
          <Legend />
        </PieChart>
      </div>

      {/* 2. Packet Size Histogram (Naya Bar Chart) */}
      <div className="chart-item">
        <h3>2. Packet Size Histogram (Bar Chart)</h3>
        <BarChart width={400} height={250} data={histogramData}>
          <XAxis dataKey="range" stroke="#ccc" />
          <YAxis stroke="#ccc" />
          <Tooltip contentStyle={{ backgroundColor: '#333', border: 'none', borderRadius: '5px', color: '#fff' }} />
          <Bar dataKey="count" fill="#51cf66" />
        </BarChart>
      </div>

      {/* 3. Traffic Timeline (Line Chart) */}
      <div className="chart-item">
        <h3>3. Traffic Over Time (Line Chart)</h3>
        <LineChart width={400} height={250} data={timelineData}>
          <XAxis dataKey="time" stroke="#ccc" />
          <YAxis stroke="#ccc" />
          <Tooltip contentStyle={{ backgroundColor: '#333', border: 'none', borderRadius: '5px', color: '#fff' }} />
          <Line type="monotone" dataKey="bytes" stroke="#ffc9c9" strokeWidth={3} />
        </LineChart>
      </div>

    </div>
  );
};

export default Charts;