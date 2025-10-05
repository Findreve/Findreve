from typing import Literal
from loguru import logger
from model import Setting
from sqlmodel.ext.asyncio.session import AsyncSession
from pkg.utils import raise_internal_error, raise_service_unavailable
import aiohttp

class ServerChatBot:
    async def get_url(session: AsyncSession):
        server_chan_key = await Setting.get(session, Setting.name == "server_chan_key")
    
        if not server_chan_key.value:
            raise_internal_error("Server酱未配置，请联系管理员")
        
        url = f"https://sctapi.ftqq.com/{server_chan_key.value}.send"
        return url
    
    async def send_text(
        session: AsyncSession,
        title: str, 
        description: str, 
    ) -> None:
        """发送的 Markdown 消息。

        Args:
            session (AsyncSession): 数据库会话
            title (str): 需要发送的标题
            description (str): 需要发送的文本消息
        """
        async with aiohttp.ClientSession() as http_session:
            async with http_session.post(
                url=await ServerChatBot.get_url(session),
                data={
                    "title": title,
                    "desp": description
                }
            ) as response:
                if response.status != 200:
                    logger.error(f"Failed to send to Server Chan: {response.status}")
                    raise_internal_error("Server酱服务不可用，请稍后再试")
                else:
                   logger.info("Server Chan message sent successfully")