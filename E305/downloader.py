from py621.public import getPosts
from uuid import uuid4
import requests
import os



def createDLlocation(location, name):
    location = location.strip()
    if location[-1] == "/":
        location = location[:-1]
    if not os.path.exists(location+'/'+name):
        os.makedirs(location+'/'+name)
    return location+"/"+name+"/"


def checkBlacklist(tags, blacklist):
    for item in blacklist:
        general = list(tags["general"])
        species = list(tags["species"])
        character = list(tags["character"])
        artist = list(tags["artist"])
        invalid = list(tags["invalid"])
        lore = list(tags["lore"])
        meta = list(tags["meta"])
        copyright = list(tags["copyright"])
        tags = []
        tags = general+species+character+artist+invalid+lore+meta+copyright
        if item in tags:
            return True
    return False


class downloadInstance():
    def __init__(self, maintags, subtags, blacklist, auth, limit, download_path):
        self.maintags = maintags
        self.subtags = subtags
        self.blacklist = blacklist
        self.username = auth.username
        self.api_key = auth.api_key
        self.auth=(self.username, self.api_key)
        self.limit = limit
        self.instanceID = str(uuid4())
        self.header = {'User-Agent': f'E305-Downloader/V0.fuck.versioning.0 (Made by Hunter The Protogen on e621, in use by {self.username} on e621)'}

    def download(self):
        # Begin by making sure the limit does not exceed the limit of the API for a single page. If it does, we split it into pages and save the remainder to use after going through the pages.
        if self.limit > 320:
            pages = self.limit // 320
        else:
            pages = 1
        # For each unique tag, we take it and add it to the main tag list before making the request.
        for subtag in self.subtags:
            tags = self.maintags + subtag
            if pages != 1:
                # We add one to the pages to offset the range function. We also add an extra page to the end of the list to use with remainder from earlier.
                looppages = pages+2
            elif pages == 1:
                # We don't need to do the second part if the limit is below 320.
                looppages = pages+1
            elif pages < 1:
                # What the fuck
                raise ValueError('Limit must be greater than 0.')
            for page in range(1, looppages):
                if page == pages+1:
                    limit = self.limit % 320
                else:
                    limit = self.limit
                posts = getPosts(False, tags, limit, page, True)
                for post in posts:
                    if checkBlacklist(post) != True:
                        url = post["file"]["url"]
                        fileEXT = post["file"]["ext"]
                        r = requests.get(url, auth=self.auth, headers=self.headers)
                        location = createDLlocation(self.location, subtag)
                        with open(location+post["id"]+"."+fileEXT+".download", "wb") as f:
                            f.write(r.content)