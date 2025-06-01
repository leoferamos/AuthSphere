import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

const styles = {
  container: {
    maxWidth: 380,
    margin: '60px auto',
    padding: 32,
    background: '#fff',
    borderRadius: 12,
    boxShadow: '0 2px 16px rgba(0,0,0,0.08)',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  logo: {
    fontWeight: 700,
    fontSize: 28,
    color: '#0070f3',
    marginBottom: 24,
    letterSpacing: 1,
  },
  input: {
    width: '100%',
    padding: 10,
    margin: '8px 0',
    borderRadius: 6,
    border: '1px solid #ddd',
    fontSize: 16,
  },
  button: {
    width: '100%',
    padding: 12,
    background: '#0070f3',
    color: '#fff',
    border: 'none',
    borderRadius: 6,
    fontWeight: 600,
    fontSize: 16,
    marginTop: 16,
    cursor: 'pointer',
  },
  link: {
    marginTop: 16,
    color: '#0070f3',
    textDecoration: 'none',
    fontSize: 15,
  },
  error: {
    color: '#d32f2f',
    marginTop: 8,
    fontSize: 14,
  }
};

const LoginForm = () => {
  const { login } = useAuth();
  const [form, setForm] = useState({ username: '', password: '' });
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await login(form);
    } catch (err) {
      setError('Invalid credentials');
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.logo}>AuthSphere</div>
      <form onSubmit={handleSubmit} style={{ width: '100%' }}>
        <input
          style={styles.input}
          type="text"
          id="username"
          name="username"
          placeholder="Username or Email"
          value={form.username}
          onChange={handleChange}
          autoFocus
          autoComplete="username"
        />
        <input
          style={styles.input}
          type="password"
          id="password"
          name="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
          autoComplete="current-password"
        />
        <button style={styles.button} type="submit">Login</button>
        {error && <div style={styles.error}>{error}</div>}
      </form>
      <a href="/register" style={styles.link}>Don't have an account? Register</a>
    </div>
  );
};

export default LoginForm;
