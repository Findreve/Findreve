<script setup>
import { ref, onMounted } from 'vue'
import storageService from '@/services/storage_service'

const cachedItemsCount = ref(0)
const lastCleanTime = ref(null)
const cacheMessage = ref('')
const cacheMessageType = ref('info')
const clearing = ref(false)

/**
 * 格式化日期显示
 * @param {Date} date - 日期对象
 * @returns {string} 格式化的日期字符串
 */
const formatDate = (date) => {
  if (!date) return ''
  try {
    return new Intl.DateTimeFormat('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    }).format(date)
  } catch (e) {
    return date.toString()
  }
}

/**
 * 更新缓存信息
 */
const updateCacheInfo = () => {
  try {
    const allItems = storageService.getAllCachedItems()
    cachedItemsCount.value = Object.keys(allItems).length
    
    const cleanTimeStr = localStorage.getItem('findreve-last-clean-time')
    lastCleanTime.value = cleanTimeStr ? new Date(parseInt(cleanTimeStr)) : null
  } catch (error) {
    console.error('获取缓存信息失败', error)
  }
}

/**
 * 清除所有缓存
 */
const clearCache = async () => {
  clearing.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 600))
    storageService.clearAllCache()
    localStorage.setItem('findreve-last-clean-time', Date.now().toString())
    updateCacheInfo()
    cacheMessage.value = '缓存已成功清除'
    cacheMessageType.value = 'success'
  } catch (error) {
    console.error('清除缓存失败', error)
    cacheMessage.value = '清除缓存失败: ' + error.message
    cacheMessageType.value = 'error'
  } finally {
    clearing.value = false
  }
}

onMounted(() => {
  updateCacheInfo()
})
</script>

<template>
  <v-card class="my-3">
    <v-card-title class="d-flex align-center">
      <v-icon icon="mdi-database" class="mr-2" color="primary"></v-icon>
      本地缓存状态
    </v-card-title>
    
    <v-card-text>
      <div class="d-flex align-center mb-3">
        <div>
          <div class="text-subtitle-1">
            已缓存物品数量: <strong>{{ cachedItemsCount }}</strong>
          </div>
          <div class="text-caption text-grey">
            上次清理时间: {{ lastCleanTime ? formatDate(lastCleanTime) : '从未清理' }}
          </div>
        </div>
        <v-spacer></v-spacer>
        <v-btn 
          color="error" 
          variant="outlined" 
          size="small" 
          @click="clearCache"
          :loading="clearing"
          prepend-icon="mdi-delete"
        >
          清除缓存
        </v-btn>
      </div>
      
      <v-alert v-if="cacheMessage" 
        :type="cacheMessageType" 
        variant="tonal" 
        closable 
        @click:close="cacheMessage = ''"
        class="mt-2" 
        density="compact"
      >
        {{ cacheMessage }}
      </v-alert>
    </v-card-text>
  </v-card>
</template>