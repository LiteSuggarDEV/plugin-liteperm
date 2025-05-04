from nonebot.adapters.onebot.v11 import Message, MessageEvent
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.rule import to_me

from ..API.admin import is_lp_admin
from ..API.logic_func import both
from ..command_manager import command
from ..config import GroupData, PermissionGroupData, UserData, data_manager
from ..nodelib import Permissions


@command.command("user", rule=both(is_lp_admin, to_me()))
async def lp_user(event: MessageEvent, matcher: Matcher, args: Message = CommandArg()):
    """
    用户权限管理
    处于指令分支 /lp user
    field: lp user <user_id> <permission|parent|perm_group> <operation> <permission_name|permission_group_name> [operation_value]
    permission:设置特定权限
    parent:操作自权限组
    """
    args_list = args.extract_plain_text().strip().split(maxsplit=5)
    allow_action_3 = ["permission", "parent", "perm_group"]
    if not len(args_list) > 1:
        await matcher.finish("请输入用户ID")
    elif len(args_list) >= 2:
        user_permission = Permissions(
            data_manager.get_user_data(args_list[1]).permissions
        )
        if args_list[2] not in allow_action_3:
            action_str = "".join(f"{i}/" for i in allow_action_3)
            return await matcher.finish(f"请输入操作：{action_str}")

        if len(args_list) == 3:
            return await matcher.finish(
                "请输入操作"
                + (
                    "del/set/list/check"
                    if args_list[2] == "permission"
                    else "add/set/del"
                )
            )
        elif len(args_list) == 4:
            await matcher.finish(
                "请输入" + ("权限组名称" if args_list[2] == "parent" else "权限名称")
            )
        elif len(args_list) == 5:
            if args_list[3] == "set":
                await matcher.finish("请输入布尔值(true/false)")
            if args_list[3] == "list" and args_list[2] == "permission":
                await matcher.finish(
                    f"{args_list[1]}的权限：\n{user_permission.permissions_str}"
                )
        elif len(args_list) == 6:
            try:
                user_data = data_manager.get_user_data(args_list[1])
                if args_list[2] == "permission":
                    if args_list[3] == "del":
                        user_permission.del_permission(args_list[4])
                        await matcher.finish(f"删除{args_list[4]}权限成功")
                    elif args_list[3] == "set":
                        if args_list[5] == "true":
                            user_permission.set_permission(args_list[4], True, False)

                        elif args_list[5] == "false":
                            user_permission.set_permission(args_list[4], False, False)
                        else:
                            return await matcher.finish("请输入布尔值(true/false)")
                    elif args_list[3] == "check":
                        if user_permission.check_permission(args_list[4]):
                            await matcher.finish(f"持有节点{args_list[4]}")
                        else:
                            await matcher.finish(f"未持有节点{args_list[4]}")
                    elif args_list[3] == "list":
                        await matcher.finish(
                            f"userid:{event.user_id}\n{user_permission.permissions_str()}"
                        )
                elif args_list[2] == "parent":
                    perm_group_data = data_manager.get_permission_group_data(
                        args_list[4], False
                    )
                    if perm_group_data is None:
                        return await matcher.finish(f"权限组{args_list[4]}不存在")
                    perm_group = Permissions(perm_group_data.permissions)
                    perm_group_str = perm_group.permissions_str
                    user_permission_str = user_permission.permissions_str
                    user_node_list = [
                        i.split(" ")[0] for i in user_permission_str.split("\n")
                    ]
                    if args_list[3] == "add":
                        for perm in perm_group_str.split("\n"):
                            for node, tf in perm.split(" "):
                                if node not in user_node_list:
                                    user_permission.set_permission(
                                        node, tf == "true", False
                                    )
                        await matcher.finish("群组权限继承添加完成")
                    elif args_list[3] == "del":
                        for perm in perm_group_str.split("\n"):
                            for node, tf in perm.split(" "):
                                if node in user_node_list:
                                    user_permission.del_permission(node)
                        await matcher.finish("群组权限继承删除完成")
                    elif args_list[3] == "set":
                        user_permission.data = Permissions(perm_group.dump_data())
                        await matcher.finish("群组权限继承覆盖设置完成")
                elif args_list[2] == "perm_group":
                    if args_list[3] == "add":
                        if args_list[4] in user_data.permission_groups:
                            return await matcher.finish("用户已加入该权限组")
                        else:
                            user_data.permission_groups.append(args_list[4])
                    elif args_list[3] == "del":
                        if args_list[4] not in user_data.permission_groups:
                            return await matcher.finish("用户未加入该权限组")
                        else:
                            user_data.permission_groups.remove(args_list[4])
                    elif args_list[3] == "list":
                        await matcher.finish(
                            f"{args_list[1]}的权限组：\n{','.join(user_data.permission_groups)}"
                        )

            finally:
                user_data.permissions = user_permission.dump_data()
                data_manager.save_user_data(args_list[1], user_data.model_dump())
