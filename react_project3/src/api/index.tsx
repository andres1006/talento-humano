import axios from "axios";

// Configuración base de Axios
const API_BASE_URL =
  process.env.REACT_APP_API_URL || "http://localhost:8000/api/v1";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Interceptor para agregar token de autenticación
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para manejar errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

// Función simple para hacer peticiones HTTP
export const makeRequest = async <T = any,>(
  method: "GET" | "POST" | "PUT" | "DELETE" | "PATCH",
  url: string,
  data?: any,
  config?: any
): Promise<T> => {
  try {
    console.log(
      `🌐 ${method} ${api.defaults.baseURL}${url}`,
      data ? { data } : ""
    );
    const response = await api.request({
      method,
      url,
      data,
      ...config,
    });
    console.log(
      `✅ ${method} ${url} - Status: ${response.status}`,
      response.data
    );
    return response.data;
  } catch (error: any) {
    console.error(
      `❌ ${method} ${url} - Error:`,
      error.response?.data || error.message
    );
    throw new Error(
      error.response?.data?.message || error.message || "Error en la petición"
    );
  }
};

// Funciones helper para cada método HTTP
export const get = <T = any,>(url: string, config?: any): Promise<T> =>
  makeRequest<T>("GET", url, undefined, config);

export const post = <T = any,>(
  url: string,
  data?: any,
  config?: any
): Promise<T> => makeRequest<T>("POST", url, data, config);

export const put = <T = any,>(
  url: string,
  data?: any,
  config?: any
): Promise<T> => makeRequest<T>("PUT", url, data, config);

export const patch = <T = any,>(
  url: string,
  data?: any,
  config?: any
): Promise<T> => makeRequest<T>("PATCH", url, data, config);

export const del = <T = any,>(url: string, config?: any): Promise<T> =>
  makeRequest<T>("DELETE", url, undefined, config);

// Función para subir archivos
export const uploadFile = async <T = any,>(
  url: string,
  file: File,
  onProgress?: (progress: number) => void
): Promise<T> => {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await api.post(url, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const progress = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          onProgress(progress);
        }
      },
    });
    return response.data;
  } catch (error: any) {
    throw new Error(
      error.response?.data?.message || error.message || "Error al subir archivo"
    );
  }
};

// Función para establecer token de autenticación
export const setAuthToken = (token: string) => {
  localStorage.setItem("token", token);
  api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
};

// Función para remover token de autenticación
export const removeAuthToken = () => {
  localStorage.removeItem("token");
  delete api.defaults.headers.common["Authorization"];
};

// Función para establecer URL base
export const setBaseURL = (url: string) => {
  api.defaults.baseURL = url;
};

export default api;
