<script setup>
const systemInfo = {
  version: '2.0.0 Alpha',
  releaseDate: '2025-07-15',
  framework: 'FastAPI + Vue'
}
</script>


<template>
  <div>
    <h2 class="text-h4 mb-4">关于 Findreve</h2>
    <v-card>
      <v-card-text>
        <p class="text-body-1 mb-4">
          Findreve 是一款强大且直观的解决方案，旨在帮助您管理个人物品，并确保丢失后能够安全找回。
          每个物品都会被分配一个唯一 ID，并生成一个安全链接，可轻松嵌入到二维码或 NFC 标签中。
          当扫描该代码时，会将拾得者引导至一个专门的网页，上面显示物品详情和您的联系信息，既保障隐私又便于沟通。
        </p>
        <p class="text-body-1 mb-4">
          无论您是在管理个人物品还是专业资产，Findreve 都能以高效、简便的方式弥合丢失与找回之间的距离。
        </p>
        
        <v-divider class="my-4"></v-divider>
        
        <div class="d-flex align-center mb-4">
          <v-icon size="large" color="primary" class="mr-3">mdi-information-outline</v-icon>
          <div>
            <div class="text-subtitle-1 font-weight-bold">系统信息</div>
            <div class="text-body-2">版本: {{ systemInfo.version }}</div>
          </div>
        </div>
        
        <div class="d-flex align-center mb-4">
          <v-icon size="large" color="primary" class="mr-3">mdi-code-tags</v-icon>
          <div>
            <div class="text-subtitle-1 font-weight-bold">技术栈</div>
            <div class="text-body-2">
              前端: Vue.js, Vuetify, Vite<br>
              后端: FastAPI, Python, SQLite
            </div>
          </div>
        </div>
        
        <div class="d-flex align-center">
          <v-icon size="large" color="primary" class="mr-3">mdi-account-group</v-icon>
          <div>
            <div class="text-subtitle-1 font-weight-bold">开发团队</div>
            <div class="text-body-2">
              由一群热爱技术的开发者共同创建和维护
            </div>
          </div>
        </div>
        
        <v-divider class="my-4"></v-divider>
        <div class="text-center">
          <v-btn color="primary" variant="text" prepend-icon="mdi-help-circle">
            帮助中心
          </v-btn>
          <v-btn color="primary" variant="text" prepend-icon="mdi-email" href="mailto:admin@yuxiaoqiu.cn">
            联系我们
          </v-btn>
          <v-btn color="primary" variant="text" prepend-icon="mdi-github" href="https://github.com/findreve">
            源代码
          </v-btn>
        </div>
        <div class="text-caption text-center mt-4">
          © 2018 - {{ new Date().getFullYear() }} 于小丘Yuerchu. 保留所有权利.
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>