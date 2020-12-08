import json
from typing import Type
import requests
import time
import os
import math
import fnmatch
import re
import requests_oauthlib

# Custom user agent header for identification within e621
headers = {"User-Agent":"esix-downloader/0.1 (by Hunter The Protogen on e621)"}

def handleCodes(StatusCode):
    if StatusCode == 200:
        return
    else:
        Codes = {
            "403": "Forbidden; Access denied",
            "404": "Not found",
            "412": "Precondition failed",
            "420": "Invalid Record; Record could not be saved",
            "421": "User Throttled; User is throttled, try again later",
            "422": "Locked; The resource is locked and cannot be modified",
            "423": "Already Exists; Resource already exists",
            "424": "Invalid Parameters; The given parameters were invalid",
            "500": "Internal Server Error; Some unknown error occurred on the server",
            "502": "Bad Gateway; A gateway server received an invalid response from the e621 servers",
            "503": "Service Unavailable; Server cannot currently handle the request or you have exceeded the request rate limit. Try again later or decrease your rate of requests.",
            "520": "Unknown Error; Unexpected server response which violates protocol",
            "522": "Origin Connection Time-out; CloudFlare's attempt to connect to the e621 servers timed out",
            "524": "Origin Connection Time-out; A connection was established between CloudFlare and the e621 servers, but it timed out before an HTTP response was received",
            "525": "SSL Handshake Failed; The SSL handshake between CloudFlare and the e621 servers failed"
        }
        raise ConnectionRefusedError("Server connection refused! HTTP Status code: " + str(StatusCode) + " " + Codes[str(StatusCode)])

def isTag(Tag, auth):
    # Since tags can't inherently be NSFW we will always verify tags on e621
    RequestLink = "https://e621.net/tags.json?"
    
    RequestLink += "search[name_matches]="
    RequestLink += Tag

    # Sends the actual request
    eRequest = requests.get(RequestLink, auth=auth, headers=headers)

    # Verify status codes
    handleCodes(eRequest.status_code)

    # Decodes the json into a a list
    eJSON = eRequest.json()

    try:
        # Try to access element name, this throws and error when the tag does not exist or is an alias, check for that in the except
        if eJSON[0]["name"] == Tag:
            print(f"Tag \"{Tag}\" is valid")
            return True
        # If the tag's name isn't the tag, assume it's a fluke on e621's servers and return false
        else:
            return False
    except:
        # Redoing the request to check if it's an alias
        RequestLink = "https://e621.net/tag_aliases.json?"
    
        RequestLink += "search[name_matches]="
        RequestLink += Tag

        # Sends the actual request
        eRequest = requests.get(RequestLink, auth=auth, headers=headers)

        # Verify status codes
        handleCodes(eRequest.status_code)

        # Decodes the json into a a list
        eJSON = eRequest.json()

        try:
            # Try to access element name, this WILL throw and exception if it actually does not exist
            if eJSON[0]["antecedent_name"] == Tag:
                alias = eJSON[0]["consequent_name"]
                print(f"Replacing alias \"{Tag}\" with \"{alias}\"")
                # Return the actual tag
                return alias
                
            # This shouldn't ever happen, but if it does, consider yourself a special snowflake
            else:
                return False
        except:
            if Tag.find(":"):
                return True
            # This tag really does not exist
            return False

# Simple function, returns a list with post
def getPosts(isSafe, Tags, Limit, Page, Check, auth):
    RequestLink = "https://e"

    # Chooses which website to use depending on the isSafe argument
    if isSafe == True:
        RequestLink += "926.net/"
    else:
        RequestLink += "621.net/"
    
    RequestLink += "posts.json?"

    # Gives a limit of post to the api (can be used for per page limits when combined with Page)
    RequestLink += "limit="
    RequestLink += str(Limit)

    # Specifies the page
    RequestLink += "&page="
    RequestLink += str(Page)


    # Handles tag formation
    RequestLink += "&tags="

    for id, Tag in enumerate(Tags):
        if Tag.find(':') == False:

            if Check == True:
                # Check the tag, it could not exist
                TagCheck = isTag(Tag, auth)

                if TagCheck == False:
                    # Tag does not exist, throw an error, this can help devs latter on
                    raise NameError("Tag (" + Tag + ") does not exist!")
                elif TagCheck == True:
                    # Tag exists and isn't an alias, put it on the request
                    RequestLink += Tag
                else:
                    # Tag is an alias, use the actual tag on the request
                    RequestLink += TagCheck
            else:
                # Don't bother with tag checks
                RequestLink += Tag
        else:
            # Don't bother with tag checks
            RequestLink += Tag
        if id != (len(Tags) - 1):
            RequestLink += "+"
    
    # Sends the actual request
    eRequest = requests.get(RequestLink, auth=auth, headers=headers)

    # Verify status codes
    handleCodes(eRequest.status_code)

    # Decodes the json into a a list
    eJSON = eRequest.json()

    # Return post from the previously defined list
    return eJSON["posts"]

def dP(isSafe, Tags, Limit, Page, Check, auth, DownloadLocation, DownloadPools, downloadActive, poolName):
    aPosts = getPosts(isSafe, Tags, Limit, Page, Check, auth)
    lastDownload = None
    queue = len(aPosts)
    print(f"{queue} files added to downloaded queue")
    listpos = 0
    while not listpos == len(aPosts):
        print(f"\n# of files in download queue:\n{queue - listpos}\n")
        aPost = aPosts[listpos] # Select the post from the list

        if not os.path.exists(DownloadLocation):
            os.makedirs(DownloadLocation)
        
        file = str(DownloadLocation+'/'+str(aPost["id"])+"."+aPost["file"]["ext"])
        if os.path.isfile(file) == True:
            fTags = fnmatch.filter(Tags, 'pool:*')
            if DownloadPools == True and not aPost["pools"] == None and not fTags == None:
                print("Post was part of (a) pool(s), downloading the pool(s)")
                PoolNumber = 0
                NumPools = len(aPost["pools"])
                while PoolNumber < NumPools:
                    pool = aPost["pools"]
                    downloadPool(isSafe, pool[PoolNumber], auth, DownloadLocation, downloadActive, poolName)
                    PoolNumber += 1
            else: 
                pass
            listpos += 1
            print(f"{file} already exists, skipping download")
            lastDownload = aPost["id"]
            continue

        print("Downloading post:")
        print(aPost["id"]) # Print the post's ID

        url = aPost["file"]["url"]
        try:
            r = requests.get(url, auth=auth, headers=headers)
        except requests.exceptions.MissingSchema:
            print("Problem downloading file, perhaps it is unavailable in safe mode? Idk what that means but it's what the site says.")
            listpos += 1
            continue


        with open(DownloadLocation+'/'+str(aPost["id"])+"."+aPost["file"]["ext"]+".download", 'wb') as f:
                f.write(r.content)
        os.rename(str(DownloadLocation+'/'+str(aPost["id"])+"."+aPost["file"]["ext"]+".download"),str(DownloadLocation+'/'+str(aPost["id"])+"."+aPost["file"]["ext"]))
        lastDownload = aPost["id"]
        fTags = fnmatch.filter(Tags, 'pool:*')
        if DownloadPools == True and not aPost["pools"] == None and not fTags == None:
            print("Post was part of (a) pool(s), downloading the pool(s)")
            PoolNumber = 0
            NumPools = len(aPost["pools"])
            while PoolNumber < NumPools:
                pool = aPost["pools"]
                downloadPool(isSafe, pool[PoolNumber], auth, DownloadLocation, downloadActive, poolName)
                PoolNumber += 1
        else: 
            pass
        listpos += 1

    print("Finished")
    return lastDownload

def downloadPosts(isSafe, Tags, Limit, Check, auth, DownloadLocation, DownloadPools, downloadActive, poolName):
    bPosts = getPosts(isSafe, Tags, Limit, 1, Check, auth)
    if len(bPosts) < Limit and Limit <= 320:
        print(f"User requested {Limit} files but only {len(bPosts)} files were available with the specified tags")
    if Limit > 320 and len(bPosts) == 320:
        print("Due to E621/E926 restrictions, downloads have to be done in batches when downloading more than 320 files.")
        print(f"Your download will be done in {math.ceil(Limit/320)} batches")
        time.sleep(2.5)
        lDivide = Limit//320
        lRemain = Limit%320
        Page = 1
        while lDivide > 0:
            lastdownload = dP(isSafe, Tags, 320, Page, Check, auth, DownloadLocation, DownloadPools, downloadActive, poolName) 
            Page = "a"+str(lastdownload)
            lDivide -= 1
            time.sleep(1)
        if lRemain > 0:
            dP(isSafe, Tags, lRemain, Page, Check, auth, DownloadLocation, DownloadPools, downloadActive, poolName)

    else:
        dP(isSafe, Tags, Limit, 1, Check, auth, DownloadLocation, DownloadPools, downloadActive, poolName)
        
#def DownloadPool(isSafe, PoolIDs, Limit, Page, Check, auth, DownloadLocation):
#    lastDownload = None
#    listpos = 0
#    try:
#        PoolID = "pool:" + str(PoolIDs[listpos])
#    except:
#        PoolID = "pool:" + str(PoolIDs)
#    aPosts = getPosts(isSafe, PoolID, Limit, Page, Check, auth)
#    queue = len(aPosts)
#    print(f"{queue} files added to downloaded queue")
#
#    while not listpos == len(aPosts):
#        print(f"\n# of files in download queue:\n{queue - listpos}\n")
#        aPost = aPosts[listpos] # Select the post from the list
#
#        if not os.path.exists(DownloadLocation):
#            os.makedirs(DownloadLocation)
#        
#        file = str(DownloadLocation+'/'+str(aPost["id"])+"."+aPost["file"]["ext"])
#        if os.path.isfile(file) == True:
#            listpos += 1
#            print(f"{file} already exists, skipping download")
#            lastDownload = aPost["id"]
#            continue
#
#        print("Downloading post:")
#        print(aPost["id"]) # Print the post's ID
#
#        url = aPost["file"]["url"]
#        try:
#            r = requests.get(url, auth=auth, headers=headers)
#        except requests.exceptions.MissingSchema:
#            print("Problem downloading file, perhaps it is unavailable in safe mode? Idk what that means but it's what the site says.")
#            listpos += 1
#            continue
#
#
#        with open(DownloadLocation+'/'+str(aPost["id"])+"."+aPost["file"]["ext"]+".download", 'wb') as f:
#                f.write(r.content)
#        os.rename(str(DownloadLocation+'/'+str(aPost["id"])+"."+aPost["file"]["ext"]+".download"),str(DownloadLocation+'/'+str(aPost["id"])+"."+aPost["file"]["ext"]))
#        lastDownload = aPost["id"]
#
#        listpos += 1
#
#    print("Finished")
#    return lastDownload

def getPoolPosts(isSafe, PoolID, auth):
    RequestLink = "https://e"

    # Chooses which website to use depending on the isSafe argument
    if isSafe == True:
        RequestLink += "926.net/"
    else:
        RequestLink += "621.net/"
    
    RequestLink += "pools.json?"

    # Gives a limit of post to the api (can be used for per page limits when combined with Page)
    RequestLink += "limit=320"

    RequestLink += "?&search[id]=" + str(PoolID)
    
    # Sends the actual request
    eRequest = requests.get(RequestLink, auth=auth, headers=headers)

    # Verify status codes
    handleCodes(eRequest.status_code)

    # Decodes the json into a a list
    eJSON = eRequest.json()

    # Return post from the previously defined list
    return eJSON

def downloadPool(isSafe, PoolID, auth, DownloadLocation, downloadActive, poolName):
    pool = getPoolPosts(isSafe, PoolID, auth)
    post_ids = pool[0]["post_ids"]
    numPosts = len(post_ids)
    positionNum = 0
    active = pool[0]["is_active"]
    if downloadActive == False and active == True:
        return

    while positionNum < numPosts:
        postId = post_ids[positionNum]
        tag = "id:" + str(postId)
        downloadPosts = getPosts(False, tag, 1, 1, False, auth)
        try:
            downloadPost = downloadPosts[0]
        except:
            downloadPost = downloadPosts
        try:
            url = downloadPost["file"]["url"]
        except:
            positionNum += 1
            continue
        try:
            r = requests.get(url, auth=auth, headers=headers)
        except requests.exceptions.MissingSchema:
            print("Problem downloading file, perhaps it is unavailable in safe mode? Idk what that means but it's what the site says.")
            positionNum += 1
            continue
        except:
            print("Problem downloading file")
            positionNum += 1
            continue

        if poolName == True:
            name = re.sub('[^\w\-_\. ]', '_', str(pool[0]["name"])) 
            DownloadFolder = DownloadLocation+'/'+name+'/'+PoolID
        else:
            DownloadFolder = DownloadLocation+'/'+PoolID

        pid = downloadPost["id"]
        print(f"Downloading post {pid}")

        page = positionNum + 1
        with open(DownloadFolder+'/'+"Page "+page+" "+str(downloadPost["id"])+"."+downloadPost["file"]["ext"]+".download", 'wb') as f:
                f.write(r.content)
        os.rename(str(DownloadFolder+'/'+"Page "+page+" "+str(downloadPost["id"])+"."+downloadPost["file"]["ext"]+".download"),str(DownloadFolder+'/'+"Page "+page+" "+str(downloadPost["id"])+"."+downloadPost["file"]["ext"]))
        positionNum += 1
    else:
        print("Pool finished downloading")
        return