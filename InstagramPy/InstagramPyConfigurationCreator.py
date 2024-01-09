# The MIT License.
# Copyright (C) 2017 The Future Shell , DeathSec.
#
# @filename    : InstagramPyConfigurationCreator.py
# @description : Create a Configuration file for Instagram-Py with ease.
import os
import json
from .colors import *

class InstagramPyConfigurationCreator:
    default_config = {
        "api-url": "https://i.instagram.com/api/v1/",
        "user-agent": "Instagram 10.26.0 Android (18/4.3; 320dpi; 720x1280; Xiaomi; HM 1SW; armani; qcom; en_US)",
        "ig-sig-key": "4f8732eb9ba7d1c8e8897a75d6474d4eb3f5279137431b2aafb71fafe2abe178",
        "ig-sig-version": "4",
        "tor": {
            "server": "127.0.0.1",
            "port": "9050",
            "protocol": "socks5",
            "control": {
                "password": "",
                "port": "9051"
            }
        }
    }

    def __init__(self, path):
        self.config_path = path

    def create(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.default_config, f)
        print(f"{Style.BRIGHT}Written Configuration at {self.config_path}{Style.RESET_ALL}")
        return True

    def easy_create(self):
        print(f"{Style.BRIGHT}Welcome to Instagram-Py Configuration Creator!{Style.RESET_ALL}")
        self.set_config_value('tor', 'server', 'Tor Server IP')
        self.set_config_value('tor', 'port', 'Tor Server Port')
        self.set_config_value('tor.control', 'port', 'Tor Control Port')
        self.set_config_value('tor.control', 'password', 'Tor Authentication Password')

        print(f"{Style.BRIGHT}Writing Configuration...{Style.RESET_ALL}")
        with open(self.config_path, 'w') as f:
            json.dump(self.default_config, f)

        print(f"{Style.BRIGHT}Written Configuration at {self.config_path}{Style.RESET_ALL}")
        return True

    def set_config_value(self, category, key, prompt):
        value = input(f"{prompt} (default=[Press Enter]):: {Style.BRIGHT + Fore.MAGENTA}{Style.RESET_ALL}")
        if value != '':
            config_keys = key.split('.')
            current_config = self.default_config
            for config_key in config_keys[:-1]:
                current_config = current_config[config_key]
            current_config[config_keys[-1]] = value

