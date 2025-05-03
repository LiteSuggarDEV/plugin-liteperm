from nonebot.adapters.onebot.v11 import Message, MessageEvent
from nonebot.matcher import Matcher
from nonebot.params import CommandArg


async def lp(event: MessageEvent, matcher: Matcher, args: Message = CommandArg()):
    args_list = args.extract_plain_text().strip().split()
    lp_0_help = "请输入参数\nlp user\nlp chat_group\nlp perm_group\n"
    lp_0 = ["user", "chat_group", "perm_group"]
    lp_2 = ["permission"]
    lp_3 = ["add", "del", "set", "list","check"]

    if len(args_list) == 0:
        return await matcher.finish(f"命令错误\n{lp_0_help}")
    elif len(args_list) == 1:
        if args_list[0] in lp_0:
            await matcher.finish(f"lp {args_list[0]} <id>")
        else:
            await matcher.finish(lp_0_help)
    elif len(args_list) == 3:
        if args_list[2] in lp_2:
            await matcher.finish(f"lp {args_list[0]} {args_list[1]} {args_list[2]} <set/add/del/check/list>")
        else:
            await matcher.finish(f"lp {args_list[0]} {args_list[1]} <permission>")
    elif len(args_list) == 4:
        if arg_li