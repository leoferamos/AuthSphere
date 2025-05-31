import React, { createContext, useContext, useEffect, useState } from 'react';
import axios from 'axios';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  const login = async ({ username, password }) => {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    const response = await axios.post(
      `${import.meta.env.VITE_API_URL}/token`,
      params,
      { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
    );
    localStorage.setItem('access_token', response.data.access_token);
    await loadUserProfile();
  };

  const loadUserProfile = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) return;
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/users/me`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    setUser(response.data);
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
  };

  useEffect(() => {
    loadUserProfile();
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
