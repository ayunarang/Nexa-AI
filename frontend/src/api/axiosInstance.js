import axios from "axios";

// Create instance for all backend API routes
const axiosInstance = axios.create({
  baseURL: "http://localhost:8000/api", // Unified base for /transcript and /search
});

// Setup session management
const initSession = async () => {
  const existing = sessionStorage.getItem("yt_session_id");
  if (existing) return existing;

  const res = await axiosInstance.get("/transcript/init-session");
  const sessionId = res.data.session_id;
  sessionStorage.setItem("yt_session_id", sessionId);
  return sessionId;
};

// Attach session_id to all requests (via query param)
const setupAxiosInterceptor = () => {
  axiosInstance.interceptors.request.use((config) => {
    const sessionId = sessionStorage.getItem("yt_session_id");
    if (sessionId) {
      const url = new URL(config.url, window.location.origin);
      url.searchParams.set("session_id", sessionId);
      config.url = url.pathname + url.search;
    }
    return config;
  });
};

// Handle tab unload: clear session on server
const setupUnloadHandler = () => {
  window.addEventListener("beforeunload", () => {
    const sessionId = sessionStorage.getItem("yt_session_id");
    if (sessionId) {
      const data = new Blob([JSON.stringify({ session_id: sessionId })], {
        type: "application/json",
      });

      navigator.sendBeacon(
        "http://localhost:8000/api/transcript/clear-session",
        data
      );
      sessionStorage.removeItem("yt_session_id");
    }
  });
};

export const initializeSession = async () => {
  const sessionId = await initSession();
  setupAxiosInterceptor();
  setupUnloadHandler();
  return sessionId;
};

export default axiosInstance;
