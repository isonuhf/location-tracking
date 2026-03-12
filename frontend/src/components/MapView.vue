<template>
  <div class="map-container">
    <div id="map"></div>
    <div class="map-controls">
      <button @click="toggleTraces" class="control-btn" :class="{ active: showTraces }">
        <span>🛣️</span> {{ showTraces ? '隐藏轨迹' : '显示轨迹' }}
      </button>
      <button @click="centerMap" class="control-btn">
        <span>📍</span> 居中
      </button>
      <button @click="zoomIn" class="control-btn">
        <span>🔍+</span>
      </button>
      <button @click="zoomOut" class="control-btn">
        <span>🔍-</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, watch, ref } from 'vue'
import L from 'leaflet'
import { useDeviceStore } from '../stores/deviceStore'

const deviceStore = useDeviceStore()
let map = null
const markers = new Map()
const polylines = new Map()
const showTraces = ref(true)

const initMap = () => {
  map = L.map('map').setView([39.9042, 116.4074], 10)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19
  }).addTo(map)
}

const getDeviceColor = (index) => {
  const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']
  return colors[index % colors.length]
}

const updateMarker = (device, index) => {
  if (!map) return

  const markerId = device.device_id
  const { latitude, longitude } = device
  const color = getDeviceColor(index)

  if (markers.has(markerId)) {
    const marker = markers.get(markerId)
    marker.setLatLng([latitude, longitude])
  } else {
    const html = `
      <div class="custom-marker" style="background-color: ${color}">
        <div class="marker-icon">🚚</div>
      </div>
    `
    const customIcon = L.divIcon({
      html: html,
      className: 'custom-marker-container',
      iconSize: [40, 40],
      iconAnchor: [20, 40],
      popupAnchor: [0, -40]
    })

    const marker = L.marker([latitude, longitude], { icon: customIcon })
      .bindPopup(`
        <div class="popup-content">
          <strong>${device.device_id}</strong><br>
          <span>📍 ${latitude.toFixed(4)}, ${longitude.toFixed(4)}</span><br>
          <span>🔋 ${device.battery || 'N/A'}%</span><br>
          <span>📶 ${device.signal_strength || 'N/A'} dBm</span><br>
          <span>✓ ${device.status}</span>
        </div>
      `)
      .addTo(map)

    markers.set(markerId, marker)
  }

  // 更新轨迹
  if (showTraces.value) {
    updateTrace(device, index)
  }
}

const updateTrace = (device, index) => {
  const markerId = device.device_id
  const { latitude, longitude } = device
  const color = getDeviceColor(index)

  if (!polylines.has(markerId)) {
    const polyline = L.polyline([[latitude, longitude]], {
      color: color,
      weight: 3,
      opacity: 0.7,
      dashArray: '5, 5'
    }).addTo(map)
    polylines.set(markerId, polyline)
  } else {
    const polyline = polylines.get(markerId)
    const latlngs = polyline.getLatLngs()

    // 限制轨迹点数（最多100个点）
    if (latlngs.length > 100) {
      latlngs.shift()
    }

    latlngs.push([latitude, longitude])
    polyline.setLatLngs(latlngs)
  }
}

const toggleTraces = () => {
  showTraces.value = !showTraces.value

  if (!showTraces.value) {
    // 隐藏所有轨迹
    polylines.forEach(polyline => {
      map.removeLayer(polyline)
    })
    polylines.clear()
  } else {
    // 重新显示轨迹
    deviceStore.getAllDevices.forEach((device, index) => {
      updateTrace(device, index)
    })
  }
}

const centerMap = () => {
  if (deviceStore.getAllDevices.length > 0) {
    const devices = deviceStore.getAllDevices
    const avgLat = devices.reduce((sum, d) => sum + d.latitude, 0) / devices.length
    const avgLon = devices.reduce((sum, d) => sum + d.longitude, 0) / devices.length
    map.setView([avgLat, avgLon], 10)
  }
}

const zoomIn = () => {
  map.zoomIn()
}

const zoomOut = () => {
  map.zoomOut()
}

watch(
  () => deviceStore.getAllDevices,
  (devices) => {
    devices.forEach((device, index) => {
      updateMarker(device, index)
    })
  },
  { deep: true }
)

onMounted(() => {
  initMap()
})

onUnmounted(() => {
  if (map) {
    map.remove()
  }
})
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 100%;
  position: relative;
}

#map {
  width: 100%;
  height: 100%;
}

.map-controls {
  position: absolute;
  bottom: 20px;
  left: 20px;
  display: flex;
  gap: 10px;
  z-index: 1000;
}

.control-btn {
  background: white;
  border: 2px solid #ddd;
  border-radius: 8px;
  padding: 10px 15px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 6px;
}

.control-btn:hover {
  background: #f5f5f5;
  border-color: #667eea;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.control-btn.active {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.control-btn span {
  font-size: 16px;
}

:deep(.custom-marker-container) {
  display: flex;
  align-items: center;
  justify-content: center;
}

:deep(.custom-marker) {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  border: 3px solid white;
}

:deep(.popup-content) {
  font-size: 13px;
  line-height: 1.6;
}

:deep(.popup-content strong) {
  display: block;
  margin-bottom: 8px;
  color: #333;
}

:deep(.popup-content span) {
  display: block;
  color: #666;
}
</style>
