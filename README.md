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

<p style="text-align: center; font-size: 32px;">Findreve</p>

***

<p style="text-align: center;">Track, Tag, and Retrieve – Simplifying Item Recovery.</p>

Findreve is a powerful yet intuitive solution designed to help you manage your belongings and ensure their safe return if lost. Each item is assigned a unique ID and generates a secure link, easily embedded into a QR code or NFC tag. When scanned, the code directs finders to a dedicated webpage displaying item details and your contact information, ensuring privacy and ease of communication. Whether you’re managing personal belongings or professional assets, Findreve bridges the gap between lost and found with efficiency and simplicity.

## Install
`Findreve` is a Python-based application. You need to have Python 3.8 or higher installed on your server. Then, clone this repository to your server and install the required dependencies:

NiceGUI: `pip3 install nicegui==2.5.0`

aiosqlite: `pip3 install aiosqlite`

## Launch
Run the following command to start Findreve:

```shell
python3 main.py
```

Upon launch, Findreve will create a SQLite database in the project's root directory and display the administrator's account and password in the console.

## License
Findreve is available in two versions:

Open Source Free Version: Licensed under the `GPLv3`.

Donation-Based Premium Version: By making a donation, you can access a version with additional features and source code, which allows further development for personal or internal use. However, redistribution of the modified or original source code is not permitted.