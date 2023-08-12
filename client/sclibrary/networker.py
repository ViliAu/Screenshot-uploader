import requests

URL = 'http://localhost:3000'
IMG_ROUTE = "/api/upload/image"
VID_ROUTE = "/api/upload/video"

def upload_media(path: str, mode: str):
    if len(path) == 0:
        print("Error: no path specified")
        return
    try:
        with open(path, "rb") as f:
            data = {"media": f}
            route = IMG_ROUTE if mode == 'image' else VID_ROUTE
            res = requests.post(
                url=URL + route,
                files=data
            )
            print(res.text)

    except:
        raise