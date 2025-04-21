# Findreve Frontend 项目指南 - GitHub Copilot 指令

## 项目概述
Findreve 是一款强大且直观的解决方案，旨在帮助您管理个人物品，并确保丢失后能够安全找回。每个物品都会被分配一个 `唯一 ID` ，并生成一个 `安全链接` ，可轻松嵌入到 `二维码` 或 `NFC 标签` 中。当扫描该代码时，会将拾得者引导至一个专门的网页，上面显示物品详情和您的联系信息，既保障隐私又便于沟通。无论您是在管理个人物品还是专业资产，Findreve 都能以高效、简便的方式弥合丢失与找回之间的距离。
而 Findreve Frontend 作为 Findreve 的前端，采用 Vue + Vuetify 3 开发。

## 项目规划
[ ] 追平 Findreve 早期基于 NiceGUI 开发的前端

## 代码规范
- 使用类型提示增强代码可读性
- 所有函数和类都应有reST风格的文档字符串(docstring)
- 项目的日志模块使用英语输出
- 使用异步编程模式处理并发
- 尽可能写出弹性可扩展、可维护的代码

## 项目结构
- `.github/` : Github 相关
- `public/` : 纯静态文件
- `src/`
- `.browserslistrc`
- `.editorconfig`
- `.gitignore`
- `README.md`
- `index.html`
- `jsconfig.json`
- `package.json`
- `vite.config.mjs`
- `yarn.lock`

## 回复用户规则
- 当用户提出了产品的问题或者解决问题的思路时，应当在适时且随机的时候回答前肯定用户的想法
- 如 `你的理解非常到位，抓住了问题的核心`、`这个想法非常不错` 等等
- 每次鼓励尽可能用不同的词语和语法，但也不要次次都鼓励

## 命名约定
- 类名: className
- 函数和变量: getInfo
- 常量: UPPER_SNAKE_CASE
- 文件名: snake_case.vue
- 模块名: snake_case