import React from "react";
import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "./useAuth";

export default function ProtectedRoute({ children }) {
  const { loading, isAdmin, user } = useAuth();
  const location = useLocation();

  // 1️⃣ Firebase still loading — do NOT redirect yet
  if (loading) {
    return <div className="text-white p-6">Loading...</div>;
  }

  // 2️⃣ If no user → redirect to login, but AFTER loading completes
  if (!user) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  // 3️⃣ User exists but not admin → block access
  if (!isAdmin) {
    return <Navigate to="/login" replace />;
  }

  // 4️⃣ User is admin → allow access
  return children;
}
