import React from 'react';
import { 
  BarChart, Bar, 
  LineChart, Line, 
  XAxis, YAxis, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

const CompareCharts = ({ hist1, hist2, time1, time2, site1Name, site2Name }) => {
  

  const ranges = ["0-100", "101-500", "501-1000", "1001-1500", "1501+"];
  const mergedHistogram = ranges.map(range => {
    const d1 = hist1?.find(x => x.range === range);
    const d2 = hist2?.find(x => x.range === range);
    return {
      range: range,
      siteA: d1 ? d1.count : 0,
      siteB: d2 ? d2.count : 0
    };
  });

  
  const timeMap = {};
  if (time1) time1.forEach(d => { timeMap[d.time] = { ...timeMap[d.time], time: d.time, siteA: d.bytes }; });
  if (time2) time2.forEach(d => { timeMap[d.time] = { ...timeMap[d.time], time: d.time, siteB: d.bytes }; });

  
  const mergedTimeline = Object.values(timeMap)
    .sort((a, b) => parseInt(a.time) - parseInt(b.time))
    .map(item => ({
      time: item.time,
      siteA: item.siteA || 0,
      siteB: item.siteB || 0
    }));

  const colorSite1 = "#00c49f"; // Green
  const colorSite2 = "#0088fe"; // Blue

  return (
    <div className="compare-charts-container" style={{ display: 'flex', flexDirection: 'column', gap: '30px', marginTop: '20px' }}>
      
      {/* 1. Grouped Bar Chart (Packet Sizes) */}
      <div className="chart-item" style={{ backgroundColor: '#1a1f36', padding: '20px', borderRadius: '10px' }}>
        <h3 style={{ color: '#fff', textAlign: 'center', marginBottom: '20px' }}>PACKET SIZE - A vs B</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={mergedHistogram} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <XAxis dataKey="range" stroke="#ccc" />
            <YAxis stroke="#ccc" />
            <Tooltip contentStyle={{ backgroundColor: '#333', border: 'none', borderRadius: '5px', color: '#fff' }} />
            <Legend wrapperStyle={{ paddingTop: '10px' }}/>
            <Bar dataKey="siteA" fill={colorSite1} name={site1Name || 'Website 1'} />
            <Bar dataKey="siteB" fill={colorSite2} name={site2Name || 'Website 2'} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* 2. Multi-Line Chart (Traffic Timeline) */}
      <div className="chart-item" style={{ backgroundColor: '#1a1f36', padding: '20px', borderRadius: '10px' }}>
        <h3 style={{ color: '#fff', textAlign: 'center', marginBottom: '20px' }}>TRAFFIC TIMELINE - A vs B</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={mergedTimeline} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <XAxis dataKey="time" stroke="#ccc" />
            <YAxis stroke="#ccc" />
            <Tooltip contentStyle={{ backgroundColor: '#333', border: 'none', borderRadius: '5px', color: '#fff' }} />
            <Legend wrapperStyle={{ paddingTop: '10px' }}/>
            <Line type="monotone" dataKey="siteA" stroke={colorSite1} strokeWidth={3} dot={{ r: 5 }} name={site1Name || 'Website 1'} />
            <Line type="monotone" dataKey="siteB" stroke={colorSite2} strokeWidth={3} dot={{ r: 5 }} name={site2Name || 'Website 2'} />
          </LineChart>
        </ResponsiveContainer>
      </div>

    </div>
  );
};

export default CompareCharts;