"""
# 初始化设置表数据
            async with db.execute("SELECT name FROM fr_settings WHERE name = 'version'") as cursor:
                if not await cursor.fetchone():
                    await db.execute(
                        "INSERT INTO fr_settings (type, name, value) VALUES (?, ?, ?)",
                        ('string', 'version', '1.0.0')
                    )
                    logging.info("插入初始版本信息: version 1.0.0")

            async with db.execute("SELECT name FROM fr_settings WHERE name = 'ver'") as cursor:
                if not await cursor.fetchone():
                    await db.execute(
                        "INSERT INTO fr_settings (type, name, value) VALUES (?, ?, ?)", 
                        ('int', 'ver', '1')
                    )
                    logging.info("插入初始版本号: ver 1")

            async with db.execute("SELECT name FROM fr_settings WHERE name = 'account'") as cursor:
                if not await cursor.fetchone():
                    account = 'admin@yuxiaoqiu.cn'
                    await db.execute(
                        "INSERT INTO fr_settings (type, name, value) VALUES (?, ?, ?)", 
                        ('string', 'account', account)
                    )
                    logging.info(f"插入初始账号信息: {account}")
                    print(f"账号: {account}")

            async with db.execute("SELECT name FROM fr_settings WHERE name = 'password'") as cursor:
                if not await cursor.fetchone():
                    password = tool.generate_password()
                    hashed_password = tool.hash_password(password)
                    await db.execute(
                        "INSERT INTO fr_settings (type, name, value) VALUES (?, ?, ?)",
                        ('string', 'password', hashed_password)
                    )
                    logging.info("插入初始密码信息")
                    print(f"密码（请牢记，后续不再显示）: {password}")
            
            async with db.execute("SELECT name FROM fr_settings WHERE name = 'SECRET_KEY'") as cursor:
                if not await cursor.fetchone():
                    secret_key = tool.generate_password(64)
                    await db.execute(
                        "INSERT INTO fr_settings (type, name, value) VALUES (?, ?, ?)",
                        ('string', 'SECRET_KEY', secret_key)
                    )
                    logging.info("插入初始密钥信息")
            
            await db.commit()
            logging.info("数据库初始化完成并提交更改")
"""