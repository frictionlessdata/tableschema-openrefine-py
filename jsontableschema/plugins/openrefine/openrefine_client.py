import requests
import six
import six.moves.urllib.parse as urlparse


class OpenRefineClient(object):
    _COMMANDS = {
        'get_version': 'command/core/get-version',
        'get_all_project_metadata': 'command/core/get-all-project-metadata',
        'get_project_metadata': 'command/core/get-project-metadata',
        'create_project_from_upload': 'command/core/create-project-from-upload',
        'delete_project': 'command/core/delete-project',
        'export_rows': 'command/core/export-rows',
    }

    def __init__(self, server_url):
        if not isinstance(server_url, six.string_types):
            raise TypeError('"server_url" must be a string')

        self.server_url = server_url

    @property
    def version(self):
        url = self._generate_url(self._COMMANDS['get_version'])
        res = requests.get(url)
        return res.json()['version']

    def create_project(self, name, filepath):
        url = self._generate_url(self._COMMANDS['create_project_from_upload'])
        with open(filepath, 'rb') as project_file:
            params = {
                'project-name': name,
            }
            files = {
                'file': project_file,
            }

            res = requests.post(url, allow_redirects=False,
                                data=params, files=files)

            if res.is_redirect and res.headers.get('location'):
                redirected_to = urlparse.urlparse(res.headers.get('location'))
                query_params = urlparse.parse_qs(redirected_to.query)
                return query_params.get('project')[0]

    def get_projects(self):
        url = self._generate_url(self._COMMANDS['get_all_project_metadata'])
        res = requests.get(url)
        return res.json().get('projects', {})

    def get_project(self, project_id):
        url = self._generate_url(self._COMMANDS['get_project_metadata'])
        res = requests.get(url, params={'project': project_id})
        if res.status_code == 200:
            return res.json()

    def delete_project(self, project_id):
        url = self._generate_url(self._COMMANDS['delete_project'])
        res = requests.post(url, params={'project': project_id})
        if res.status_code == 200:
            return res.json().get('code') == 'ok'

    def export_project(self, project_id, file_format='csv'):
        url = self._generate_url(self._COMMANDS['export_rows'])
        res = requests.post(url, params={
            'project': project_id,
            'format': file_format,
        })
        return res.text

    def _generate_url(self, command):
        return urlparse.urljoin(self.server_url, command)
