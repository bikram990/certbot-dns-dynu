"""Tests for certbot_dns_dynu.dns_dynu"""

import os
import unittest

import mock
from requests.exceptions import HTTPError

from certbot.plugins import dns_test_common
from certbot.plugins import dns_test_common_lexicon
from certbot.plugins.dns_test_common import DOMAIN

from certbot.tests import util as test_util

AUTH_TOKEN = '00000000-0000-0000-0000-000000000000'


class AuthenticatorTest(test_util.TempDirTestCase,
                        dns_test_common_lexicon.BaseLexiconAuthenticatorTest):

    def setUp(self):
        super(AuthenticatorTest, self).setUp()

        from certbot_dns_dynu.dns_dynu import Authenticator

        path = os.path.join(self.tempdir, 'file.ini')
        dns_test_common.write(
            {"dynu_auth_token": AUTH_TOKEN},
            path
        )

        print("File content: ")
        # print(open(path).read())
        with open(path) as f:
            print(f.read())

        self.config = mock.MagicMock(dynu_credentials=path,
                                     dynu_propagation_seconds=0)  # don't wait during tests

        self.auth = Authenticator(self.config, "dynu")

        self.mock_client = mock.MagicMock()
        # _get_dynu_client | pylint: disable=protected-access
        self.auth._get_dynu_client = mock.MagicMock(return_value=self.mock_client)



class DynuLexiconClientTest(unittest.TestCase,
                                dns_test_common_lexicon.BaseLexiconClientTest):
    DOMAIN_NOT_FOUND = HTTPError('422 Client Error: Unprocessable Entity for url: {0}.'.format(DOMAIN))
    LOGIN_ERROR = HTTPError('401 Client Error: Unauthorized')

    def setUp(self):
        from certbot_dns_dynu.dns_dynu import _DynuLexiconClient

        self.client = _DynuLexiconClient(auth_token=AUTH_TOKEN, ttl=0)

        self.provider_mock = mock.MagicMock()
        self.client.provider = self.provider_mock


if __name__ == "__main__":
    unittest.main()  # pragma: no cover