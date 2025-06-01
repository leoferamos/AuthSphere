import React, { useEffect, useState } from 'react';
import { getActiveFormFields } from '../api/formFields';
import { registerUser } from '../api/register';

const styles = {
  container: {
    maxWidth: 420,
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
  },
  success: {
    color: '#388e3c',
    marginTop: 8,
    fontSize: 14,
  }
};

const FIELD_ORDER = ['username', 'email', 'password', 'consent_lgpd'];

const RegisterForm = () => {
  const [fields, setFields] = useState([]);
  const [form, setForm] = useState({});
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    getActiveFormFields().then((data) => {
      const ordered = FIELD_ORDER.map((name) => data.find((f) => f.name === name)).filter(Boolean);
      setFields(ordered);
    });
  }, []);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    if (name === 'confirm_password') {
      setConfirmPassword(value);
    } else {
      setForm((prev) => ({
        ...prev,
        [name]: type === 'checkbox' ? checked : value,
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    if (form.password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    try {
      await registerUser(form);
      setSuccess('Registration successful! You can now log in.');
      setForm({});
      setConfirmPassword('');
    } catch (err) {
      if (err.response?.status === 409) {
        const detail = err.response?.data?.detail;
        if (typeof detail === 'string' && detail.toLowerCase().includes('username')) {
          setError('This username is already taken. Please choose another.');
        } else if (typeof detail === 'string' && detail.toLowerCase().includes('email')) {
          setError('This email is already registered. Please use another or log in.');
        } else {
          setError('Username or email already in use.');
        }
      } else {
        const detail = err.response?.data?.detail;
        if (Array.isArray(detail)) {
          setError(detail.map((e) => e.msg || JSON.stringify(e)).join(', '));
        } else if (detail?.errors) {
          setError(Object.values(detail.errors).join(', '));
        } else {
          setError(detail || 'Registration failed');
        }
      }
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.logo}>AuthSphere</div>
      <form onSubmit={handleSubmit} style={{ width: '100%' }}>
        {fields.map((field) => (
          <div key={field.name}>
            <input
              style={styles.input}
              type={field.field_type}
              id={field.name}
              name={field.name}
              placeholder={field.label}
              required={field.is_required}
              value={form[field.name] || ''}
              onChange={handleChange}
              checked={field.field_type === 'checkbox' ? form[field.name] || false : undefined}
            />
            {}
            {field.name === 'password' && (
              <input
                style={styles.input}
                type="password"
                id="confirm_password"
                name="confirm_password"
                placeholder="Confirm Password"
                required
                value={confirmPassword}
                onChange={handleChange}
              />
            )}
          </div>
        ))}
        <button style={styles.button} type="submit">Register</button>
        {error && <div style={styles.error}>{error}</div>}
        {success && <div style={styles.success}>{success}</div>}
      </form>
      <a href="/login" style={styles.link}>Already have an account? Login</a>
    </div>
  );
};

export default RegisterForm;