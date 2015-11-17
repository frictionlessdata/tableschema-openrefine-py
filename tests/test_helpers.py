import os
import vcr

FIXTURES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'fixtures')


def create_vcr():
    my_vcr = vcr.VCR(
        path_transformer=vcr.VCR.ensure_suffix('.yaml'),
        cassette_library_dir='fixtures/vcr_cassettes',
        record_mode='once',
    )

    return my_vcr
