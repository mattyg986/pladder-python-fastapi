import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import * as api from '../services/api';

export default function Dashboard() {
  const { user, signOut, getToken } = useAuth();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [healthStatus, setHealthStatus] = useState(null);
  const [apiData, setApiData] = useState(null);

  // Check API health on component mount
  useEffect(() => {
    const checkApiHealth = async () => {
      try {
        setLoading(true);
        const response = await api.get('/api/health');
        setHealthStatus(response.data);
        setError(null);
      } catch (err) {
        console.error('Error checking API health:', err);
        setError('Could not connect to the API');
      } finally {
        setLoading(false);
      }
    };

    checkApiHealth();
  }, []);

  // Example of making an authenticated API request
  const fetchProtectedData = async () => {
    try {
      setLoading(true);
      const token = getToken();
      if (!token) {
        setError('No authentication token available');
        return;
      }

      const response = await api.get('/api/v1/agents', token);
      setApiData(response.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching protected data:', err);
      setError('Failed to fetch data from API');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        marginBottom: '2rem' 
      }}>
        <h1>Dashboard</h1>
        <button 
          onClick={signOut}
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: '#6B46C1',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Sign Out
        </button>
      </div>
      
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
        gap: '1rem' 
      }}>
        {/* User info card */}
        <div style={{ 
          padding: '1.5rem',
          backgroundColor: 'white',
          borderRadius: '8px',
          boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)'
        }}>
          <h2>Welcome, {user?.email}</h2>
          <p>This is your protected dashboard.</p>
        </div>

        {/* API health status */}
        <div style={{ 
          padding: '1.5rem',
          backgroundColor: 'white',
          borderRadius: '8px',
          boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)'
        }}>
          <h2>API Status</h2>
          {loading ? (
            <p>Loading...</p>
          ) : error ? (
            <p style={{ color: 'red' }}>{error}</p>
          ) : (
            <div>
              <p>Status: {healthStatus?.status}</p>
              <p>Timestamp: {healthStatus?.timestamp}</p>
            </div>
          )}
        </div>
      </div>

      {/* Protected data section */}
      <div style={{ marginTop: '2rem' }}>
        <button 
          onClick={fetchProtectedData}
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: '#4299E1',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            marginBottom: '1rem'
          }}
          disabled={loading}
        >
          Fetch Agents
        </button>
        
        {loading ? (
          <p>Loading...</p>
        ) : error ? (
          <p style={{ color: 'red' }}>{error}</p>
        ) : apiData ? (
          <div style={{ 
            padding: '1.5rem',
            backgroundColor: 'white',
            borderRadius: '8px',
            boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)'
          }}>
            <h2>Agents Data</h2>
            <pre>{JSON.stringify(apiData, null, 2)}</pre>
          </div>
        ) : null}
      </div>
    </div>
  );
} 