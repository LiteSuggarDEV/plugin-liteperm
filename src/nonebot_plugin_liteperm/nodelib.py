class Node:
    data: dict[str, dict[str, dict | bool]]
    node_list: list[str]
    permissions: str = ""

    def __init__(self, data: dict, node: str = ""):
        self.data = data["nodes"]
        self.node_list = node.split(".")

    @property
    def nodes(self) -> dict:
        return self.data

    def set_value(self, n_value: bool):
        node_list = self.node_list
        data = self.data
        dict_tmp = data
        for index, value in enumerate(node_list):
            if index == len(node_list) - 1:
                if value == "*":
                    dict_tmp["__all__"] = n_value
                else:
                    dict_tmp[value]["__has__"] = n_value
            elif dict_tmp.get(value):
                dict_tmp = dict_tmp[value]
            else:
                dict_tmp[value] = {
                    "__has__": True,
                    "__all__": False,
                }
                dict_tmp = dict_tmp[value]

    def has(self) -> bool:
        data = self.data
        node_list = self.node_list
        dict_tmp = data
        for index, value in enumerate(node_list):
            if isall := dict_tmp.get("__all__"):
                return True
            elif isall is None:
                dict_tmp["__all__"] = False
            if index == len(node_list) - 1:
                if value in dict_tmp:
                    if has := (dict_tmp[value]).get("__has__") is True:
                        return True
                    elif has is None:
                        dict_tmp[value]["__has__"] = True
                        return True
                    else:
                        return False
                elif dict_tmp.get(value):
                    dict_tmp = dict_tmp[value]
                else:
                    return False
        return False

    def _print_dict_recursive(self, value: dict | None = None, path=""):
        d = self.data.copy() if value is None else value
        for key, value in d.items():
            if key == "__all__":
                if value is True:
                    full_path = f"{path}.*" if path else "*"
                    self.permissions += f"{full_path} {value}\n"
            elif key == "__has__":
                values = [v for k, v in d.items()]
                for i in values:
                    if isinstance(i, dict):
                        break
                else:
                    if value is True:
                        full_path = path if path else "."
                        self.permissions += f"{full_path} {value}\n"

                if value is False:
                    full_path = path if path else "."
                    self.permissions += f"{full_path} {value}\n"
            elif isinstance(value, dict):
                new_path = f"{path}.{key}" if path else key
                # 先递归处理子字典
                self._print_dict_recursive(value, new_path)
                # 检查子字典处理后是否需要打印当前路径
                if "__all__" not in value and "__has__" not in value:
                    self.permissions += f"{new_path} {value}\n"
            else:
                full_path = f"{path}.{key}" if path else key
                self.permissions += f"{full_path} {value}\n"

    @property
    def permission(self) -> str:
        self._print_dict_recursive()
        return self.permissions
