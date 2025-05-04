# plugin-liteperm

基于权限节点+特殊权限+权限组的依赖权限管理插件！

>本项目灵感来自于[LuckPerms](https://github.com/LuckPerms/LuckPerms)

# NoneBot Plugin LitePerms 文档

## 📖 指令文档

### 通用命令结构

```
/lp [对象类型] [操作类型] [操作] [目标] [值]
```

---

### 用户权限管理 (lp user)

```
/lp user [用户ID] [操作类型] [操作] [目标节点/组] [值]
```

**操作类型**：

1. **permission** - 直接权限管理
   - `set [节点] [true/false]`：设置权限节点状态
   - `del [节点]`：删除权限节点
   - `check [节点]`：检查权限节点
   - `list`：列出所有权限

2. **parent** - 继承组管理
   - `add [组名]`：添加继承组
   - `del [组名]`：移除继承组
   - `set [组名]`：覆盖为指定组的权限

3. **perm_group** - 权限组管理
   - `add [组名]`：添加权限组
   - `del [组名]`：移除权限组

**示例**：

```
/lp user 123456 permission set lp.admin true
/lp user 123456 parent add admin_group
```

---

### 群组权限管理 (lp group)

```
/lp group [群号] [操作类型] [操作] [目标节点/组] [值]
```

（参数格式与用户权限管理相同）

---

### 权限组管理 (lp perm_group)

```
/lp perm_group [组名] [操作类型] [操作] [目标节点/组] [值]
```

**新增操作类型**：

- **to** - 组操作
  - `create`：创建新权限组
  - `remove`：删除权限组

**示例**：

```
/lp perm_group admin to create
/lp perm_group admin permission set system.* true
```

---

### 命令权限管理 (lp command)

```
/lp command [命令名] [操作类型] [操作] [权限节点] [值]
```

**操作类型**：

- [set_permission](file:///home/johnrichard/LiteSuggarDEV/plugin-liteperm/src/nonebot_plugin_liteperm/nodelib.py#L59-L74)：设置命令权限节点
- `command del`：删除命令权限配置

**示例**：

```
/lp command ping set_permission lp.user.ping true
```

---
