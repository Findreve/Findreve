/**
 * plugins/vuetify.js
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Composables
import { createVuetify } from 'vuetify'

// 预设主题以防止闪烁
const setInitialTheme = () => {
  // 检查本地存储中的主题首选项
  const savedTheme = localStorage.getItem('vuetify-theme-preference') || 'dark'
  
  // 在DOM加载前应用主题类，避免闪烁
  document.documentElement.classList.add(`v-theme--${savedTheme}`)
  
  return savedTheme
}

const defaultTheme = setInitialTheme()

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    defaultTheme,
    themes: {
      light: {
        dark: false,
        colors: {
          primary: '#1867C0',
          secondary: '#5CBBF6',
        }
      },
      dark: {
        dark: true,
        colors: {
          primary: '#2196F3', 
          secondary: '#03A9F4',
        }
      }
    },
    options: {
      // 启用自定义属性以提高渲染性能
      customProperties: true,
      // 缓存主题以避免重新计算
      cspNonce: 'findreve-theme',
      // 减少主题变化时的闪烁
      variations: false
    }
  },
  defaults: {
    VBtn: { 
      variant: 'flat' 
    },
  }
})
