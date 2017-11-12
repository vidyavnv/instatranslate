import http.client, urllib.request, urllib.parse, urllib.error, base64

from constants import OCP

def get_video_insights(video_id):
    headers = {
        'Ocp-Apim-Subscription-Key': '821863b59d28469d93e6a001d72e89c3',
    }

    params = urllib.parse.urlencode({
        # 'language': '{string}',
    })
    try:
        conn = http.client.HTTPSConnection('videobreakdown.azure-api.net')
        conn.request("GET", "/Breakdowns/Api/Partner/Breakdowns/"+ video_id +"?" + str(params), "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


get_video_insights('fde36fc40e')