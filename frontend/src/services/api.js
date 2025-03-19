/**
 * API service for handling authenticated requests to the backend
 */

// Determine if we're running in the browser
const isBrowser = typeof window !== 'undefined';

// Get the API URL based on environment - use localhost for browser requests
const API_URL = isBrowser 
  ? (process.env.REACT_APP_API_URL?.replace('http://backend', 'http://localhost') || 'http://localhost:8000') 
  : (process.env.REACT_APP_API_URL || 'http://backend:8000');

console.log("API Service initialized with URL:", API_URL);
console.log("Running in browser:", isBrowser);

/**
 * Make an authenticated API request
 * @param {string} endpoint - API endpoint to call (without the base URL)
 * @param {Object} options - Request options
 * @param {string} token - Authentication token
 * @returns {Promise} - Fetch promise
 */
export const apiRequest = async (endpoint, options = {}, token = null) => {
  console.log("API URL:", API_URL);
  const url = `${API_URL}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;
  console.log("Making API request to:", url);
  
  // Set up default headers
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };
  
  // Add authorization header if token is provided
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  // Merge options with defaults
  const fetchOptions = {
    ...options,
    headers,
  };
  
  try {
    console.log(`Fetching ${url} with options:`, fetchOptions);
    const response = await fetch(url, fetchOptions);
    console.log(`Received response from ${url}:`, response.status);
    
    // Parse response
    let data;
    const contentType = response.headers.get('Content-Type');
    if (contentType && contentType.includes('application/json')) {
      data = await response.json();
    } else {
      data = await response.text();
    }
    
    // Check if the request was successful
    if (!response.ok) {
      console.error(`API request failed: ${response.status}`, data);
      throw new Error(data.detail || data.message || `API request failed with status ${response.status}`);
    }
    
    return { data, status: response.status, ok: response.ok };
  } catch (error) {
    console.error('API request error:', error);
    // Check if this is a network error (e.g. CORS, connection refused)
    if (error.message && (
      error.message.includes('NetworkError') || 
      error.message.includes('Failed to fetch') ||
      error.message.includes('Network request failed')
    )) {
      console.error('Network error detected - possible CORS or connection issue');
      // You might want to show a user-friendly message here
    }
    throw error;
  }
};

/**
 * Make an authenticated GET request
 * @param {string} endpoint - API endpoint
 * @param {string} token - Authentication token
 * @returns {Promise} - API response
 */
export const get = async (endpoint, token) => {
  return apiRequest(endpoint, { method: 'GET' }, token);
};

/**
 * Make an authenticated POST request
 * @param {string} endpoint - API endpoint
 * @param {Object} data - Request body data
 * @param {string} token - Authentication token
 * @returns {Promise} - API response
 */
export const post = async (endpoint, data, token) => {
  return apiRequest(
    endpoint,
    {
      method: 'POST',
      body: JSON.stringify(data),
    },
    token
  );
};

/**
 * Make an authenticated PUT request
 * @param {string} endpoint - API endpoint
 * @param {Object} data - Request body data
 * @param {string} token - Authentication token
 * @returns {Promise} - API response
 */
export const put = async (endpoint, data, token) => {
  return apiRequest(
    endpoint,
    {
      method: 'PUT',
      body: JSON.stringify(data),
    },
    token
  );
};

/**
 * Make an authenticated DELETE request
 * @param {string} endpoint - API endpoint
 * @param {string} token - Authentication token
 * @returns {Promise} - API response
 */
export const del = async (endpoint, token) => {
  return apiRequest(endpoint, { method: 'DELETE' }, token);
};

// Example API functions
export const getUserInfo = (token) => {
  return get('/api/v1/auth/me', token);
};

export const getPublicData = () => {
  return get('/api/v1/auth/public-data');
};

// Agents API
export const fetchAgents = async (token) => {
  const response = await get('/api/v1/agents', token);
  return response.data;
};

export const fetchAgent = async (agentId, token) => {
  const response = await get(`/api/v1/agents/${agentId}`, token);
  return response.data;
};

export const createAgent = async (agentData, token) => {
  const response = await post('/api/v1/agents', agentData, token);
  return response.data;
};

// Tasks API
export const fetchTasks = async (token) => {
  const response = await get('/api/v1/tasks', token);
  return response.data || [];
};

export const fetchAgentTasks = async (agentId, token) => {
  const response = await get(`/api/v1/agents/${agentId}/tasks`, token);
  return response.data || [];
};

export const createAgentTask = async (agentId, taskData, token) => {
  const response = await post(`/api/v1/agents/${agentId}/tasks`, taskData, token);
  return response.data;
};

export const fetchTaskStatus = async (agentId, taskId, token) => {
  const response = await get(`/api/v1/agents/${agentId}/tasks/${taskId}`, token);
  return response.data;
};