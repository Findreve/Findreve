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

<script>
/**
 * 缓存状态组件
 * 
 * 显示当前本地缓存的状态信息，支持清除缓存
 */
import storageService from '@/services/storage_service';

export default {
  name: 'CacheStatus',
  
  data() {
    return {
      cachedItemsCount: 0,
      lastCleanTime: null,
      cacheMessage: '',
      cacheMessageType: 'info',
      clearing: false
    }
  },
  
  created() {
    this.updateCacheInfo();
  },
  
  methods: {
    /**
     * 更新缓存信息
     */
    updateCacheInfo() {
      try {
        const allItems = storageService.getAllCachedItems();
        this.cachedItemsCount = Object.keys(allItems).length;
        
        // 获取上次清理时间（这里需要在storage_service中添加记录）
        const cleanTimeStr = localStorage.getItem('findreve-last-clean-time');
        this.lastCleanTime = cleanTimeStr ? new Date(parseInt(cleanTimeStr)) : null;
      } catch (error) {
        console.error('获取缓存信息失败', error);
      }
    },
    
    /**
     * 清除所有缓存
     */
    async clearCache() {
      this.clearing = true;
      
      try {
        // 小延迟以显示加载效果
        await new Promise(resolve => setTimeout(resolve, 600));
        
        storageService.clearAllCache();
        localStorage.setItem('findreve-last-clean-time', Date.now().toString());
        
        this.updateCacheInfo();
        this.cacheMessage = '缓存已成功清除';
        this.cacheMessageType = 'success';
      } catch (error) {
        console.error('清除缓存失败', error);
        this.cacheMessage = '清除缓存失败: ' + error.message;
        this.cacheMessageType = 'error';
      } finally {
        this.clearing = false;
      }
    },
    
    /**
     * 格式化日期显示
     * 
     * @param {Date} date - 日期对象
     * @returns {string} 格式化的日期字符串
     */
    formatDate(date) {
      if (!date) return '';
      
      try {
        return new Intl.DateTimeFormat('zh-CN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit'
        }).format(date);
      } catch (e) {
        return date.toString();
      }
    }
  }
}
</script>
