<!-- src/views/Login.vue -->
<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="login-card elevation-4">
          <v-card-title class="text-center pt-6 pb-6">
            <h2>登录 Findreve</h2>
          </v-card-title>
          
          <v-card-text>
            <v-alert
              v-if="tokenExpired"
              type="warning"
              variant="tonal"
              icon="mdi-clock-alert-outline"
              class="mb-4"
            >
              登录已过期，请重新登录
            </v-alert>

            <div v-if="checkingToken" class="text-center py-4">
              <v-progress-circular
                indeterminate
                color="primary"
                :size="50"
                :width="5"
              ></v-progress-circular>
              <div class="mt-3">正在验证登录状态...</div>
            </div>

            <v-form v-else @submit.prevent="login" ref="loginForm" v-model="formValid">
              <v-text-field
                v-model="username"
                label="用户名"
                prepend-inner-icon="mdi-account"
                required
                :disabled="loading"
                :rules="usernameRules"
                variant="outlined"
                density="comfortable"
              ></v-text-field>
              
              <v-text-field
                v-model="password"
                label="密码"
                type="password"
                prepend-inner-icon="mdi-lock"
                required
                :disabled="loading"
                :rules="passwordRules"
                variant="outlined"
                density="comfortable"
                autocomplete="current-password"
              ></v-text-field>
              
              <v-btn 
                type="submit" 
                color="primary" 
                block 
                :loading="loading"
                :disabled="loading || !formValid"
                class="mt-2"
              >
                登录
              </v-btn>
              
            </v-form>
            
            <v-alert
              v-if="errorMessage"
              type="error"
              closable
              variant="tonal"
              @click:close="errorMessage = ''"
              class="mt-4"
            >
              {{ errorMessage }}
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
/**
 * 登录页面组件
 * 
 * 处理用户登录认证，成功后保存token并重定向
 * 包含表单验证、记住我功能和错误处理
 * 支持显示令牌过期的提示
 * 支持自动验证现有令牌并跳转
 */
import apiService from '@/services/api_service';

export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '',
      loading: false,
      formValid: false,
      tokenExpired: false,
      checkingToken: true, // 是否正在验证令牌
      usernameRules: [
        v => !!v || '用户名不能为空'
      ],
      passwordRules: [
        v => !!v || '密码不能为空',
        v => (v && v.length >= 6) || '密码长度不能小于6位'
      ]
    }
  },

  created() {
    // 检查是否是因为令牌过期而重定向
    this.tokenExpired = this.$route.query.expired === 'true';
    
    // 如果不是因为令牌过期重定向，则验证令牌
    if (!this.tokenExpired) {
      this.validateExistingToken();
    } else {
      this.checkingToken = false;
    }
  },

  methods: {
    /**
     * 验证现有令牌
     * 
     * 检查本地是否有JWT令牌，如果有则验证其有效性
     * 如果令牌有效，自动重定向到目标页面
     */
    async validateExistingToken() {
      try {
        this.checkingToken = true;
        const token = localStorage.getItem('user-token');
        
        // 如果有令牌，验证其有效性
        if (token) {
          const isValid = await apiService.validateToken();
          
          if (isValid) {
            // 令牌有效，重定向到目标页面
            console.log('令牌有效，正在重定向');
            const redirectPath = this.$route.query.redirect || '/';
            this.$router.push(redirectPath);
            return;
          } else {
            // 令牌无效，清除
            console.log('令牌无效，已清除');
            localStorage.removeItem('user-token');
          }
        }
      } catch (error) {
        console.error('验证令牌时出错:', error);
      } finally {
        this.checkingToken = false;
      }
    },

    /**
     * 处理用户登录
     * 
     * 发送登录请求到后端API，处理成功和失败情况
     * 支持表单验证
     */
    async login() {
      // 表单验证
      const { valid } = await this.$refs.loginForm.validate();
      if (!valid) return;
      
      this.loading = true;
      this.errorMessage = '';
      
      try {
        const result = await apiService.login(this.username, this.password);
        
        if (result.success) {
          // 登录成功
          this.$root.$emit('show-toast', {
            color: 'success',
            message: '登录成功，正在跳转...'
          });
          
          // 登录成功后重定向
          const redirectPath = this.$route.query.redirect || '/';
          this.$router.push(redirectPath);
        } else {
          // 登录失败
          this.errorMessage = result.error;
        }
      } catch (error) {
        console.error('登录错误:', error);
        this.errorMessage = error.message || '登录过程中发生错误，请稍后再试';
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.login-card {
  border-radius: 8px;
  padding: 16px;
}

/* 确保移动设备上有合适的内边距 */
@media (max-width: 600px) {
  .v-container {
    padding: 12px;
  }
}
</style>