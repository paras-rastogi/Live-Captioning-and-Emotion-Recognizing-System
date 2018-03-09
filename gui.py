import os
from Tkinter import *
import tkFileDialog
from PIL import ImageTk,Image
from gcloud import S2TConverter, Translate
from audioi import AudioStream
from wcloud import tone_sentiment
from threading import Thread
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

aud_type_opt = ["Record", "Upload", "System Audio"]
from languages import languages, lang_opt


########################################################## CREATE GUI ################################################################
class GUI():
    def __init__(self):
        self.root = Tk()
        self.root.title("CAPTION")
        #root.state('zoomed')                               #for windows
        #root.attributes("-zoomed", True)                   #for linux
        ############################# TOP LABELS ####################################
        self.lanLabel = Label(self.root, text='Language')
        self.lanLabel.grid(row=0, column=0, padx=2, pady=2)
        self.langtype = StringVar(self.root)
        self.langtype.set(lang_opt[0])                                           # default value
        self.langSelect = OptionMenu(self.root, self.langtype, *lang_opt)
        self.langSelect.grid(row=0, column=1, padx=2, pady=2)
        self.audLabel = Label(self.root, text='Audio Input Type')
        self.audLabel.grid(row=1, column=0, padx=2, pady=2)
        self.audtype = StringVar(self.root)
        self.audtype.set(aud_type_opt[0])                                        # default value
        self.audSelect = OptionMenu(self.root, self.audtype, *aud_type_opt, command = self.visibilityControl)
        self.audSelect.grid(row=1, column=1, padx=2, pady=2)
        self.fileButton = Button(text='Select Audio File', command=self.getFile)
        self.fileButton.grid(row=3, column=0, padx=2, pady=2)
        self.fileButton.grid_remove()
        self.submitButton = Button(self.root, text='Submit', command=self.submitFn)
        self.submitButton.grid(row=4, column=0)
        self.stopButton = Button(self.root, text='Stop', command=self.stopFn)
        self.stopButton.grid(row=4, column=1)
        self.root.mainloop()
##        t=Thread(self.root.mainloop())
##        t.daemon = True # this line tells the thread to quit if the GUI (master thread) quits.
##        t.start()

        self.textBox = None
        self.openfileName = None

    def addText(self, quote):
        self.textBox.insert(END, " "+quote)
        self.textBox.see("end")

    def stopFn(self):
        self.root.destroy()
        exit(0)


    def submitFn(self):
        display = Tk()
        scroll = Scrollbar(display)
        scroll.pack(side=RIGHT, fill=Y)
        self.textBox = Text(display, height=4, width=50, wrap=WORD, yscrollcommand=scroll.set)
    ##    scroll.pack(side=RIGHT, fill=Y)
        self.textBox.pack(side=LEFT, fill=Y)
        self.textBox.tag_configure("center", justify='center')
    ##    scroll.config(command=textBox.yview)
    ##    textBox.config(yscrollcommand=scroll.set)
        quote = "Starting Captioning\n"
        self.textBox.insert(END, quote)
        self.textBox.see("end")
        start(self)



    def getFile(self):
        self.openfileName = tkFileDialog.askopenfilename(initialdir = os.getcwd, title = "Select file", filetypes = (("mp3 files","*.mp3"),("wav files","*.wav")))
        if (not openfileName):
            return
        print openfileName



    def visibilityControl(self, x):
        if x=='Upload':
            self.fileButton.grid()
        else:
            self.fileButton.grid_remove()
        return self.audtype.get()



    def selectedAudtype(self):
        return self.audtype.get()



    def selectedLangtype(self):
        return self.langtype.get()

def listen_print_loop(self, responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()
            num_chars_printed = len(transcript)

        else:
            tones = None
            message = transcript + overwrite_chars
            lang = self.selectedLangtype()
            # if lang != 'English':
            obj = Translate(languages[lang])
            temp = obj.translate(message)
            data = tone_sentiment(temp)
            tones = data['document_tone']['tones']
            # else:
            #     data = tone_sentiment(message)
            #     tones = data['document_tone']['tones']
            if tones:
                print color_text(message,tones[0]["tone_name"])
            else:
                print color_text(message, 'Tentative')
            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                print 'Exiting..'
                break

            num_chars_printed = 0



def start(self):
    lang = languages[self.selectedLangtype()]
    aud = self.selectedAudtype()
    audInpCode = 6
    RATE = 16000
    CHUNK = int(RATE/10) # (int(RATE)/10)
    if aud == "Record":
        audInpCode = 6
    elif aud == "System Audio":
        audInpCode = 12

    conv = S2TConverter(RATE, lang)
    streaming_config = conv.get_streaming_config()
    while True:
        try:
            with AudioStream(RATE, CHUNK, audInpCode) as stream:
                responses = conv.get_responses(stream)
                listen_print_loop(self, responses)
        except:
            pass
