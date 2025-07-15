<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isLoggedIn = ref(false)
const isLoading = ref(true)

// 检查登录状态
const checkLoginStatus = () => {
  isLoggedIn.value = !!localStorage.getItem('user-token')
}

// 退出登录
const logout = () => {
  localStorage.removeItem('user-token')
  isLoggedIn.value = false
  
  if (router.currentRoute.value.meta.requiresAuth) {
    router.push('/')
  }
}

// 路由变化时检查登录状态
watch(() => router.currentRoute.value, () => {
  checkLoginStatus()
})

// 组件创建时检查登录状态
checkLoginStatus()

// 确保主题和样式已完全加载后再显示内容
nextTick(() => {
  setTimeout(() => {
    isLoading.value = false
  }, 200)
})

// 路由变化时的加载状态
router.beforeEach(() => {
  isLoading.value = true
})

router.afterEach(() => {
  setTimeout(() => {
    isLoading.value = false
  }, 100)
})
</script>

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