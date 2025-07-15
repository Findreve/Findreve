<template>
  <div>
    <h2 class="text-h4 mb-4">用户设置</h2>
    
    <!-- 添加缓存状态组件 -->
    <CacheStatus />
    
    <v-divider class="my-4"></v-divider>
    
    <v-card class="mb-4">
      <v-card-title>个人信息</v-card-title>
      <v-card-text>
        <v-form>
          <v-row>
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="userInfo.username"
                label="用户名"
                readonly
                variant="outlined"
                density="comfortable"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="userInfo.email"
                label="邮箱地址"
                variant="outlined"
                density="comfortable"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-btn color="primary" class="mr-2">更新信息</v-btn>
              <v-btn color="secondary" variant="outlined">修改密码</v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
    
    <v-card>
      <v-card-title>系统设置</v-card-title>
      <v-card-text>
        <v-list>
          <v-list-item>
            <template v-slot:prepend>
              <v-switch v-model="settings.darkMode" color="primary"></v-switch>
            </template>
            <v-list-item-title>深色模式</v-list-item-title>
            <v-list-item-subtitle>启用后将使用深色主题</v-list-item-subtitle>
          </v-list-item>
          
          <v-list-item>
            <template v-slot:prepend>
              <v-switch v-model="settings.notifications" color="primary"></v-switch>
            </template>
            <v-list-item-title>通知提醒</v-list-item-title>
            <v-list-item-subtitle>接收物品状态变更通知</v-list-item-subtitle>
          </v-list-item>
        </v-list>
        
        <div class="d-flex justify-end mt-4">
          <v-btn color="primary">保存设置</v-btn>
        </div>
      </v-card-text>
    </v-card>
    
    <p class="text-caption text-center mt-4">更多设置功能正在开发中...</p>
  </div>
</template>

<script>
import CacheStatus from '@/components/CacheStatus.vue';

export default {
  name: 'UserSettingsComponent',
  components: {
    CacheStatus
  },
  data() {
    return {
      userInfo: {
        username: 'admin',
        email: 'admin@example.com'
      },
      settings: {
        darkMode: false,
        notifications: true
      }
    }
  }
};
</script>
