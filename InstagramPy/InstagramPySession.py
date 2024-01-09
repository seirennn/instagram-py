# The MIT License.
# Copyright (C) 2017 The Future Shell , DeathSec.
#
# @filename    : InstagramPySession.py
# @description : Creates a new session, checks for configuration, and gets critical data,
#                loads, and saves data too.

import json
import os
import uuid
import hashlib
import requests
from stem import Signal
from stem.control import Controller

DEFAULT_PATH = os.path.expanduser('~')


class InstagramPySession:
    def __init__(self, username, password_list, configuration, save_location, cli):
        self.username = username
        self.cli = cli
        self.password_list = password_list
        self.password_list_length = 0
        self.password_list_md5_sum = None
        self.password_list_buffer = None
        self.eopl = False
        self.current_line = 1
        self.ip = None
        self.cli = None
        self.bot = requests.Session()

        if not os.path.isfile(self.password_list):
            self.cli.ReportError(f"Password list not found at {self.password_list}")

        # Note: Always open password list with errors ignored because all password list
        # mostly has a wrong encoding or the user's PC does not support it!
        with open(self.password_list, encoding='utf-8', errors='ignore') as f:
            self.password_list_buffer = f.readlines()
            self.password_list_md5_sum = hashlib.md5(f.read().encode('utf-8')).hexdigest()
            self.password_list_length = len(self.password_list_buffer)

        if configuration == DEFAULT_PATH:
            configuration = f"{DEFAULT_PATH}/instapy-config.json"
        if save_location == DEFAULT_PATH:
            save_location = f"{DEFAULT_PATH}/.instagram-py/"

        dump_location = f"{save_location}dump.json"

        if not os.path.isfile(configuration):
            self.cli.ReportError(f"Configuration file not found at {configuration}")
        else:
            try:
                with open(configuration, "r") as fp:
                    config_data = json.load(fp)
            except Exception as err:
                self.cli.ReportError(f"Invalid configuration file at {configuration}")

            self.api_url = config_data['api-url']
            self.user_agent = config_data['user-agent']
            self.ig_sig_key = config_data['ig-sig-key']
            self.ig_sig_version = config_data['ig-sig-version']
            self.tor_proxy = f"{config_data['tor']['protocol']}://{config_data['tor']['server']}:{config_data['tor']['port']}"
            self.OpenTorController(config_data['tor']['control']['port'], config_data['tor']['control']['password'])

            self.bot.proxies = {"https": self.tor_proxy, "http": self.tor_proxy}
            self.bot.headers.update({
                'Connection': 'close',
                'Accept': '*/*',
                'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Cookie2': '$Version=1',
                'Accept-Language': 'en-US',
                'User-Agent': self.user_agent
            })

            try:
                self.ip = self.bot.get('https://icanhazip.com').content.rstrip().decode()
            except (BaseException, Exception) as err:
                self.cli.ReportError("Connection to host failed, check your connection and Tor configuration.")

        if not os.path.exists(save_location):
            try:
                os.mkdir(save_location)
            except (BaseException, Exception) as err:
                self.cli.ReportError(err)
            self.save_data = save_location
        else:
            self.save_data = save_location

        self.dump_data = dump_location
        self.current_save = None
        self.magic_cookie = None

        self.ReadSaveFile(False)

    def ReadSaveFile(self, is_resume):
        self.CreateSaveFile(is_resume)
        if self.current_save:
            save_file = json.load(open(self.current_save, 'r'))
            self.current_line = save_file['line-count']
            if self.password_list_md5_sum == save_file['password-file-md5'] and self.username == save_file['username']:
                self.password = self.password_list_buffer[self.current_line - 1].strip()
            return True
        return False

    def UpdateSaveFile(self):
        if self.current_save:
            with open(self.current_save, 'w') as updatefile:
                json.dump({
                    "username": str(self.username),
                    "password-file-md5": str(self.password_list_md5_sum),
                    "line-count": self.current_line
                }, updatefile)

    def CreateSaveFile(self, is_resume):
        if self.current_save is None and self.save_data is not None:
            save = f"{self.save_data}{hashlib.sha224(self.username.encode('utf-8')).hexdigest()}.dat"
            self.current_save = save
            if not os.path.isfile(save) or not is_resume:
                self.UpdateSaveFile()

    def ReadDumpFile(self, username):
        if self.dump_data:
            if os.path.isfile(self.dump_data):
                json_dump = json.load(open(self.dump_data, 'r'))
                return json_dump.get(username)

    def WriteDumpFile(self, info):
        if self.dump_data:
            json_dump = {}
            if os.path.isfile(self.dump_data):
                json_dump = json.load(open(self.dump_data, 'r'))
            json_dump[info['id']] = info
            with open(self.dump_data, 'w') as dump_file:
                json.dump(json_dump, dump_file)
            return True
        return False

    def CurrentPassword(self):
        return self.password

    def NextPassword(self):
        if not self.current_line > self.password_list_length:
            self.password = self.password_list_buffer[self.current_line - 1].strip()
            self.current_line += 1
        else:
            self.eopl = True

    def GetUsername(self):
        return self.username

    def md5sum(self, fp, block_size=2**20):
        md5 = hashlib.md5()
        for data in iter(lambda: fp.read(block_size), b''):
            md5.update(data)
        return md5

    def ChangeIPAddress(self):
        if self.tor_controller:
            self.tor_controller.signal(Signal.NEWNYM)
            self.ip = self.bot.get('https://icanhazip.com').content.rstrip().decode()
            return True
        return False

    def OpenTorController(self, port, password):
        try:
            self.tor_controller = Controller.from_port(port=int(port))
            if password:
                self.tor_controller.authenticate(password=password)
            else:
                self.tor_controller.authenticate()
        except Exception as err:
            self.cli.ReportError(f"Tor configuration invalid or server down :: {err}")

