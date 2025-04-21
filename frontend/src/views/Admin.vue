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
        <v-list-item prepend-icon="mdi-qrcode-scan" title="生成码" value="qrcodes" @click="currentTab = 'qrcodes'"></v-list-item>
        <v-list-item prepend-icon="mdi-account-cog" title="用户设置" value="settings" @click="currentTab = 'settings'"></v-list-item>
        <v-list-item prepend-icon="mdi-information" title="关于系统" value="about" @click="currentTab = 'about'"></v-list-item>
      </v-list>
      <template v-slot:append>
        <div class="pa-2">
          <v-btn block color="primary" @click="drawer = false">
            关闭菜单
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>

    <!-- 主内容区 -->
    <v-main>
      <v-container>
        <!-- 仪表盘 -->
        <div v-if="currentTab === 'dashboard'">
          <h2 class="text-h4 mb-4">仪表盘</h2>
          <v-row>
            <v-col cols="12" sm="6" lg="3">
              <v-card class="mx-auto" color="primary" theme="dark">
                <v-card-text>
                  <div class="text-overline">所有物品</div>
                  <div class="text-h4">{{ itemStats.total }}</div>
                  <v-progress-linear model-value="100" color="white" class="mt-2"></v-progress-linear>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" sm="6" lg="3">
              <v-card class="mx-auto" color="success">
                <v-card-text>
                  <div class="text-overline">正常物品</div>
                  <div class="text-h4">{{ itemStats.normal }}</div>
                  <v-progress-linear :model-value="getPercentage('normal')" color="white" class="mt-2"></v-progress-linear>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" sm="6" lg="3">
              <v-card class="mx-auto" color="error">
                <v-card-text>
                  <div class="text-overline">丢失物品</div>
                  <div class="text-h4">{{ itemStats.lost }}</div>
                  <v-progress-linear :model-value="getPercentage('lost')" color="white" class="mt-2"></v-progress-linear>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" sm="6" lg="3">
              <v-card class="mx-auto" color="info">
                <v-card-text>
                  <div class="text-overline">扫描次数</div>
                  <div class="text-h4">{{ itemStats.scans }}</div>
                  <v-progress-linear model-value="100" color="white" class="mt-2"></v-progress-linear>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </div>

        <!-- 物品管理 -->
        <div v-if="currentTab === 'items'">
          <div class="d-flex justify-space-between align-center mb-4">
            <h2 class="text-h4">物品管理</h2>
            <v-btn 
              color="primary" 
              prepend-icon="mdi-plus" 
              @click="openItemDialog()" 
              class="text-none"
            >
              添加物品
            </v-btn>
          </div>

          <!-- 物品筛选和搜索 -->
          <v-card class="mb-4">
            <v-card-text>
              <v-row>
                <v-col cols="12" sm="4">
                  <v-text-field
                    v-model="search"
                    label="搜索物品"
                    prepend-inner-icon="mdi-magnify"
                    single-line
                    hide-details
                    variant="outlined"
                    density="comfortable"
                    class="rounded-lg"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="4">
                  <v-select
                    v-model="statusFilter"
                    :items="statusOptions"
                    label="状态筛选"
                    variant="outlined"
                    density="comfortable"
                    hide-details
                    class="rounded-lg"
                  ></v-select>
                </v-col>
                <v-col cols="12" sm="4" class="d-flex align-center">
                  <v-btn color="primary" variant="text" prepend-icon="mdi-refresh" @click="fetchItems">刷新数据</v-btn>
                  <v-btn color="error" variant="text" prepend-icon="mdi-filter-remove" @click="resetFilters">重置筛选</v-btn>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <!-- 物品列表表格 -->
          <v-data-table
            :headers="headers"
            :items="filteredItems"
            :loading="loading"
            :items-per-page="10"
            :search="search"
            :no-data-text="loading ? '加载中...' : '没有找到匹配的物品'"
          >
            <!-- 自定义状态显示 -->
            <template v-slot:item.status="{ item }">
              <v-chip
                :color="getStatusColor(item.status)"
                size="small"
                class="text-white"
              >
                {{ getStatusText(item.status) }}
              </v-chip>
            </template>

            <!-- 自定义日期显示 -->
            <template v-slot:item.created_at="{ item }">
              {{ formatDate(item.created_at) }}
            </template>

            <!-- 操作按钮 -->
            <template v-slot:item.actions="{ item }">
              <div class="d-flex">
                <v-btn 
                  icon 
                  color="info" 
                  variant="text" 
                  size="small"
                  @click="openItemDialog(item)"
                  class="mr-1"
                >
                  <v-icon>mdi-pencil</v-icon>
                  <v-tooltip activator="parent" location="top">编辑</v-tooltip>
                </v-btn>
                <v-btn 
                  icon 
                  color="error" 
                  variant="text" 
                  size="small"
                  @click="confirmDelete(item)"
                  class="mr-1"
                >
                  <v-icon>mdi-delete</v-icon>
                  <v-tooltip activator="parent" location="top">删除</v-tooltip>
                </v-btn>
                <v-btn 
                  icon 
                  color="success" 
                  variant="text" 
                  size="small"
                  @click="showQRCode(item)"
                >
                  <v-icon>mdi-qrcode</v-icon>
                  <v-tooltip activator="parent" location="top">二维码</v-tooltip>
                </v-btn>
              </div>
            </template>
          </v-data-table>
        </div>

        <!-- 其他标签页内容 -->
        <div v-if="currentTab === 'qrcodes'">
          <h2 class="text-h4 mb-4">生成二维码</h2>
          <p>此功能正在开发中...</p>
        </div>
        
        <div v-if="currentTab === 'settings'">
          <h2 class="text-h4 mb-4">用户设置</h2>
          
          <!-- 添加缓存状态组件 -->
          <CacheStatus />
          
          <v-divider class="my-4"></v-divider>
          
          <p>其他设置功能正在开发中...</p>
        </div>
        
        <div v-if="currentTab === 'about'">
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
              <div class="text-caption text-right">版本: 1.0.0</div>
            </v-card-text>
          </v-card>
        </div>
      </v-container>
    </v-main>

    <!-- 物品编辑对话框 -->
    <v-dialog v-model="itemDialog" max-width="600px">
      <v-card>
        <v-card-title class="text-h5 bg-primary text-white pa-4">
          {{ editItem.id ? '编辑物品' : '添加新物品' }}
        </v-card-title>
        <v-card-text class="pt-4">
          <v-form ref="itemForm" v-model="formValid">
            <v-container>
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    v-model="editItem.name"
                    label="物品名称"
                    required
                    :rules="[v => !!v || '物品名称不能为空']"
                    variant="outlined"
                    density="comfortable"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="editItem.key"
                    label="物品标识码"
                    required
                    :rules="[v => !!v || '标识码不能为空']"
                    :disabled="!!editItem.id"
                    variant="outlined"
                    density="comfortable"
                    hint="用于生成二维码的唯一标识，创建后不可修改"
                    persistent-hint
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="editItem.phone"
                    label="联系电话"
                    required
                    :rules="[
                      v => !!v || '联系电话不能为空',
                      v => /^\d{11}$/.test(v) || '请输入有效的11位手机号码'
                    ]"
                    variant="outlined"
                    density="comfortable"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="editItem.icon"
                    label="图标 (可选)"
                    placeholder="例如：mdi-laptop"
                    variant="outlined"
                    density="comfortable"
                    hint="Material Design Icons的图标名称"
                    persistent-hint
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-select
                    v-model="editItem.status"
                    :items="[
                      { title: '正常', value: 'ok' },
                      { title: '丢失', value: 'lost' }
                    ]"
                    label="物品状态"
                    required
                    variant="outlined"
                    density="comfortable"
                  ></v-select>
                </v-col>
                <v-col cols="12" v-if="editItem.status === 'lost'">
                  <v-textarea
                    v-model="editItem.context"
                    label="丢失上下文"
                    variant="outlined"
                    rows="3"
                    placeholder="请描述物品丢失的时间、地点等信息..."
                  ></v-textarea>
                </v-col>
              </v-row>
            </v-container>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" variant="text" @click="itemDialog = false">取消</v-btn>
          <v-btn 
            color="primary" 
            @click="saveItem" 
            :loading="saving"
            :disabled="!formValid"
          >
            保存
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 确认删除对话框 -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title class="text-h5 bg-error text-white pa-4">确认删除</v-card-title>
        <v-card-text class="pt-4">
          <p class="text-body-1">您确定要删除物品 "{{ deleteItem?.name || '' }}" 吗？</p>
          <p class="text-caption text-error">此操作不可逆，删除后将无法恢复。</p>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" variant="text" @click="deleteDialog = false">取消</v-btn>
          <v-btn 
            color="error" 
            @click="deleteItemConfirm" 
            :loading="deleting"
          >
            确认删除
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 二维码展示对话框 -->
    <v-dialog v-model="qrDialog" max-width="350">
      <v-card>
        <v-card-title class="text-h5 bg-primary text-white pa-4">物品二维码</v-card-title>
        <v-card-text class="text-center pa-4">
          <div v-if="selectedItem">
            <p class="text-h6 mb-2">{{ selectedItem.name }}</p>
            <p class="text-subtitle-2 mb-4">ID: {{ selectedItem.key }}</p>
            <!-- 二维码图片 -->
            <div class="bg-white pa-4 d-inline-block rounded">
              <img 
                :src="getQRCodeUrl(selectedItem.key)" 
                alt="QR Code" 
                width="200" 
                height="200"
              />
            </div>
            <p class="text-caption mt-3">请使用屏幕截图或保存图片功能保存二维码</p>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" variant="text" @click="qrDialog = false">关闭</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
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
import CacheStatus from '@/components/CacheStatus.vue';

export default {
  name: 'AdminView',
  components: {
    CacheStatus
  },
  data() {
    return {
      // 界面控制
      drawer: false,
      currentTab: 'dashboard',
      loading: false,
      search: '',
      statusFilter: 'all',
      
      // 物品管理
      items: [],
      editItem: {
        id: null,
        key: '',
        name: '',
        icon: '',
        phone: '',
        status: 'ok',
        context: ''
      },
      defaultItem: {
        id: null,
        key: '',
        name: '',
        icon: '',
        phone: '',
        status: 'ok',
        context: ''
      },
      
      // 对话框控制
      itemDialog: false,
      deleteDialog: false,
      qrDialog: false,
      saving: false,
      deleting: false,
      formValid: false,
      
      // 选中的物品和删除项
      selectedItem: null,
      deleteItem: null,
      
      // 表格配置
      headers: [
        { title: 'ID', key: 'id', sortable: true },
        { title: '物品名称', key: 'name', sortable: true },
        { title: '标识码', key: 'key', sortable: true },
        { title: '状态', key: 'status', sortable: true },
        { title: '创建时间', key: 'created_at', sortable: true },
        { title: '操作', key: 'actions', sortable: false }
      ],
      
      statusOptions: [
        { title: '全部状态', value: 'all' },
        { title: '正常', value: 'ok' },
        { title: '丢失', value: 'lost' }
      ],
      
      // 仪表盘数据
      itemStats: {
        total: 0,
        normal: 0,
        lost: 0,
        scans: 0
      }
    }
  },
  
  computed: {
    /**
     * 过滤后的物品列表
     * 
     * 根据搜索文本和状态筛选条件过滤物品列表
     * @returns {Array} 过滤后的物品数组
     */
    filteredItems() {
      let result = [...this.items];
      
      // 应用状态筛选
      if (this.statusFilter !== 'all') {
        result = result.filter(item => item.status === this.statusFilter);
      }
      
      return result;
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
     * 从API获取所有物品数据并更新统计信息
     */
    async fetchItems() {
      try {
        this.loading = true;
        
        const data = await apiService.get('/api/admin/items');
        
        if (data.code === 0 && Array.isArray(data.data)) {
          this.items = data.data;
          this.updateStats();
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
      } finally {
        this.loading = false;
      }
    },
    
    /**
     * 更新统计信息
     * 
     * 根据物品列表计算各种统计数据
     */
    updateStats() {
      // 计算物品总数
      this.itemStats.total = this.items.length;
      
      // 计算正常和丢失物品数量
      this.itemStats.normal = this.items.filter(item => item.status === 'ok').length;
      this.itemStats.lost = this.items.filter(item => item.status === 'lost').length;
      
      // 假设扫描次数是从物品中累计的一个属性，如果没有可以模拟一个值
      // this.itemStats.scans = this.items.reduce((sum, item) => sum + (item.scans || 0), 0) || 42;
    },
    
    /**
     * 计算百分比
     * 
     * @param {string} type - 物品类型（normal或lost）
     * @returns {number} 百分比值
     */
    getPercentage(type) {
      if (this.itemStats.total === 0) return 0;
      return Math.round((this.itemStats[type] / this.itemStats.total) * 100);
    },
    
    /**
     * 打开物品对话框
     * 
     * @param {Object|null} item - 要编辑的物品，为null时表示添加新物品
     */
    openItemDialog(item = null) {
      if (item) {
        this.editItem = JSON.parse(JSON.stringify(item)); // 深拷贝
      } else {
        this.editItem = JSON.parse(JSON.stringify(this.defaultItem));
        // 为新物品生成一个随机标识码
        this.editItem.key = this.generateRandomKey();
      }
      this.$nextTick(() => {
        if (this.$refs.itemForm) {
          this.$refs.itemForm.resetValidation();
        }
      });
      this.itemDialog = true;
    },
    
    /**
     * 保存物品
     * 
     * 根据是否有ID决定是添加新物品还是更新现有物品
     */
    async saveItem() {
      if (!this.formValid) return;
      
      try {
        this.saving = true;
        let data;
        
        if (this.editItem.id) {
          // 更新现有物品
          const params = new URLSearchParams();
          const { id, key, name, icon, phone, status, context } = this.editItem;
          
          params.append('id', id);
          params.append('key', key);
          params.append('name', name);
          params.append('icon', icon || '');
          params.append('phone', phone);
          params.append('status', status);
          
          // 只有在状态为lost且有context时，才添加context参数
          if (status === 'lost' && context) {
            params.append('context', context);
          }
          
          data = await apiService.patch(`/api/admin/items?${params.toString()}`, '');
          
        } else {
          // 添加新物品
          const params = new URLSearchParams();
          const { key, name, icon, phone } = this.editItem;
          
          params.append('key', key);
          params.append('name', name);
          params.append('icon', icon || '');
          params.append('phone', phone);
          
          data = await apiService.post(`/api/admin/items?${params.toString()}`, '');
        }
        
        if (data.code !== 0) {
          throw new Error(data.msg || '保存物品失败');
        }
        
        this.$nextTick(() => {
          this.$root.$emit('show-toast', {
            color: 'success',
            message: this.editItem.id ? '物品更新成功' : '物品添加成功'
          });
        });
        
        this.itemDialog = false;
        this.fetchItems(); // 刷新物品列表
        
      } catch (error) {
        console.error('保存物品错误:', error);
        this.$nextTick(() => {
          this.$root.$emit('show-toast', {
            color: 'error',
            message: error.message || '保存物品失败'
          });
        });
      } finally {
        this.saving = false;
      }
    },
    
    /**
     * 确认删除物品
     * 
     * @param {Object} item - 要删除的物品
     */
    confirmDelete(item) {
      this.deleteItem = item;
      this.deleteDialog = true;
    },
    
    /**
     * 确认删除物品
     */
    async deleteItemConfirm() {
      if (!this.deleteItem || !this.deleteItem.id) return;
      
      try {
        this.deleting = true;
        
        const data = await apiService.delete(`/api/admin/items?id=${encodeURIComponent(this.deleteItem.id)}`);
        
        if (data.code !== 0) {
          throw new Error(data.msg || '删除物品失败');
        }
        
        this.$nextTick(() => {
          this.$root.$emit('show-toast', {
            color: 'success',
            message: '物品已成功删除'
          });
        });
        
        this.deleteDialog = false;
        this.fetchItems(); // 刷新物品列表
        
      } catch (error) {
        console.error('删除物品错误:', error);
        this.$nextTick(() => {
          this.$root.$emit('show-toast', {
            color: 'error',
            message: error.message || '删除物品失败'
          });
        });
      } finally {
        this.deleting = false;
      }
    },
    
    /**
     * 显示二维码
     * 
     * @param {Object} item - 要显示二维码的物品
     */
    showQRCode(item) {
      this.selectedItem = item;
      this.qrDialog = true;
    },
    
    /**
     * 获取二维码URL
     * 
     * @param {string} key - 物品标识码
     * @returns {string} 二维码图片URL
     */
    getQRCodeUrl(key) {
      // 使用QR Server API生成二维码
      const currentUrl = window.location.origin;
      const foundUrl = `${currentUrl}/found?key=${encodeURIComponent(key)}`;
      return `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(foundUrl)}`;
    },
    
    /**
     * 生成随机标识码
     * 
     * @returns {string} 随机生成的标识码
     */
    generateRandomKey() {
      // 生成一个8位的随机字母数字组合
      const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
      let result = '';
      for (let i = 0; i < 8; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length));
      }
      return result;
    },
    
    /**
     * 获取状态对应的颜色
     * 
     * @param {string} status - 物品状态
     * @returns {string} 对应的颜色名称
     */
    getStatusColor(status) {
      const statusMap = {
        ok: "success",
        lost: "error",
        default: "grey"
      };
      return statusMap[status] || statusMap.default;
    },
    
    /**
     * 获取状态对应的文本
     * 
     * @param {string} status - 物品状态
     * @returns {string} 对应的状态文本
     */
    getStatusText(status) {
      const statusMap = {
        ok: "正常",
        lost: "丢失",
        default: "未知"
      };
      return statusMap[status] || statusMap.default;
    },
    
    /**
     * 格式化日期显示
     * 
     * @param {string} create_time - 日期字符串
     * @returns {string} 格式化的日期文本
     */
    formatDate(dateStr) {
      if (!dateStr) return "未知时间";
      
      try {
        const date = new Date(dateStr);
        return new Intl.DateTimeFormat('zh-CN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit'
        }).format(date);
      } catch (e) {
        return dateStr;
      }
    },
    
    /**
     * 重置所有筛选条件
     */
    resetFilters() {
      this.search = '';
      this.statusFilter = 'all';
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

/* 确保数据表格在移动设备上响应式滚动 */
@media (max-width: 768px) {
  .v-data-table {
    overflow-x: auto;
  }
}
</style>