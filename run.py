import os
import sys
import py621
import yaml

if os.path.isfile('settings.yml') == False:
    print("settings.yml not detected, creating file...")
    settings = open('settings.yml', 'a+')
    settings.write("""
    username : 'Your username here'
    api_key : 'your api key here'
    tags : {"your", "tags", "here"}
    files_to_download : 320 #Number of posts to download
    download_location : 'folder' #Name of the folder to download to
    mode : E926 #Use 'E621' or 'E926'
    """)
    settings.close()
    print("Please fill out the file and run this program again.")
    sys.exit(0)
with open('settings.yml', 'r') as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)
if cfg['username'] == 'Your username here' or cfg["api_key"] == 'your api key here' or cfg["tags"] == ["your", "tags", "here"]:
    print("\nPlease edit the settings.yml file before you continue\n")
    sys.exit(0)
username = cfg['username']
api_key = cfg['api_key']
tags = cfg['tags']
limit = 327
download_to = "downloads/"+cfg['download_location']
if cfg['mode'] == 'E621' or cfg['mode'] == 'e621':
    SFW = False
else:
    SFW = True
py621.public.downloadPosts(SFW, tags, limit, True, username, api_key, download_to)