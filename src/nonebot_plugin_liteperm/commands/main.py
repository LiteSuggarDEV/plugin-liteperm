from nonebot.adapters.onebot.v11 import Message, MessageEvent
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.rule import to_me

from ..command_manager import command


@command.command("", rule=to_me())
async def lp(event: MessageEvent, matcher: Matcher, args: Message = CommandArg()):
    args_list = args.extract_plain_text().strip().split()
    lp_0_help = (
        "LP LitePerms\n请输入参数\nlp user\nlp chat_group\nlp perm_group\nlp command\n"
    )

    if not args_list:
        await matcher.finish(lp_0_help)
