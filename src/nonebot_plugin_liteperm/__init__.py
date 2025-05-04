from nonebot.plugin import PluginMetadata, require

require("nonebot_plugin_localstore")


__plugin_meta__ = PluginMetadata(
    name="LitePerm 权限管理插件", # type: ignore
    description="基于权限节点/权限组/特殊权限的权限管理插件。",
    usage="https://github.com/LiteSuggarDEV/plugin-liteperm/blob/main/README.md",
    homepage="https://github.com/LiteSuggarDEV/plugin-liteperm/",
    type="application",
    supported_adapters={"~onebot.v11"},
)
