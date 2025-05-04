import nonebot.matcher as nbm
from nonebot import get_driver, logger
from nonebot.adapters import Event
from nonebot.matcher import Matcher
from nonebot.message import event_preprocessor

driver = get_driver()
command_starts = driver.config.command_start  # 获取配置的命令起始符（如 ["/", "!"]）


@event_preprocessor
async def check_on_command(matcher: Matcher, event: Event):
    # 获取消息文本并去除首尾空格
    msg = event.get_message().extract_plain_text().strip()

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
                            ...
                            # todo
                    except (StopIteration, AttributeError):
                        continue
                    except Exception as e:
                        logger.error(f"Matcher检查错误: {e}")
