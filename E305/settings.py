import os


def initSettings():
    if not os.path.isdir("./settings"):
        os.mkdir("settings")
    if not os.path.isfile("settings/settings.yml"):
        settings = open('settings/settings.yml', 'a+')
        settings.write("""
        username : None
        api_key : None
        """)
        settings.close()
    if not os.path.isfile("settings/blacklist.txt"):
        Blacklist = open("settings/blacklist.txt", 'a+')
        Blacklist.write("""
        \# List of all locally blacklisted tags. One tag per line.
                        """)
        Blacklist.close()
