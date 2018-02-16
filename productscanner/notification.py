import requests

from retrying import retry

pushover_url = 'https://api.pushover.net/1/messages.json'

@retry(stop_max_attempt_number=3, wait_random_min=1000, wait_random_max=5000)
def send(user, token, **kwargs):
    parameters = dict(kwargs, user=user, token=token)
    files = None

    if 'attachment' in parameters:
        files = { 'attachment': ('attachment.jpg', parameters['attachment'], 'image/jpeg') }
        del parameters['attachment']

    respoonse = requests.post(pushover_url, data=parameters, files=files)
    if respoonse.status_code != 200:
        raise RuntimeError('An error occurred while sending HTTP reqeust')