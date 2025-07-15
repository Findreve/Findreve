<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import apiService from '@/services/api_service'

const emit = defineEmits(['show-toast'])
const route = useRoute()
const router = useRouter()

// 表单数据
const username = ref('')
const password = ref('')
const errorMessage = ref('')
const loading = ref(false)
const formValid = ref(false)
const tokenExpired = ref(false)
const checkingToken = ref(true)
const loginForm = ref(null)

// 表单验证规则
const usernameRules = [
  v => !!v || '用户名不能为空'
]
const passwordRules = [
  v => !!v || '密码不能为空',
  v => (v && v.length >= 6) || '密码长度不能小于6位'
]

// 验证现有令牌
const validateExistingToken = async () => {
  try {
    checkingToken.value = true
    const token = localStorage.getItem('user-token')
    
    if (token) {
      const isValid = await apiService.validateToken()
      
      if (isValid) {
        console.log('令牌有效，正在重定向')
        const redirectPath = route.query.redirect || '/'
        router.push(redirectPath)
        return
      } else {
        console.log('令牌无效，已清除')
        localStorage.removeItem('user-token')
      }
    }
  } catch (error) {
    console.error('验证令牌时出错:', error)
  } finally {
    checkingToken.value = false
  }
}

// 处理用户登录
const login = async () => {
  const { valid } = await loginForm.value.validate()
  if (!valid) return
  
  loading.value = true
  errorMessage.value = ''
  
  try {
    const result = await apiService.login(username.value, password.value)
    
    if (result.success) {
      // 登录成功
      emit('show-toast', {
        color: 'success',
        message: '登录成功，正在跳转...'
      })
      
      // 登录成功后重定向
      const redirectPath = route.query.redirect || '/'
      router.push(redirectPath)
    } else {
      // 登录失败
      errorMessage.value = result.error
    }
  } catch (error) {
    console.error('登录错误:', error)
    errorMessage.value = error.message || '登录过程中发生错误，请稍后再试'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  // 检查是否是因为令牌过期而重定向
  tokenExpired.value = route.query.expired === 'true'
  
  // 如果不是因为令牌过期重定向，则验证令牌
  if (!tokenExpired.value) {
    validateExistingToken()
  } else {
    checkingToken.value = false
  }
})
</script>

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
