## postgre备份

备份会生成一个registry.sql文件。
```
# su - postgres
$ pg_dump registry -f registry.sql
```

## postgre恢复

registry.sql是备份过程中生成的文件。
```
# su - postgres
$ psql -d registry -f registry.sql 
```

## 使用外部数据库初始化
```
# psql --username postgres
psql (9.6.10)
Type "help" for help.
postgres=# CREATE DATABASE registry ENCODING 'UTF8';
CREATE DATABASE
postgres=# \c registry;
You are now connected to database "registry" as user "postgres".
registry=# CREATE TABLE schema_migrations(version bigint not null primary key, dirty boolean not null);
CREATE TABLE
registry-# \quit
```