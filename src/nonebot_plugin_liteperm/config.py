import json
import os
from dataclasses import dataclass
from pathlib import Path

from nonebot_plugin_localstore import get_plugin_data_dir
from pydantic import BaseModel

plugin_data_dir = get_plugin_data_dir()
os.makedirs(plugin_data_dir, exist_ok=True)


class BasicDataModel(BaseModel, extra="allow"):
    def __getattr__(self, item) -> str:
        if item in self.__dict__:
            return self.__dict__[item]
        if self.__pydantic_extra__ and item in self.__pydantic_extra__:
            return self.__pydantic_extra__[item]
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{item}'"
        )
class Config(BasicDataModel):
    default_permission_group_name: str = "default"

@dataclass
class Data_Manager:
    plugin_data_dir: Path = plugin_data_dir
    group_data_path: Path = plugin_data_dir / "group_data"
    user_data_path: Path = plugin_data_dir / "user_data"
    permission_groups_path: Path = plugin_data_dir / "permission_groups"

    os.makedirs(group_data_path, exist_ok=True)
    os.makedirs(user_data_path, exist_ok=True)
    os.makedirs(permission_groups_path, exist_ok=True)

    def save_user_data(self, user_id: str, data: dict[str, str | dict | bool]):
        UserData.model_validate(data)
        data_path = self.user_data_path / f"{user_id}.json"
        with open(data_path, "w") as f:
            json.dump(data, f)

    def save_group_data(self, group_name: str, data: dict[str, str | dict | bool]):
        GroupData.model_validate(data)
        data_path = self.group_data_path / f"{group_name}.json"
        with open(data_path, "w") as f:
            json.dump(data, f)

    def save_permission_group_data(
        self, group_name: str, data: dict[str, str | dict | bool]
    ):
        PermissionGroupData.model_validate(data)
        data_path = self.permission_groups_path / f"{group_name}.json"
        with open(data_path, "w") as f:
            json.dump(data, f)

    def get_group_data(self, group_id: str):
        data_path = self.group_data_path / f"{group_id}.json"
        if not data_path.exists():
            data = GroupData()
            with open(data_path, "w") as f:
                json.dump(data.model_dump(), f)
            return data
        with open(data_path) as f:
            return GroupData(**json.load(f))

    def get_permission_group_data(self, group_name: str):
        data_path = self.permission_groups_path / f"{group_name}.json"
        if not data_path.exists():
            data = PermissionGroupData()
            with open(data_path, "w") as f:
                json.dump(data.model_dump(), f)
            return data
        with open(data_path) as f:
            return PermissionGroupData(**json.load(f))

    def get_user_data(self, user_id: str):
        data_path = self.user_data_path / f"{user_id}.json"
        if not data_path.exists():
            data = UserData()
            with open(data_path, "w") as f:
                json.dump(data.model_dump(), f)
            return data
        with open(data_path) as f:
            return UserData(**json.load(f))


class UserData(BasicDataModel):
    permission_groups: list[str] = []
    permissions: dict[str, str | dict | bool] = {}


class GroupData(BasicDataModel):
    permission_groups: list[str] = []
    permissions: dict[str, str | dict | bool] = {}


class PermissionGroupData(BasicDataModel):
    permissions: dict[str, str | dict | bool] = {}


data_manager = Data_Manager()
