import os
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk,Image
from gcloud import S2TConverter, Translate
from audioi import AudioStream
from wcloud import tone_sentiment


root=None
openfileName=None
audtype = None
langtype = None
fileButton = None
textBox = None
aud_type_opt = ["Record", "Upload", "System Audio"]
lang_opt = ["English", "Hindi", "Tamil", "Telgu"]
languages = {"English":'en-US',
             "Hindi":'hi-IN',
             "Tamil":'ta-IN',
             "Telugu":'te-IN',
            }


def listen_print_loop(responses):
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
            message = transcript + overwrite_chars
            data = tone_sentiment(message)
            tones = data['document_tone']['tones']
            if tones:
                print(f'{message}: {tones[0]["tone_name"]}')
            else:
                print(f'{message}: can\'t find tone.')
            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                print('Exiting..')
                break

            num_chars_printed = 0



def start():
    lang = languages[selectedLangtype()]
    aud = selectedAudtype()
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
                listen_print_loop(responses)
        except:
            pass




###################################################### ADD TEXT ##############################################################
def addText(quote):
    global textBox
    textBox.insert(END, " "+quote)
    textBox.see("end")


###################################################### STOP BUTTON ###########################################################
def stopFn():
    exit(0)

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

    # Calling the submit backend
    start()


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
