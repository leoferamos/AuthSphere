import React, { createContext, useContext, useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  const login = async ({ username, password }) => {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    await axios.post(
      `${import.meta.env.VITE_API_URL}/token`,
      params,
      { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
    );
    const userData = await loadUserProfile();
    if (userData?.permissions?.includes('admin:access')) {
      navigate('/admin');
    } else {
      navigate('/');
    }
  };

  const loadUserProfile = async () => {
    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/users/me`);
      setUser(response.data);
      return response.data;
    } catch {
      setUser(null);
      return null;
    }
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
