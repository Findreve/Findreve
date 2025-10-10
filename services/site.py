"""
站点信息服务。
"""

from pkg import conf


async def get_version() -> str:
    """
    返回站点版本信息。
    """
    return conf.VERSION
