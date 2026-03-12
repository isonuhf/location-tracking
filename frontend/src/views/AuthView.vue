<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <h1>🚚 运输车队追踪系统</h1>
        <p>Vehicle Tracking System</p>
      </div>

      <div class="auth-tabs">
        <button
          :class="['tab', { active: isLogin }]"
          @click="isLogin = true"
        >
          登录
        </button>
        <button
          :class="['tab', { active: !isLogin }]"
          @click="isLogin = false"
        >
          注册
        </button>
      </div>

      <form @submit.prevent="handleSubmit" class="auth-form">
        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <div class="form-group">
          <label>用户名</label>
          <input
            v-model="formData.username"
            type="text"
            placeholder="Enter username"
            required
          />
        </div>

        <div v-if="!isLogin" class="form-group">
          <label>邮箱</label>
          <input
            v-model="formData.email"
            type="email"
            placeholder="Enter email"
            required
          />
        </div>

        <div class="form-group">
          <label>密码</label>
          <input
            v-model="formData.password"
            type="password"
            placeholder="Enter password"
            required
          />
        </div>

        <div v-if="!isLogin" class="form-group">
          <label>确认密码</label>
          <input
            v-model="formData.confirmPassword"
            type="password"
            placeholder="Confirm password"
            required
          />
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="submit-btn"
        >
          {{ loading ? '处理中...' : (isLogin ? '登录' : '注册') }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

const isLogin = ref(true)
const loading = ref(false)
const error = ref(null)
const formData = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const handleSubmit = async () => {
  error.value = null

  if (!isLogin.value && formData.value.password !== formData.value.confirmPassword) {
    error.value = '密码不匹配'
    return
  }

  loading.value = true
  try {
    if (isLogin.value) {
      const success = await authStore.login(formData.value.username, formData.value.password)
      if (success) {
        router.push('/')
      } else {
        error.value = authStore.error
      }
    } else {
      const success = await authStore.register(
        formData.value.username,
        formData.value.email,
        formData.value.password
      )
      if (success) {
        error.value = null
        isLogin.value = true
        formData.value = { username: '', email: '', password: '', confirmPassword: '' }
      } else {
        error.value = authStore.error
      }
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-container {
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.auth-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 400px;
  padding: 40px;
}

.auth-header {
  text-align: center;
  margin-bottom: 30px;
}

.auth-header h1 {
  margin: 0;
  font-size: 24px;
  color: #333;
}

.auth-header p {
  margin: 8px 0 0 0;
  font-size: 14px;
  color: #999;
}

.auth-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  border-bottom: 2px solid #f0f0f0;
}

.tab {
  flex: 1;
  padding: 12px;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  color: #999;
  border-bottom: 3px solid transparent;
  transition: all 0.3s ease;
}

.tab.active {
  color: #667eea;
  border-bottom-color: #667eea;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 13px;
  font-weight: 600;
  color: #333;
}

.form-group input {
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.error-message {
  padding: 10px 12px;
  background: #fee;
  color: #c33;
  border-radius: 6px;
  font-size: 13px;
  margin-bottom: 10px;
}

.submit-btn {
  padding: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
