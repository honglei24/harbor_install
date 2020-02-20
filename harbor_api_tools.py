#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from requests.auth import HTTPBasicAuth
import json
import sys
import getopt

harbor_url = "https://test.harbor.com"
admin_username = "admin"
admin_password = "Harbor12345"


class Harbor(object):
    def __init__(self, url, username, password):
        self.url = url
        self.auth = HTTPBasicAuth(username, password)
        self.project_special = {}
        self.project_state = {}

    def get_projects(self):
        url = self.url + "/api/projects"
        r_project = requests.get(url=url, auth=self.auth, verify=False)
        r_project.raise_for_status()
        project_data = json.loads(r_project.text)
        return project_data

    def list_project(self):
        project_data = self.get_projects()
        for i in project_data:
            project_name = i.get('name')
            project_id = i.get('project_id')
            project_repo = i.get('repo_count')
            print("\033[0;32m project name:{}\tproject id:{}\tproject repo count:{}\033[0m".format(project_name,
                                                                                                   project_id,
                                                                                                   project_repo))

    def get_targets(self):
        url = self.url + "/api/targets"
        r_target = requests.get(url=url, auth=self.auth, verify=False)
        r_target.raise_for_status()
        target_data = json.loads(r_target.text)
        return target_data

    def list_target(self):
        target_data = self.get_targets()
        for i in target_data:
            target_id = i.get('name')
            target_name = i.get('id')
            print("\033[0;32m target name:{}\ttarget id:{}\033[0m".format(target_name, target_id))

    def create_targets(self, endpoint="https://test.harbor.com", name="remote", username="admin",
                       pwd="Harbor12345"):
        params = {"endpoint": endpoint, "name": name, "insecure": False, "username": username,
                  "password": pwd}
        url = self.url + "/api/targets"
        r_target = requests.post(url=url, auth=self.auth, verify=False, json=params)
        if r_target.status_code != 201:
            print("\033[0;31m create target {} failed, endpoint={}.\033[0m".format(name, endpoint))
            return

        print("\033[0;32m create target {} succeeded, endpoint={}.\033[0m".format(name, endpoint))

    def get_repositories(self, project_id):
        url = self.url + "/api/repositories"
        params = {"project_id": project_id}
        data = requests.get(url=url, auth=self.auth, verify=False, params=params)
        response_json = json.loads(data.text)
        repositories = []
        for r in response_json:
            repositories.append(r)
            print(r)

        return repositories

    def create_policy(self, targets=[], projects=[], name="replication", kind="Manual"):
        params = {"name": name, "projects": projects, "targets": targets, "trigger": {"kind": kind}}
        url = self.url + "/api/policies/replication"
        # print(params)
        r_target = requests.post(url=url, auth=self.auth, verify=False, json=params)
        print(r_target)
        if r_target.status_code != 201:
            print("\033[0;31m create policy {} failed.\033[0m".format(name))
            return

        print("\033[0;32m create policy {} succeeded.\033[0m".format(name))


def usage():
    prefix = "python harbor_api_tools.py"
    msg = '''该工具是针对harbor v1.7.0的工具，由于各个版本的API有变化，所以其他版本不能用此工具。
该工具提供的功能有：
1. 打印所有项目
# {} --list-projects

2. 打印所有仓库
# {} --list-target

3. 创建仓库
# {} --create-target --target=<target_name> --endpoint=<endpoint> --username=<username> --password=<password>

4. 创建复制任务
# {} --create-policy --target_id=<target_id> --project_id=<project_id> --policy=<policy_name> --kind=<kind>
'''.format(prefix, prefix, prefix, prefix)
    print(msg)


def main(argv):
    harbor = Harbor(url=harbor_url, username=admin_username, password=admin_password)

    try:
        opts, args = getopt.getopt(argv, "hle:c:t:p:U:P:",
                                   ["create-policy", "create-target", "list-projects", "list-target", "endpoint=",
                                    "target=", "project_id=", "target_id=", "username=", "password=", "kind=",
                                    "policy="])
    except getopt.GetoptError:
        usage
        sys.exit(2)

    print("username")
    if_create_policy = False
    if_create_target = False
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-l", "--list-projects"):
            harbor.list_project()
            sys.exit()
        elif opt in ("-U", "--username"):
            username = arg
        elif opt in ("-P", "--password"):
            pwd = arg
        elif opt in ("-t", "--target"):
            target = arg
        elif opt in ("-e", "--endpoint"):
            endpoint = arg
        elif opt in ("-c", "--create-target"):
            if_create_target = True
        elif opt in "--list-target":
            harbor.list_target()
        elif opt in "--policy":
            policy = arg
        elif opt in "--target_id":
            t_id = arg
        elif opt in "--kind":
            kind = arg
        elif opt in ("-p", "--project_id"):
            p_id = arg
        elif opt in "--create-policy":
            print("aaa")
            if_create_policy = True

    if if_create_target:
        harbor.create_targets(endpoint=endpoint, name=target, username=username, pwd=pwd)
        sys.exit()

    if if_create_policy:
        targets = [{"id": int(t_id)}]
        projects = [{"project_id": int(p_id)}]
        harbor.create_policy(targets=targets, projects=projects, name=policy, kind=kind)
        sys.exit()


if __name__ == '__main__':
    main(sys.argv[1:])
