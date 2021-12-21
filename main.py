import sys
import argparse
from E305.settings import initSettings
from E305.tagsloader import *
from E305.downloader import downloadInstance

parser = argparse.ArgumentParser(
    description='A command line tool used to bulk download images from e621/e926.')
parser.add_argument('-mf', '--mainfile',
                    help='The file containing the list of main tags to download.')
parser.add_argument('-cf', '--commonfile',
                    help='The file containing the list of common tags to download.')
parser.add_argument(
    '-t', '--tags', help='A comma sepreated list of main tags to download. In the format of \'tag1,tag2,tag3\'')
parser.add_argument('-st', '--subtags',
                    help='A comma sepreated list of sub tags to download. In the format of \'tag1,tag2,tag3\'')
args = parser.parse_args()


def main():
    settings = initSettings()
    auth = {"username": settings["username"],
            "api_key": settings["api_key"]
            }
    if (args.mainfile != None) and (args.tags == None):
        maintags = maintagsloader(args.mainfile, 'file')
    elif (args.tags != None) and (args.mainfile == None):
        maintags = maintagsloader(args.tags, 'string')
    else:
        print('Please provide a valid main file or tags. Use -h for help.')
        sys.exit()
    if (args.commonfile != None) and (args.subtags == None):
        subtags = subtagsloader(args.commonfile, 'file')
    elif (args.subtags != None) and (args.commonfile == None):
        subtags = subtagsloader(args.subtags, 'string')
    else:
        print('Please provide a valid common file or subtags. Use -h for help.')
        sys.exit()
    blacklist = loadblacklist()
    E305INST = downloadInstance(
        maintags, subtags, blacklist, auth, settings["limit"], settings["download_path"])


if __name__ == "__main__":
    main()
