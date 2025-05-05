import nonebot.matcher as nbm
from nonebot import get_driver, logger
from nonebot.adapters import Event
from nonebot.exception import IgnoredException, NoneBotException
from nonebot.matcher import Matcher
from nonebot.message import event_preprocessor

from .config import data_manager
from .nodelib import Permissions

driver = get_driver()
command_starts = driver.config.command_start  # 获取配置的命令起始符（如 ["/", "!"]）


@event_preprocessor
async def check_on_command(matcher: Matcher, event: Event):
    # 获取消息文本并去除首尾空格
    msg = event.get_message().extract_plain_text().strip()
    user_id = event.get_user_id()
    if event.__class__.__name__.startswith("Group"):
        group_id: str | None = event.group_id  # type: ignore
    else:
        group_id = None
    # 遍历所有可能的命令起始符
    for start in command_starts:
        if msg.startswith(start):
            cmd_part = msg[len(start) :].split(maxsplit=1)[0]

            for priority_group in nbm.matchers.values():
                for matcher_cls in priority_group:
                    try:
                        # 检查是否是on_command创建的Matcher
                        if not (
                            matcher_cls.type == "message"
                            and any(
                                rule.call.__name__ == "_check_command"
                                for rule in matcher_cls.rule.checkers
                            )
                        ):
                            continue

                        # 从规则中提取命令参数
                        command_rule = next(
                            rule
                            for rule in matcher_cls.rule.checkers
                            if rule.call.__name__ == "_check_command"
                        )
                        commands = command_rule.call.args[0]

                        # 处理命令格式
                        all_commands = {
                            cmd if isinstance(cmd, str) else cmd[0] for cmd in commands
                        }

                        if cmd_part in all_commands:
                            if not data_manager.config.cmd_permission_checker:
                                return
                            cmd_data = data_manager.get_command_settings()
                            if cmd_part in cmd_data.commands:
                                user_data = data_manager.get_user_data(user_id)
                                user_permissions = Permissions(user_data.permissions)
                                user_permission_groups = user_data.permission_groups
                                for permission in cmd_data.commands[cmd_part].keys():
                                    for group in user_permission_groups:
                                        perm_group_data = (
                                            data_manager.get_permission_group_data(
                                                group
                                            )
                                        )
                                        if perm_group_data is None:
                                            user_permission_groups.remove(group)
                                            data_manager.save_user_data(
                                                user_id, user_data.model_dump()
                                            )
                                        elif Permissions(
                                            perm_group_data.permissions
                                        ).check_permission(permission):
                                            return
                                    if user_permissions.check_permission(permission):
                                        return
                                    elif group_id is not None:
                                        group_data = data_manager.get_group_data(
                                            group_id
                                        )
                                        group_permissions = Permissions(
                                            group_data.permissions
                                        )
                                        if group_permissions.check_permission(
                                            permission
                                        ):
                                            return
                                        group_perm_groups = group_data.permission_groups
                                        for group_perm_group in group_perm_groups:
                                            if (
                                                data_manager.get_permission_group_data(
                                                    group_perm_group
                                                )
                                                is None
                                            ):
                                                group_data.permission_groups.remove(
                                                    group_perm_group
                                                )
                                                data_manager.save_group_data(
                                                    group_id, group_data.model_dump()
                                                )
                                            elif Permissions(
                                                data_manager.get_permission_group_data(
                                                    group_perm_group
                                                ).permissions  # type: ignore
                                            ).check_permission(permission):
                                                return
                                        raise IgnoredException(
                                            f"Permission {permission} denied"
                                        )
                                    else:
                                        raise IgnoredException(
                                            f"Permission {permission} denied"
                                        )
                    except (StopIteration, AttributeError):
                        continue
                    except NoneBotException as e:
                        raise e
                    except Exception as e:
                        logger.error(f"Matcher检查错误: {e}")
