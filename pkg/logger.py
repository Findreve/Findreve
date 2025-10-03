"""
日志配置模块

负责配置 loguru 和接管标准库的日志
"""

import sys
import logging
from loguru import logger


class InterceptHandler(logging.Handler):
    """
    拦截标准库的日志并转发到 loguru
    """
    def emit(self, record: logging.LogRecord) -> None:
        # 获取对应的 loguru 级别
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # 查找调用者的帧
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging(debug: bool = False) -> None:
    """
    配置日志系统
    
    :param debug: 是否启用调试模式
    """
    # 配置 loguru
    # 移除默认的 handler
    logger.remove()

    # 根据 DEBUG 模式配置不同的日志级别和格式
    if debug:
        logger.add(
            sys.stderr,
            level="DEBUG"
        )
    else:
        logger.add(
            sys.stderr,
            level="INFO"
        )

    # 接管 uvicorn 的日志
    logging.getLogger("uvicorn").handlers = [InterceptHandler()]
    logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
    logging.getLogger("uvicorn.error").handlers = [InterceptHandler()]

    # 接管 SQLAlchemy 的日志
    logging.getLogger("sqlalchemy.engine").handlers = [InterceptHandler()]
    logging.getLogger("sqlalchemy.pool").handlers = [InterceptHandler()]

    # 设置日志级别
    if debug:
        logging.getLogger("uvicorn").setLevel(logging.DEBUG)
        logging.getLogger("uvicorn.access").setLevel(logging.DEBUG)
        logging.getLogger("uvicorn.error").setLevel(logging.DEBUG)
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
        logging.getLogger("sqlalchemy.pool").setLevel(logging.DEBUG)
    else:
        logging.getLogger("uvicorn").setLevel(logging.INFO)
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
        logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
        logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
        logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)
