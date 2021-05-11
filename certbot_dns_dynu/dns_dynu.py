"""DNS Authenticator for Dynu."""

import logging

import zope.interface
from certbot import interfaces
from certbot import errors

from certbot.plugins import dns_common
from certbot.plugins import dns_common_lexicon

from lexicon.providers import dynu

logger = logging.getLogger(__name__)


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for Dynu."""

    description = 'Obtain certificates using a DNS TXT record ' + \
                  '(if you are using Dynu for DNS.)'

    ttl = 60

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):
        super(Authenticator, cls).add_parser_arguments(
            add, default_propagation_seconds=60)
        add("credentials", help="Dynu credentials file.")

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return 'This plugin configures a DNS TXT record to respond to a dns-01 challenge using ' + \
               'Dynu API'

    def _setup_credentials(self):
        self._configure_file('credentials',
                             'Absolute path to Dynu credentials file')
        dns_common.validate_file_permissions(self.conf('credentials'))
        self.credentials = self._configure_credentials(
            'credentials',
            'Dynu credentials file',
            {
                'auth-token': 'Dynu-compatible API key (API-Key)',
            }
        )

    def _perform(self, domain, validation_name, validation):
        self._get_dynu_client().add_txt_record(
            domain, validation_name, validation)

    def _cleanup(self, domain, validation_name, validation):
        self._get_dynu_client().del_txt_record(
            domain, validation_name, validation)

    def _get_dynu_client(self):
        return _DynuLexiconClient(
            self.credentials.conf('auth-token'),
            self.ttl
        )


class _DynuLexiconClient(dns_common_lexicon.LexiconClient):
    """
    Encapsulates all communication with the Dynu via Lexicon.
    """

    def __init__(self, auth_token, ttl):
        super(_DynuLexiconClient, self).__init__()

        config = dns_common_lexicon.build_lexicon_config('dynu', {
            'ttl': ttl,
        }, {
            'auth_token': auth_token,
        })

        self.provider = dynu.Provider(config)

    def _handle_http_error(self, e, domain_name):
        if domain_name in str(e) and (
            # 4.0 and 4.1 compatibility
            str(e).startswith('422 Client Error: Unprocessable Entity for url:') or
            # 4.2
            str(e).startswith('404 Client Error: Not Found for url:')
        ):
            return  # Expected errors when zone name guess is wrong
        return super(_DynuLexiconClient, self)._handle_http_error(e, domain_name)

