/**
 * API Service for Equai AI
 * Handles all backend communication
 */
import axios from 'axios';

// Use environment-specific base URL
const API_BASE_URL = import.meta.env.DEV 
  ? 'http://localhost:5000/api' 
  : '/api'; // For production, proxy through Vercel

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Solve a math problem with AI - automatically detects problem type
 * @param {string} input - Any mathematical problem
 * @returns {Promise} API response with solution and steps
 */
export const solveProblem = async (input) => {
  try {
    const response = await api.post('/solve', {
      input
    });
    return response.data;
  } catch (error) {
    console.error('Error solving problem:', error);
    throw error;
  }
};

/**
 * Get graph URL
 * @param {string} filename - Graph filename
 * @returns {string} Full graph URL
 */
export const getGraphUrl = (filename) => {
  if (!filename) return null;
  if (filename.startsWith('/api/graph/')) {
    return import.meta.env.DEV 
      ? `http://localhost:5000${filename}`
      : `${filename}`;
  }
  return import.meta.env.DEV
    ? `http://localhost:5000/api/graph/${filename}`
    : `/api/graph/${filename}`;
};

/**
 * Get problem-solving history
 * @param {number} limit - Number of results to retrieve
 * @returns {Promise} API response with history
 */
export const getHistory = async (limit = 20) => {
  try {
    const response = await api.get('/history', {
      params: { limit },
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching history:', error);
    throw error;
  }
};

/**
 * Get usage analytics
 * @returns {Promise} API response with analytics
 */
export const getAnalytics = async () => {
  try {
    const response = await api.get('/analytics');
    return response.data;
  } catch (error) {
    console.error('Error fetching analytics:', error);
    throw error;
  }
};

/**
 * Generate graph from expression
 * @param {string} expr - Mathematical expression
 * @param {number} xmin - Minimum x value
 * @param {number} xmax - Maximum x value
 * @returns {string} Graph URL
 */
export const generateGraph = (expr, xmin = -10, xmax = 10) => {
  return import.meta.env.DEV
    ? `http://localhost:5000/api/graph?expr=${encodeURIComponent(expr)}&xmin=${xmin}&xmax=${xmax}`
    : `/api/graph?expr=${encodeURIComponent(expr)}&xmin=${xmin}&xmax=${xmax}`;
};

export default api;