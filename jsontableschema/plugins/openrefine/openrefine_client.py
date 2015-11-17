import requests
import six
import six.moves.urllib.parse as urlparse


class OpenRefineClient(object):
    def __init__(self, server_url):
        if not isinstance(server_url, six.string_types):
            raise TypeError('"server_url" must be a string')

        self.server_url = server_url

    @property
    def version(self):
        response = requests.get(self._generate_url('command/core/get-version'))
        return response.json()['version']

    def _generate_url(self, command):
        return urlparse.urljoin(self.server_url, command)
