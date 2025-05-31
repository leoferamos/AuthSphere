import React, { useEffect, useState } from 'react';
import { getActiveFormFields } from '../api/formFields';
import { registerUser } from '../api/register';

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
      const detail = err.response?.data?.detail;
      if (Array.isArray(detail)) {
        setError(detail.map((e) => e.msg || JSON.stringify(e)).join(', '));
      } else if (detail?.errors) {
        setError(Object.values(detail.errors).join(', '));
      } else {
        setError(detail || 'Registration failed');
      }
    }
  };

  function formatErrorMessage(msg) {
    if (msg.includes('at least 3 characters')) {
      return 'Username must be at least 3 characters long.';
    }
    if (msg.includes('at least 8 characters')) {
      return 'Password must be at least 8 characters long.';
    }
    if (msg.toLowerCase().includes('passwords do not match')) {
      return 'Passwords do not match.';
    }
    if (msg.toLowerCase().includes('is required')) {
      return 'Please fill in all required fields.';
    }
    return msg;
  }

  let errorMessage = '';
  if (error) {
    if (Array.isArray(error)) {
      errorMessage = error.map((e) => e.msg || JSON.stringify(e)).join(', ');
    } else if (typeof error === 'object') {
      errorMessage = JSON.stringify(error);
    } else {
      errorMessage = error;
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      {fields.map((field) => (
        <React.Fragment key={field.name}>
          <div>
            <label htmlFor={field.name}>{field.label}:</label>
            {field.field_type === 'checkbox' ? (
              <input
                type="checkbox"
                id={field.name}
                name={field.name}
                required={field.is_required}
                checked={form[field.name] || false}
                onChange={handleChange}
              />
            ) : (
              <input
                type={field.field_type}
                id={field.name}
                name={field.name}
                required={field.is_required}
                value={form[field.name] || ''}
                onChange={handleChange}
              />
            )}
          </div>
          {/* Renderiza Confirm Password logo após Password */}
          {field.name === 'password' && (
            <div>
              <label htmlFor="confirm_password">Confirm Password:</label>
              <input
                type="password"
                id="confirm_password"
                name="confirm_password"
                required
                value={confirmPassword}
                onChange={handleChange}
              />
            </div>
          )}
        </React.Fragment>
      ))}
      <button type="submit">Register</button>
      {error && <div style={{ color: 'red' }}>{formatErrorMessage(error)}</div>}
      {success && <div style={{ color: 'green' }}>{success}</div>}
    </form>
  );
};

export default RegisterForm;