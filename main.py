from gui import *
from wcloud import *
from gcloud import *
from audioi import *
from threading import Thread
from time import sleep
import multiprocessing as mp
from gui import color_text, BCOLORS
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
##mainbackend_obj=None
##def test(gui_obj):
##    global mainbackend_obj
##    mainbackend_obj.gui_obj=gui_obj
##    mainbackend_obj.start()
class MainGUI(GUI):

    def submitFn(self):
        GUI.submitFn(self)
##        sleep(1)
        mainback_obj=Mainbackend(self)
        mainback_obj.run1()




class Mainbackend():
    def __init__(self, gui_obj):
        self.gui_obj=gui_obj
    def run1(self):

##            a=input("number: ")
##            print(a)
        lang = languages[self.gui_obj.selectedLangtype()]
        aud = self.gui_obj.selectedAudtype()
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
##        self.gui_obj.addText()
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
                message = transcript + overwrite_chars
                lang = self.gui_obj.selectedLangtype()
                if lang != 'English':
                    obj = Translate(languages[lang])
                    temp = obj.translate(message)
                    data = tone_sentiment(temp)
                    tones = data['document_tone']['tones']
                else:
                    data = tone_sentiment(message)
                    tones = data['document_tone']['tones']
                    if tones:
                        print(message,':',tones[0]["tone_name"])
                    else:
                        print(message,': can\'t find tone.')
                # Exit recognition if any of the transcribed phrases could be
                # one of our keywords.
                if re.search(r'\b(exit|quit)\b', transcript, re.I):
                    print('Exiting..')
                    break

                num_chars_printed = 0
def color_text(text, color=None):
    """
    :desc: Colors the text
    """

    if color is None:
        return text

    return '{0}{1}{2}'.format(BCOLORS[color], text, BCOLORS['ENDC'])
if __name__=='__main__':
    print(color_text('Anger','Anger'),color_text('Fear','Fear'),color_text('Joy','Joy'),color_text('Sadness','Sadness'),color_text('Analytical','Analytical'),color_text('Confident','Confident'),color_text('Tentative','Tentative'))
    gui_obj=MainGUI()
    mainbackend_obj=Mainbackend(gui_obj)


##    gui_obj.start()
##    mainbackend_obj=Mainbackend(self)
