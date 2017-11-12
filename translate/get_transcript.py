



def download_transcript(video_id,input_lang):
    import http.client, urllib.request, urllib.parse, urllib.error, base64
    headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': '821863b59d28469d93e6a001d72e89c3',
            }

    params = urllib.parse.urlencode({
        # Request parameters
        'language': input_lang,
        })

    try:
        conn = http.client.HTTPSConnection('videobreakdown.azure-api.net')
        conn.request("GET", "/Breakdowns/Api/Partner/Breakdowns/"+video_id+"/VttUrl?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        data = data.decode("utf-8")
        data=data.replace('"','')
        # The below line gets the entire file with time info, if we use this later to get better output
        urllib.request.urlretrieve(data, video_id+".txt")

        formated_transcript = open(video_id+"_formated.txt",'w+')
        # The below code formats the code for the tts

        with open(video_id+'.txt','r') as file:
            file.readline()
            for line in file:
                if not line.isspace() and not "-->" in line:
                    formated_transcript.write(line)

        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))



