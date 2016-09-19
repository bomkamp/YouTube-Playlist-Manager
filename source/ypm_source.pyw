#!/usr/bin/python
# -*- coding: utf-8 -*-
#@AUTHOR: Greg Bomkamp
#@Date: 9/12/2016
#@REQUIRES: Most modules are installed with python 3.5 but may need to use pip to install: youtube_dl, pillow, tkinter. May need to download libav most recent version and extract the contents of downloaded /usr/bin/ to the same directory as youtube_dl.py for it to convert to mp3.
#@INPUT: Directory to a folder, URL to a YouTube video or playlist
#@OUTPUT: A set of .mp3 files (one pulled from each video in the playlist) downloaded to the directory given in INPUT.

#This software was written to practice using python libraries and is not intended for use to delibrately break YouTube ToS or for commercial purposes.
#Multiple imports of same packages allow application support
import tkinter
from tkinter import *
import os,sys,youtube_dl,ctypes
from PIL import Image, ImageTk
#explicit import due to runtime errors
from tkinter import filedialog
from youtube_dl import *

class YPM:

    #initial elements to create when starting application
    def __init__(self, master):

        self.frameStart = Frame(master)
        self.frameDone = Frame(master)
        self.startDir=os.getcwd()
        self.errors=0
        self.Ready()

    def Ready(self):
        #prepare frame
        try:
            self.status.grid_forget()
        except:
            pass
        self.frameStart.grid_forget()
        self.frameDone.grid_forget()
        self.frameStart.grid(padx=10,pady=10)
        
        #prepare logo image for initial window.
        image=Image.open(self.startDir+"/YouTube-96.png")
        img = ImageTk.PhotoImage(image)
        SplashLogo = Label(self.frameStart,image=img)
        SplashLogo.image = img

        #Prepare directory selection
        self.dirBox = Entry(self.frameStart,width=35)
        self.dirBox.delete(0,END)
        self.dirBox.insert(0,"MP3 download folder path...")
        self.buttonFileExplorer = Button(self.frameStart,text="...",command=self.Get_file_location)
        
        #prepare box to paste youtube playlist URL
        self.linkBox = Entry(self.frameStart,width=35)
        self.linkBox.delete(0,END)
        self.linkBox.insert(0,"")
        
        #start and exit button
        self.start = Button(self.frameStart,text="Start",command=self.Check_path,width=10) #update function here for starting code
        exitButton = Button(self.frameStart,text="Exit",command=self.frameStart.quit,width=10)

        #move elements into a nicer layout
        self.frameStart.columnconfigure(0, weight=0)
        self.frameStart.rowconfigure(1, weight=2,pad=10)
        SplashLogo.grid(row=1,column=0,columnspan=2,rowspan=2)
        Label(self.frameStart, text="Download Folder: ").grid(row=3)
        Label(self.frameStart, text="YouTube Playlist URL: ").grid(row=4,sticky=E)
        self.dirBox.grid(row=3,column=1,padx=10)
        self.buttonFileExplorer.grid(row=3,column=2)
        self.linkBox.grid(row=4,column=1)
        self.start.grid(row=5,column=1,pady=7,columnspan=2)
        exitButton.grid(row=5,column=0,pady=7,columnspan=2)
        root.update()
        
    #method to redirect the mainloop depending on whether to download path is acceptable
    def Check_path(self):
        URL=self.linkBox.get()
        DLs=self.dirBox.get()
        try:
            os.chdir(DLs)
            self.Download_playlist()
        except:
            ctypes.windll.user32.MessageBoxW(None,"Error opening download directory. Please check your path.","ERROR", 0)
            self.Ready()

    #create a method to bring up a directory explorer to select a download location
    def Get_file_location(self):
        directory = filedialog.askdirectory(initialdir='~/')
        self.dirBox.delete(0,END)
        self.dirBox.insert(0,directory)

    def Download_playlist(self):
        #grab information from GUI for processing
        URL=self.linkBox.get()
        DLs=self.dirBox.get()

        #check selected download directory for a log folder if DNE: create it with log file
        if os.path.exists('./.log'):
            pass
        else:
            os.mkdir('./.log')
        #open log file: if it exists do not overwrite    
        self.log=open("./.log/log.txt", "a+")
        self.log.close()

        #Clear current frame and create new display elements to make more clean
        self.frameDone.grid_forget()
        self.frameStart.grid_forget()
        self.frameDone.grid(padx=120,pady=60)
        restartButton = Button(self.frameDone,text="New Playlist",command=self.Ready)
        exitButton = Button(self.frameDone,text="Exit",command=self.frameStart.quit,width=10)
        self.status = Label(self.frameDone,text="Working...")

        #Place new elements onto frame.
        self.status.grid(row=3,column=3,columnspan=2,rowspan=2)
        exitButton.grid(row=5,column=2,columnspan=2,rowspan=2)
        restartButton.grid(row=5,column=4,columnspan=2,rowspan=2)

        #update to make new display appear showing that processing was started.
        root.update()

        #define how to download mp3s - this is specific format for youtube_dl.py
        ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio':True,
            'quiet':True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'download_archive': DLs+'/.log/log.txt',
        }
        
        #begin processing the link that was provided

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([URL])
            self.status.config(text='Done!')
        except Exception as e:
            ctypes.windll.user32.MessageBoxW(None,repr(e),"ERROR", 0)
            self.status.config(text='Errors appear to have occurred. \nCheck your YouTube Playlist link and \ninternet connection then try again.')
            pass
#necessary for the application lifecycle to start
root = Tk()
root.wm_title('YouTube Playlist MP3 Manager')
root.maxsize(400,200)
root.minsize(400,200)
img = ImageTk.PhotoImage(file='yt.ico')
root.tk.call('wm', 'iconphoto',root._w,img)
app=YPM(root)

root.mainloop()
try:
    #if its already been close this wont need to be done
    root.destroy()
except:
    pass
