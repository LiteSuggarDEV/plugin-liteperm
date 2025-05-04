from nonebot import get_driver

from .config import data_manager

__VERSION__ = "v1.00"
banner = f"""\033[34m▗▖   ▗▄▄▖
▐▌   ▐▌ ▐▌  \033[96mLitePerms\033[34m  \033[1;4;34mV{__VERSION__}\033[0m\033[34m
▐▌   ▐▛▀▘   is initializing...
▐▙▄▄▖▐▌\033[0m"""


@get_driver().on_startup
async def load_config():
    global __VERSION__
    import asyncio
    import subprocess
    import sys

    __VERSION__ = "unknown"
    try:
        process = await asyncio.create_subprocess_exec(
            sys.executable,
            "-m",
            "pip",
            "show",
            "nonebot-plugin-suggarchat",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await process.communicate()
        try:
            __VERSION__ = stdout.decode("utf-8").split("\n")[1].split(": ")[1]
        except IndexError:
            __VERSION__ = "unknown"
    except subprocess.CalledProcessError:
        __VERSION__ = "unknown"
    except Exception:
        __VERSION__ = "unknown"
    print(banner)
    data_manager.init()
