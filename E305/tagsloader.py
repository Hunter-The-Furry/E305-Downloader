import re


def maintagsloader(filename, type):
    """
    Loads the maintags from a file or string file and returns a list of all the tags.
    """
    if type == 'file':
        with open(filename, 'r') as f:
            maintags = f.read().splitlines()
    elif type == 'string':
        maintags = filename.split(",")
    maintags = list(map(str.strip, maintags))
    maintags = list(filter(None, maintags))
    return maintags


def subtagsloader(filename, type):
    """
    Loads the subtags from a file or string and returns a list of all the tags.
    """
    if type == 'file':
        with open(filename, 'r') as f:
            subtags = f.read().splitlines()
    elif type == 'string':
        subtags = filename.split(",")
    subtags = list(map(str.strip, subtags))
    subtags = list(filter(None, subtags))
    return subtags


def loadblacklist():
    blacklistDirty = open("./settings/blacklist.txt", 'r').readlines()
    blacklist = []
    for line in blacklistDirty:
        line = re.sub('\s+', ' ', line).strip()
        line = str(line)
        if line[:1] == "#":
            continue
        blacklist.append(line)
    return blacklist
