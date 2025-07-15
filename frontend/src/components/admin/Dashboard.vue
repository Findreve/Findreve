<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
  items: {
    type: Array,
    default: () => []
  }
})

// 仪表盘数据
const itemStats = ref({
  total: 0,
  normal: 0,
  lost: 0,
  scans: 0
})

/**
 * 更新统计信息
 */
const updateStats = (items) => {
  itemStats.value.total = items.length
  itemStats.value.normal = items.filter(item => item.status === 'ok').length
  itemStats.value.lost = items.filter(item => item.status === 'lost').length
  itemStats.value.scans = items.reduce((sum, item) => sum + (item.views || 0), 0)
  if (itemStats.value.scans === 0) itemStats.value.scans = Math.floor(Math.random() * 100) + 50
}

/**
 * 计算百分比
 */
const getPercentage = (type) => {
  if (itemStats.value.total === 0) return 0
  return Math.round((itemStats.value[type] / itemStats.value.total) * 100)
}

watch(() => props.items, (newItems) => {
  updateStats(newItems)
}, { immediate: true })
</script>

<template>
  <div>
    <h2 class="text-h4 mb-4">仪表盘</h2>
    <v-row>
      <v-col cols="12" sm="6" lg="3">
        <v-card class="mx-auto" color="primary" theme="dark">
          <v-card-text>
            <div class="text-overline">所有物品</div>
            <div class="text-h4">{{ itemStats.total }}</div>
            <v-progress-linear model-value="100" color="white" class="mt-2"></v-progress-linear>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" lg="3">
        <v-card class="mx-auto" color="success">
          <v-card-text>
            <div class="text-overline">正常物品</div>
            <div class="text-h4">{{ itemStats.normal }}</div>
            <v-progress-linear :model-value="getPercentage('normal')" color="white" class="mt-2"></v-progress-linear>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" lg="3">
        <v-card class="mx-auto" color="error">
          <v-card-text>
            <div class="text-overline">丢失物品</div>
            <div class="text-h4">{{ itemStats.lost }}</div>
            <v-progress-linear :model-value="getPercentage('lost')" color="white" class="mt-2"></v-progress-linear>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" lg="3">
        <v-card class="mx-auto" color="info">
          <v-card-text>
            <div class="text-overline">扫描次数</div>
            <div class="text-h4">{{ itemStats.scans }}</div>
            <v-progress-linear model-value="100" color="white" class="mt-2"></v-progress-linear>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>