import React, { useEffect, useState } from 'react';
import { getActiveFormFields } from '../api/formFields';
import { registerUser } from '../api/register';

const RegisterForm = () => {
  const [fields, setFields] = useState([]);
  const [form, setForm] = useState({});
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    getActiveFormFields().then(setFields);
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    try {
      await registerUser(form);
      setSuccess('Registration successful! You can now log in.');
      setForm({});
    } catch (err) {
      setError(
        err.response?.data?.detail?.errors
          ? Object.values(err.response.data.detail.errors).join(', ')
          : err.response?.data?.detail || 'Registration failed'
      );
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {fields.map((field) => (
        <div key={field.name}>
          <label htmlFor={field.name}>{field.label}:</label>
          <input
            type={field.field_type}
            id={field.name}
            name={field.name}
            required={field.is_required}
            value={form[field.name] || ''}
            onChange={handleChange}
          />
        </div>
      ))}
      <button type="submit">Register</button>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {success && <div style={{ color: 'green' }}>{success}</div>}
    </form>
  );
};

export default RegisterForm;