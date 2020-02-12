#! /bin/bash

set -e

work_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo ${work_dir}

. ${work_dir}/custom.cfg

[ -f {__WORK_DIR}${__CERT_DIR__}${__DOMAIN}.key ] || openssl genrsa -out {__WORK_DIR}${__CERT_DIR__}${__DOMAIN}.key 4096
[ -f {__WORK_DIR}${__CERT_DIR__}${__DOMAIN}.csr ] || openssl req -sha512 -new -subj "/C=NJ/ST=NanJing/L=NanJing/O=example/OU=Personal/CN=${__DOMAIN}" -key {__WORK_DIR}${__CERT_DIR__}${__DOMAIN}.key -out {__WORK_DIR}${__CERT_DIR__}${__DOMAIN}.csr

\cp ${work_dir}/harbor.cfg.template ${work_dir}/harbor.cfg
for key in $(grep = ${work_dir}/custom.cfg | awk -F"=" '{print $1}'); do eval "value=\$$key"; sed -i "s#${key}#${value}#g" ${work_dir}/harbor.cfg ; done


sudo sh install.sh
