# 组件

此文件夹中的 Vue 模板文件会被自动导入。

## 🚀 使用方法

自动导入功能由 [unplugin-vue-components](https://github.com/unplugin/unplugin-vue-components) 实现。该插件会自动导入 `src/components` 目录下创建的 `.vue` 文件，并将它们注册为全局组件。这意味着你可以在应用程序中直接使用任何组件而无需手动导入。

以下示例假设存在一个位于 `src/components/MyComponent.vue` 的组件：

```vue
<template>
  <div>
    <MyComponent />
  </div>
</template>

<script lang="ts" setup>
  //
</script>
```

当模板渲染时，组件的导入语句会被自动内联，最终呈现为：

```vue
<template>
  <div>
    <MyComponent />
  </div>
</template>

<script lang="ts" setup>
  import MyComponent from '@/components/MyComponent.vue'
</script>
```