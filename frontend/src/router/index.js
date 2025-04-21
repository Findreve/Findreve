// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Found from '@/views/Found.vue'
import Admin from '@/views/Admin.vue'
import Login from '@/views/Login.vue'
import NotFound from '@/views/NotFound.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    meta: { title: '主页'},
    component: Home
  },
  {
    path: '/found',
    name: 'Found',
    meta: { title: '关于此物品'},
    component: Found
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin,
    meta: {
      requiresAuth: true,
      title: 'Findreve 仪表盘'
    }
  },
  {
    path: '/login',
    name: 'Login',
    meta: { title: '登录 Findreve'},
    component: Login
  },
  // 添加404路由，必须放在最后以匹配所有未定义的路径
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
    meta: { title: '404 - 页面未找到' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫，用于检查用户是否已登录并更新页面标题
router.beforeEach((to, from, next) => {
  // 更新页面标题
  document.title = to.meta.title || 'Findreve'
  
  const isAuthenticated = localStorage.getItem('user-token') // 简单的认证检查，实际应用中可能更复杂
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    // 如果路由需要认证但用户未登录，重定向到登录页
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router