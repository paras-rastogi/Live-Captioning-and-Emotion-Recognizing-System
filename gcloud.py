from google.cloud import speech, translate
from google.cloud.speech import enums, types
import pyaudio


"""
## This class is for all the API calls to google cloud for speech to text conversion.
@ param: rate: Sampling rate of the audio in HERTZ
@ param: language: language in which speech is sent as an input
"""
class S2TConverter:

    def __init__(self, rate, language='en-US'):
        self.client = speech.SpeechClient()
        self.rate = rate
        self.language = language
        self.streaming_config = self.get_streaming_config()

    """
    ## This method creates configuration for streeming
    """
    def get_streaming_config(self):
        config = types.RecognitionConfig(
                     encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                     sample_rate_hertz=self.rate,
                     language_code=self.language,
                 )

        streaming_config = types.StreamingRecognitionConfig(
                               config=config,
                               interim_results=True,
                           )

        return streaming_config

    def get_responses(self, stream):
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                        for content in audio_generator
                    )
        responses = self.client.streaming_recognize(self.streaming_config, requests)

        return responses


class Translate:

    def __init__(self, from_language='en', to_language='en'):
        self.from_language = from_language
        self.to_language = to_language
        self.client = translate.Client(target_language=to_language)

    def translate(self, text):
        if self.from_language == self.to_language:
            return text
        return self._call_translate(text)

    def _call_translate(self, text):
        resp = self.client.translate(text)
        if 'translatedText' in resp.keys():
            return resp['translatedText']
