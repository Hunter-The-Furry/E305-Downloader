import os
import py621
import sys
import tkinter
from tkinter import messagebox
from tkinter import filedialog
import yaml

if os.path.isfile('settings.yml') == False:
    downloadPath = os.path.join( os.getenv('USERPROFILE'), 'Downloads')
    settings = open('settings.yml', 'a+')
    settings.write(f"""
    username : 'Your username here'
    api_key : 'your api key here'
    tags : {{"your", "tags", "here"}}
    check_tags : True #Whether or not to check if tags are valid
    files_to_download : 320 #Number of posts to download
    download_path : {downloadPath}
    download_location : 'Folder'
    mode : E926 #Use 'E621' or 'E926'
    download_pools : False #Whether or not to download all the posts in a pool if a post is part of one
    download_active : False #download pools that are marked as active
    pool_name : True #Set the pool download folder to the pool name
    """)
    settings.close()

class e621Downloader:
    with open('settings.yml', 'r') as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
    username = cfg['username']
    apiKey = cfg['api_key']
    tags = cfg['tags']
    checkTags = cfg['check_tags']
    filesDownload = cfg['files_to_download']
    downloadLocation = cfg['download_location']
    mode = cfg['mode'] 
    downloadPools = cfg['download_pools']
    downloadActive = cfg['download_active']
    poolName = cfg['pool_name']

    def __init__(self):
        #create root window
        self.root = tkinter.Tk()
        #Create two frames
        #One frame for the top of the window
        #Another frame for bottom of the window
        self.frameOne = tkinter.Frame(self.root)
        self.frameTwo = tkinter.Frame(self.root)
        self.frameThree = tkinter.Frame(self.root)
        #Create two labels
        self.prompt_label = tkinter.Label(self.frameOne, text = 'Enter tags in a comma seperated list: ')
        self.entry = tkinter.Entry(self.frameOne, width = 100)
        self.folder_button = tkinter.Button(self.frameTwo, text = 'Downloads Location', command = self.folderSelect)
        self.folder_label = tkinter.Label(self.frameTwo, text = f'Current download location: {self.downloadLocation}')
        #Pack top frame widgets
        self.folder_button.pack(side = 'left')
        self.folder_label.pack(side = 'left')
        self.prompt_label.pack(side = 'left')
        self.entry.pack(side = 'left')
        #Create the button widgets
        self.run_button = tkinter.Button(self.frameThree, text = 'Run download', command = self.runDownloader)
        self.update_button = tkinter.Button(self.frameThree, text = 'Update settings', command = self.update)
        #root.destroy exits/destroys the main window
        self.quit_button = tkinter.Button(self.frameThree, text = 'Quit', command = self.root.destroy)
        #Pack the buttons
        self.run_button.pack()
        self.update_button.pack(side = 'left')
        self.quit_button.pack(side = 'left')
        
        #Now pack the frames also
        self.frameOne.pack()
        self.frameTwo.pack()
        self.frameThree.pack()
        tkinter.mainloop()

    def folderSelect(self):
        self.downloadLocation = filedialog.askdirectory(title = 'Select Download Folder')

    def update(self):
        tagsF = "{" + self.tags + "}"
        writeData = f"""
        username : {self.username}
        api_key : {self.apiKey}
        tags : {tagsF}
        check_tags : {self.checkTags}
        files_to_download : {self.filesDownload}
        download_location : {self.downloadLocation}
        mode : {self.mode}
        download_pools : {self.downloadPools} 
        download_active : {self.downloadActive}
        pool_name : {self.poolName}
        """
        try:
            with open('settings.yml', 'w') as f:
                self.cfg = yaml.dump(writeData, f)
        except:
            messagebox.showinfo('Error', "An error has occurred while trying to update your settings")

    def resetOptions(self):
        with open('settings.yml', 'r') as f:
            cfg = yaml.load(f, Loader=yaml.FullLoader)
        self.username = cfg['username']
        self.apiKey = cfg['api_key']
        self.tags = cfg['tags']
        self.checkTags = cfg['check_tags']
        self.filesDownload = cfg['files_to_download']
        self.downloadLocation = cfg['download_location']
        self.mode = cfg['mode'] 
        self.downloadPools = cfg['download_pools']
        self.downloadActive = cfg['download_active']
        self.poolName = cfg['pool_name']
        
    def runDownloader(self):
        py621.run.runPy621()
gui = e621Downloader()