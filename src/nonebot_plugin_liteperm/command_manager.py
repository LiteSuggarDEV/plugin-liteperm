from nonebot.plugin.on import CommandGroup
from nonebot.rule import to_me

command = CommandGroup(
    ("lp", "LP", "LitePerm"), priority=10, block=True, rule=to_me(), prefix_aliases=True
)
