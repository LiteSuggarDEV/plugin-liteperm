import os

from dotenv import load_dotenv
from nonebot.adapters.onebot.v11 import Event

from ..config import UserData, data_manager
from ..nodelib import Permissions

load_dotenv()
ENV_ADMINS = os.getenv("LP_ADMINS", [])


async def is_lp_admin(event: Event) -> bool:
    """
    判断是否为管理员
    """
    user_id = event.get_user_id()
    user_data: UserData = data_manager.get_user_data(user_id)
    return user_id in ENV_ADMINS or Permissions(user_data.permissions).check_permission(
        "lp.admin"
    )
