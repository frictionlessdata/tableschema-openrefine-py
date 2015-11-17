import os
import vcr

FIXTURES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'fixtures')


def create_vcr():
    my_vcr = vcr.VCR(
        cassette_library_dir='fixtures/vcr_cassettes',
        record_mode='new_episodes',
    )

    return my_vcr
