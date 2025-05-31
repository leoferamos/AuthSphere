import axios from 'axios';

export const registerUser = async (data) => {
  const response = await axios.post(
    `${import.meta.env.VITE_API_URL}/users/`,
    data
  );
  return response.data;
};