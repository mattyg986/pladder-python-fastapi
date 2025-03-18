import axios from 'axios';

const API_URL = '/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Agents API
export const fetchAgents = async () => {
  const response = await api.get('/agents');
  return response.data;
};

export const fetchAgent = async (agentId) => {
  const response = await api.get(`/agents/${agentId}`);
  return response.data;
};

export const createAgent = async (agentData) => {
  const response = await api.post('/agents', agentData);
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
  const response = await api.post(`/agents/${agentId}/tasks`, taskData);
  return response.data;
};

export const fetchTaskStatus = async (agentId, taskId) => {
  const response = await api.get(`/agents/${agentId}/tasks/${taskId}`);
  return response.data;
};

export default api;