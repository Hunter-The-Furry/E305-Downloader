import os
import py621
import sys
import tkinter
from tkinter import messagebox
from tkinter import filedialog
import yaml

if os.path.isfile('settings.yml') == False:
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
    with open('settings.yml', 'r') as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
    downLoc = cfg['download_location']
class e621Downloader:
    def __init__(self):
        with open('settings.yml', 'r') as f:
            cfg = yaml.load(f, Loader=yaml.FullLoader)
        downLoc = cfg['download_location']
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
        self.folder_label = tkinter.Label(self.frameTwo, text = f'Current download location: {downLoc}')
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
        #This method converts kilometers into miles

    def yamlRead(self):
        with open('settings.yml', 'r') as f:
            self.cfg = yaml.load(f, Loader=yaml.FullLoader)

    def yamlWrite(self, writeData):
        with open('settings.yml', 'w') as f:
            self.cfg = yaml.dump(writeData, f)


    def folderSelect(self):
        self.downloadLocation = filedialog.askdirectory(title = 'Select Download Folder')
        download_location = str(self.downloadLocation)
        pog = {'download_location': download_location}
        with open('settings.yml', 'a') as f:
            data = yaml.dump(pog, f)
    def update(self):
        kilo = float(self.entry.get())
        miles = kilo * 0.6214
        messagebox.showinfo('Results', str(kilo)+ ' kilometers is equal to ' + str(miles) + ' miles')
    def runDownloader(self):
        py621.run.runPy621()
gui = e621Downloader()