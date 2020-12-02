import json
from typing import Type
import requests
import time
import os
import math

# Custom user agent header for identification within e621
headers = {"User-Agent":"esix-offline/0.1 (by Intoxicated_Furry on e621)"}

def handleCodes(StatusCode):
    if StatusCode == 200:
        return
    else:
        raise ConnectionRefusedError("Server connection refused! HTTP Status code: " + str(StatusCode))

def isTag(Tag):
    # Since tags can't inherently be NSFW we will always verify tags on e621
    RequestLink = "https://e621.net/tags.json?"
    
    RequestLink += "search[name_matches]="
    RequestLink += Tag

    # Sends the actual request
    eRequest = requests.get(RequestLink, headers=headers)

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
        eRequest = requests.get(RequestLink, headers=headers)

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
                print(f"Unable to check tag \"{Tag}\"")
                return True
            # This tag really does not exist
            return False

# Simple function, returns a list with post
def getPosts(isSafe, Tags, Limit, Page, Check, Username, ApiKey):
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
        if Check == True:
            # Check the tag, it could not exist
            TagCheck = isTag(Tag)

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
        
        if id != (len(Tags) - 1):
            RequestLink += "+"
    
    # Sends the actual request
    eRequest = requests.get(RequestLink, auth=(Username, ApiKey), headers=headers)

    # Verify status codes
    handleCodes(eRequest.status_code)

    # Decodes the json into a a list
    eJSON = eRequest.json()

    # Return post from the previously defined list
    return eJSON["posts"]

def dP(isSafe, Tags, Limit, Page, Check, Username, ApiKey, DownloadLocation):
    aPosts = getPosts(isSafe, Tags, Limit, Page, Check, Username, ApiKey)
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
            listpos += 1
            print(f"{file} already exists, skipping download")
            break

        print("Downloading post:")
        print(aPost["id"]) # Print the post's ID

        url = aPost["file"]["url"]

        r = requests.get(url)



        with open(DownloadLocation+'/'+str(aPost["id"])+"."+aPost["file"]["ext"], 'wb') as f:
                f.write(r.content)
        lastDownload = aPost["id"]
        
        listpos += 1

    print("Finished")
    return lastDownload

def downloadPosts(isSafe, Tags, Limit, Check, Username, ApiKey, DownloadLocation):
    bPosts = getPosts(isSafe, Tags, Limit, 1, Check, Username, ApiKey)
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
            try:
                lastdownload = dP(isSafe, Tags, 320, Page, Check, Username, ApiKey, DownloadLocation) 
                if lastdownload == None:
                    raise NameError("Variable lastDownload returned None when it should have returned an ID")
                Page = "a"+str(lastdownload)
                lDivide -= 1
                time.sleep(1)
            except:
                if input("Try again? (Y/N)") == "Y":
                    downloadPosts(isSafe, Tags, Limit, Check, Username, ApiKey, DownloadLocation)
                else:
                    return
        if lRemain > 0:
            dP(isSafe, Tags, lRemain, Page, Check, Username, ApiKey, DownloadLocation)

    else:
        dP(isSafe, Tags, Limit, 1, Check, Username, ApiKey, DownloadLocation)
        