from dotenv import load_dotenv
from nonebot import on_command
from nonebot.rule import to_me

from .API.admin import is_lp_admin
from .API.logic_func import both
from .commands.main import lp

load_dotenv()
on_command(
    "lp", aliases={"liteperms", "LitePerms", "LP"}, rule=both(is_lp_admin, to_me())
).append_handler(lp)
