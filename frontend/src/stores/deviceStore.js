import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useDeviceStore = defineStore('device', () => {
  const devices = ref(new Map())
  const selectedDeviceId = ref(null)

  const updateLocation = (locationData) => {
    devices.value.set(locationData.device_id, {
      ...devices.value.get(locationData.device_id),
      ...locationData
    })
  }

  const getDevice = (deviceId) => {
    return devices.value.get(deviceId)
  }

  const getAllDevices = computed(() => {
    return Array.from(devices.value.values())
  })

  const selectDevice = (deviceId) => {
    selectedDeviceId.value = deviceId
  }

  const getSelectedDevice = computed(() => {
    return selectedDeviceId.value ? devices.value.get(selectedDeviceId.value) : null
  })

  return {
    devices,
    selectedDeviceId,
    updateLocation,
    getDevice,
    getAllDevices,
    selectDevice,
    getSelectedDevice
  }
})
