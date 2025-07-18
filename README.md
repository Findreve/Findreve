<h1 align="center">
  <br>
  <a href="https://find.yxqi.cn" alt="logo" ><img src="./docs/Findreve.png" width="150"/></a>
  <br>
  Findreve (Community)
  <br>
</h1>
<h4 align="center">标记、追踪与找回 —— 就这么简单。</h4>
<h4 align="center">Track, Tag, and Retrieve – Simplifying Item Recovery.</h4>

<p align="center">
  <a href="https://www.yxqi.cn">Homepage</a> •
  <a href="https://find.yxqi.cn">Demo</a> •
  <a href="./CHANGELOG.md">ChangeLog</a> •
  <a href="https://github.com/Findreve/Findreve/releases">Download</a> •
  <a href="#License">License</a>
</p>

## 介绍 Introduction
Findreve 是一款强大且直观的解决方案，旨在帮助您管理个人物品，并确保丢失后能够安全找回。
每个物品都会被分配一个 `唯一 ID` ，并生成一个 `安全链接` ，可轻松嵌入到 `二维码` 或 `NFC 标签` 中。
当扫描该代码时，会将拾得者引导至一个专门的网页，上面显示物品详情和您的联系信息，既保障隐私又便于沟通。
无论您是在管理个人物品还是专业资产，Findreve 都能以高效、简便的方式弥合丢失与找回之间的距离。
同时，Findreve 还是一个模板项目，对新人开发者较为友好，你可以通过 Findreve 学习到后端的路由操作、数据与数据库管理、
JWT 与 OAuth2 认证鉴权，还有基于 Vue 前端的各种支持。它还是一个脚手架，能让你通过这个脚手架二改出功能更加完整甚至丰富的系统。

Findreve is a powerful and intuitive solution, an enhanced version of Findreve, designed
to help you manage your personal items and ensure their safe recovery in case of loss. Each
item is assigned a "unique ID" and a "secure link" is generated, which can be easily embedded
into a "QR code" or "NFC tag". When this code is scanned, the finder is directed to a
dedicated webpage displaying the item's details and your contact information, ensuring both
privacy and ease of communication. Whether you are managing personal items or professional
assets, Findreve bridges the gap between loss and recovery in an efficient and simple way.

## 快速开始
在 [最新发行版](https://github.com/Findreve/Findreve/releases/latest) 中下载，然后按照要求启动即可。

使用下面的命令来启动 Findreve:

Run the following command to start Findreve:

> python main.py

您可能需要准备 Findreve 的前端文件才可正常启动。

<!--

```bash
# Windows
findreve.exe

# Linux
# 解压
tar -zxvf findreve_VERSION_OS_ARCH.tar.gz
# 赋予执行权限
chmod +x ./findreve
# 启动 Findreve
./findreve
```
-->

启动后， Findreve 会在程序的根目录自动创建 SQLite 数据库，并在
终端显示管理员账号密码。请注意，账号密码仅显示一次，请注意保管。
账号默认为 `admin@yuxiaoqiu.cn`

Upon launch, Findreve will create a SQLite database in the project's root directory and
display the administrator's account and password in the console.

## 构建
你需要安装Python 3.8 以上的版本。然后，clone 本仓库到您的服务器并解压，然后安装下面的依赖：

You need to have Python 3.8 or higher installed on your server. Then, clone this repository
to your server and install the required dependencies:

> `pip install -r requirements.txt`

然后进入 `frontend` 文件夹，编译前端文件：

```bash
# 安装依赖
yarn install

# 编译
yarn build
```

编译完成后，将 `dist` 文件夹拷贝到 Findreve 根目录。

## 技术栈 Stacks

- frontend: `Vue.js` + `Vuetify`
- Backend: `FastAPI`

## 许可证 License
此仓库的 Findreve 是社区版，完全免费，基于 GPLv3 协议。

Open Source Free Version: Licensed under the `GPLv3`.

基于赞助的专业版：基于您的赞助，您可获得附加功能和源代码的版本，允许进一步开发用于个人或内部使用。
然而，不允许重新分发修改后的或原始的源代码。

Donation-Based Premium Version: By making a donation, you can access a version with additional features
and source code, which allows further development for personal or internal use. However, redistribution
of the modified or original source code is not permitted.