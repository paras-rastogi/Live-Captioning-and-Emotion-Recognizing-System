from gui import *
from wcloud import *
from gcloud import *
from audioi import *
from threading import Thread
from time import sleep
from gui import color_text, BCOLORS
import sys
from PyQt4 import QtGui, QtCore
from demo import Window

BCOLORS = {
    'Confident': '\033[95m',
    'Joy': '\033[94m',
    'Analytical': '\033[92m',
    'Fear': '\033[93m',
    'Anger': '\033[91m',
    'ENDC': '\033[0m',
    'Sadness': '\033[1m',
    'UNDERLINE': '\033[4m',
    'Tentative': '\033[0;36m'
}


def color_text(text, color=None):
    """
    :desc: Colors the text
    """

    if color is None:
        return text

    return '{0}{1}{2}'.format(BCOLORS[color], text, BCOLORS['ENDC'])


def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())


if __name__=='__main__':
    print color_text('Anger','Anger'),color_text('Fear','Fear'),color_text('Joy','Joy'),color_text('Sadness','Sadness'),color_text('Analytical','Analytical'),color_text('Confident','Confident'),color_text('Tentative','Tentative')

    run()


##    gui_obj.start()
##    mainbackend_obj=Mainbackend(self)
