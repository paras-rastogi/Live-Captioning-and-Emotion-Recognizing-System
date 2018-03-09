from gui import *
from wcloud import *
from gcloud import *
from audioi import *
from threading import Thread
from time import sleep
import multiprocessing as mp
GUI()
##mainbackend_obj=None
##def test(gui_obj):
##    global mainbackend_obj
##    mainbackend_obj.gui_obj=gui_obj
##    mainbackend_obj.start()
##class MainGUI(GUI):
##    
##    def submitFn(self):
##        GUI.submitFn(self)
####        sleep(1)
##        test(self)
##        
##
##
##
##
##class Mainbackend(Thread):
##    def __init__(self):
##        Thread.__init__(self)
##        self.gui_obj=None
##    def run(self):
##        while(1):
##            a=input("number: ")
##            print(a)
##            self.gui_obj.addText(a)
##
##
##if __name__=='__main__':
##    mainbackend_obj=Mainbackend()
##    gui_obj=MainGUI()
##    
##    gui_obj.start()
####    mainbackend_obj=Mainbackend(self)
##
##    
