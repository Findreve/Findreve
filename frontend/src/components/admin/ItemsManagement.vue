<script setup>
import { ref, computed, watch } from 'vue'
import apiService from '@/services/api_service'

const props = defineProps({
  items: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['refresh'])

// 界面控制
const loading = ref(false)
const search = ref('')
const statusFilter = ref('all')

// 物品管理
const editItem = ref({
  id: null,
  key: '',
  name: '',
  icon: '',
  phone: '',
  status: 'ok',
  context: ''
})
const defaultItem = {
  id: null,
  key: '',
  name: '',
  icon: '',
  phone: '',
  status: 'ok',
  context: ''
}

// 对话框控制
const itemDialog = ref(false)
const deleteDialog = ref(false)
const qrDialog = ref(false)
const saving = ref(false)
const deleting = ref(false)
const formValid = ref(false)

// 选中的物品和删除项
const selectedItem = ref(null)
const deleteItem = ref(null)

// 表格配置
const headers = [
  { title: 'ID', key: 'id', sortable: true },
  { title: '物品名称', key: 'name', sortable: true },
  { title: '标识码', key: 'key', sortable: true },
  { title: '状态', key: 'status', sortable: true },
  { title: '创建时间', key: 'created_at', sortable: true },
  { title: '操作', key: 'actions', sortable: false }
]

const statusOptions = [
  { title: '全部状态', value: 'all' },
  { title: '正常', value: 'ok' },
  { title: '丢失', value: 'lost' }
]

/**
 * 过滤后的物品列表
 */
const filteredItems = computed(() => {
  let result = [...props.items]
  if (statusFilter.value !== 'all') {
    result = result.filter(item => item.status === statusFilter.value)
  }
  return result
})

/**
 * 打开物品对话框
 */
const openItemDialog = (item = null) => {
  editItem.value = item ? JSON.parse(JSON.stringify(item)) : JSON.parse(JSON.stringify(defaultItem))
  if (!item) {
    editItem.value.key = generateRandomKey()
  }
  itemDialog.value = true
}

/**
 * 保存物品
 */
const saveItem = async () => {
  if (!formValid.value) return
  
  try {
    saving.value = true
    let data
    
    if (editItem.value.id) {
      const params = new URLSearchParams()
      const { id, key, name, icon, phone, status, context } = editItem.value
      
      params.append('id', id)
      params.append('key', key)
      params.append('name', name)
      params.append('icon', icon || '')
      params.append('phone', phone)
      params.append('status', status)
      
      if (status === 'lost' && context) {
        params.append('context', context)
      }
      
      data = await apiService.patch(`/api/admin/items?${params.toString()}`, '')
    } else {
      const params = new URLSearchParams()
      const { key, name, icon, phone } = editItem.value
      
      params.append('key', key)
      params.append('name', name)
      params.append('icon', icon || '')
      params.append('phone', phone)
      
      data = await apiService.post(`/api/admin/items?${params.toString()}`, '')
    }
    
    if (data.code !== 0) {
      throw new Error(data.msg || '保存物品失败')
    }
    
    itemDialog.value = false
    emit('refresh')
  } catch (error) {
    console.error('保存物品错误:', error)
  } finally {
    saving.value = false
  }
}

/**
 * 确认删除物品
 */
const confirmDelete = (item) => {
  deleteItem.value = item
  deleteDialog.value = true
}

/**
 * 确认删除物品
 */
const deleteItemConfirm = async () => {
  if (!deleteItem.value?.id) return
  
  try {
    deleting.value = true
    const data = await apiService.delete(`/api/admin/items?id=${encodeURIComponent(deleteItem.value.id)}`)
    
    if (data.code !== 0) {
      throw new Error(data.msg || '删除物品失败')
    }
    
    deleteDialog.value = false
    emit('refresh')
  } catch (error) {
    console.error('删除物品错误:', error)
  } finally {
    deleting.value = false
  }
}

/**
 * 显示二维码
 */
const showQRCode = (item) => {
  selectedItem.value = item
  qrDialog.value = true
}

/**
 * 获取二维码URL
 */
const getQRCodeUrl = (key) => {
  const currentUrl = window.location.origin
  const foundUrl = `${currentUrl}/found?key=${encodeURIComponent(key)}`
  return `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(foundUrl)}`
}

/**
 * 生成随机标识码
 */
const generateRandomKey = () => {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  let result = ''
  for (let i = 0; i < 8; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  return result
}

/**
 * 获取状态对应的颜色
 */
const getStatusColor = (status) => {
  const statusMap = {
    ok: "success",
    lost: "error",
    default: "grey"
  }
  return statusMap[status] || statusMap.default
}

/**
 * 获取状态对应的文本
 */
const getStatusText = (status) => {
  const statusMap = {
    ok: "正常",
    lost: "丢失",
    default: "未知"
  }
  return statusMap[status] || statusMap.default
}

/**
 * 格式化日期显示
 */
const formatDate = (dateStr) => {
  if (!dateStr) return "未知时间"
  try {
    const date = new Date(dateStr)
    return new Intl.DateTimeFormat('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date)
  } catch (e) {
    return dateStr
  }
}

/**
 * 重置所有筛选条件
 */
const resetFilters = () => {
  search.value = ''
  statusFilter.value = 'all'
}
</script>

<template>
  <div>
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
            <v-btn color="primary" variant="text" prepend-icon="mdi-refresh" @click="refreshItems">刷新数据</v-btn>
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
  </div>
</template>

<style scoped>
/* 确保数据表格在移动设备上响应式滚动 */
@media (max-width: 768px) {
  .v-data-table {
    overflow-x: auto;
  }
}
</style>
