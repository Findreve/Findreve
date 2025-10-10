"""
管理员相关业务逻辑。
"""

from typing import Iterable, List

from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from model import Setting
from model import SettingResponse


async def fetch_settings(
    session: AsyncSession,
    name: str | None = None,
) -> List[SettingResponse]:
    """
    按名称获取设置项，默认返回全部。
    """
    data: list[SettingResponse] = []

    if name:
        setting = await Setting.get(session, Setting.name == name)
        if setting:
            data.append(SettingResponse.model_validate(setting))
        else:
            raise HTTPException(404, detail="Setting not found")
    else:
        settings: Iterable[Setting] | None = await Setting.get(session, fetch_mode="all")
        if settings:
            data = [SettingResponse.model_validate(s) for s in settings]

    return data


async def update_setting_value(
    session: AsyncSession,
    name: str,
    value: str,
) -> bool:
    """
    更新设置项的值。
    """
    setting = await Setting.get(session, Setting.name == name)
    if not setting:
        raise HTTPException(404, detail="Setting not found")

    setting.value = value
    await Setting.save(session)

    return True
