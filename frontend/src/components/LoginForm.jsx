import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

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
    <form onSubmit={handleSubmit}>
      <label htmlFor="username">Username:</label>
      <input type="text" id="username" name="username" value={form.username} onChange={handleChange} />
      <label htmlFor="password">Password:</label>
      <input type="password" id="password" name="password" value={form.password} onChange={handleChange} />
      <button type="submit">Login</button>
      {error && <div style={{ color: 'red' }}>{error}</div>}
    </form>
  );
};

export default LoginForm;
