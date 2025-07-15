<script setup>
import { ref, onMounted, computed } from 'vue'
import storageService from '@/services/storage_service'

// 缓存相关状态
const isFromCache = ref(false)
const showCacheAlert = ref(false)
const refreshing = ref(false)
const cacheTimestamp = ref(null)

// 本地存储键名
const HOME_CACHE_KEY = 'home-data'

// 格式化缓存时间
const formatCacheTime = computed(() => {
  if (!cacheTimestamp.value) return ''
  
  try {
    const date = new Date(cacheTimestamp.value)
    return new Intl.DateTimeFormat('zh-CN', {
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date)
  } catch (e) {
    return '未知时间'
  }
})

// 从服务加载主页数据
const fetchHomeData = async () => {
  await new Promise(resolve => setTimeout(resolve, 800))
  return {
    socialLinks,
    devSkills,
    designSkills,
    musicSkills,
    projects,
    musicWorks,
    timeline
  }
}

// 从本地存储加载数据
const loadFromCache = () => {
  try {
    const cachedItem = storageService.getItemFromCache(HOME_CACHE_KEY)
    
    if (cachedItem) {
      const cachedTimestamp = storageService.getCacheTimestamp(HOME_CACHE_KEY)
      if (cachedTimestamp) {
        cacheTimestamp.value = cachedTimestamp
        isFromCache.value = true
        showCacheAlert.value = true
      }
      console.log('Using cached home page data')
      return true
    }
  } catch (error) {
    console.error('Error loading cached data:', error)
  }
  return false
}

// 保存数据到本地存储
const saveToCache = async () => {
  try {
    const currentData = await fetchHomeData()
    storageService.saveItemToCache(HOME_CACHE_KEY, currentData)
    console.log('Home page data cached')
  } catch (error) {
    console.error('Error saving data to cache:', error)
  }
}

// 刷新数据
const refreshData = async () => {
  refreshing.value = true
  try {
    const newData = await fetchHomeData()
    storageService.saveItemToCache(HOME_CACHE_KEY, newData)
    isFromCache.value = false
    showCacheAlert.value = false
    console.log('Home data refreshed successfully')
  } catch (error) {
    console.error('Error refreshing home data:', error)
  } finally {
    refreshing.value = false
  }
}

// 组件挂载时执行
onMounted(async () => {
  const hasCachedData = loadFromCache()
  
  if (!hasCachedData) {
    try {
      await fetchHomeData()
      saveToCache()
    } catch (error) {
      console.error('Error fetching initial home data:', error)
    }
  }
})

// 静态数据定义

// 社交媒体链接
const socialLinks = [
  { icon: 'mdi-github', url: 'https://github.com/Yuerchu' },
  { icon: 'mdi-music', url: 'https://music.163.com/#/artist?id=48986728' },
  { icon: 'mdi-web', url: 'https://www.yxqi.cn' },
  { icon: 'mdi-email', url: 'mailto:admin@yuxiaoqiu.cn' },
];

// 开发技能
const devSkills = [
  { name: 'Python', color: 'amber-darken-1' },
  { name: 'Kotlin', color: 'purple-lighten-2' },
  { name: 'Golang', color: 'light-blue' },
  { name: 'Lua', color: 'blue-darken-4' },
  { name: 'C', color: 'red' },
  { name: 'HTML/CSS', color: 'red-darken-3' },
  { name: 'JavaScript', color: 'lime-darken-3' },
  { name: 'Git', color: 'amber-darken-3' },
  { name: 'Docker', color: 'light-blue-darken-1' },
];

// 设计技能
const designSkills = [
  { name: 'Photoshop', color: 'blue-darken-4' },
  { name: 'Premiere', color: 'indigo-darken-3' },
  { name: 'After Effects', color: 'indigo-darken-4' },
  { name: 'Audition', color: 'purple-darken-4' },
  { name: 'Illustrator', color: 'amber-darken-3' },
  { name: 'UI/UX', color: 'pink-darken-2' },
  { name: 'SAI2', color: 'grey-darken-3' },
];

// 音乐技能
const musicSkills = [
  { name: 'FL Studio', color: 'orange-darken-2' },
  { name: '作曲', color: 'deep-purple' },
  { name: '编曲', color: 'indigo' },
  { name: '混音', color: 'blue' },
  { name: '母带处理', color: 'teal' },
  { name: 'Midi创作', color: 'cyan' },
];

// 项目作品
const projects = [
  {
    title: 'DiskNext',
    tag: 'B端系统',
    tagColor: 'primary',
    image: 'https://cdn.vuetifyjs.com/images/cards/sunshine.jpg',
    description: '基于 NiceGUI 打造的高性能网盘系统，提供快速、安全的文件存储与分享服务。',
    link: 'https://pan.yxqi.cn',
    tech: ['Python', 'NiceGUI', 'SQLite', 'Docker']
  },
  {
    title: 'Findreve',
    tag: 'C端应用',
    tagColor: 'success',
    image: 'https://cdn.vuetifyjs.com/images/cards/road.jpg',
    description: '个人主页与物品丢失找回系统，帮助用户追踪和找回丢失物品。',
    link: 'https://i.yxqi.cn',
    tech: ['Vue', 'Vuetify', 'FastAPI', 'MySQL']
  },
  {
    title: 'HeyAuth',
    tag: 'B+C端系统',
    tagColor: 'info',
    image: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg',
    description: '多应用授权系统，提供统一的身份验证和权限管理服务。',
    link: 'https://auth.yxqi.cn',
    tech: ['Python', 'JWT', 'OAuth2', 'Redis']
  }
];

// 音乐作品
const musicWorks = [
  {
    title: '与枫同奔 Run With Fun',
    tag: '词曲',
    description: '我愿如流星赶月那样飞奔，向着远方的梦想不断前行。',
    link: 'https://music.163.com/#/song?id=2148944359',
    cover: 'https://cdn.vuetifyjs.com/images/cards/foster.jpg'
  },
  {
    title: 'HeyFun\'s Story',
    tag: '自设印象曲',
    description: '飞奔在星辰大海之间的少年，勇敢探索未知的世界。',
    link: 'https://music.163.com/#/song?id=1889436124',
    cover: 'https://cdn.vuetifyjs.com/images/cards/house.jpg'
  },
  {
    title: '2020Fall',
    tag: '年度纯音乐',
    description: '耗时6个月完成的年度纯音乐作品，记录2020年的回忆。',
    link: 'https://music.163.com/#/song?id=1863630345',
    cover: 'https://cdn.vuetifyjs.com/images/cards/store.jpg'
  }
];

// 时间线
const timeline = [
  {
    title: '梦开始的地方',
    date: '2022年1月21日',
    content: '购买了第一台服务器，并搭建了第一个 Wordpress 站点，开始了我的网络创作之旅。',
    color: 'primary',
    icon: 'mdi-server'
  },
  {
    title: '音乐作品发布',
    date: '2023年10月29日',
    content: '在网易云音乐发布了收官作《与枫同奔 Release》，截止到 2025 年 4 月 21 日获得了 7000+ 播放。',
    color: 'deep-purple',
    icon: 'mdi-music'
  },
  {
    title: '自建生态计划开始',
    date: '2024年3月1日',
    content: '从 Cloudreve 项目脱离，开始自建网盘系统 DiskNext ，迈出了建立个人技术生态的第一步。',
    color: 'amber',
    icon: 'mdi-cloud'
  },
  {
    title: '当前进展',
    date: '现在',
    content: '目前正在开发 HeyAuth、Findreve、DiskNext 三个核心系统，构建完整的个人应用生态。',
    color: 'success',
    icon: 'mdi-rocket'
  }
];

</script>

<template>
  <v-container fluid>
    <!-- 顶部封面区 -->
    <v-parallax
      src="https://www.yxqi.cn/wp-content/uploads/2024/07/2f02c888032aba72abd82588de04f880.webp"
      height="400"
    >
      <div class="d-flex flex-column fill-height justify-center align-center text-white">
          <v-avatar size="150" class="mb-5 elevation-10 hover-scale">
            <v-img src="https://www.yxqi.cn/wp-content/uploads/2024/08/4a2eb538026d80effb0349aa7acfe628.webp" alt="头像"></v-img>
          </v-avatar>
        <h1 class="text-h2 font-weight-bold mb-2">于小丘</h1>
        <div class="text-h6 mb-3">开发者 / 音乐人 / 创造者</div>
        <div class="d-flex">
          <v-btn
            v-for="(link, i) in socialLinks"
            :key="i"
            :icon="link.icon"
            :href="link.url"
            variant="text"
            color="white"
            class="mx-2"
            target="_blank"
          ></v-btn>
        </div>
      </div>
    </v-parallax>

    <!-- 显示缓存状态提示 -->
    <v-slide-y-transition>
      <v-alert
        v-if="isFromCache && showCacheAlert"
        color="info"
        variant="tonal"
        density="compact"
        class="ma-2 text-center"
        closable
        @click:close="showCacheAlert = false"
      >
        <div class="d-flex align-center justify-center">
          <span>正在使用缓存数据，数据更新时间: {{ formatCacheTime }}</span>
          <v-btn
            v-if="!refreshing"
            variant="text"
            size="small"
            prepend-icon="mdi-refresh"
            class="ml-2"
            @click="refreshData"
          >
            刷新
          </v-btn>
          <v-progress-circular
            v-else
            indeterminate
            size="20"
            width="2"
            color="primary"
            class="ml-2"
          ></v-progress-circular>
        </div>
      </v-alert>
    </v-slide-y-transition>

    <!-- 关于我 -->
    <v-container class="py-12">
      <v-row>
        <v-col cols="12" class="text-center mb-8">
          <h2 class="text-h3 font-weight-bold">关于我</h2>
          <div class="mx-auto mt-3 text-body-1 max-width-text">
            目前是机电一体化专业大二学生，坐标广州。最喜欢用代码创造有趣的东西，主攻 Python 开发（Golang/PHP/Flutter正在努力修炼中！）。
            我的开源作品有HFR-Cloud、Hash-Checker，商业项目有 HeyAuth授权系统 和 HeyPress嘿帕主题 ，是多个知名开源项目的贡献者。
          </div>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" md="4">
          <v-card class="fill-height hover-card">
            <v-card-item>
              <v-card-title class="text-h5">
                <v-icon color="primary" class="mr-2" icon="mdi-code-tags"></v-icon>
                开发技能
              </v-card-title>
            </v-card-item>
            <v-card-text>
              <p class="mb-2">专注于全栈开发，以 Python 为主力语言，同时熟悉多种编程语言与框架。</p>
              <v-chip-group>
                <v-chip v-for="(skill, i) in devSkills" :key="i" :color="skill.color" variant="flat" size="small" class="ma-1">
                  {{ skill.name }}
                </v-chip>
              </v-chip-group>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="4">
          <v-card class="fill-height hover-card">
            <v-card-item>
              <v-card-title class="text-h5">
                <v-icon color="error" class="mr-2" icon="mdi-palette"></v-icon>
                设计技能
              </v-card-title>
            </v-card-item>
            <v-card-text>
              <p class="mb-2">熟练使用各种创意软件，从平面设计到视频剪辑，热衷于创造视觉体验。</p>
              <v-chip-group>
                <v-chip v-for="(skill, i) in designSkills" :key="i" :color="skill.color" variant="flat" size="small" class="ma-1">
                  {{ skill.name }}
                </v-chip>
              </v-chip-group>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="4">
          <v-card class="fill-height hover-card">
            <v-card-item>
              <v-card-title class="text-h5">
                <v-icon color="success" class="mr-2" icon="mdi-music"></v-icon>
                音乐技能
              </v-card-title>
            </v-card-item>
            <v-card-text>
              <p class="mb-2">热衷于音乐创作和制作，擅长使用各种音乐软件创造独特的声音。</p>
              <v-chip-group>
                <v-chip v-for="(skill, i) in musicSkills" :key="i" :color="skill.color" variant="flat" size="small" class="ma-1">
                  {{ skill.name }}
                </v-chip>
              </v-chip-group>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- 项目展示 -->
    <v-sheet color="grey-lighten-4" class="py-12">
      <v-container>
        <v-row>
          <v-col cols="12" class="text-center mb-8">
            <h2 class="text-h3 font-weight-bold">我的项目</h2>
            <div class="mx-auto mt-3 text-body-1 max-width-text">
              这些是我最近开发的一些项目，涵盖了不同的技术栈和应用场景。
            </div>
          </v-col>
        </v-row>

        <v-row>
          <v-col v-for="(project, i) in projects" :key="i" cols="12" sm="6" lg="4">
            <v-card class="fill-height hover-card">
              <v-img 
                :src="project.image"
                height="200" 
                cover
                class="align-end text-white"
                gradient="to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.8) 100%"
              >
                <v-card-title class="text-h5">{{ project.title }}</v-card-title>
              </v-img>
              <v-card-text>
                <div class="d-flex align-center mb-3">
                  <v-chip :color="project.tagColor" size="small" variant="flat">{{ project.tag }}</v-chip>
                  <v-spacer></v-spacer>
                  <v-tooltip location="top" text="查看项目">
                    <template v-slot:activator="{ props }">
                      <v-btn icon="mdi-open-in-new" size="small" variant="text" :href="project.link" target="_blank" v-bind="props"></v-btn>
                    </template>
                  </v-tooltip>
                </div>
                <p>{{ project.description }}</p>
                <v-chip-group>
                  <v-chip v-for="(tech, j) in project.tech" :key="j" size="x-small" variant="outlined" class="mr-1">
                    {{ tech }}
                  </v-chip>
                </v-chip-group>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-sheet>

    <!-- 音乐作品 -->
    <v-container class="py-12">
      <v-row>
        <v-col cols="12" class="text-center mb-8">
          <h2 class="text-h3 font-weight-bold">音乐作品</h2>
          <div class="mx-auto mt-3 text-body-1 max-width-text">
            音乐是我另一种表达自我的方式，这些是我创作的一些音乐作品。
          </div>
        </v-col>
      </v-row>

      <v-row>
        <v-col v-for="(music, i) in musicWorks" :key="i" cols="12" md="4">
          <v-card class="fill-height hover-card">
            <v-img 
              :src="music.cover"
              height="200" 
              cover
            ></v-img>
            <v-card-item>
              <v-card-title>{{ music.title }}</v-card-title>
              <v-card-subtitle>{{ music.tag }}</v-card-subtitle>
            </v-card-item>
            <v-card-text>
              <p>{{ music.description }}</p>
            </v-card-text>
            <v-card-actions>
              <v-btn 
                prepend-icon="mdi-play-circle" 
                variant="tonal" 
                color="primary" 
                :href="music.link"
                target="_blank"
              >
                试听
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- 时间线 -->
    <v-sheet color="grey-lighten-4" class="py-12">
      <v-container>
        <v-row>
          <v-col cols="12" class="text-center mb-8">
            <h2 class="text-h3 font-weight-bold">我的历程</h2>
            <div class="mx-auto mt-3 text-body-1 max-width-text">
              这是我的个人发展历程，每一步都是宝贵的经验。
            </div>
          </v-col>
        </v-row>

        <v-row justify="center">
          <v-col cols="12" md="8">
            <v-timeline side="end" align="start">
              <v-timeline-item
                v-for="(event, i) in timeline"
                :key="i"
                :dot-color="event.color"
                :icon="event.icon"
                size="small"
              >
                <div class="d-flex justify-space-between mb-2">
                  <strong class="text-primary">{{ event.title }}</strong>
                  <div class="text-caption">{{ event.date }}</div>
                </div>
                <div>{{ event.content }}</div>
              </v-timeline-item>
            </v-timeline>
          </v-col>
        </v-row>
      </v-container>
    </v-sheet>

    <!-- 联系我 -->
    <v-container class="py-12">
      <v-row>
        <v-col cols="12" class="text-center mb-8">
          <h2 class="text-h3 font-weight-bold">联系我</h2>
          <div class="mx-auto mt-3 text-body-1 max-width-text">
            如果你有任何问题或者合作机会，欢迎随时联系我。
          </div>
        </v-col>
        
      </v-row>
    </v-container>

    <v-footer class="text-center d-flex flex-column">
      <div class="pt-4 pb-2 text-white">
        <strong>Copyright (C) 2018-{{ new Date().getFullYear() }} 于小丘Yuerchu. </strong> All Rights Reserved.
        <a href="https://beian.miit.gov.cn/" target="_blank" class="text-decoration-none">粤ICP备2024285776号-1</a> · 
        <a href="http://www.beian.gov.cn/" target="_blank" class="text-decoration-none">粤公网安备 44020302000232 号</a>
      </div>
    </v-footer>
  </v-container>
</template>

<style scoped>
.max-width-text {
  max-width: 700px;
}

.hover-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.hover-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 14px 28px rgba(0,0,0,0.15), 0 10px 10px rgba(0,0,0,0.12) !important;
}

.hover-scale {
  transition: transform 0.3s ease;
}

.hover-scale:hover {
  transform: scale(1.1);
}
</style>