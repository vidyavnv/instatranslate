#! /usr/bin/env python3

# -*- coding: utf-8 -*-

###
#Copyright (c) Microsoft Corporation
#All rights reserved.
#MIT License
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the ""Software""), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
###


def tts(video_id,input_lang,output_lang):
    import http.client, urllib.parse, json
    from xml.etree import ElementTree


    #Note: The way to get api key:
    #Free: https://www.microsoft.com/cognitive-services/en-us/subscriptions?productId=/products/Bing.Speech.Preview
    #Paid: https://portal.azure.com/#create/Microsoft.CognitiveServices/apitype/Bing.Speech/pricingtier/S0

    tts_file_name = video_id+"_formated.txt"
    lang_to_translate_to = output_lang
    lang_to_translate_from = input_lang
    output_file = video_id+"_tts.mp3"



    apiKey = "4898119e0e9043d28c31ad6dad9adc53"

    params = ""
    headers = {"Ocp-Apim-Subscription-Key": apiKey}

    #AccessTokenUri = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken";
    AccessTokenHost = "api.cognitive.microsoft.com"
    path = "/sts/v1.0/issueToken"

    # Connect to server to get the Access Token
    print ("Connect to server to get the Access Token")
    conn = http.client.HTTPSConnection(AccessTokenHost)
    conn.request("POST", path, params, headers)
    response = conn.getresponse()
    print(response.status, response.reason)

    data = response.read()
    conn.close()

    accesstoken = data.decode("UTF-8")
    print ("Access Token: " + accesstoken)

    body = ElementTree.Element('speak', version='1.0')
    body.set('{http://www.w3.org/XML/1998/namespace}lang', lang_to_translate_to)
    voice = ElementTree.SubElement(body, 'voice')
    voice.set('{http://www.w3.org/XML/1998/namespace}lang', lang_to_translate_to)
    voice.set('{http://www.w3.org/XML/1998/namespace}gender', 'Male')
    if(lang_to_translate_to=="en-US"):
        voice.set('name', 'Microsoft Server Speech Text to Speech Voice ('+lang_to_translate_to+', BenjaminRUS)')
    elif(lang_to_translate_to=="fr-FR"):
        voice.set('name', 'Microsoft Server Speech Text to Speech Voice ('+lang_to_translate_to+', Paul, Apollo)')
    else:
        voice.set('name', 'Microsoft Server Speech Text to Speech Voice ('+lang_to_translate_to+', Stefan, Apollo)')


    input_text = open(tts_file_name,'r')
    txt = input_text.read()
    voice.text = txt

    headers = {"Content-type": "application/ssml+xml",
                            "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3",
                            "Authorization": "Bearer " + accesstoken,
                            "X-Search-AppId": "07D3234E49CE426DAA29772419F436CA",
                            "X-Search-ClientID": "1ECFAE91408841A480F00935DC390960",
                            "User-Agent": "TTSForPython"}

    #Connect to server to synthesize the wave
    print ("\nConnect to server to synthesize the wave")
    conn = http.client.HTTPSConnection("speech.platform.bing.com")
    conn.request("POST", "/synthesize", ElementTree.tostring(body), headers)
    response = conn.getresponse()
    print(response.status, response.reason)

    data = response.read()
    conn.close()
    file = open(output_file,"wb")
    file.write(data)
    print("The synthesized wave length: %d" %(len(data)))


