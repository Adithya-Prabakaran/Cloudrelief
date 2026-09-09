import axios from "axios";

// Points at the FastAPI backend. Swapping the backend host (e.g. to an
// Oracle Cloud VM or an AWS API Gateway URL) later means only changing
// VITE_API_URL — no other frontend file needs to change.
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const apiClient = axios.create({
  baseURL: API_URL,
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("cloudrelief_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default apiClient;
