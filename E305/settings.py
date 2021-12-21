import os
import yaml


def initSettings():
    if os.path.isfile("./settings/settings.yml"):
        with open('./settings/settings.yml', 'r') as f:
            settings = yaml.load(f, Loader=yaml.FullLoader)
            auth = settings
    if not os.path.isdir("./settings"):
        os.mkdir("settings")
    if not os.path.isfile("settings/settings.yml"):
        username = input(
            "Please input your username: ")
        api_key = input(
            "To enable API access, you must go to your profile page (Account > My profile) and generate an API key, provide that key here: ")
        while True:
            try:
                limit = int(input(
                    "Please input the limit on the number of images to download: "))
                break
            except ValueError:
                print("Invalid input. Please input an integer.")
        download_path = input(
            "Please input the main to place the downloaded subfolder into: ")
        settings = open('settings/settings.yml', 'a+')
        settings.write("""
        username : {}
        api_key : {}
        limit : {}
        download_path : {}
        """.format(str(username), str(api_key), int(limit), str(download_path)))

        settings.close()
        with open('./settings/settings.yml', 'r') as f:
            settingsyaml = yaml.load(f, Loader=yaml.FullLoader)
            auth = settingsyaml

    if not os.path.isfile("settings/blacklist.txt"):
        Blacklist = open("settings/blacklist.txt", 'a+')
        Blacklist.write(
            """# List of all locally blacklisted tags. One tag per line.""")
        Blacklist.close()

    return(auth)
