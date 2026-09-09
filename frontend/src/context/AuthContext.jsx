import { createContext, useContext, useEffect, useState } from "react";
import apiClient from "../api/client";

const AuthContext = createContext(null);

const STORAGE_KEY = "cloudrelief_token";
const USER_KEY = "cloudrelief_user";

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const raw = localStorage.getItem(USER_KEY);
    return raw ? JSON.parse(raw) : null;
  });

  useEffect(() => {
    if (user) {
      localStorage.setItem(USER_KEY, JSON.stringify(user));
    } else {
      localStorage.removeItem(USER_KEY);
    }
  }, [user]);

  const setSession = (data) => {
    localStorage.setItem(STORAGE_KEY, data.access_token);
    const nextUser = { user_id: data.user_id, email: data.email, role: data.role };
    setUser(nextUser);
    return nextUser;
  };

  const login = async (email, password) => {
    const { data } = await apiClient.post("/api/auth/login", { email, password });
    return setSession(data);
  };

  const register = async (email, password, full_name) => {
    const { data } = await apiClient.post("/api/auth/register", { email, password, full_name });
    return setSession(data);
  };

  const logout = () => {
    localStorage.removeItem(STORAGE_KEY);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, register, logout }}>{children}</AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
