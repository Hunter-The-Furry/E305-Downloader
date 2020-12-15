import sys
import py621
import yaml
from requests_oauthlib import OAuth1

def runPy621():
    with open('settings.yml', 'r') as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
    if cfg['username'] == 'Your username here' or cfg["api_key"] == 'your api key here' or cfg["tags"] == ["your", "tags", "here"]:
        print("\nPlease edit the settings.yml file before you continue\n")
        sys.exit(0)
    username = cfg['username']
    api_key = cfg['api_key']
    tags = cfg['tags']
    limit = cfg['files_to_download']
    download_to = "downloads/"+cfg['download_location']
    if cfg['mode'] == 'E621' or cfg['mode'] == 'e621':
        isSafe = False
    else:
        isSafe = True
    download_pools = cfg['download_pools']
    downloadActive = cfg["download_active"]
    poolName = cfg["pool_name"]
    check = cfg['check_tags']
    auth = (username, api_key)
    py621.download.downloadPosts(isSafe, tags, limit, check, auth, download_to, download_pools, downloadActive, poolName)