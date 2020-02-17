# harbor
本文整合了harbor部署，升级，软硬件需求和测试相关文档。

部署主要是参照官方的部署文档，采用online部署的模式来安装harbor组件。为了简化参数修改，增加了prepre.sh脚本。

官方1.7.0部署参照：https://github.com/goharbor/harbor/blob/v1.7.0/docs/installation_guide.md

## 部署图
![部署图](./images/harbor-部署图.jpg)

绿色部分属于harbor部署范围，harbor包含的组件参照！[组件](#组件)章节中的实线框内的部分。同一个site内可以部署多个harbor来达到高可用的目的。初期部署一个。

蓝色部分由云平台提供：
* 负载均衡器
* 共享存储
* PostgreSQL
* 部署harbor组件所用的服务器（服务器如软硬件配置参照！[软硬件需求](#软硬件需求)）

## 组件
Harbor在架构上主要由6个组件构成：
1. Proxy：Harbor的registry, UI, token等服务，通过一个前置的反向代理统一接收浏览器、Docker客户端的请求，并将请求转发给后端不同的服务。
2. Registry： 负责储存Docker镜像，并处理docker push/pull 命令。由于我们要对用户进行访问控制，即不同用户对Docker image有不同的读写权限，Registry会指向一个token服务，强制用户的每次docker pull/push请求都要携带一个合法的token, Registry会通过公钥对token 进行解密验证。
3. Core services： 这是Harbor的核心功能，主要提供以下服务：
+ UI：提供图形化界面，帮助用户管理registry上的镜像（image）, 并对用户进行授权。
+ webhook：为了及时获取registry 上image状态变化的情况， 在Registry上配置webhook，把状态变化传递给UI模块。
+ token 服务：负责根据用户权限给每个docker push/pull命令签发token. Docker 客户端向Regiøstry服务发起的请求,如果不包含token，会被重定向到这里，获得token后再重新向Registry进行请求。
4. Database：为core services提供数据库服务，负责储存用户权限、审计日志、Docker image分组信息等数据。我们采用外部数据库。
5.ob Services：提供镜像远程复制功能，可以把本地镜像同步到其他Harbor实例中。
6. Log collector：为了帮助监控Harbor运行，负责收集其他组件的log，供日后进行分析。
各个组件之间的关系如下图所示：
![组件图](./images/harbor-组件图.jpg)

## 软硬件需求
参照
https://github.com/goharbor/harbor/edit/master/docs/1.10/install-config/installation-prereqs.md
### 硬件

|Resource|Minimum|Recommended|
|---|---|---|
|CPU|2 CPU|4 CPU|
|Mem|4 GB|8 GB|
|Disk|40 GB|160 GB|

### 操作系统
|OS|
|---|
|CentOS 7.4 / Ubuntu 18.04|
安装和升级是基于ubuntu 18.04验证的。
为了和泰山新村保持版本一致，推荐Centos 7.4

### 软件
|Software|Version|
|---|---|
|Docker engine|Version 17.06.0-ce+ or higher|
|Docker Compose|Version 1.18.0 or higher|
|Openssl|Latest is preferred|

## 部署手册
```
# git clone https://gitlab.oneitfarm.com/hl/harbor.git
# cd harbor
# vim custom.cfg
根据实际环境信息修改配置文件。
__DOMAIN=test.harbor.com
__UI_URL_PROTOCOL=https
__WORK_DIR=/data/
__CERT_DIR=cert/
__HARBOR_ADMIN_PASSWORD=Harbor12345
__DB_HOST=192.168.3.2
__DB_PASSWORD=123456
__DB_PORT=5432
__DB_USER=postgres

# ./prepare.sh
# ./install.sh
```

## 升级
下面的步骤是从v1.7.0升级到v1.7.5的步骤。升级到其他步骤，需要修改对应的tag。
参照：https://github.com/goharbor/harbor/blob/v1.7.5/docs/migration_guide.md
假设harbor所在目录为${work_dir}
```
cd ${work_dir}/harbor
docker-compose down

mkdir -p /my_backup_dir
cd ..
mv harbor /my_backup_dir/harbor

cp -r /data/database /my_backup_dir/

docker pull goharbor/harbor-migrator:v1.7.5

wget https://storage.googleapis.com/harbor-releases/release-1.7.0/harbor-online-installer-v1.7.5.tgz

tar -zxvf harbor-online-installer-v1.7.5.tgz
cd harbor 

cp /my_backup_dir/harbor/harbor.cfg ./
harbor_cfg=“${work_dir}/harbor/harbor.cfg”
docker run -it --rm -v ${harbor_cfg}:/harbor-migration/harbor-cfg/harbor.cfg goharbor/harbor-migrator:1.7.5 --cfg up

./install.sh
```

## 回滚
参照：https://github.com/goharbor/harbor/blob/v1.7.5/docs/migration_guide.md#roll-back-from-an-upgrade
```
cd ${work_dir}
rm harbor -rf
mv /my_backup_dir/harbor harbor
cp -r /my_backup_dir/database /data
cd /harbor
./install.sh
```

## registry压力测试
参照：https://docs.openstack.org/developer/performance-docs/test_results/container_repositories/registry2/index.html
```
# git clone https://gitlab.oneitfarm.com/hl/harbor.git
# cd harbor
# vi test.py
修改test.py里的并发数，habor信息
# python test.py
```
在测试目录下会生成测试报告。后缀为csv的是测试结果。
