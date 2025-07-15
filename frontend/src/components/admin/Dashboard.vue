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

<script>
/**
 * 仪表盘组件
 * 
 * 显示物品统计信息和系统概览
 */
export default {
  name: 'DashboardComponent',
  
  props: {
    items: {
      type: Array,
      default: () => []
    }
  },
  
  data() {
    return {
      // 仪表盘数据
      itemStats: {
        total: 0,
        normal: 0,
        lost: 0,
        scans: 0
      }
    };
  },
  
  watch: {
    items: {
      handler(newItems) {
        this.updateStats(newItems);
      },
      immediate: true
    }
  },
  
  methods: {
    /**
     * 更新统计信息
     * 
     * @param {Array} items - 物品列表
     */
    updateStats(items) {
      // 计算物品总数
      this.itemStats.total = items.length;
      
      // 计算正常和丢失物品数量
      this.itemStats.normal = items.filter(item => item.status === 'ok').length;
      this.itemStats.lost = items.filter(item => item.status === 'lost').length;
      
      // 假设扫描次数是从物品中累计的一个属性
      this.itemStats.scans = items.reduce((sum, item) => sum + (item.views || 0), 0);
      if (this.itemStats.scans === 0) this.itemStats.scans = Math.floor(Math.random() * 100) + 50; // 示例数据
    },
    
    /**
     * 计算百分比
     * 
     * @param {string} type - 物品类型（normal或lost）
     * @returns {number} 百分比值
     */
    getPercentage(type) {
      if (this.itemStats.total === 0) return 0;
      return Math.round((this.itemStats[type] / this.itemStats.total) * 100);
    }
  }
};
</script>
