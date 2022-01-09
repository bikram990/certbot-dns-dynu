certbot-dns-dynu
============

Dynu DNS Authenticator plugin for [Certbot](https://certbot.eff.org/).

This plugin is built from the ground up and follows the development style and life-cycle
of other `certbot-dns-*` plugins found in the
[Official Certbot Repository](https://github.com/certbot/certbot).

Installation
------------

```
pip install --upgrade certbot
pip install certbot-dns-dynu
```

Verify:

```
$ certbot plugins --text

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
* dns-dynu
Description: Obtain certificates using a DNS TXT record (if you are using Dynu
for DNS.)
Interfaces: Authenticator, Plugin
Entry point: dns-dynu = certbot_dns_dynu.dns_dynu:Authenticator

...
...
```

Configuration
-------------

The credentials file e.g. `~/dynu-credentials.ini` should look like this:

```
dns_dynu_auth_token = AbCbASsd!@34
```

Usage
-----


```
certbot ... \
        --authenticator dns-dynu  \
        --dns-dynu-credentials ~/dynu-credentials.ini \
        certonly
```

FAQ
-----

##### Why such long name for a plugin?

This follows the upstream nomenclature: `certbot-dns-<dns-provider>`.

##### Why do I have to use `:` separator in the name? And why are the configuration file parameters so weird?

This is a limitation of the Certbot interface towards _third-party_ plugins.

For details read the discussions:

- https://github.com/certbot/certbot/issues/6504#issuecomment-473462138
- https://github.com/certbot/certbot/issues/6040
- https://github.com/certbot/certbot/issues/4351
- https://github.com/certbot/certbot/pull/6372

Development
-----------

Create a virtualenv, install the plugin (`editable` mode),
spawn the environment and run the test:

```
virtualenv -p python3 .venv
. .venv/bin/activate
pip install -e .
docker-compose up -d
./test/run_certonly.sh test/dynu-credentials.ini
```

License
--------

Copyright (c) 2021 [Bikramjeet Singh](https://github.com/bikram990)

Credits
--------
[PowerDNS](https://github.com/pan-net-security/certbot-dns-powerdns)

[dns-lexicon](https://github.com/AnalogJ/lexicon)

Helpful links
--------

[DNS Plugin list](https://certbot.eff.org/docs/using.html?highlight=dns#dns-plugins)

[acme.sh](https://github.com/acmesh-official/acme.sh)

[dynu with acme.sh](https://gist.github.com/tavinus/15ea64c50ac5fb7cea918e7786c94a95)

[dynu api](https://www.dynu.com/Support/API)






