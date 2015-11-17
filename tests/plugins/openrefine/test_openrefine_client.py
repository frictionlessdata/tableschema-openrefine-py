import vcr
import jsontableschema.plugins.openrefine.openrefine_client as openrefine_cli


OpenRefineClient = openrefine_cli.OpenRefineClient
VCR_CASSETTE = 'fixtures/vcr_cassettes/openrefine_client.yaml'


class TestOpenRefineClient(object):
    _DEFAULT_URL = 'http://localhost:3333'

    @vcr.use_cassette(VCR_CASSETTE)
    def test_recline_version(self):
        client = OpenRefineClient(self._DEFAULT_URL)
        assert client.version == '2.5'
