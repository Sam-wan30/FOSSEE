import React, { useState, useEffect, useMemo } from 'react';
import axios from 'axios';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  PointElement,
  LineElement,
} from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';
import './index.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  PointElement,
  LineElement
);

const API_BASE_URL = process.env.REACT_APP_API_URL || 
  (process.env.NODE_ENV === 'production' 
    ? 'https://chemical-equipment-backend.onrender.com/api'
    : 'http://localhost:8000/api');

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [summary, setSummary] = useState(null);
  const [history, setHistory] = useState([]);
  const [datasetData, setDatasetData] = useState(null);
  const [currentDatasetId, setCurrentDatasetId] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const [authCredentials, setAuthCredentials] = useState({ username: '', password: '' });

  // Create axios instance with auth - updates when credentials change
  const api = useMemo(() => {
    return axios.create({
      baseURL: API_BASE_URL,
      auth: {
        username: authCredentials.username,
        password: authCredentials.password,
      },
    });
  }, [authCredentials.username, authCredentials.password]);

  useEffect(() => {
    if (isAuthenticated) {
      loadHistory();
      loadSummary();
    }
  }, [isAuthenticated]);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    
    const loginUsername = username;
    const loginPassword = password;
    
    if (!loginUsername || !loginPassword) {
      setError('Please enter both username and password');
      return;
    }
    
    try {
      // Test authentication with current credentials using history endpoint
      // (works even when no data is uploaded yet)
      const testApi = axios.create({
        baseURL: API_BASE_URL,
        auth: {
          username: loginUsername,
          password: loginPassword,
        },
      });
      
      // Use history endpoint for auth test - returns empty array if no data, but requires auth
      await testApi.get('/history/');
      
      // Set credentials for future API calls
      setAuthCredentials({ username: loginUsername, password: loginPassword });
      setIsAuthenticated(true);
      setSuccess('Login successful!');
    } catch (err) {
      console.error('Login error:', err);
      if (err.response?.status === 401) {
        setError('Invalid credentials. Please check your username and password.');
      } else {
        setError(err.response?.data?.error || 'Login failed. Please try again.');
      }
    }
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setUsername('');
    setPassword('');
    setAuthCredentials({ username: '', password: '' });
    setSummary(null);
    setHistory([]);
    setDatasetData(null);
    setCurrentDatasetId(null);
  };

  const handleFileSelect = (e) => {
    setSelectedFile(e.target.files[0]);
    setError('');
    setSuccess('');
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file first');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await api.post('/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setSuccess('File uploaded successfully!');
      setSummary(response.data.summary);
      setCurrentDatasetId(response.data.dataset.id);
      
      // Automatically load the full dataset data and charts
      await loadDatasetData(response.data.dataset.id);
      
      // Load history to show updated list
      await loadHistory();
      
      setSelectedFile(null);
      document.querySelector('input[type="file"]').value = '';
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const loadSummary = async (datasetId = null) => {
    try {
      const url = datasetId ? `/summary/${datasetId}/` : '/summary/';
      const response = await api.get(url);
      setSummary(response.data);
    } catch (err) {
      // If no datasets exist, that's okay - user just needs to upload one
      if (err.response?.status === 404 && err.response?.data?.error === 'No datasets available') {
        console.log('No datasets available yet');
      } else {
        console.error('Failed to load summary:', err);
      }
    }
  };

  const loadHistory = async () => {
    try {
      const response = await api.get('/history/');
      setHistory(response.data);
    } catch (err) {
      console.error('Failed to load history:', err);
    }
  };

  const loadDatasetData = async (datasetId) => {
    try {
      const response = await api.get(`/dataset/${datasetId}/`);
      setDatasetData(response.data.data);
      setCurrentDatasetId(datasetId);
      await loadSummary(datasetId);
    } catch (err) {
      setError('Failed to load dataset data');
    }
  };

  const downloadPDF = async (datasetId) => {
    try {
      const response = await api.get(`/report/${datasetId}/`, {
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `equipment_report_${datasetId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      setError('Failed to generate PDF report');
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="login-container">
        <div className="chemical-background">
          <div className="floating-elements">
            <div className="element beaker">🧪</div>
            <div className="element molecule">⚗️</div>
            <div className="element test-tube">🧫</div>
            <div className="element letter-h">H</div>
            <div className="element letter-n">N</div>
            <div className="element letter-o">O</div>
            <div className="element letter-s">S</div>
            <div className="element letter-p">P</div>
          </div>
        </div>
        <div className="login-content">
          <div className="login-header">
            <div className="beaker-icon">⚗️</div>
            <h1 className="main-title">Chemical Equipment</h1>
            <h2 className="sub-title">Parameter Visualizer</h2>
            <p className="description">Monitor and analyze your equipment data</p>
          </div>
          <div className="login-form-container">
            <form onSubmit={handleLogin} className="login-form">
              <div className="input-group">
                <span className="input-icon">👤</span>
                <input
                  type="text"
                  placeholder="Enter your username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="login-input"
                  required
                />
              </div>
              <div className="input-group">
                <span className="input-icon">🔒</span>
                <input
                  type="password"
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="login-input"
                  required
                />
              </div>
              <button type="submit" className="signin-button">
                Sign In
              </button>
            </form>
            {error && <div className="error-message">{error}</div>}
          </div>
          <p className="secure-text">Secure access to your equipment monitoring dashboard</p>
        </div>
      </div>
    );
  }

  const typeDistributionData = summary
    ? {
        labels: Object.keys(summary.equipment_type_distribution),
        datasets: [
          {
            label: 'Equipment Count',
            data: Object.values(summary.equipment_type_distribution),
            backgroundColor: [
              '#667eea',
              '#764ba2',
              '#f093fb',
              '#4facfe',
              '#00f2fe',
              '#43e97b',
              '#fa709a',
            ],
          },
        ],
      }
    : null;

  const parameterData = summary
    ? {
        labels: ['Flowrate', 'Pressure', 'Temperature'],
        datasets: [
          {
            label: 'Average Values',
            data: [
              summary.avg_flowrate,
              summary.avg_pressure,
              summary.avg_temperature,
            ],
            backgroundColor: '#667eea',
          },
        ],
      }
    : null;

  return (
    <div className="container">
      <h1>Chemical Equipment Parameter Visualizer</h1>
      <button onClick={handleLogout} className="logout-button">
        Logout
      </button>
      
      {success && <div className="success">{success}</div>}
      {error && <div className="error">{error}</div>}

      <div className="card upload-section">
        <h2>Upload CSV File</h2>
        <div className="file-input-wrapper">
          <input
            type="file"
            accept=".csv"
            onChange={handleFileSelect}
            id="file-input"
          />
          <label htmlFor="file-input" className="file-input-label">
            Choose CSV File
          </label>
        </div>
        {selectedFile && (
          <div className="selected-file">Selected: {selectedFile.name}</div>
        )}
        <button
          onClick={handleUpload}
          disabled={!selectedFile || loading}
          className="upload-button"
        >
          {loading ? 'Uploading...' : 'Upload File'}
        </button>
      </div>

      {summary && (
        <>
          <div className="card">
            <h2>Summary Statistics</h2>
            <div className="summary-grid">
              <div className="summary-item">
                <h3>Total Equipment</h3>
                <p>{summary.total_count}</p>
              </div>
              <div className="summary-item">
                <h3>Avg Flowrate</h3>
                <p>{summary.avg_flowrate}</p>
              </div>
              <div className="summary-item">
                <h3>Avg Pressure</h3>
                <p>{summary.avg_pressure}</p>
              </div>
              <div className="summary-item">
                <h3>Avg Temperature</h3>
                <p>{summary.avg_temperature}</p>
              </div>
            </div>
          </div>

          <div className="card">
            <h2>Equipment Type Distribution</h2>
            <div className="chart-container">
              <Pie data={typeDistributionData} />
            </div>
          </div>

          <div className="card">
            <h2>Average Parameters</h2>
            <div className="chart-container">
              <Bar data={parameterData} />
            </div>
          </div>

          {currentDatasetId && (
            <div className="card">
              <div className="action-buttons">
                <button
                  onClick={() => loadDatasetData(currentDatasetId)}
                  className="action-button"
                >
                  View Full Data Table
                </button>
                <button
                  onClick={() => downloadPDF(currentDatasetId)}
                  className="action-button download"
                >
                  Download PDF Report
                </button>
              </div>
            </div>
          )}

          {datasetData && (
            <div className="card">
              <h2>Equipment Data Table</h2>
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Equipment Name</th>
                    <th>Type</th>
                    <th>Flowrate</th>
                    <th>Pressure</th>
                    <th>Temperature</th>
                  </tr>
                </thead>
                <tbody>
                  {datasetData.map((row, index) => (
                    <tr key={index}>
                      <td>{row['Equipment Name']}</td>
                      <td>{row.Type}</td>
                      <td>{row.Flowrate}</td>
                      <td>{row.Pressure}</td>
                      <td>{row.Temperature}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}

      {history.length > 0 && (
        <div className="card history-section">
          <h2>Upload History (Last 5)</h2>
          {history.map((dataset) => (
            <div
              key={dataset.id}
              className="history-item"
              onClick={() => loadDatasetData(dataset.id)}
            >
              <h3>{dataset.name}</h3>
              <p>
                Uploaded: {new Date(dataset.uploaded_at).toLocaleString()} | 
                Count: {dataset.total_count} | 
                Avg Flowrate: {dataset.avg_flowrate?.toFixed(2)} | 
                Avg Pressure: {dataset.avg_pressure?.toFixed(2)} | 
                Avg Temperature: {dataset.avg_temperature?.toFixed(2)}
              </p>
              <div className="action-buttons">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    downloadPDF(dataset.id);
                  }}
                  className="action-button download"
                >
                  Download PDF
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
