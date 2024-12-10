import requests
def send_flip(text: str):
    url = 'http://127.0.0.1:5000'
    payload = {
        'message': text
    }
    requests.post(url, json=payload)
