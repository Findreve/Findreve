<script setup>
/**
 * 404错误页面组件
 * 当用户访问不存在的路由时显示此页面
 */
</script>

<template>
  <v-container class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" class="text-center">
        <v-card elevation="3" class="pa-6">
          <v-card-title class="text-h4 mb-4">
            <v-icon size="x-large" color="error" class="me-2">mdi-alert-circle</v-icon>
            404 - 页面未找到
          </v-card-title>
          
          <v-card-text class="text-body-1 mb-4">
            很抱歉，您访问的页面不存在或已被移除。
          </v-card-text>
          
          <v-card-actions class="justify-center">
            <v-btn
              color="primary"
              variant="elevated"
              size="large"
              @click="$router.push('/')"
            >
              返回首页
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>