<!-- src/views/Admin.vue -->
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

<script>
/**
 * 管理面板组件
 * 
 * 提供物品管理功能，包括添加、编辑、删除物品，
 * 以及查看物品状态和生成二维码等功能。
 * 
 * 此组件还包含仪表盘视图，显示物品统计信息和最近活动。
 */
import apiService from '@/services/api_service';
import Dashboard from '@/components/admin/Dashboard.vue';
import ItemsManagement from '@/components/admin/ItemsManagement.vue';
import UserSettings from '@/components/admin/UserSettings.vue';
import AboutSystem from '@/components/admin/AboutSystem.vue';

export default {
  name: 'AdminView',
  components: {
    Dashboard,
    ItemsManagement,
    UserSettings,
    AboutSystem
  },
  data() {
    return {
      // 界面控制
      drawer: false,
      currentTab: 'dashboard',
      items: [], // 保存物品数据以便共享给子组件
    }
  },
  
  created() {
    // 检查用户是否已登录
    this.checkAuth();
    // 获取物品列表
    this.fetchItems();
  },
  
  methods: {
    /**
     * 检查用户是否已登录
     * 
     * 如果未登录，重定向到登录页面
     */
    checkAuth() {
      const token = localStorage.getItem('user-token');
      if (!token) {
        this.$router.push({
          path: '/login',
          query: { redirect: this.$route.fullPath }
        });
      }
    },
    
    /**
     * 获取物品列表
     * 
     * 从API获取所有物品数据
     */
    async fetchItems() {
      try {
        const data = await apiService.get('/api/admin/items');
        
        if (data.code === 0 && Array.isArray(data.data)) {
          this.items = data.data;
        } else {
          throw new Error(data.msg || '获取物品列表失败');
        }
      } catch (error) {
        console.error('获取物品列表错误:', error);
        this.$nextTick(() => {
          this.$root.$emit('show-toast', {
            color: 'error',
            message: error.message || '加载物品数据失败'
          });
        });
      }
    },
    
    /**
     * 退出登录
     */
    logout() {
      localStorage.removeItem('user-token');
      this.$router.push('/login');
      this.$nextTick(() => {
        this.$root.$emit('show-toast', {
          color: 'info',
          message: '您已成功退出登录'
        });
      });
    }
  }
};
</script>

<style scoped>
.admin-container {
  min-height: 100vh;
  padding: 0;
}
</style>