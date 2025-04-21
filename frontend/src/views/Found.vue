<!-- src/views/Found.vue -->
<template>
  <v-container class="found-container">
    <v-row justify="center">
      <v-col cols="12" md="8" lg="6">
        <!-- 加载状态显示 -->
        <v-skeleton-loader
          v-if="loading && !item"
          type="card, article"
          class="mx-auto"
        ></v-skeleton-loader>

        <!-- 错误信息显示 -->
        <v-alert
          v-if="error"
          type="error"
          variant="tonal"
          closable
          class="mb-4"
        >
          {{ error }}
        </v-alert>

        <!-- 物品详情卡片 -->
        <v-card v-if="item" class="found-item-card">
          <v-card-title class="text-h4 d-flex align-center">
            <v-icon :icon="item.icon || 'mdi-tag'" size="large" class="mr-2"></v-icon>
            {{ item.name || '未命名物品' }}
          </v-card-title>

          <v-card-subtitle class="text-subtitle-1">
            ID: {{ item.id || '未知' }}
            <v-chip v-if="isFromCache" size="x-small" color="grey" class="ml-2" variant="outlined">缓存</v-chip>
          </v-card-subtitle>

          <v-divider class="my-2"></v-divider>

          <v-card-text>
            <div class="d-flex align-center mb-4">
              <v-chip
                :color="getStatusColor(item.status)"
                class="mr-2"
                variant="elevated"
              >
                {{ getStatusText(item.status) }}
              </v-chip>
              <span class="text-caption">最后更新: {{ formatDate(item.updated_at) }}</span>
            </div>

            <!-- 物品描述或者丢失上下文 - 只在丢失状态下显示 -->
            <div v-if="item.status === 'lost' && item.context" class="mb-4">
              <v-alert variant="tonal" color="error" class="context-box">
                <div class="text-subtitle-1 font-weight-bold mb-2">丢失信息</div>
                <div>{{ item.context }}</div>
              </v-alert>
            </div>

            <!-- 创建者/主人信息 -->
            <v-card variant="outlined" class="mb-4">
              <v-card-title class="text-h6">
                <v-icon icon="mdi-account" class="mr-2"></v-icon>
                联系信息
              </v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item v-if="item.phone">
                    <template v-slot:prepend>
                      <v-icon icon="mdi-phone"></v-icon>
                    </template>
                    <v-list-item-title>{{ item.phone }}</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>

            <!-- 仍在加载更新数据时显示 -->
            <div v-if="loading && isFromCache" class="text-center my-3">
              <v-progress-circular
                indeterminate 
                size="24"
                width="2"
                color="primary"
                class="mr-2"
              ></v-progress-circular>
              <span class="text-caption">正在获取最新数据...</span>
            </div>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              variant="tonal"
              prepend-icon="mdi-phone"
              v-if="item.phone"
              :href="`tel:${item.phone}`"
            >
              联系失主
            </v-btn>
          </v-card-actions>
        </v-card>

        <!-- 未找到物品信息时显示 -->
        <v-alert
          v-if="!loading && !error && !item"
          type="warning"
          variant="tonal"
          class="mt-4"
        >
          未找到物品信息，请检查链接是否正确。
        </v-alert>
      </v-col>
    </v-row>
    
  </v-container>
</template>

<script>
/**
 * 物品详情页面
 * 
 * 显示找到的物品的详细信息，包括联系方式、物品状态等
 * 支持从本地缓存加载数据，提高页面加载速度
 */
import apiService from '@/services/api_service';
import storageService from '@/services/storage_service';

export default {
  name: "FoundView",
  data() {
    return {
      key: null,
      item: null,
      loading: true,
      error: null,
      showQRDialog: false,
      isFromCache: false, // 标识数据是否来自缓存
    };
  },
  created() {
    // 从URL获取物品的key
    const urlParams = new URLSearchParams(window.location.search);
    this.key = urlParams.get('key');
    
    if (this.key) {
      // 尝试先从缓存获取数据
      this.loadFromCacheAndFetch();
    } else {
      this.loading = false;
      this.error = "缺少物品标识，无法获取信息";
    }
  },
  methods: {
    /**
     * 从缓存加载数据并获取最新数据
     * 
     * 优先显示本地缓存的数据，同时从API获取最新数据
     */
    async loadFromCacheAndFetch() {
      try {
        // 先尝试从缓存获取数据
        const cachedItem = storageService.getItemFromCache(this.key);
        
        if (cachedItem) {
          // 如果有缓存，立即显示
          this.item = cachedItem;
          this.isFromCache = true;
          this.loading = true; // 保持加载状态，同时获取最新数据
          
          // 在后台获取最新数据
          this.fetchItemDetails(true);
        } else {
          // 没有缓存，直接获取最新数据
          this.loading = true;
          this.fetchItemDetails(false);
        }
      } catch (err) {
        console.error("Error loading cached data:", err);
        // 如果缓存加载失败，直接获取最新数据
        this.fetchItemDetails(false);
      }
    },
    
    /**
     * 获取物品详情数据
     * 
     * @param {boolean} isBackground - 是否在后台获取数据（已显示缓存数据）
     */
    async fetchItemDetails(isBackground = false) {
      try {
        if (!isBackground) {
          this.loading = true;
        }
        
        const data = await apiService.getObject(this.key);
        
        // 更新本地缓存
        storageService.saveItemToCache(this.key, data);
        
        // 更新界面数据
        this.item = data;
        this.isFromCache = false;
        
      } catch (err) {
        console.error("Error fetching item details:", err);
        
        // 如果是后台请求且已有缓存数据显示，则不显示错误
        if (!isBackground || !this.item) {
          this.error = "获取物品信息失败：" + err.message;
        }
      } finally {
        this.loading = false;
      }
    },
    
    /**
     * 获取状态对应的颜色
     * 
     * @param {string} status - 物品状态
     * @returns {string} 对应的颜色名称
     */
    getStatusColor(status) {
      const statusMap = {
        ok: "success",
        lost: "error",
        default: "grey"
      };
      return statusMap[status] || statusMap.default;
    },
    
    /**
     * 获取状态对应的文本
     * 
     * @param {string} status - 物品状态
     * @returns {string} 对应的状态文本
     */
    getStatusText(status) {
      const statusMap = {
        ok: "正常",
        lost: "丢失",
        default: "未知"
      };
      return statusMap[status] || statusMap.default;
    },
    
    /**
     * 格式化日期显示
     * 
     * @param {string} dateStr - 日期字符串
     * @returns {string} 格式化的日期文本
     */
    formatDate(dateStr) {
      if (!dateStr) return "未知时间";
      
      try {
        const date = new Date(dateStr);
        return new Intl.DateTimeFormat('zh-CN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit'
        }).format(date);
      } catch (e) {
        return dateStr;
      }
    }
  }
};
</script>

<style scoped>
.found-container {
  padding-top: 20px;
  padding-bottom: 40px;
}

.found-item-card {
  border-radius: 12px;
  overflow: hidden;
}

.context-box {
  border-left: 4px solid;
}
</style>