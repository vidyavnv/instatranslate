import http.client, urllib.request, urllib.parse, urllib.error, base64

headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '821863b59d28469d93e6a001d72e89c3',
        }

params = urllib.parse.urlencode({
    # Request parameters
    })

try:
    conn = http.client.HTTPSConnection('videobreakdown.azure-api.net')
    conn.request("GET", "/Breakdowns/Api/Partner/Breakdowns/fde36fc40e?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
