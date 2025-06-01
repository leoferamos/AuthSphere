// src/pages/AdminPage.jsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

const AdminPage = () => {
  const { user } = useAuth();
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const fetchLogs = async () => {
      const token = localStorage.getItem('access_token');
      const res = await axios.get(`${import.meta.env.VITE_API_URL}/users/logs`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setLogs(res.data);
    };
    fetchLogs();
  }, []);

  return (
    <div>
      <h1>Admin Panel</h1>
      <h2>Logs</h2>
      <ul>
        {logs.map(log => (
          <li key={log.id}>{log.action} - {log.timestamp}</li>
        ))}
      </ul>
      {}
    </div>
  );
};

export default AdminPage;