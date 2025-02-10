#!/bin/bash

action=$1
domain=$2
email=$3

dryrun() {
  echo "Dry run mode"
  certbot certonly --config-dir ./test/config --work-dir ./test/work --logs-dir ./test/logs \
  --agree-tos --email "${email}" \
  --authenticator dns-dynu --dns-dynu-credentials ./test/dynu-credentials.ini \
  --test-cert --dry-run -n -d "${domain}"
}

test() {
  echo "Test mode"
  certbot certonly --config-dir ./test/config --work-dir ./test/work --logs-dir ./test/logs \
  --agree-tos --email "${email}" \
  --authenticator dns-dynu --dns-dynu-credentials ./test/dynu-credentials.ini \
  --test-cert -n -d "${domain}"
}

live() {
  echo "Live mode"
  certbot certonly --config-dir ./test/config --work-dir ./test/work --logs-dir ./test/logs \
  --agree-tos --email "${email}" \
  --authenticator dns-dynu --dns-dynu-credentials ./test/dynu-credentials.ini \
  -n -d "${domain}"
}

usage() {
  echo "$0 <action> <email> <domain>"
  echo "$1 is invalid action"
  echo "valid actions dryrun test live"
  exit 64
}



case $action in
  dryrun)
    dryrun
    ;;
  test)
    test
    ;;
  live)
    live
    ;;
  *)
    usage $0
    ;;
esac
