<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import apiService from '@/services/api_service'
import Dashboard from '@/components/admin/Dashboard.vue'
import ItemsManagement from '@/components/admin/ItemsManagement.vue'
import UserSettings from '@/components/admin/UserSettings.vue'
import AboutSystem from '@/components/admin/AboutSystem.vue'

const router = useRouter()

// 界面控制
const drawer = ref(false)
const currentTab = ref('dashboard')
const items = ref([])

// 检查用户是否已登录
const checkAuth = () => {
  const token = localStorage.getItem('user-token')
  if (!token) {
    router.push({
      path: '/login',
      query: { redirect: router.currentRoute.value.fullPath }
    })
  }
}

// 获取物品列表
const fetchItems = async () => {
  try {
    const data = await apiService.get('/api/admin/items')
    
    if (data.code === 0 && Array.isArray(data.data)) {
      items.value = data.data
    } else {
      throw new Error(data.msg || '获取物品列表失败')
    }
  } catch (error) {
    console.error('获取物品列表错误:', error)
    nextTick(() => {
      emit('show-toast', {
        color: 'error',
        message: error.message || '加载物品数据失败'
      })
    })
  }
}

// 退出登录
const logout = () => {
  localStorage.removeItem('user-token')
  router.push('/login')
  nextTick(() => {
    emit('show-toast', {
      color: 'info',
      message: '您已成功退出登录'
    })
  })
}

// 组件创建时执行
checkAuth()
fetchItems()
</script>

<template>
  <v-container fluid class="admin-container">
    <!-- 页面顶部应用栏 -->
    <v-app-bar flat density="comfortable" :elevation="1">
      <template v-slot:prepend>
        <v-app-bar-nav-icon @click="drawer = !drawer" color="white"></v-app-bar-nav-icon>
      </template>
      <v-app-bar-title class="text-white">Findreve 管理面板</v-app-bar-title>
      <template v-slot:append>
        <v-menu>
          <template v-slot:activator="{ props }">
            <v-btn icon v-bind="props" color="white">
              <v-avatar size="36">
                <v-img src="https://www.yxqi.cn/wp-content/uploads/2024/08/4a2eb538026d80effb0349aa7acfe628.webp" alt="用户头像"></v-img>
              </v-avatar>
            </v-btn>
          </template>
          <v-list>
            <v-list-item @click="logout">
              <template v-slot:prepend>
                <v-icon icon="mdi-logout" color="error"></v-icon>
              </template>
              <v-list-item-title>退出登录</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </template>
    </v-app-bar>

    <!-- 侧边导航栏 -->
    <v-navigation-drawer v-model="drawer" temporary>
      <template v-slot:prepend>
        <div class="pa-4 text-center">
          <v-avatar size="96" class="mb-2">
            <v-img src="https://www.yxqi.cn/wp-content/uploads/2024/08/4a2eb538026d80effb0349aa7acfe628.webp" alt="Logo"></v-img>
          </v-avatar>
          <div class="text-h6">Findreve</div>
          <div class="text-caption">物品丢失找回系统</div>
        </div>
      </template>
      <v-divider></v-divider>
      <v-list nav>
        <v-list-item prepend-icon="mdi-view-dashboard" title="仪表盘" value="dashboard" @click="currentTab = 'dashboard'"></v-list-item>
        <v-list-item prepend-icon="mdi-tag-multiple" title="物品管理" value="items" @click="currentTab = 'items'"></v-list-item>
        <v-list-item prepend-icon="mdi-account-cog" title="用户设置" value="settings" @click="currentTab = 'settings'"></v-list-item>
        <v-list-item prepend-icon="mdi-information" title="关于系统" value="about" @click="currentTab = 'about'"></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- 主内容区 -->
    <v-main>
      <v-container>
        <!-- 使用拆分后的组件 -->
        <Dashboard v-if="currentTab === 'dashboard'" :items="items" />
        <ItemsManagement v-if="currentTab === 'items'" :items="items" @refresh="fetchItems" />
        <UserSettings v-if="currentTab === 'settings'" />
        <AboutSystem v-if="currentTab === 'about'" />
      </v-container>
    </v-main>
  </v-container>
</template>

<style scoped>
.admin-container {
  min-height: 100vh;
  padding: 0;
}
</style>