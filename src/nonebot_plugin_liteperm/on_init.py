import contextlib

from nonebot import get_driver

from .config import data_manager

__VERSION__ = "v1.00"
banner_template = """\033[34m▗▖   ▗▄▄▖
▐▌   ▐▌ ▐▌  \033[96mLitePerms\033[34m  \033[1;4;34mV{version}\033[0m\033[34m
▐▌   ▐▛▀▘   is initializing...
▐▙▄▄▖▐▌\033[0m"""


@get_driver().on_startup
async def load_config():
    import asyncio
    import subprocess
    import sys

    version = "unknown"
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
        with contextlib.suppress(IndexError):
            version = stdout.decode("utf-8").split("\n")[1].split(": ")[1]
    except subprocess.CalledProcessError:
        pass
    except Exception:
        pass

    print(banner_template.format(version=version))
    data_manager.init()
