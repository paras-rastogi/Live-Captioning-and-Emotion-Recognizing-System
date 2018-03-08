import os
import cv2
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk,Image
import numpy as np

root=None
openfileName=None
audtype = None
langtype = None
fileButton = None
textBox = None
aud_type_opt = ["Record", "Upload", "System Audio"]
lang_opt = ["English", "Hindi", "Tamil", "Telgu"]


###################################################### ADD TEXT ##############################################################
def addText(quote):
    global textBox
    textBox.insert(END, " "+quote)
    textBox.see("end")


###################################################### STOP BUTTON ###########################################################
def stopFn():
    return

###################################################### SUBMIT BUTTON ###########################################################
def submitFn():
    global textBox
    display = Tk()
    scroll = Scrollbar(display)
    scroll.pack(side=RIGHT, fill=Y)
    textBox = Text(display, height=4, width=50, wrap=WORD, yscrollcommand=scroll.set)
##    scroll.pack(side=RIGHT, fill=Y)
    textBox.pack(side=LEFT, fill=Y)
    textBox.tag_configure("center", justify='center')
##    scroll.config(command=textBox.yview)
##    textBox.config(yscrollcommand=scroll.set)
    quote = "Starting Captioning\n"
    textBox.insert(END, quote)
    textBox.see("end")

    
###################################################### OPENING AUDIO FILE ###########################################################
def getFile():
    global openfileName,ipPanel,opPanel,imx,imy,ipimg,opimg
    openfileName = filedialog.askopenfilename(initialdir = os.getcwd, title = "Select file", filetypes = (("mp3 files","*.mp3"),("wav files","*.wav")))
    if (not openfileName):
        return
    print(openfileName)


####################################################### VISIBILITY ##################################################################
def visibilityControl(x):
    global fileButton
    if x=='Upload':
        fileButton.grid()
    else:
        fileButton.grid_remove()
    return audtype.get()

    
####################################################### FUNCTION FOR AUDIO TYPE #####################################################
def selectedAudtype():
    global audtype
    return audtype.get()


################################################### FUNCTION FOR LANGUAGE TYPE #####################################################
def selectedLangtype():
    global langtype
    return langtype.get()
    

########################################################## CREATE GUI ################################################################
def createGUI():
    global root, openfileName, audtype, langtype, fileButton
    root = Tk()
    root.title("CAPTION")
    #root.state('zoomed')                               #for windows
    #root.attributes("-zoomed", True)                   #for linux
    ############################# TOP LABELS ####################################
    lanLabel = Label(root, text='Language')
    lanLabel.grid(row=0, column=0, padx=2, pady=2)
    langtype = StringVar(root)
    langtype.set(lang_opt[0])                                           # default value
    langSelect = OptionMenu(root, langtype, *lang_opt)
    langSelect.grid(row=0, column=1, padx=2, pady=2)
    audLabel = Label(root, text='Audio Input Type')
    audLabel.grid(row=1, column=0, padx=2, pady=2)
    audtype = StringVar(root)
    audtype.set(aud_type_opt[0])                                        # default value
    audSelect = OptionMenu(root, audtype, *aud_type_opt, command = visibilityControl)
    audSelect.grid(row=1, column=1, padx=2, pady=2)
    fileButton = Button(text='Select Audio File', command=getFile)
    fileButton.grid(row=3, column=0, padx=2, pady=2)
    fileButton.grid_remove()
    submitButton = Button(root, text='Submit', command=submitFn)
    submitButton.grid(row=4, column=0)
    stopButton = Button(root, text='Stop', command=stopFn)
    stopButton.grid(row=4, column=1)
    root.mainloop()
