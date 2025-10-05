from typing import Literal
from loguru import logger
from model import Setting
from sqlmodel.ext.asyncio.session import AsyncSession
from pkg.utils import raise_internal_error, raise_service_unavailable
import aiohttp

webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send"

class WeChatBot:
    async def get_key(session: AsyncSession):
        key = await Setting.get(session, Setting.name == "wechat_bot_key")
    
        if not key.value:
            raise_internal_error("企业微信机器人未配置，请联系管理员")
        return key.value
    
    async def send_text(
        session: AsyncSession, 
        text: str, 
        mentioned_all: bool = False,
        mentioned_list: list[str] = [],
        mentioned_mobile_list: list[str] = []
    ) -> None:
        """发送文本类型的消息。

        Args:
            session (AsyncSession): 数据库会话
            text (str): 需要发送的文本消息
            mentioned_all (bool, optional): 是否提及所有人 Defaults to False.
            mentioned_list (list[str], optional): 提及的用户列表 Defaults to [].
            mentioned_mobile_list (list[str], optional): 提及的手机号码列表 Defaults to [].
        """
        key = await WeChatBot.get_key(session)
        
        async with aiohttp.ClientSession() as http_session:
            async with http_session.post(
                url=f"{webhook_url}?key={key}",
                json={
                    "msgtype": "text",
                    "text": {
                        "content": text
                    },
                    "mentioned_list": ["@all"] if mentioned_all else mentioned_list,
                    "mentioned_mobile_list": ["@all"] if mentioned_all else mentioned_mobile_list
                }
            ) as response:
                if response.status != 200:
                    logger.error(f"Failed to send WeChat message: {response.status}")
                    raise_internal_error("企业微信机器人服务不可用，请稍后再试")
                else:
                    resp_json = await response.json()
                    if resp_json.get("errcode") != 0:
                        logger.error(f"WeChat API error: {resp_json.get('errmsg')}")
                        raise_service_unavailable("发送企业微信消息失败，请稍后再试或联系管理员")
                    else:
                        logger.info("WeChat message sent successfully")
    
    async def send_markdown(
        session: AsyncSession, 
        markdown: str, 
        version: Literal['v1', 'v2'],
        mentioned_all: bool = False,
        mentioned_list: list[str] = [],
        mentioned_mobile_list: list[str] = []
    ) -> None:
        key = await WeChatBot.get_key(session)
        
        if version == 'v1':
            payload = {
                "msgtype": "markdown",
                "markdown": {
                    "content": markdown,
                    "mentioned_list": ["@all"] if mentioned_all else mentioned_list,
                    "mentioned_mobile_list": ["@all"] if mentioned_all else mentioned_mobile_list
                }
            }
        elif version == 'v2':
            payload = {
                "msgtype": "markdown_v2",
                "markdown_v2": {
                    "content": markdown,
                    "mentioned_list": ["@all"] if mentioned_all else mentioned_list,
                    "mentioned_mobile_list": ["@all"] if mentioned_all else mentioned_mobile_list
                }
            }
        
        async with aiohttp.ClientSession() as http_session:
            async with http_session.post(
                url=f"{webhook_url}?key={key}",
                json=payload
            ) as response:
                if response.status != 200:
                    logger.error(f"Failed to send WeChat message: {response.status}")
                    raise_internal_error("企业微信机器人服务不可用，请稍后再试")
                else:
                    resp_json = await response.json()
                    if resp_json.get("errcode") != 0:
                        logger.error(f"WeChat API error: {resp_json.get('errmsg')}")
                        raise_service_unavailable("发送企业微信消息失败，请稍后再试或联系管理员")
                    else:
                        logger.info("WeChat message sent successfully")