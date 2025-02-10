#!/bin/bash

old_version=`cat version.txt | tr -d '[:space:]'`
env_name=$1
version=$2
timestamp=`date +%y%m%d%s`

build() {
  export VERSION_VAR="${version}.${1}"
  python -m build --wheel
  python -m twine upload --repository "${env_name}" "dist/certbot_dns_dynu-${VERSION_VAR}-py3-none-any.whl" --config-file .pypirc
  if [ "v${version}" != "v${old_version}" ]; then
    echo "${version}" > version.txt
    git add version.txt
    git commit -m "updated version to ${version}."
  fi
}


usage() {
  echo "$0 <env> <version>"
  echo "$1 is invalid env"
  echo "valid env testpypi pypi"
  exit 64
}

case ${env_name} in
  testpypi)
    build "dev${timestamp}"
    ;;
  pypi)
    build "post${timestamp}"
    ;;
  *)
    usage $0
    ;;
esac
