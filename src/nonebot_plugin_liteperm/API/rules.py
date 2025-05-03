from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import override

from nonebot.adapters.onebot.v11 import Event
from nonebot.log import logger

from ..config import data_manager
from ..nodelib import Permissions


@dataclass
class PermissionChecker:
    """
    权限检查器基类
    args:
        permission: 权限节点
    """

    permission: str

    def checker(self, k_id: str = "") -> Callable[[Event], Awaitable[bool]]:
        """生成可被 Rule 使用的检查器闭包

        Args:
            k_id (str, optional): 用户/群OD. Defaults to "".

        Returns:
            Callable[[Event], Awaitable[bool]]: 供Rule检查的Async函数
        """

        # 捕获当前权限值到闭包中
        current_perm = self.permission

        async def _checker(event: Event | None = None) -> bool:
            """实际执行检查的协程函数"""
            # 通过闭包访问类变量（self.permission）
            return (
                await self._check_permission(event, current_perm)
                if not k_id
                else await self._check_permission_on_id(k_id, current_perm)
            )

        return _checker

    async def _check_permission(self, event: Event, perm: str) -> bool:
        raise NotImplementedError("Awaitable '_check_permission' not implemented")

    # 这里需要做显式区分调用
    async def _check_permission_on_id(self, id: str, current_perm: str) -> bool:
        return NotImplementedError(
            "awaitable '__check_permission_on_id' not implemented"
        )


@dataclass
class UserPermissionChecker(PermissionChecker):
    """
    用户权限检查器
    """

    @override
    async def _check_permission(self, event: Event, perm: str) -> bool:
        user_id = event.get_user_id()
        user_data = data_manager.get_user_data(user_id)
        logger.debug(f"checking user permission {user_id} {perm}")
        perm_groups = user_data.permission_groups
        for permg in perm_groups:
            if Permissions(
                data_manager.get_permission_group_data(permg).permissions
            ).check_permission(perm):
                return True
        return Permissions(user_data.model_dump()).check_permission(perm)

    @override
    async def _check_permission_on_id(self, uid: str, perm: str) -> bool:
        user_data = data_manager.get_user_data(uid)
        logger.debug(f"checking user permission {uid}")
        perm_groups = user_data.permission_groups
        for perm_g in perm_groups:
            if Permissions(
                data_manager.get_permission_group_data(perm_g).permissions
            ).check_permission(perm):
                return True
        return Permissions(user_data.model_dump()).check_permission(perm)


@dataclass
class GroupPermissionChecker(PermissionChecker):
    """
    群组权限检查器
    args:
        only_group: 是否只允许群事件
    """

    only_group: bool = True

    @override
    async def _check_permission(self, event: Event, perm: str) -> bool:
        if not event.__class__.__name__.startswith("Group") and not self.only_group:
            return True
        else:
            return False
        group_id = event.group_id
        group_data = data_manager.get_group_data(group_id)
        logger.debug(f"checking group permission {group_id} {perm}")
        perm_groups = group_data.permission_groups
        for permg in perm_groups:
            if Permissions(
                data_manager.get_permission_group_data(permg).permissions
            ).check_permission(perm):
                return True
        return Permissions(group_data.model_dump()).check_permission(perm)

    @override
    async def _check_permission_on_id(self, gid: str, perm: str) -> bool:
        group_data = data_manager.get_group_data(gid)
        logger.debug(f"checking group permission {gid}")
        perm_groups = group_data.permission_groups
        for perm_g in perm_groups:
            if Permissions(
                data_manager.get_permission_group_data(perm_g).permissions
            ).check_permission(perm):
                return True
        return Permissions(group_data.model_dump()).check_permission(perm)
