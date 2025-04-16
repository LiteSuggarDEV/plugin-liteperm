import json


class Permissions:
    def __init__(self):
        # 初始化权限数据，存储根节点的子节点
        self.permissions_data = {}

    def add_permission(self, node: str, has_permission: bool):
        node_parts = node.split(".")
        current_children = self.permissions_data  # 当前层级的子节点字典

        for i, part in enumerate(node_parts):
            # 不存在创建新节点
            if part not in current_children:
                current_children[part] = {"has_permission": False, "children": {}}
            current_node = current_children[part]
            # 最后一个部分设权
            if i == len(node_parts) - 1:
                current_node["has_permission"] = has_permission
            # 下一层
            current_children = current_node["children"]

    def check_permission(self, node: str) -> bool:
        node_parts = node.split(".")
        current_children = self.permissions_data  # 当前层级的子节点字典
        current_node = None

        for part in node_parts:
            if part in current_children:
                current_node = current_children[part]
                current_children = current_node["children"]
            elif "*" in current_children:
                current_node = current_children["*"]
                current_children = current_node["children"]
            else:
                return False  # 没有找到节点或通配符

        # 返回最终节点的权限
        return current_node["has_permission"] if current_node else False

    def save_to_file(self, filename: str):
        with open(filename, "w") as f:
            json.dump(self.permissions_data, f, indent=4)

    def load_from_file(self, filename: str):
        with open(filename) as f:
            self.permissions_data = json.load(f)


permissions = Permissions()
