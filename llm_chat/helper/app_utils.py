import os

import pkg_resources

from llm_chat.config import MyConfig
from llm_chat.helper.single_instance_metaclass import SingleInstanceMetaClass
from llm_chat.helper.utils import subfolder_exists




class AppUtils(metaclass=SingleInstanceMetaClass):

    def get_package_version(self, package_name):
        try:
            version = pkg_resources.get_distribution(package_name).version
            return version
        except pkg_resources.DistributionNotFound:
            return f"{package_name} is not installed."

    def get_root_dir(self):
        if subfolder_exists(MyConfig().root, "llm_chat_command") or MyConfig().root == "/app":
            dir = MyConfig().root
        else:
            dir = os.path.dirname(MyConfig().root)
        return dir

    def get_root_sub_dir(self, sub_folder: str):
        dir = os.path.join(self.get_root_dir(), sub_folder)
        os.makedirs(dir, exist_ok=True)
        return dir

    def get_log_dir(self):
        return self.get_root_sub_dir("logs")

    def get_data_dir(self):
        return self.get_root_sub_dir("data")
