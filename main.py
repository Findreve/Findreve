from loguru import logger

# 导入配置模块
from pkg.env import load_config
from pkg.logger import setup_logging
from pkg.startup import startup

# 加载配置
host, port, debug = load_config()

# 配置日志
setup_logging(debug)

# 记录启动信息
logger.info(f"Debug mode: {'enabled' if debug else 'disabled'}")
logger.info(f"Starting Findreve on http://{host}:{port}")

# 导入应用实例
from app import app

# 执行启动流程
startup(app)

# 作为主程序启动时
if __name__ == '__main__':
    import uvicorn

    # 启动服务器
    uvicorn.run(
        'app:app',
        host=host,
        port=port,
        log_config=None,  # 禁用 uvicorn 默认的日志配置，使用 loguru
        reload=debug,  # 调试模式下启用热重载
    )