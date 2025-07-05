import asyncio
from typing import Any, override

from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.matcher import Matcher
from nonebot.params import Depends

from ..API.admin import is_lp_admin
from ..config import CommandConfig, data_manager
from .cmd_utils import parse_command
from .main import PermissionHandler, command


class PermissionOperation(PermissionHandler):
    @override
    async def execute(
        self, command: str, operation: str, node: str, value: str
    ) -> tuple[str, dict[str, Any]]:
        result = " "
        command_data = data_manager.get_command_settings()
        if operation == "set":
            command_data.commands[command][node] = (
                True if value.lower() == "true" else False
            )
            return "✅ 操作成功", command_data.model_dump()
        elif operation == "del":
            if command in command_data.commands:
                if node in command_data.commands[command]:
                    del command_data.commands[command][node]
                    return "✅ 操作成功", command_data.model_dump()
            else:
                return "❌ 节点不存在", {}
        return result, command_data.model_dump()


class DelPermissionSetting(PermissionHandler):
    async def execute(
        self, command: str, operation: str, node: str, value: str
    ) -> tuple[str, dict[str, Any]]:
        result = "❌ 操作失败"
        command_data = data_manager.get_command_settings()
        if operation == "del" and command in command_data.commands:
            del command_data.commands[command]
            result = "✅ 操作成功"
        return result, command_data.model_dump()


class ListHandler(PermissionHandler):
    async def execute(
        self, user_id: str, operation: str, command: str, _: str
    ) -> tuple[str, dict[str, Any]]:
        result = "❌ 操作失败"
        command_data = data_manager.get_command_settings()
        if operation == "list":
            result = "已设置的命令："
            for command in command_data.commands:
                result += f"\n{command} {''.join(f'{node} ,' for node, _ in command_data.commands[command].items())}"
        return result, {}


def get_handler(
    action_type: str,
) -> PermissionHandler | None:
    handlers: dict[str, PermissionHandler] = {
        "set_permission": PermissionOperation(),
        "command": DelPermissionSetting(),
        "list": ListHandler(),
    }
    return handlers.get(action_type)


@command.command("command", permission=is_lp_admin).handle()
async def lp_user(
    event: MessageEvent,
    matcher: Matcher,
    params: tuple[str, str, str, str, str] = Depends(parse_command),
):
    command_name, action_type, operation, target, value = params
    handler = get_handler(action_type)
    if handler is None:
        await matcher.finish("❌ 未知操作类型")
    try:
        result, data = await handler.execute(command_name, operation, target, value)
    except ValueError as e:
        result = f"❌ 操作失败：{e!s}"
    finally:
        lock = asyncio.locks.Lock()
        async with lock:
            if data:
                data_manager.save_command_settings(CommandConfig(**data))

    await matcher.finish(result)
