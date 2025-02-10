"""Tests for certbot_dns_dynu.dns_dynu"""

import os
import logging

import mock

from certbot.plugins import dns_test_common
from certbot.plugins import dns_test_common_lexicon
from certbot.tests import util as test_util

from src.certbot_dns_dynu.dns_dynu import Authenticator

AUTH_TOKEN = "00000000-0000-0000-0000-000000000000"
logger = logging.getLogger(__name__)


class AuthenticatorTest(
    test_util.TempDirTestCase, dns_test_common_lexicon.BaseLexiconDNSAuthenticatorTest
):
    """AuthenticatorTest"""

    def setUp(self):
        super().setUp()

        path = os.path.join(self.tempdir, "file.ini")
        dns_test_common.write({"dynu_auth_token": AUTH_TOKEN}, path)

        with open(path, encoding="utf-8") as f:
            logger.info("File content: %s", f.read())

        self.config = mock.MagicMock(
            dynu_credentials=path, dynu_propagation_seconds=0
        )  # don't wait during tests

        self.auth = Authenticator(config=self.config, name="dynu")
