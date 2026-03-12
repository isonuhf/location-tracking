<template>
  <div class="app">
    <div class="header">
      <div class="header-left">
        <h1>🚚 运输车队实时追踪系统</h1>
        <p class="subtitle">Real-time Vehicle Tracking System</p>
      </div>

      <div class="header-right">
        <div class="status-indicator">
          <span :class="['indicator', wsConnected ? 'connected' : 'disconnected']"></span>
          <span class="status-text">{{ wsConnected ? '已连接' : '未连接' }}</span>
        </div>
        <div class="header-stats">
          <div class="stat-item">
            <span class="stat-icon">🚚</span>
            <span class="stat-label">车辆</span>
            <span class="stat-value">{{ deviceCount }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-icon">✓</span>
            <span class="stat-label">在线</span>
            <span class="stat-value">{{ onlineCount }}</span>
          </div>
        </div>
        <div class="user-section">
          <span class="username">{{ authStore.user?.username }}</span>
          <button @click="handleLogout" class="logout-btn">登出</button>
        </div>
      </div>
    </div>

    <div class="container">
      <DevicePanel />
      <MapView />
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import MapView from './components/MapView.vue'
import DevicePanel from './components/DevicePanel.vue'
import { WebSocketService } from './services/websocket'
import { useDeviceStore } from './stores/deviceStore'
import { useAuthStore } from './stores/authStore'

const router = useRouter()
const deviceStore = useDeviceStore()
const authStore = useAuthStore()
const wsConnected = ref(false)
let wsService = null
let refreshInterval = null

const deviceCount = computed(() => deviceStore.getAllDevices.length)
const onlineCount = computed(() =>
  deviceStore.getAllDevices.filter(d => d.status === 'active').length
)

const fetchDevices = async () => {
  try {
    const response = await fetch('http://localhost:8000/devices')
    const devices = await response.json()
    devices.forEach(device => {
      deviceStore.updateLocation(device)
    })
  } catch (error) {
    console.error('Failed to fetch devices:', error)
  }
}

const handleLogout = () => {
  authStore.logout()
  router.push('/auth')
}

onMounted(async () => {
  // Fetch initial device list
  await fetchDevices()

  // Connect WebSocket for real-time updates
  wsService = new WebSocketService('ws://localhost:8000/ws')
  try {
    await wsService.connect()
    wsConnected.value = true
  } catch (error) {
    console.error('Failed to connect WebSocket:', error)
    wsConnected.value = false
  }

  // Refresh devices every 5 seconds
  refreshInterval = setInterval(fetchDevices, 5000)
})

onUnmounted(() => {
  if (wsService) {
    wsService.disconnect()
  }
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>

<style scoped>
.app {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.header-left h1 {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.subtitle {
  margin: 4px 0 0 0;
  font-size: 13px;
  opacity: 0.9;
  font-weight: 400;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 30px;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.2);
  padding: 8px 16px;
  border-radius: 20px;
  backdrop-filter: blur(10px);
}

.indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
}

.indicator.connected {
  background-color: #4caf50;
  animation: pulse 2s infinite;
}

.indicator.disconnected {
  background-color: #f44336;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.status-text {
  font-size: 13px;
  font-weight: 600;
}

.header-stats {
  display: flex;
  gap: 20px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.15);
  padding: 8px 16px;
  border-radius: 8px;
  backdrop-filter: blur(10px);
}

.stat-icon {
  font-size: 18px;
}

.stat-label {
  font-size: 12px;
  opacity: 0.9;
}

.stat-value {
  font-size: 18px;
  font-weight: 700;
  min-width: 24px;
}

.user-section {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(255, 255, 255, 0.15);
  padding: 8px 16px;
  border-radius: 8px;
  backdrop-filter: blur(10px);
}

.username {
  font-size: 13px;
  font-weight: 600;
}

.logout-btn {
  padding: 6px 12px;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.container {
  display: flex;
  flex: 1;
  overflow: hidden;
  gap: 0;
}
</style>
