// src/pages/AdminPage.jsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

const API = import.meta.env.VITE_API_URL;

const styles = {
  container: {
    maxWidth: 1100,
    margin: '40px auto',
    padding: 32,
    background: '#fff',
    borderRadius: 16,
    boxShadow: '0 2px 24px rgba(0,0,0,0.10)',
    fontFamily: 'Inter, Arial, sans-serif',
  },
  header: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 32,
  },
  logo: {
    fontWeight: 700,
    fontSize: 32,
    color: '#0070f3',
    letterSpacing: 1,
  },
  section: {
    marginBottom: 36,
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    marginTop: 12,
    background: '#fafbfc',
    borderRadius: 8,
    overflow: 'hidden',
  },
  th: {
    background: '#f0f4f8',
    color: '#222',
    fontWeight: 600,
    padding: '12px 8px',
    borderBottom: '1px solid #eaeaea',
    textAlign: 'left',
  },
  td: {
    padding: '10px 8px',
    borderBottom: '1px solid #eaeaea',
    fontSize: 15,
  },
  actions: {
    display: 'flex',
    gap: 8,
  },
  button: {
    padding: '7px 16px',
    border: 'none',
    borderRadius: 6,
    fontWeight: 600,
    fontSize: 15,
    cursor: 'pointer',
    background: '#0070f3',
    color: '#fff',
    transition: 'background 0.2s',
  },
  danger: {
    background: '#d32f2f',
    color: '#fff',
  },
  input: {
    padding: 8,
    borderRadius: 5,
    border: '1px solid #ddd',
    fontSize: 15,
    marginRight: 8,
    marginBottom: 6,
  },
  message: {
    margin: '12px 0',
    fontSize: 15,
    color: '#388e3c',
  },
  error: {
    margin: '12px 0',
    fontSize: 15,
    color: '#d32f2f',
  },
  logList: {
    maxHeight: 220,
    overflowY: 'auto',
    background: '#f8f9fa',
    borderRadius: 8,
    padding: 12,
    fontSize: 14,
    marginTop: 8,
  },
  logItem: {
    borderBottom: '1px solid #ececec',
    padding: '6px 0',
  },
  label: {
    fontWeight: 600,
    marginRight: 6,
  }
};

const AdminPage = () => {
  const { user } = useAuth();
  const [users, setUsers] = useState([]);
  const [logs, setLogs] = useState([]);
  const [newUser, setNewUser] = useState({ username: '', email: '', password: '', consent_lgpd: false });
  const [rolesEdit, setRolesEdit] = useState({});
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Fetch users and logs
  useEffect(() => {
    fetchAll();
  }, []);

  const fetchAll = async () => {
    setLoading(true);
    setError('');
    try {
      const [usersRes, logsRes] = await Promise.all([
        axios.get(`${API}/users/`, { withCredentials: true }),
        axios.get(`${API}/users/logs`, { withCredentials: true }),
      ]);
      setUsers(usersRes.data);
      setLogs(logsRes.data);
    } catch (err) {
      setError('Failed to fetch users or logs');
    }
    setLoading(false);
  };

  // Register new user
  const handleRegister = async (e) => {
    e.preventDefault();
    setMessage('');
    setError('');
    try {
      await axios.post(`${API}/users/`, newUser, { withCredentials: true });
      setMessage('User registered!');
      setNewUser({ username: '', email: '', password: '', consent_lgpd: false });
      fetchAll();
    } catch (err) {
      setError('Error registering user');
    }
  };

  // Delete user
  const handleDelete = async (userId) => {
    if (!window.confirm('Are you sure you want to delete this user?')) return;
    setError('');
    try {
      await axios.delete(`${API}/users/users/${userId}`, { withCredentials: true });
      setMessage('User deleted');
      fetchAll();
    } catch (err) {
      setError('Error deleting user');
    }
  };

  // Anonymize user
  const handleAnonymize = async (userId) => {
    if (!window.confirm('Anonymize this user? (LGPD)')) return;
    setError('');
    try {
      await axios.delete(`${API}/users/users/${userId}/anonymize`, { withCredentials: true });
      setMessage('User anonymized');
      fetchAll();
    } catch (err) {
      setError('Error anonymizing user');
    }
  };

  // Update user roles
  const handleUpdateRoles = async (userId) => {
    setError('');
    try {
      await axios.patch(
        `${API}/users/users/${userId}/roles`,
        { roles: rolesEdit[userId]?.split(',').map(r => r.trim()).filter(Boolean) || [] },
        { withCredentials: true }
      );
      setMessage('Roles updated!');
      fetchAll();
    } catch (err) {
      setError('Error updating roles');
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <div style={styles.logo}>AuthSphere Admin</div>
        <div>
          <span style={{ fontWeight: 500, color: '#444', marginRight: 12 }}>
            {user?.username}
          </span>
        </div>
      </div>

      {message && <div style={styles.message}>{message}</div>}
      {error && <div style={styles.error}>{error}</div>}
      {loading && <div style={{ color: '#888', marginBottom: 12 }}>Loading...</div>}

      {/* Register New User */}
      <div style={styles.section}>
        <div style={{ fontSize: 20, fontWeight: 600, marginBottom: 10 }}>Register New User</div>
        <form onSubmit={handleRegister} style={{ display: 'flex', gap: 12, flexWrap: 'wrap', alignItems: 'center' }}>
          <input
            style={styles.input}
            placeholder="Username"
            value={newUser.username}
            onChange={e => setNewUser({ ...newUser, username: e.target.value })}
            required
          />
          <input
            style={styles.input}
            placeholder="Email"
            type="email"
            value={newUser.email}
            onChange={e => setNewUser({ ...newUser, email: e.target.value })}
            required
          />
          <input
            style={styles.input}
            placeholder="Password"
            type="password"
            value={newUser.password}
            onChange={e => setNewUser({ ...newUser, password: e.target.value })}
            required
          />
          <label style={{ display: 'flex', alignItems: 'center', fontSize: 15 }}>
            <input
              type="checkbox"
              checked={newUser.consent_lgpd}
              onChange={e => setNewUser({ ...newUser, consent_lgpd: e.target.checked })}
              style={{ marginRight: 6 }}
            />
            LGPD Consent
          </label>
          <button style={styles.button} type="submit">Register</button>
        </form>
      </div>

      {/* Users Table */}
      <div style={styles.section}>
        <div style={{ fontSize: 20, fontWeight: 600, marginBottom: 10 }}>Users</div>
        <table style={styles.table}>
          <thead>
            <tr>
              <th style={styles.th}>Username</th>
              <th style={styles.th}>Email</th>
              <th style={styles.th}>Roles</th>
              <th style={styles.th}>Active</th>
              <th style={styles.th}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map(u => (
              <tr key={u.id}>
                <td style={styles.td}>{u.username}</td>
                <td style={styles.td}>{u.email}</td>
                <td style={styles.td}>
                  <input
                    style={styles.input}
                    value={
                      rolesEdit[u.id] !== undefined
                        ? rolesEdit[u.id]
                        : (u.roles ? u.roles.join(',') : '')
                    }
                    onChange={e => {

                      const filtered = e.target.value
                        .split(',')
                        .map(r => r.trim())
                        .filter(r => r && !r.includes(':'))
                        .join(',');
                      setRolesEdit({ ...rolesEdit, [u.id]: filtered });
                    }}
                    placeholder="Comma separated roles (ex: admin,user)"
                  />
                  <button
                    style={{ ...styles.button, marginLeft: 6, background: '#388e3c' }}
                    onClick={() => handleUpdateRoles(u.id)}
                  >
                    Save
                  </button>
                </td>
                <td style={styles.td}>{u.is_active ? 'Yes' : 'No'}</td>
                <td style={styles.td}>
                  <div style={styles.actions}>
                    <button
                      style={styles.button}
                      onClick={() => handleAnonymize(u.id)}
                      title="Anonymize (LGPD)"
                    >
                      Anonymize
                    </button>
                    <button
                      style={{ ...styles.button, ...styles.danger }}
                      onClick={() => handleDelete(u.id)}
                      title="Delete"
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            ))}
            {users.length === 0 && (
              <tr>
                <td style={styles.td} colSpan={5}>No users found.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Audit Logs */}
      <div style={styles.section}>
        <div style={{ fontSize: 20, fontWeight: 600, marginBottom: 10 }}>Audit Logs</div>
        <div style={styles.logList}>
          {logs.length === 0 && <div style={{ color: '#888' }}>No logs found.</div>}
          {logs.map(log => (
            <div key={log.id} style={styles.logItem}>
              <span style={styles.label}>{log.action}</span>
              <span>
                {log.user_id ? `User: ${log.user_id}` : 'User: (deleted)'} | {new Date(log.timestamp).toLocaleString()}
              </span>
              {log.details && (
                <span style={{ color: '#555', marginLeft: 8 }}>({log.details})</span>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AdminPage;