#! /bin/bash

set -e

work_dir="$( cd "$( dirname "${0}" )" && pwd )"
#echo ${work_dir}

. ${work_dir}/custom.cfg


\cp ${work_dir}/harbor.cfg.template ${work_dir}/harbor.cfg
for key in $(grep = ${work_dir}/custom.cfg | awk -F"=" '{print $1}'); do eval "value=\$$key"; sed -i "s#${key}#${value}#g" ${work_dir}/harbor.cfg ; done
