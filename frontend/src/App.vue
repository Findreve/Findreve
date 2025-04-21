<!-- src/App.vue -->
<template>
  <v-app>
    <!-- 添加加载指示器 -->
    <div v-if="isLoading" class="loading-overlay">
      <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
    </div>
    
    <!-- 使用过渡效果包装主内容 -->
    <v-main>
      <v-fade-transition>
        <router-view v-if="!isLoading"></router-view>
      </v-fade-transition>
    </v-main>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      isLoggedIn: false,
      isLoading: true
    }
  },
  created() {
    this.checkLoginStatus()
  },
  mounted() {
    // 确保主题和样式已完全加载后再显示内容
    this.$nextTick(() => {
      // 短暂延迟确保DOM完全渲染
      setTimeout(() => {
        this.isLoading = false
      }, 200)
    })

    // 添加路由变化时的加载状态
    this.$router.beforeEach((to, from, next) => {
      this.isLoading = true
      next()
    })

    this.$router.afterEach(() => {
      // 路由加载完成后，短暂延迟以确保组件已渲染
      setTimeout(() => {
        this.isLoading = false
      }, 100)
    })
  },
  methods: {
    checkLoginStatus() {
      this.isLoggedIn = !!localStorage.getItem('user-token')
    },
    logout() {
      localStorage.removeItem('user-token')
      this.isLoggedIn = false
      
      // 如果在管理页面退出，则重定向到首页
      if (this.$route.meta.requiresAuth) {
        this.$router.push('/')
      }
    }
  },
  watch: {
    $route() {
      this.checkLoginStatus()
    }
  }
}
</script>

<style>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.7);
  z-index: 9999;
}
</style>