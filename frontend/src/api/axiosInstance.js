import axios from "axios";
import { toast } from "sonner";

const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

const setupAxiosInterceptor = () => {
  axiosInstance.interceptors.request.use(
    (config) => {
      const sessionId = sessionStorage.getItem("yt_session_id");
      if (!sessionId) {
        toast.error("Missing session ID. Try reloading.");
        return Promise.reject({
          message: "Missing session ID. Try reloading.",
          isSessionError: true,
        });
      }

      const url = new URL(config.url, config.baseURL);
      url.searchParams.set("session_id", sessionId);
      config.url = url.pathname + url.search;

      return config;
    },
    (error) => {
      toast.error("Something went wrong with the request.");
      return Promise.reject(error);
    }
  );

  axiosInstance.interceptors.response.use(
    (response) => response,
    (error) => {
      if (!error?.isSessionError) {
        toast.error("Something went wrong with the response.");
      }
      return Promise.reject(error);
    }
  );
};

const setupUnloadHandler = () => {
  window.addEventListener("beforeunload", () => {
    const sessionId = sessionStorage.getItem("yt_session_id");
    if (sessionId) {
      const data = new Blob([JSON.stringify({ session_id: sessionId })], {
        type: "application/json",
      });

      navigator.sendBeacon(
        `${import.meta.env.VITE_API_BASE_URL}/transcript/clear-session`,
        data
      );

      sessionStorage.removeItem("yt_session_id");
    }
  });
};

export const initializeSession = async () => {
  setupAxiosInterceptor();
  setupUnloadHandler();
};

export default axiosInstance;
