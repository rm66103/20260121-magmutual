import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Get all users with optional filters
 * @param {Object} filters - Filter options
 * @param {string} filters.start_date - Filter users created on/after this date (YYYY-MM-DD)
 * @param {string} filters.end_date - Filter users created on/before this date (YYYY-MM-DD)
 * @param {string} filters.profession - Filter by exact profession match
 * @returns {Promise<Array>} Array of user objects
 */
export const getAllUsers = async (filters = {}) => {
  try {
    const params = {};
    if (filters.start_date) params.start_date = filters.start_date;
    if (filters.end_date) params.end_date = filters.end_date;
    if (filters.profession) params.profession = filters.profession;

    const response = await api.get('/users', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching users:', error);
    throw error;
  }
};

/**
 * Get a single user by ID
 * @param {string} id - User ID
 * @returns {Promise<Object>} User object
 */
export const getUserById = async (id) => {
  try {
    const response = await api.get(`/users/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching user ${id}:`, error);
    throw error;
  }
};

/**
 * Search users by profession using semantic similarity
 * @param {string} profession - Profession text to search for
 * @param {number} limit - Maximum number of results (default: 10)
 * @param {Object} filters - Filter options
 * @param {string} filters.start_date - Filter users created on/after this date (YYYY-MM-DD)
 * @param {string} filters.end_date - Filter users created on/before this date (YYYY-MM-DD)
 * @returns {Promise<Array>} Array of user objects with similarity_score
 */
export const searchUsersByProfession = async (profession, limit = 10, filters = {}) => {
  try {
    const params = {
      profession,
      limit,
    };
    if (filters.start_date) params.start_date = filters.start_date;
    if (filters.end_date) params.end_date = filters.end_date;
    
    const response = await api.get('/users/search', { params });
    return response.data;
  } catch (error) {
    console.error('Error searching users by profession:', error);
    throw error;
  }
};

export default api;
