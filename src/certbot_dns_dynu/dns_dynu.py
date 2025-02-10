"""DNS Authenticator for Dynu."""

import logging

from typing import Callable

from certbot import errors
from certbot.plugins import dns_common_lexicon

logger = logging.getLogger(__name__)


class Authenticator(dns_common_lexicon.LexiconDNSAuthenticator):
    """DNS Authenticator for Dynu."""

    description = "Obtain certificates using a DNS TXT record (if you are using Dynu for DNS.)"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._add_provider_option("auth_token", "Auth Token to access the Dynu API", "auth_token")

    @classmethod
    def add_parser_arguments(
        cls,
        add: Callable[..., None],  # pylint: disable=arguments-differ
        default_propagation_seconds: int = 60,
    ) -> None:
        super().add_parser_arguments(
            add=add, default_propagation_seconds=default_propagation_seconds
        )
        add("credentials", help="Dynu credentials file.")

    def more_info(self):
        return (
            "This plugin configures a DNS TXT record to respond to a dns-01 challenge using "
            + "Dynu API"
        )

    @property
    def _provider_name(self) -> str:
        return "dynu"

    def _handle_http_error(self, e, domain_name):
        if domain_name in str(e) and (
            # 4.0 and 4.1 compatibility
            str(e).startswith("422 Client Error: Unprocessable Entity for url:")
            or
            # 4.2
            str(e).startswith("404 Client Error: Not Found for url:")
        ):
            return None  # Expected errors when zone name guess is wrong
        return super()._handle_http_error(e, domain_name)

    def _handle_general_error(self, e, domain_name):
        # Error from https://github.com/dns-lexicon/dns-lexicon/blob/main/src/lexicon/_private/
        # providers/dynu.py#L43
        if str(e) == "No matching domain found":
            return errors.PluginError(
                f"Unexpected error determining zone identifier for {domain_name}: {e}"
            )  # Expected error when zone name guess is wrong.
        return super()._handle_general_error(e, domain_name)
