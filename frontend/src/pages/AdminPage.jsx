// src/pages/AdminPage.jsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

const API = import.meta.env.VITE_API_URL;

const AdminPage = () => {
  const { user } = useAuth();
  const [users, setUsers] = useState([]);
  const [logs, setLogs] = useState([]);
  const [newUser, setNewUser] = useState({ username: '', email: '', password: '', consent_lgpd: false });
  const [rolesEdit, setRolesEdit] = useState({});
  const [message, setMessage] = useState('');

  // Fetch users (you'll need to implement this endpoint in your backend)
  useEffect(() => {
    axios.get(`${API}/users/`).then(res => setUsers(res.data)).catch(() => {});
    axios.get(`${API}/users/logs`).then(res => setLogs(res.data)).catch(() => {});
  }, []);

  // Register new user
  const handleRegister = async (e) => {
    e.preventDefault();
    setMessage('');
    try {
      await axios.post(`${API}/users/`, newUser);
      setMessage('User registered!');
      setNewUser({ username: '', email: '', password: '', consent_lgpd: false });
      // Optionally, refresh users list
    } catch (err) {
      setMessage('Error registering user');
    }
  };

  // Delete user
  const handleDelete = async (userId) => {
    if (!window.confirm('Are you sure?')) return;
    await axios.delete(`${API}/users/users/${userId}`);
    setUsers(users.filter(u => u.id !== userId));
  };

  // Anonymize user
  const handleAnonymize = async (userId) => {
    if (!window.confirm('Anonymize this user?')) return;
    await axios.delete(`${API}/users/users/${userId}/anonymize`);
    setUsers(users.filter(u => u.id !== userId));
  };

  // Update user roles
  const handleUpdateRoles = async (userId) => {
    await axios.patch(`${API}/users/users/${userId}/roles`, { roles: rolesEdit[userId] || [] });
    setMessage('Roles updated!');
  };

  return (
    <div>
      <h1>Admin Dashboard</h1>
      {message && <div style={{ color: 'green' }}>{message}</div>}

      <h2>Register New User</h2>
      <form onSubmit={handleRegister}>
        <input placeholder="Username" value={newUser.username} onChange={e => setNewUser({ ...newUser, username: e.target.value })} required />
        <input placeholder="Email" type="email" value={newUser.email} onChange={e => setNewUser({ ...newUser, email: e.target.value })} required />
        <input placeholder="Password" type="password" value={newUser.password} onChange={e => setNewUser({ ...newUser, password: e.target.value })} required />
        <label>
          <input type="checkbox" checked={newUser.consent_lgpd} onChange={e => setNewUser({ ...newUser, consent_lgpd: e.target.checked })} />
          LGPD Consent
        </label>
        <button type="submit">Register</button>
      </form>

      <h2>Users</h2>
      <table border="1">
        <thead>
          <tr>
            <th>Username</th><th>Email</th><th>Roles</th><th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map(u => (
            <tr key={u.id}>
              <td>{u.username}</td>
              <td>{u.email}</td>
              <td>
                <input
                  value={rolesEdit[u.id]?.join(',') || ''}
                  onChange={e => setRolesEdit({ ...rolesEdit, [u.id]: e.target.value.split(',').map(r => r.trim()) })}
                  placeholder="Comma separated roles"
                />
                <button onClick={() => handleUpdateRoles(u.id)}>Update Roles</button>
              </td>
              <td>
                <button onClick={() => handleDelete(u.id)}>Delete</button>
                <button onClick={() => handleAnonymize(u.id)}>Anonymize</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Audit Logs</h2>
      <ul>
        {logs.map(log => (
          <li key={log.id}>{log.action} - {log.timestamp}</li>
        ))}
      </ul>
    </div>
  );
};

export default AdminPage;