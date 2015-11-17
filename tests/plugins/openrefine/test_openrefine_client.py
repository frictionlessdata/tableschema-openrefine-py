import os
import six
import pytest
import jsontableschema.plugins.openrefine.openrefine_client as openrefine_cli
import tests.test_helpers as test_helpers


VCR = test_helpers.create_vcr()
OpenRefineClient = openrefine_cli.OpenRefineClient


class TestOpenRefineClient(object):
    _DEFAULT_URL = 'http://localhost:3333'
    _CLIENT = OpenRefineClient(_DEFAULT_URL)

    @classmethod
    @VCR.use_cassette()
    def setup_class(cls):
        cls._original_projects_ids = cls._CLIENT.get_projects().keys()

    @classmethod
    @VCR.use_cassette()
    def teardown_class(cls):
        current_projects_ids = cls._CLIENT.get_projects().keys()
        del_ids = set(current_projects_ids) - set(cls._original_projects_ids)

        for project_id in del_ids:
            assert cls._CLIENT.delete_project(project_id)

    def test_invalid_url_raises_exception(self):
        with pytest.raises(TypeError):
            not_a_string = 1000
            OpenRefineClient(not_a_string)

    @VCR.use_cassette()
    def test_version(self):
        assert self._CLIENT.version == '2.5'

    @VCR.use_cassette()
    def test_create_project(self):
        name = 'Annual Global Temperatures'
        filepath = os.path.join(test_helpers.FIXTURES_PATH, 'annual.csv')
        project_id = self._create_project(name, filepath)
        project = self._CLIENT.get_project(project_id)
        assert project is not None
        assert project['name'] == name

    @VCR.use_cassette()
    def test_create_project_raises_when_file_doesnt_exist(self):
        if six.PY2:
            expected_exception = IOError
        else:
            expected_exception = FileNotFoundError

        filepath = 'non-existent-file.csv'
        with pytest.raises(expected_exception):
            self._create_project(filepath=filepath)

    @VCR.use_cassette()
    def test_get_project(self):
        project_id = self._create_project()
        assert self._CLIENT.get_project(project_id) is not None

    @VCR.use_cassette()
    def test_get_projects(self):
        created_projects_ids = [self._create_project()
                                for _ in range(2)]

        projects_ids = self._CLIENT.get_projects().keys()

        for project_id in created_projects_ids:
            assert project_id in projects_ids

    @VCR.use_cassette()
    def test_delete_project(self):
        project_id = self._create_project()
        assert self._CLIENT.delete_project(project_id)
        assert self._CLIENT.get_project(project_id) is None

    @VCR.use_cassette()
    def test_delete_project_deleting_inexistent_project_doesnt_raise(self):
        inexistent_project_id = '1000'
        assert self._CLIENT.delete_project(inexistent_project_id)

    def _create_project(self,
                        name='Annual Global Temperatures',
                        filepath=os.path.join(test_helpers.FIXTURES_PATH,
                                              'annual.csv')):
        return self._CLIENT.create_project(name, filepath)
