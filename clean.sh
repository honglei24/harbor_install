#! /bin/bash

domain=test.harbor.com
for i in `seq 1 1000`
do
  docker rmi ${domain}/test/nginx-$i:latest
  curl -k -X DELETE -H 'Accept: text/plain' -u admin:Harbor12345  "https://${domain}/api/repositories/test/nginx-${i}/tags/latest"
done
