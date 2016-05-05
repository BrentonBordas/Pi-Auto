#--Acts as media playback controller and GUI--#
#Pi Auto Media Player created by Todd Farr
#most recent update 3may2016
#
#for use in python3
#command for terminal for changing audio output
#amixer cset numid=3 2 # if using Hdmi output
#1 if using headphones
#

import tkinter as tk
from tkinter import *
from tkinter import ttk # used for formatting , 2.7 might be import ttk 
import pygame, sys, os, random
from functools import partial
from glob import glob

LARGE_FONT = ("Verdana", 12)
global listcount
global f
global test_ary
global current_song
global play_count # used to pause and upause playback

class PiAuto(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Pi Auto")
        
        container= tk.Frame(self) 
        container.pack( side="top", fill="both", expand = True)
       
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        
        self.frames = {}
        
        for F in (StartPage,Playing,
                  Menu, Songs):
                  #External, MediaPlayer, Video): # add all pages and just brings to front 
            frame = F(container, self)
            
            self.frames[F] = frame
            
            frame.grid(row=0, column=0, sticky="nsew")
            
            self.show_frame(StartPage)
        
        os.chdir('/media/pi/MUSIC')# path and name of usb drive
        g = glob('*.mp3') # creates list on mp3 files
        g.extend(glob('*ogg')) # extends list to include ogg files
        g.extend(glob('*.wav')) # extends list to include wav files
        print (g)
        global f
        f = g 
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
        #pygame.init()
        #pygame.display.set_mode(FULLSCREEN)
            ### params  may fix buzzing noise
        listcount = 0            
        ###??? how to destroy windows such as splash screen???###
        
            
        def callback(song):
            global play_count
            #need to store the array index to load a different song 
            self.show_frame(Playing)
            pygame.mixer.music.stop()
            play_count=2
            pygame.mixer.music.load(song) # loads n'th item in list
            pygame.mixer.music.play(0) # playes song one time
            
        #scrollbar = Scrollbar(self.frames[Songs])
        #scrollbar.pack(side=RIGHT, fill=Y)
        #mylist = Listbox(self.frames[Songs], yscrollcommand = scrollbar.set)    
        #global test_ary
        #test_ary = []
        for afile in f:
            temp_count = listcount
            b = "b" + str(listcount)
            b = tk.Button(self.frames[Songs],
                          text=afile,command= partial(callback,
                          f[temp_count]), fg='black', bg='grey').pack()
###            '''test_ary.append(tk.Button(self.frames[Songs],
###                          text=afile,command= partial(callback,
###                          f[temp_count]), fg='black', bg='grey'))'''
            
###            #mylist.insert(END, "buttons" + b)
            print (afile, listcount)
            listcount += 1
        #print(mylist)
        #mylist.pack(side=LEFT, fill = BOTH)
        
    def show_frame(self, cont):    # cont
        
        frame = self.frames[cont]    #cont
        frame.tkraise()     

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)   
        # the following should be formated similar to the text below
        # in three quotes 
        label = ttk.Label(self, text='''
                                    Welcome to the splash screen. 
                                    Pi Auto is a Beta program still in testing 
                                    and will not be liable for any fire, death, 
                                    or bad music played from this device.
                                    Use at your own descretion''') 
        label.pack(pady=10, padx=10)
        
        btn1 = ttk.Button(self, text="Agree",
                          command = lambda:controller.show_frame(Menu))
        btn1.pack()
        
        btn2 = ttk.Button(self, text="Disagree", command = quit)
        btn2.pack()
        
class Menu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        
        btn1 = ttk.Button(self, text="Songs",
                          command = lambda:controller.show_frame(Songs))
        btn1.pack()
        '''btn2 = ttk.Button(self, text="Video",
                          command = lambda:controller.show_frame(Video))
        btn2.pack()
        
        btn3 = ttk.Button(self, text="External",
                          command = lambda:controller.show_frame(External))
        btn3.pack()
        '''
        btn4 = ttk.Button(self, text="Exit", command = quit)
        btn4.pack()
#
#--
#
class Songs(tk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent) 
        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)
        label = ttk.Label(self, text="Songs page")
        label.pack()
        
        def callback_shuffle():
            global f
            global play_count
            controller.show_frame(Playing)
            f_length = len(f)
            print(f_length)
            r_int = random.randint(0,(f_length -1))
            print(r_int)   
            ###
            ###Playing.__init__.label.config(text= f[r_int])
            ###
            pygame.mixer.music.stop()
            play_count=2
            pygame.mixer.music.load(f[r_int]) # loads random item in list
            pygame.mixer.music.play(0)
            self.update_idletasks()
        


        btn1 = ttk.Button(self, text="Shuffle songs",
                          command = callback_shuffle)
        '''global test_ary

        for abutton in test_ary:
            abutton.pack()
            '''
        btn1.pack()
        #scrollbar.config(command = .yview) 


class Playing(tk.Frame): # can i pass song name here for partial
    #command after playing a song via button
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ###string1 = "playing" + str(current_song)###
        song_var = StringVar()
##        song_var.set('Playing the song name you selected')
##        label = ttk.Label(self, textvariable = song_var)
##        label.pack()
##        song_var.set('Playing the song name you selected')
        
        
        def pause():
            global play_count
            if (play_count%2==0):
                pygame.mixer.music.pause()
                play_count += 1
            else:
                pygame.mixer.music.unpause()
                play_count += 1
        def next_song():
            global f
            global play_count
            controller.show_frame(Playing)
            f_length = len(f)
##            print(f_length)
            r_int = random.randint(0,(f_length -1))
##            print(r_int)   
            pygame.mixer.music.stop()
            play_count=2
            pygame.mixer.music.load(f[r_int]) # loads random item in list
            pygame.mixer.music.play(0)

    
        label = ttk.Label(self, text = 'Playing the song name you selected')
        label.pack()
##        self.update_idletasks()
        btn1 = ttk.Button(self, text="Menu",
                          command = lambda:controller.show_frame(Menu))
        btn1.pack()
        btn2 = ttk.Button(self, text="Stop",
                          command = lambda:pygame.mixer.music.stop())
        btn2.pack()
        btn3 = ttk.Button(self, text="Next",
                          command = next_song)
        btn3.pack()    
        btn3 = ttk.Button(self, text="Pause", command = pause)
        btn3.pack()    
        btn4 = ttk.Button(self, text="Exit", command = quit)
        btn4.pack()

     
'''class Video(tk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent) 
        #insert functionality code here
        label = ttk.Label(self, text="Video Page")
        label.pack()
        btn1 = ttk.Button(self, text="Menu",
                          command = lambda:controller.show_frame(Menu))
        btn1.pack()
class External(tk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent) 
        #insert functionality code here
        label = ttk.Label(self, text="External Page")
        label.pack()
        btn1 = ttk.Button(self, text="Menu",
                       command = lambda:controller.show_frame(Menu))
        btn1.pack()
''
class MediaPlayer(tk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent) 
        #insert functionality code here
        
        label = ttk.Label(self, text="page two")
        label.pack()
        btn1 = ttk.Button(self, text="Menu",
                          command = lambda:controller.show_frame(Menu))
        btn1.pack()
'''            
app = PiAuto()
app.mainloop()
