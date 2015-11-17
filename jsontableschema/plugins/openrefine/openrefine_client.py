import requests
import six.moves.urllib.parse as urlparse


class OpenRefineClient(object):
    def __init__(self, server_url):
        self.server_url = server_url

    @property
    def version(self):
        response = requests.get(self._generate_url('command/core/get-version'))
        return response.json()['version']

    def _generate_url(self, command):
        return urlparse.urljoin(self.server_url, command)
