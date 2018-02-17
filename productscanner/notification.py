import requests

from retrying import retry

from . import config

@retry(stop_max_attempt_number=3, wait_random_min=1000, wait_random_max=5000)
def send(title, message, url, image_url=None):
    for name, authentication in config.notification.items():
        handler = globals().get('handle_{name}'.format(name=name), lambda *args, **kwargs: None)
        handler(authentication, title, message, url, image_url)

def handle_pushover(authentication, title, message, url, image_url=None):
    from notification import Pushover

    parameters = {
        'title': title,
        'message': message,
        'url': url,
    }

    if image_url:
        response = requests.get(image_url)
        if response.status_code == 200:
            parameters['attachment'] = response.content

    Pushover(**authentication).notify(**parameters)