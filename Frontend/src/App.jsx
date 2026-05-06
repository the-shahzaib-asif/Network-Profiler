import React, { useState } from 'react';
import SummaryCard from './components/SummaryCard';
import Charts from './components/Charts';
import CompareCharts from './Components/CompareCharts';

const App = () => {
  const [url1, setUrl1] = useState('');
  const [url2, setUrl2] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [networkData, setNetworkData] = useState(null);
  const [compareData, setCompareData] = useState(null);
  const [mode, setMode] = useState('single');

  const checkValidation = async (e) => {
    e.preventDefault();
    setLoading(true);
    setNetworkData(null);
    setCompareData(null);
    setError('');

    if (mode === 'single') {
      if (!url1.startsWith('http://') && !url1.startsWith('https://')) {
        setError("You Entered Incorrect URL !!!");
        setLoading(false);
        return;
      }
    } else {
      if ((!url1.startsWith('http://') && !url1.startsWith('https://')) || 
          (!url2.startsWith('http://') && !url2.startsWith('https://'))) {
        setError("Both URLs must be correct (start with http/https)!!!");
        setLoading(false);
        return;
      }
    }

    try {
      if(mode === 'single') {
        const res = await fetch('http://127.0.0.1:5000/api/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ url: url1 }), 
        });

        const data = await res.json();
        setNetworkData(data);
      } else {
        const res = await fetch('http://127.0.0.1:5000/api/compare', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ url1: url1, url2: url2 }), 
        });
        const data = await res.json();
        setCompareData(data);
      }
    } catch (err) {
      console.error("Error:", err);
      setError("Server connection failed!");
    } finally {
      setLoading(false); 
    }
  };

  return (
    <div className="container">
      <h1>Network Fingerprint Generator</h1>

      <div className="modeBtn">
        <button id="singlebtn" onClick={() => {
          setMode('single'); setError('');
        }} style={{backgroundColor: mode === 'single' ? '#007BFF' : '#ccc', color: mode === 'single' ? 'white' : 'black'}}>
          Single Mode
        </button>

        <button id='comparebtn' onClick={() => {
          setMode('compare'); setError('');
        }} style={{backgroundColor: mode === 'compare' ? '#007BFF' : '#ccc', color: mode === 'compare' ? 'white' : 'black'}}>
          Compare
        </button>
      </div>
      
      <form onSubmit={checkValidation} style={{ display: 'flex', justifyContent: 'center', flexWrap: 'wrap', gap: '10px' }}>
        <input 
          id="input"
          type="text" 
          placeholder="Website 1 (e.g. https://google.com)"
          value={url1}
          onChange={(e) => setUrl1(e.target.value)}
        />
        {mode === 'compare' && (
          <input 
            id="input2"
            type="text" 
            placeholder="Website 2 (e.g. https://youtube.com)"
            value={url2}
            onChange={(e) => setUrl2(e.target.value)}
          />
        )}
        <button type="submit" id="main_btn">
          {loading ? 'Analyzing...' : (mode === 'single' ? 'Analyze' : 'Compare')}
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

      {networkData && !loading && mode === 'single' && (
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

      {compareData && !loading && mode === 'compare' && (
        <div id="compareGraph">
         
          <h2 id="GraphText">Comparison Results</h2> 
          
          <div id="graphResult" style={{ display: 'flex', justifyContent: 'space-around', gap: '20px' }}>
            <div id="web1" style={{ flex: 1 }}>
              <h3 style={{ color: '#00c49f' }}>{compareData.website1.url}</h3>
              <SummaryCard
                summary={compareData.website1.data.summary}
                classification={compareData.website1.data.classification}
              />
            </div>

            <div id="web2" style={{ flex: 1 }}>
              <h3 style={{ color: '#0088fe' }}>{compareData.website2.url}</h3>
              <SummaryCard
                summary={compareData.website2.data.summary} 
                classification={compareData.website2.data.classification}
              />
            </div>
          </div>

          {/* NEW Combine/Merge Chart*/}
          <div style={{ marginTop: '40px' }}>
             <CompareCharts
                hist1={compareData.website1.data.histogram_stats}
                hist2={compareData.website2.data.histogram_stats}
                time1={compareData.website1.data.time_series}
                time2={compareData.website2.data.time_series}
                site1Name={compareData.website1.url}
                site2Name={compareData.website2.url}
             />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;