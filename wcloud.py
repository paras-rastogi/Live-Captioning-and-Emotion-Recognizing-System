from __future__ import print_function
import json
from os.path import join, dirname
from watson_developer_cloud import ToneAnalyzerV3
def tone_sentiment(text):
    tone_analyzer = ToneAnalyzerV3(
        username='bf734eee-2cf2-48b7-99fe-42a12e11f63c',
        password='raSTeIk6uaKB',
        version='2017-09-21',
        url = 'https://gateway.watsonplatform.net/tone-analyzer/api')
    tone = tone_analyzer.tone({"text":text},sentences=False)
    return tone
