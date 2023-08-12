import requests

URL = 'http://localhost:3000'

def send_image(path):
    if len(path) == 0:
        print("Error: no path specified")
        return
    res = requests.post(
        url=URL,
        files=None
    )

def send_video():
    pass
