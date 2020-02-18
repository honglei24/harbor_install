#! /bin/bash

set -e

work_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo ${work_dir}

. ${work_dir}/custom.cfg

openssl genrsa -out {__WORK_DIR}${__CERT_DIR__}ca.key 4096
openssl req -x509 -new -nodes -sha512 -days 3650 -subj "/C=NJ/ST=NanJing/L=NanJing/O=example/OU=Personal/CN=${__DOMAIN}" -key {__WORK_DIR}${__CERT_DIR__}ca.key -out {__WORK_DIR}${__CERT_DIR__}ca.crt

openssl genrsa -out {__WORK_DIR}${__CERT_DIR__}${__DOMAIN}.key 4096
openssl req -sha512 -new -subj "/C=NJ/ST=NanJing/L=NanJing/O=example/OU=Personal/CN=${__DOMAIN}" -key {__WORK_DIR}${__CERT_DIR__}${__DOMAIN}.key -out {__WORK_DIR}${__CERT_DIR__}${__DOMAIN}.csr

cat > v3.ext <<-EOF
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEnciphermentopenssl x509 -in certificate.pem -text -noout
extendedKeyUsage = serverAuth 
subjectAltName = @alt_names

[alt_names]
DNS.1=${__DOMAIN}
IP.1=${__DOMAIN}
EOF

openssl x509 -req -sha512 -days 3650 -extfile v3.ext -CA {__WORK_DIR}${__CERT_DIR__}ca.crt -CAkey {__WORK_DIR}${__CERT_DIR__}ca.key -CAcreateserial -in {__WORK_DIR}${__CERT_DIR__}${__DOMAIN}.csr -out {__WORK_DIR}${__CERT_DIR__}${__DOMAIN}.crt


\cp ${work_dir}/harbor.cfg.template ${work_dir}/harbor.cfg
for key in $(grep = ${work_dir}/custom.cfg | awk -F"=" '{print $1}'); do eval "value=\$$key"; sed -i "s#${key}#${value}#g" ${work_dir}/harbor.cfg ; done

