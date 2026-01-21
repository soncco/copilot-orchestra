/**
 * API Client with Axios
 */
import axios, { AxiosInstance, AxiosRequestConfig, AxiosError } from 'axios';
import { Notify } from 'quasar';

interface ApiConfig {
  baseURL: string;
  timeout: number;
}

class ApiClient {
  private client: AxiosInstance;
  private accessTokenKey: string;
  private refreshTokenKey: string;

  constructor(config: ApiConfig) {
    this.accessTokenKey =
      import.meta.env.VITE_JWT_ACCESS_TOKEN_KEY || 'travesia_access_token';
    this.refreshTokenKey =
      import.meta.env.VITE_JWT_REFRESH_TOKEN_KEY || 'travesia_refresh_token';

    this.client = axios.create({
      baseURL: config.baseURL,
      timeout: config.timeout,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        const token = this.getAccessToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config as AxiosRequestConfig & {
          _retry?: boolean;
        };

        // If 401 and we have a refresh token, try to refresh
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          const refreshToken = this.getRefreshToken();
          if (refreshToken) {
            try {
              const response = await axios.post(
                `${config.baseURL}/auth/refresh/`,
                {
                  refresh: refreshToken,
                }
              );

              const { access } = response.data;
              this.setAccessToken(access);

              // Retry original request
              if (originalRequest.headers) {
                originalRequest.headers.Authorization = `Bearer ${access}`;
              }
              return this.client(originalRequest);
            } catch (refreshError) {
              // Refresh failed, clear tokens and redirect to login
              this.clearTokens();
              window.location.href = '/login';
              return Promise.reject(refreshError);
            }
          } else {
            // No refresh token, redirect to login
            this.clearTokens();
            window.location.href = '/login';
          }
        }

        // Show error notification
        this.handleError(error);

        return Promise.reject(error);
      }
    );
  }

  private handleError(error: AxiosError) {
    let message = 'Ha ocurrido un error';

    if (error.response) {
      // Server responded with error
      const data = error.response.data as { detail?: string; message?: string };
      message = data.detail || data.message || `Error ${error.response.status}`;
    } else if (error.request) {
      // Request made but no response
      message = 'No se pudo conectar con el servidor';
    } else {
      // Something else happened
      message = error.message;
    }

    Notify.create({
      type: 'negative',
      message,
      position: 'top',
      timeout: 3000,
    });
  }

  // Token management
  getAccessToken(): string | null {
    return localStorage.getItem(this.accessTokenKey);
  }

  setAccessToken(token: string): void {
    localStorage.setItem(this.accessTokenKey, token);
  }

  getRefreshToken(): string | null {
    return localStorage.getItem(this.refreshTokenKey);
  }

  setRefreshToken(token: string): void {
    localStorage.setItem(this.refreshTokenKey, token);
  }

  setTokens(access: string, refresh: string): void {
    this.setAccessToken(access);
    this.setRefreshToken(refresh);
  }

  clearTokens(): void {
    localStorage.removeItem(this.accessTokenKey);
    localStorage.removeItem(this.refreshTokenKey);
  }

  // HTTP methods
  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.get<T>(url, config);
    return response.data;
  }

  async post<T>(
    url: string,
    data?: unknown,
    config?: AxiosRequestConfig
  ): Promise<T> {
    const response = await this.client.post<T>(url, data, config);
    return response.data;
  }

  async put<T>(
    url: string,
    data?: unknown,
    config?: AxiosRequestConfig
  ): Promise<T> {
    const response = await this.client.put<T>(url, data, config);
    return response.data;
  }

  async patch<T>(
    url: string,
    data?: unknown,
    config?: AxiosRequestConfig
  ): Promise<T> {
    const response = await this.client.patch<T>(url, data, config);
    return response.data;
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.delete<T>(url, config);
    return response.data;
  }
}

// Create singleton instance
const apiClient = new ApiClient({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  timeout: Number(import.meta.env.VITE_API_TIMEOUT) || 10000,
});

export default apiClient;
