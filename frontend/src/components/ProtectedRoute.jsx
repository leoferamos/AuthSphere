import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Navigate, useLocation } from 'react-router-dom';

export function ProtectedRoute({ children, requiredPermissions = [] }) {
  const { user } = useAuth();
  const location = useLocation();

  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  const hasPermission = requiredPermissions.every(perm =>
    user.permissions.includes(perm)
  );

  return hasPermission ? children : <Navigate to="/unauthorized" replace />;
}