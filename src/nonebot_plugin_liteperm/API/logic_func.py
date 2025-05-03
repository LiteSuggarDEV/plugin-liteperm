from collections.abc import Awaitable, Coroutine

from nonebot.adapters.onebot.v11 import Event


def both(
    func1: Awaitable[bool] | Coroutine, func2: Awaitable[bool] | Coroutine, perm: str
) -> Awaitable[bool] | Coroutine:
    """用于 组合两个检查器（且判断）

    Args:
        func1 (Awaitable[bool] | Coroutine): 检查器一
        func2 (Awaitable[bool] | Coroutine): 检查器二
        perm (str): 需要检查的权限节点

    Returns:
        Awaitable[bool] | Coroutine: 返回的协程函数

    Example:
        rule = both(UserPermissionChecker(perm).checker(), GroupPermissionChecker(perm).checker(), perm)
    """

    async def _both(event: Event) -> bool:
        return await func1(event, perm) and await func2(event, perm)

    return _both


def either(
    func1: Awaitable[bool] | Coroutine, func2: Awaitable[bool] | Coroutine, perm: str
) -> Awaitable[bool] | Coroutine:
    """用于 组合两个检查器（或判断）

    Args:
        func1 (Awaitable[bool] | Coroutine): 检查器一
        func2 (Awaitable[bool] | Coroutine): 检查器二
        perm (str): 需要检查的权限节点

    Returns:
        Awaitable[bool] | Coroutine: 返回的协程函数

    Example:
        rule = either(UserPermissionChecker(perm).checker(), GroupPermissionChecker(perm).checker(), perm)
    """

    async def _either(event: Event) -> bool:
        return await func1(event, perm) or await func2(event, perm)

    return _either


def neither(
    func1: Awaitable[bool] | Coroutine, func2: Awaitable[bool] | Coroutine, perm: str
) -> Awaitable[bool] | Coroutine:
    """用于 组合两个检查器（且非判断）

    Args:
        func1 (Awaitable[bool] | Coroutine): 检查器一
        func2 (Awaitable[bool] | Coroutine): 检查器二
        perm (str): 需要检查的权限节点

    Returns:
        Awaitable[bool] | Coroutine: 返回的协程函数

    Example:
        rule = neither(UserPermissionChecker(perm).checker(), GroupPermissionChecker(perm).checker(), perm)
    """

    async def _neither(event: Event) -> bool:
        return not await func1(event, perm) and not await func2(event, perm)

    return _neither
