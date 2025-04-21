/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'

// 先导入样式，确保在应用挂载前已加载CSS
import './assets/styles/global.css' // 导入全局样式

// 添加预加载完成标志以避免闪屏
document.addEventListener('DOMContentLoaded', () => {
  document.documentElement.setAttribute('data-app-loaded', 'true')
})

// 创建应用实例
const app = createApp(App)

// 异步导入其他依赖以优化初始加载
Promise.all([
  import('./plugins/vuetify'),  // Vuetify
  import('./router'),           // 路由
  import('./services/api_service'), // API服务
  import('./services/storage_service') // 本地存储服务
]).then(([{ default: vuetify }, { default: router }, { default: apiService }, { default: storageService }]) => {
  
  // 添加全局事件总线功能
  app.config.globalProperties.$root = {
    $on: (event, callback) => {
      if (!app.config.globalProperties._eventBus) app.config.globalProperties._eventBus = {}
      if (!app.config.globalProperties._eventBus[event]) app.config.globalProperties._eventBus[event] = []
      app.config.globalProperties._eventBus[event].push(callback)
    },
    $off: (event, callback) => {
      if (!app.config.globalProperties._eventBus || !app.config.globalProperties._eventBus[event]) return
      if (!callback) {
        app.config.globalProperties._eventBus[event] = []
      } else {
        app.config.globalProperties._eventBus[event] = app.config.globalProperties._eventBus[event].filter(cb => cb !== callback)
      }
    },
    $emit: (event, ...args) => {
      if (!app.config.globalProperties._eventBus || !app.config.globalProperties._eventBus[event]) return
      app.config.globalProperties._eventBus[event].forEach(callback => callback(...args))
    }
  }

  // 将API服务注册为全局属性
  app.config.globalProperties.$api = apiService
  
  // 将存储服务注册为全局属性
  app.config.globalProperties.$storage = storageService
  
  // 定期清理过期缓存
  setInterval(() => {
    storageService.cleanExpiredCache();
  }, 30 * 60 * 1000); // 每30分钟执行一次

  // 使用插件
  app.use(router)
  app.use(vuetify)

  // 确保所有资源都加载完毕后再挂载应用
  setTimeout(() => {
    app.mount('#app')
  }, 0)
})
