import axios from 'axios';

export const getActiveFormFields = async () => {
  const response = await axios.get(`${import.meta.env.VITE_API_URL}/form-fields`);
  return response.data;
};