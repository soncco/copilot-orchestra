/**
 * Authentication Service
 */
import apiClient from './api';
import type {
  LoginCredentials,
  LoginResponse,
  RegisterData,
  User,
} from 'src/types';

class AuthService {
  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    const response = await apiClient.post<LoginResponse>(
      '/auth/login/',
      credentials
    );

    if (response.tokens?.access && response.tokens?.refresh) {
      apiClient.setTokens(response.tokens.access, response.tokens.refresh);
    }

    return response;
  }

  async register(data: RegisterData): Promise<User> {
    return apiClient.post<User>('/auth/register/', data);
  }

  async logout(): Promise<void> {
    apiClient.clearTokens();
  }

  async getProfile(): Promise<User> {
    return apiClient.get<User>('/auth/profile/');
  }

  async updateProfile(data: Partial<User>): Promise<User> {
    return apiClient.patch<User>('/auth/profile/', data);
  }

  async refreshToken(): Promise<{ access: string }> {
    const refreshToken = apiClient.getRefreshToken();
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await apiClient.post<{ access: string }>(
      '/auth/refresh/',
      {
        refresh: refreshToken,
      }
    );

    apiClient.setAccessToken(response.access);
    return response;
  }

  isAuthenticated(): boolean {
    return !!apiClient.getAccessToken();
  }

  // MFA methods
  async enableMFA(): Promise<{ qr_code: string; secret: string }> {
    return apiClient.post<{ qr_code: string; secret: string }>(
      '/auth/mfa/enable/'
    );
  }

  async verifyMFA(code: string): Promise<{ verified: boolean }> {
    return apiClient.post<{ verified: boolean }>('/auth/mfa/verify/', {
      code,
    });
  }

  async disableMFA(code: string): Promise<{ disabled: boolean }> {
    return apiClient.post<{ disabled: boolean }>('/auth/mfa/disable/', {
      code,
    });
  }
}

export default new AuthService();
