import os
import sys
import py621
import yaml
from requests_oauthlib import OAuth1

if os.path.isfile('settings.yml') == False:
    print("settings.yml not detected, creating file...")
    settings = open('settings.yml', 'a+')
    settings.write("""
    username : 'Your username here'
    api_key : 'your api key here'
    tags : {"your", "tags", "here"}
    check_tags : True #Whether or not to check if tags are valid
    files_to_download : 320 #Number of posts to download
    download_location : 'folder' #Name of the folder to download to
    mode : E926 #Use 'E621' or 'E926'
    download_pools : False #Whether or not to download all the posts in a pool if a post is part of one
    download_active : False #download pools that are marked as active
    pool_name : True #Set the pool download folder to the pool name
    """)
    settings.close()
    print("Please fill out the file and run this program again.")
    input()
    sys.exit(0)
with open('settings.yml', 'r') as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)
if cfg['username'] == 'Your username here' or cfg["api_key"] == 'your api key here' or cfg["tags"] == [
    "your",
    "tags",
        "here"]:
    print("\nPlease edit the settings.yml file before you continue\n")
    sys.exit(0)
username = cfg['username']
api_key = cfg['api_key']
tags = cfg['tags']
limit = cfg['files_to_download']
download_to = "downloads/" + cfg['download_location']
if cfg['mode'] == 'E621' or cfg['mode'] == 'e621':
    isSafe = False
else:
    isSafe = True
download_pools = cfg['download_pools']
downloadActive = cfg["download_active"]
poolName = cfg["pool_name"]
check = cfg['check_tags']
auth = (username, api_key)
py621.download.downloadPosts(
    isSafe,
    tags,
    limit,
    check,
    auth,
    download_to,
    download_pools,
    downloadActive,
    poolName)

input()
