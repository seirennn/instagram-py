# The MIT License.
# Copyright (C) 2017 The Future Shell, DeathSec.
#
# @filename    : InstagramPyDumper.py
# @description : Dumps succession logs for the given username

import json
import os


class InstagramPyDumper:
    def __init__(self, username):
        self.dump_data = "{}/.instagram-py/dump.json".format(os.path.expanduser('~'))
        self.required_info = self.load_required_info(username)

    def load_required_info(self, username):
        if not os.path.isfile(self.dump_data):
            return None
        json_dump = json.load(open(self.dump_data, 'r'))
        return json_dump.get(username, None)

    def Dump(self):
        if self.required_info is None:
            print("No Log Found!")
        else:
            print(
                "Username    : {}\nPassword    : {}\nAttacked On : {}"
                .format(self.required_info['id'],
                        self.required_info['password'],
                        self.required_info['started']
                        )
            )
        return True

