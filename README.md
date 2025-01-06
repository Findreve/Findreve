<!--
 * @Author: 于小丘 海枫
 * @Date: 2024-11-29 20:06:02
 * @LastEditors: Yuerchu admin@yuxiaoqiu.cn
 * @LastEditTime: 2024-11-29 20:28:54
 * @FilePath: /Findreve/README.md
 * @Description: Findreve
 * 
 * Copyright (c) 2018-2024 by 于小丘Yuerchu, All Rights Reserved. 
-->

<h1 align="center">
  <br>
  <a href="https://find.yxqi.cn" alt="logo" ><img src="./static/Findreve.png" width="150"/></a>
  <br>
  Findreve (Community)
  <br>
</h1>
<h4 align="center">标记、追踪与找回 —— 就这么简单。</h4>
<h4 align="center">Track, Tag, and Retrieve – Simplifying Item Recovery.</h4>

<p align="center">
  <a href="https://www.yxqi.cn">Homepage</a> •
  <a href="https://find.yxqi.cn">Demo</a> •
  <a href="https://findreve.yxqi.cn">Documents</a> •
  <a href="https://github.com/Findreve/Findreve/releases">Download</a> •
  <a href="#License">License</a>
</p>

## 介绍 Introduction
Findreve 是一款强大且直观的解决方案，旨在帮助您管理个人物品，并确保丢失后能够安全找回。每个物品都会被分配一个 `唯一 ID` ，并生成一个 `安全链接` ，可轻松嵌入到 `二维码` 或 `NFC 标签` 中。当扫描该代码时，会将拾得者引导至一个专门的网页，上面显示物品详情和您的联系信息，既保障隐私又便于沟通。无论您是在管理个人物品还是专业资产，Findreve 都能以高效、简便的方式弥合丢失与找回之间的距离。

Findreve-Pro is a powerful and intuitive solution, an enhanced version of Findreve, designed
to help you manage your personal items and ensure their safe recovery in case of loss. Each
item is assigned a "unique ID" and a "secure link" is generated, which can be easily embedded
into a "QR code" or "NFC tag". When this code is scanned, the finder is directed to a
dedicated webpage displaying the item's details and your contact information, ensuring both
privacy and ease of communication. Whether you are managing personal items or professional
assets, Findreve bridges the gap between loss and recovery in an efficient and simple way.

## 安装 Install
你需要安装Python 3.8 以上的版本。然后，clone 本仓库到您的服务器并解压，然后安装下面的依赖：

You need to have Python 3.8 or higher installed on your server. Then, clone this repository
to your server and install the required dependencies:

- **NiceGUI**: `pip install nicegui==2.5.0`
- **aiosqlite**: `pip install aiosqlite`
- **QRCode**: `pip install QRCode`

## 启动 Launch
使用下面的命令来启动 Findreve:

Run the following command to start Findreve:
> Python main.py

启动后， Findreve 会在程序的根目录自动创建 SQLite 数据库，并在
终端显示管理员账号密码。请注意，账号密码仅显示一次，请注意保管。

Upon launch, Findreve will create a SQLite database in the project's root directory and
display the administrator's account and password in the console.

## 技术栈 Stacks
- Nicegui

## 许可证 License
此仓库的 Findreve 是社区版，完全免费，基于 GPLv3 协议。

Open Source Free Version: Licensed under the `GPLv3`.

基于赞助的专业版：基于您的赞助，您可获得附加功能和源代码的版本，允许进一步开发用于个人或内部使用。然而，不允许重新分发修改后的或原始的源代码。

Donation-Based Premium Version: By making a donation, you can access a version with additional features and source code, which allows further development for personal or internal use. However, redistribution of the modified or original source code is not permitted.