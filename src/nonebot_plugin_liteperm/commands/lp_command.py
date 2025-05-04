from nonebot.adapters.onebot.v11 import Message, MessageEvent
from nonebot.matcher import Matcher
from nonebot.params import CommandArg


async def lp_command(event: MessageEvent, matcher: Matcher, args: Message = CommandArg()):
    args_list = args.extract_plain_text().strip().split()
    pass
