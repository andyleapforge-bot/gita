import React from "react";
import { Route, Routes, Navigate, useLocation } from "react-router-dom";

import Sidebar from "./components/Sidebar";
import Topbar from "./components/Topbar";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Users from "./pages/Users";
import Shloks from "./pages/Shloks";
import Videos from "./pages/Videos";
import Analytics from "./pages/Analytics";
import Settings from "./pages/Settings";

import ProtectedRoute from "./auth/ProtectedRoute";

export default function App() {
  return (
    <div className="min-h-screen flex text-gray-900 app-shell">

      <Routes>
        {/* PUBLIC ROUTE */}
        <Route path="/login" element={<Login />} />

        {/* PROTECTED ROUTES — ONLY ACCESSIBLE AFTER LOGIN */}
        <Route
          path="/*"
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        />
      </Routes>

    </div>
  );
}

function Layout() {
  const { pathname } = useLocation();
  const pageTitleMap = {
    "/": "Dashboard",
    "/users": "Users",
    "/shloks": "Sholks list to add",
    "/videos": "Videos",
    "/analytics": "Analytics",
    "/settings": "Settings",
  };
  const currentTitle = pageTitleMap[pathname] || "Dashboard";
  return (
    <div className="flex w-full">

      {/* SIDEBAR IS ALWAYS VISIBLE AFTER LOGIN */}
      <Sidebar />

      <main className="flex-1 bg-white/80 backdrop-blur-[1px]">
        <Topbar title={currentTitle} />

        <div className="p-6">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/users" element={<Users />} />
            <Route path="/shloks" element={<Shloks />} />
            <Route path="/videos" element={<Videos />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/settings" element={<Settings />} />

            {/* ANY UNKNOWN PATH REDIRECTS TO DASHBOARD */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </main>

    </div>
  );
}
