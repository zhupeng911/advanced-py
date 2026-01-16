import requests
import json

# super manager login system
def super_manager_login(host: str):
    print("------super manager(17888888888) login system------")
    p = "/api/v2/super-manage/account/login"
    url = "http://" + host + p
    result = requests.post(url, json = {
        "tel": "17888888888",
        "password": "9156fee3a50b305f97e00ce90348ccb2"  # 初始化密码
        # "password": "8a1066d58639315e6b0599e79ca39275"    # 修改后密码
    })
    if result.status_code != 200:
        raise Exception('http status code is not 200: %s' % result.content.decode('utf-8'))
    ret = json.loads(result.content)
    if ret['code'] != 0:
        raise Exception('api code is not 0: %s' % ret['message'])
    if 'data' in ret:
        print("------super manager login system success, token:", ret['data']["token"])
        return ret['data']

# bind node
def node_bind(host: str, body: dict, token: str):
    p = "/api/v2/super-manage/org-config/node/bind"
    url = "http://" + host + p
    headers = {
        'authorization': 'data-flow ' + token
    }
    result = requests.post(url, json=body, headers=headers)
    if result.status_code != 200:
        raise Exception('http status code is not 200: %s' % result.content.decode('utf-8'))
    ret = json.loads(result.content)
    if ret['code'] != 0:
        raise Exception('api code is not 0: %s' % ret['message'])
    if 'data' in ret:
        return ret['data']

def database_create(host: str, body: dict, token: str):
    p = "/api/v2/super-manage/org-config/database/creatOrUpdate"
    url = "http://" + host + p
    headers = {
        'authorization': 'data-flow ' + token
    }
    result = requests.post(url, json=body, headers=headers)
    if result.status_code != 200:
        raise Exception('http status code is not 200: %s' % result.content.decode('utf-8'))
    ret = json.loads(result.content)
    if ret['code'] != 0:
        raise Exception('api code is not 0: %s' % ret['message'])


def org_root_create(host: str, body: dict, token: str):
    p = "/api/v2/super-manage/org-config/root/creatOrUpdate"
    url = "http://" + host + p
    headers = {
        'authorization': 'data-flow ' + token
    }
    result = requests.post(url, json=body, headers=headers)
    if result.status_code != 200:
        raise Exception('http status code is not 200: %s' % result.content.decode('utf-8'))
    ret = json.loads(result.content)
    if ret['code'] != 0:
        raise Exception('api code is not 0: %s' % ret['message'])


if __name__ == '__main__':
    print("------start setup dataflow------")
    host = "127.0.0.1:8080"
    f = open("configs.json", "r")
    json_str = f.read()
    load_dict = json.loads(json_str)
    # 超级管理员登录
    login_ret = super_manager_login(host=host)
    token: str = login_ret['token']

    for key, org_list in load_dict.items():
        for org in org_list:
            # 绑定节点
            node = org["node"]
            print("--------------------begin setup ", node["org_name"], "--------------------")
            print("------start bind org:", node["org_name"], " node")
            node_bind_ret = node_bind(host=host, body=node, token=token)
            # 创建数据库
            database = org["database"]
            database["org_id"] = node_bind_ret
            print("------start create org:", node["org_name"], " database ip:", database["ip"], "port:", database["port"], "db name:", database["db_name"])
            database_create_ret = database_create(host=host, body=database, token=token)
            # 创建机构root账户
            org_root = org["org_root"]
            org_root["org_id"] = node_bind_ret
            print("------create org:", node["org_name"], " root account")
            org_root_ret = org_root_create(host=host, body=org_root, token=token)