<template>
  <div class="device-panel">
    <div class="panel-header">
      <div class="header-title">
        <h2>🚚 运输车队</h2>
        <span class="device-count">{{ deviceStore.getAllDevices.length }}</span>
      </div>
      <div class="header-stats">
        <div class="stat">
          <span class="stat-label">在线</span>
          <span class="stat-value">{{ onlineCount }}</span>
        </div>
        <div class="stat">
          <span class="stat-label">离线</span>
          <span class="stat-value">{{ offlineCount }}</span>
        </div>
      </div>
    </div>

    <div class="search-box">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="搜索车辆..."
        class="search-input"
      />
    </div>

    <div class="device-list">
      <div
        v-for="(device, index) in filteredDevices"
        :key="device.device_id"
        class="device-item"
        :class="{ active: deviceStore.selectedDeviceId === device.device_id }"
        :style="{ borderLeftColor: getDeviceColor(index) }"
        @click="deviceStore.selectDevice(device.device_id)"
      >
        <div class="device-header">
          <div class="device-title">
            <span class="device-icon">🚚</span>
            <span class="device-id">{{ device.device_id }}</span>
          </div>
          <span class="device-status" :class="device.status">
            {{ device.status === 'active' ? '在线' : '离线' }}
          </span>
        </div>

        <div class="device-info">
          <div class="info-row">
            <span class="info-icon">📍</span>
            <span class="info-label">位置</span>
            <span class="info-value">{{ device.latitude?.toFixed(4) }}, {{ device.longitude?.toFixed(4) }}</span>
          </div>

          <div class="info-row">
            <span class="info-icon">🔋</span>
            <span class="info-label">电池</span>
            <div class="battery-bar">
              <div class="battery-fill" :style="{ width: device.battery + '%', backgroundColor: getBatteryColor(device.battery) }"></div>
            </div>
            <span class="info-value">{{ device.battery || 'N/A' }}%</span>
          </div>

          <div class="info-row">
            <span class="info-icon">📶</span>
            <span class="info-label">信号</span>
            <span class="info-value">{{ device.signal_strength || 'N/A' }} dBm</span>
          </div>

          <div class="info-row">
            <span class="info-icon">⏱️</span>
            <span class="info-label">更新</span>
            <span class="info-value">{{ formatTime(device.timestamp) }}</span>
          </div>
        </div>
      </div>

      <div v-if="filteredDevices.length === 0" class="empty-state">
        <span class="empty-icon">📭</span>
        <p>暂无车辆数据</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useDeviceStore } from '../stores/deviceStore'
import { ref, computed } from 'vue'

const deviceStore = useDeviceStore()
const searchQuery = ref('')

const filteredDevices = computed(() => {
  return deviceStore.getAllDevices.filter(device =>
    device.device_id.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const onlineCount = computed(() => {
  return deviceStore.getAllDevices.filter(d => d.status === 'active').length
})

const offlineCount = computed(() => {
  return deviceStore.getAllDevices.filter(d => d.status !== 'active').length
})

const getDeviceColor = (index) => {
  const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']
  return colors[index % colors.length]
}

const getBatteryColor = (battery) => {
  if (battery > 60) return '#4caf50'
  if (battery > 30) return '#ff9800'
  return '#f44336'
}

const formatTime = (timestamp) => {
  if (!timestamp) return 'N/A'
  const date = new Date(timestamp)
  const now = new Date()
  const diff = Math.floor((now - date) / 1000)

  if (diff < 60) return '刚刚'
  if (diff < 3600) return `${Math.floor(diff / 60)}分钟前`
  if (diff < 86400) return `${Math.floor(diff / 3600)}小时前`
  return date.toLocaleTimeString()
}
</script>

<style scoped>
.device-panel {
  width: 300px;
  height: 100%;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.panel-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.header-title h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
}

.device-count {
  background: rgba(255, 255, 255, 0.3);
  color: white;
  border-radius: 12px;
  padding: 4px 12px;
  font-size: 12px;
  font-weight: 600;
}

.header-stats {
  display: flex;
  gap: 16px;
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-label {
  font-size: 11px;
  opacity: 0.8;
}

.stat-value {
  font-size: 18px;
  font-weight: 700;
}

.search-box {
  padding: 12px 16px;
  background: white;
  border-bottom: 1px solid #e0e0e0;
}

.search-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 13px;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.device-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.device-item {
  background: white;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 8px;
  border-left: 4px solid #667eea;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.device-item:hover {
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.device-item.active {
  background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
  border-left-color: #667eea;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
}

.device-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.device-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.device-icon {
  font-size: 18px;
}

.device-id {
  font-weight: 600;
  font-size: 14px;
  color: #333;
}

.device-status {
  font-size: 11px;
  padding: 4px 8px;
  border-radius: 4px;
  background-color: #e0e0e0;
  color: #666;
  font-weight: 600;
}

.device-status.active {
  background-color: #4caf50;
  color: white;
}

.device-info {
  font-size: 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #666;
}

.info-icon {
  font-size: 13px;
  min-width: 16px;
}

.info-label {
  min-width: 40px;
  font-weight: 500;
  color: #999;
}

.info-value {
  flex: 1;
  color: #333;
  font-weight: 500;
  word-break: break-all;
}

.battery-bar {
  flex: 1;
  height: 4px;
  background: #e0e0e0;
  border-radius: 2px;
  overflow: hidden;
  margin: 0 4px;
}

.battery-fill {
  height: 100%;
  transition: width 0.3s ease;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: #999;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 12px;
  opacity: 0.5;
}

.empty-state p {
  margin: 0;
  font-size: 14px;
}

/* 滚动条美化 */
.device-list::-webkit-scrollbar {
  width: 6px;
}

.device-list::-webkit-scrollbar-track {
  background: transparent;
}

.device-list::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 3px;
}

.device-list::-webkit-scrollbar-thumb:hover {
  background: #999;
}
</style>
