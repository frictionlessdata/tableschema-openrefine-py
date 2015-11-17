import os
import six
import pytest
import jsontableschema.plugins.openrefine.openrefine_client as openrefine_cli
import tests.test_helpers as test_helpers


VCR = test_helpers.create_vcr()
VCR_CASSETTE = 'openrefine_client.yaml'
OpenRefineClient = openrefine_cli.OpenRefineClient


class TestOpenRefineClient(object):
    _DEFAULT_URL = 'http://localhost:3333'
    _CLIENT = OpenRefineClient(_DEFAULT_URL)

    def test_invalid_url_raises_exception(self):
        with pytest.raises(TypeError):
            not_a_string = 1000
            OpenRefineClient(not_a_string)

    @VCR.use_cassette(VCR_CASSETTE)
    def test_version(self):
        assert self._CLIENT.version == '2.5'

    @VCR.use_cassette(VCR_CASSETTE)
    def test_create_project(self):
        name = 'Annual Global Temperatures'
        filepath = os.path.join(test_helpers.FIXTURES_PATH, 'annual.csv')
        project_id = self._create_project(name, filepath)
        project = self._CLIENT.get_project(project_id)
        assert project is not None
        assert project['name'] == name

    @VCR.use_cassette(VCR_CASSETTE)
    def test_create_project_raises_when_file_doesnt_exist(self):
        if six.PY2:
            expected_exception = IOError
        else:
            expected_exception = FileNotFoundError

        filepath = 'non-existent-file.csv'
        with pytest.raises(expected_exception):
            self._create_project(filepath=filepath)

    @VCR.use_cassette(VCR_CASSETTE)
    def test_get_project(self):
        project_id = self._create_project()
        assert self._CLIENT.get_project(project_id) is not None

    @VCR.use_cassette(VCR_CASSETTE)
    def test_get_projects(self):
        created_projects_ids = [self._create_project()
                                for _ in range(2)]

        projects_ids = self._CLIENT.get_projects().keys()

        for project_id in created_projects_ids:
            assert project_id in projects_ids

    def _create_project(self,
                        name='Annual Global Temperatures',
                        filepath=os.path.join(test_helpers.FIXTURES_PATH,
                                              'annual.csv')):
        return self._CLIENT.create_project(name, filepath)
