
def upload_to_indexer(vid_name):
    import http.client, urllib.request, urllib.parse, urllib.error, base64

    # from poster.encode import multipart_encode
    url_pre = "https://instatranslatefile.blob.core.windows.net/resources/"
    headers = {
            # Request headers
            'Content-Type': 'multipart/form-data',
            'Ocp-Apim-Subscription-Key': '821863b59d28469d93e6a001d72e89c3',
            }

    url  = url_pre+vid_name
    print(url)
    params = urllib.parse.urlencode({
        # Request parameters
        'name': vid_name,
        'privacy': 'Public',
        'videoUrl': url,
        'language': 'en-US',
        'callbackUrl': 'https://510c57fa.ngrok.io/addVideoDetailsToDB',
        'externalId' : vid_name
        })

    try:
        conn = http.client.HTTPSConnection('videobreakdown.azure-api.net')
        conn.request("POST", "/Breakdowns/Api/Partner/Breakdowns?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


