import os
from asyncio import to_thread

from dotenv import load_dotenv
from nonebot.adapters.onebot.v11 import Event

from .logic_func import either
from .rules import UserPermissionChecker

load_dotenv()
ENV_ADMINS = os.getenv("LP_ADMINS", [])


async def is_lp_admin(event: Event) -> bool:
    """
    判断是否为管理员
    """
    return await either(
        UserPermissionChecker("lp.admin").checker(event.get_user_id()),
        to_thread(lambda: event.get_user_id() in ENV_ADMINS),
        "lp.admin",
    )
