import axios from 'axios';

const API_URL = 'http://localhost:5000/api'; // Adjust this URL if necessary

export const getPriceDistribution = async () => {
  const response = await axios.get(`${API_URL}/price_distribution`);
  return response.data;
};

export const getScatterPlot = async () => {
  const response = await axios.get(`${API_URL}/scatter_plot`);
  return response.data;
};
