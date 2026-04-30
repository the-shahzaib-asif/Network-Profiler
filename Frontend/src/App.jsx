import React, { useState } from 'react';
import SummaryCard from './components/SummaryCard';
import Charts from './components/Charts';

const App = () => {
  const [url, setUrl] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [networkData, setNetworkData] = useState(null);

  const checkValidation = async (e) => {
    e.preventDefault();
    setLoading(true);
    setNetworkData(null);

    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      setError("You Entered Incorrect URL!!!");
      setLoading(false);
      return;
    }

    setError('');
    
    try {
      const res = await fetch('http://127.0.0.1:5000/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url }), 
      });

      const data = await res.json();
      setNetworkData(data);
    } catch (err) {
      console.error("Error:", err);
    } finally {
      setLoading(false); 
    }
  };

  return (
    <div className="container">
      <h1>Network Fingerprint Generator</h1>
      
      <form onSubmit={checkValidation}>
        <input 
          id="input"
          type="text" 
          placeholder="https://example.com"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <button type="submit" id="main_btn">
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
      </form>

      {loading && (
        <div style={{ textAlign: 'center', marginTop: '40px', marginBottom: '40px' }}>
          <div className="spinner"></div>
          <p id="loading_text">Please Wait!!!!</p>
        </div>
      )}

      {error && <p id="errorMsg">{error}</p>}
      <br/>

      {networkData && !loading && (
        <div id="graph">
          <h2 id="Graph_Text">Analysis Complete for: {networkData.target_url}</h2>
          
      
        <SummaryCard 
          summary={networkData.summary} 
          classification={networkData.classification} 
         />
          
          <Charts 
  protocolData={networkData.protocol_stats} 
  timelineData={networkData.time_series} 
  histogramData={networkData.histogram_stats} 
/>
        </div>
      )}
    </div>
  );
}

export default App;