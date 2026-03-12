import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authService } from '../services/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token'))
  const loading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!token.value && !!user.value)

  const register = async (username, email, password) => {
    loading.value = true
    error.value = null
    try {
      await authService.register(username, email, password)
      return true
    } catch (err) {
      error.value = err.message
      return false
    } finally {
      loading.value = false
    }
  }

  const login = async (username, password) => {
    loading.value = true
    error.value = null
    try {
      await authService.login(username, password)
      token.value = authService.getToken()
      user.value = await authService.getMe()
      return true
    } catch (err) {
      error.value = err.message
      return false
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    authService.logout()
    user.value = null
    token.value = null
  }

  const checkAuth = async () => {
    if (!token.value) return false
    try {
      user.value = await authService.getMe()
      return !!user.value
    } catch {
      logout()
      return false
    }
  }

  return {
    user,
    token,
    loading,
    error,
    isAuthenticated,
    register,
    login,
    logout,
    checkAuth
  }
})
