/**
 * Auth Store - Pinia
 */
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import authService from 'src/services/auth.service';
import type { User, LoginCredentials } from 'src/types';

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  // Getters
  const isAuthenticated = computed(() => !!user.value);
  const isAdmin = computed(() => user.value?.is_admin || false);
  const isManager = computed(() => user.value?.is_manager || false);
  const isSales = computed(() => user.value?.is_sales || false);
  const isGuide = computed(() => user.value?.is_guide || false);
  const isOperations = computed(() => user.value?.is_operations || false);
  const fullName = computed(() =>
    user.value ? `${user.value.first_name} ${user.value.last_name}` : ''
  );
  const userRole = computed(() => user.value?.role || 'guest');

  // Actions
  async function login(credentials: LoginCredentials) {
    loading.value = true;
    error.value = null;

    try {
      const response = await authService.login(credentials);
      user.value = response.user;
      return response;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Error de login';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function logout() {
    loading.value = true;

    try {
      await authService.logout();
      user.value = null;
    } catch (err) {
      console.error('Error al cerrar sesión:', err);
    } finally {
      loading.value = false;
    }
  }

  async function fetchProfile() {
    if (!authService.isAuthenticated()) {
      return;
    }

    loading.value = true;
    error.value = null;

    try {
      user.value = await authService.getProfile();
    } catch (err) {
      error.value =
        err instanceof Error ? err.message : 'Error al cargar perfil';
      // If profile fetch fails, probably token is invalid
      user.value = null;
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function updateProfile(data: Partial<User>) {
    loading.value = true;
    error.value = null;

    try {
      user.value = await authService.updateProfile(data);
    } catch (err) {
      error.value =
        err instanceof Error ? err.message : 'Error al actualizar perfil';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  function clearError() {
    error.value = null;
  }

  // Initialize store
  async function initialize() {
    if (authService.isAuthenticated() && !user.value) {
      try {
        await fetchProfile();
      } catch (err) {
        // If initialization fails, just clear auth
        await logout();
      }
    }
  }

  return {
    // State
    user,
    loading,
    error,
    // Getters
    isAuthenticated,
    isAdmin,
    isManager,
    isSales,
    isGuide,
    isOperations,
    fullName,
    userRole,
    // Actions
    login,
    logout,
    fetchProfile,
    updateProfile,
    clearError,
    initialize,
  };
});
