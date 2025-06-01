import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import { AuthProvider } from './contexts/AuthContext';
import { AdminRoute } from './components/AdminRoute';
import AdminPage from './pages/AdminPage';

const Home = () => (
  <div>
    <h1>AuthSphere</h1>
    <p>Welcome to the AuthSphere frontend!</p>
  </div>
);

const App = () => (
  <AuthProvider>
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/admin" element={
          <AdminRoute>
            <AdminPage />
          </AdminRoute>
        } />
      </Routes>
    </Router>
  </AuthProvider>
);

export default App;
