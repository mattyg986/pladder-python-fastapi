import { supabase } from './supabase';

// Base URL for API requests (in development, uses proxy in package.json)
const API_BASE_URL = '/api/v1';

/**
 * Make an authenticated request to the API
 * @param {string} endpoint - The API endpoint to call
 * @param {Object} options - Fetch options
 * @returns {Promise<any>} - API response
 */
export const apiRequest = async (endpoint, options = {}) => {
  try {
    // Get the current session for auth token
    const { data: { session } } = await supabase.auth.getSession();
    
    // Set default headers
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };
    
    // Add authorization header if we have a session
    if (session?.access_token) {
      headers['Authorization'] = `Bearer ${session.access_token}`;
    }

    // Build request URL
    const url = `${API_BASE_URL}${endpoint}`;
    
    // Make the request
    const response = await fetch(url, {
      ...options,
      headers,
    });
    
    // Parse JSON response
    const data = await response.json();
    
    // Handle API errors
    if (!response.ok) {
      throw new Error(data.detail || 'API request failed');
    }
    
    return data;
  } catch (error) {
    console.error('API request error:', error);
    throw error;
  }
};

// Example API functions
export const getUserInfo = () => {
  return apiRequest('/auth/me');
};

export const getPublicData = () => {
  return apiRequest('/auth/public-data');
};

// Agents API
export const fetchAgents = async () => {
  const response = await apiRequest('/agents');
  return response.data;
};

export const fetchAgent = async (agentId) => {
  const response = await apiRequest(`/agents/${agentId}`);
  return response.data;
};

export const createAgent = async (agentData) => {
  const response = await apiRequest('/agents', {
    method: 'POST',
    body: JSON.stringify(agentData),
  });
  return response.data;
};

// Tasks API
export const fetchTasks = async () => {
  // In a real application, you would have an endpoint to fetch all tasks
  // For now, we'll simulate empty data
  return [];
};

export const fetchAgentTasks = async (agentId) => {
  // In a real application, you would fetch tasks for a specific agent
  // For now, we'll simulate empty data
  return [];
};

export const createAgentTask = async (agentId, taskData) => {
  const response = await apiRequest(`/agents/${agentId}/tasks`, {
    method: 'POST',
    body: JSON.stringify(taskData),
  });
  return response.data;
};

export const fetchTaskStatus = async (agentId, taskId) => {
  const response = await apiRequest(`/agents/${agentId}/tasks/${taskId}`);
  return response.data;
};