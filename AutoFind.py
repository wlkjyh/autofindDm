import json
import os
from pyDes import des, ECB, PAD_PKCS5
import binascii
import requests
import time, datetime
import threading


like = ['分享活动']
timeSleep = 0.01

activeList = []

headers = {
    'standardUA': '{"channelName": "dmkj_Android", "countryCode": "CN", "createTime": 1604663529774, "device": "HUAWEI vmos","hardware": "vphw71", "modifyTime": 1604663529774, "operator": "%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8","screenResolution": "1080-2115", "startTime": 1605884705024, "sysVersion": "Android 25 7.1.2","system": "android", "uuid": "12:34:56:31:97:80", "version": "4.6.0"}',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length': '309',
    'Host': 'appdmkj.5idream.net',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'okhttp/3.11.0',
}


def Apply(account, pwd):
    """
    账号登陆,返回uid和token
    account  登陆账号
    pwd      加密后的密码
    :param account:
    :param pwd:
    :return:
    """
    pwd_ = get_pwd(pwd)
    url = 'https://appdmkj.5idream.net/v2/login/phone'
    data = {
        'pwd': pwd_,
        'account': account,
        'version': '4.6.0'
    }

    response = requests.post(url=url, headers=headers, data=data).json()
    response.update(account=account, pwd=pwd)
    response1 = json.dumps(response)
    with open('token', mode='w', encoding='utf-8') as f:
        f.write(response1)

    return response


def get_time(accounts_data, id):
    """
    获取活动开始时间
    :param accounts_data:
    :param id:
    :return:
    """
    url = 'https://appdmkj.5idream.net/v2/activity/detail'
    token = accounts_data['token']
    uid = accounts_data['uid']
    data_get_time = {
        'uid': uid,  # 登陆接口获取
        'token': token,  # 登陆接口获取
        'activityId': int(id),  # 活动ID
        'version': '4.6.0',
    }

    set_data = requests.post(url=url, headers=headers, data=data_get_time).json()
    time_ = set_data['data']['joindate'].split('-')[0]
    time_data = [time_[0:4], time_[5:7], time_[8:10], time_[11:13], time_[14:16], set_data['data']['activityName']]
    print(set_data['data']['activityName'])
    return time_data


def get_activit(accounts_data):
    """
    获取可以报名的活动
    uid     每个账号不同的uid
    token   账号的token
    :param accounts_data
    :return:
    """
    activitys = []
    url = 'https://appdmkj.5idream.net/v2/activity/activities'
    token = accounts_data['token']
    uid = accounts_data['uid']
    data = {
        'joinStartTime': '',
        'token': token,  # 登陆接口获取
        'startTime': '',
        'endTime': '',
        'joinFlag': '1',
        'collegeFlag': '',
        'catalogId': '',
        'joinEndTime': '',
        'specialFlag': '',
        'status': '',
        'keyword': '',
        'version': '4.6.0',
        'uid': uid,  # 登陆接口获取
        'sort': '',
        'page': '1',
        'catalogId2': '',
        'level': '',
    }
    response = requests.post(url=url, headers=headers, data=data).json()
    lists_data = response['data']['list']

    # print(lists_data)
    for data_ in lists_data:
        activityId = data_['activityId']
        name = data_['name']
        statusText = data_['statusText']
        activity = {'activityId': activityId, 'name': name, 'statusText': statusText}
        activitys.append(activity)
    return activitys


def main(passwd, id):
    """
    提交报名函数
    :param passwd:
    :param id:
    :return:
    """
    while True:
        info = [{"conent": "", "content": "", "fullid": "79857", "key": 1, "notList": "false", "notNull": "false",
                 "system": 0,
                 "title": "姓名"}]

        data1 = {
            'uid': passwd['uid'],  # 登陆接口获取
            'token': str(passwd['token']),  # 登陆接口获取
            'remark': '',
            'data': str(info),  # 活动报名参数
            'activityId': id,  # 活动ID
            'version': '4.6.0',
        }
        response1 = requests.post(url='https://appdmkj.5idream.net/v2/signup/submit', data=data1,
                                  headers=headers).json()
        # print(response1)
        try:
            if response1['msg'] == '此活动你已经报名,不能重复报名':
                print('活动报名成功')

                break
        except KeyError:
            ...


def get_pwd(s):
    """
    获取密码加密结果
    :param s:
    :return:
    """
    KEY = '51434574'
    secret_key = KEY
    k = des(secret_key, ECB, pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(s, padmode=PAD_PKCS5)
    return binascii.b2a_hex(en).upper().decode('utf-8')

def JoinActive(passwd,passwd1,activeId):
    global timeSleep
    time_ = get_time(passwd['data'], activeId)
    startTime = datetime.datetime(int(time_[0]), int(time_[1]), int(time_[2]), int(time_[3]), int(time_[4]), 00)
    # 前5秒开始报名
    openStartTime = startTime - datetime.timedelta(seconds=5)
    print('任务队列准备处理,活动名称:%s,报名开始时间:%s,队列开始执行时间:%s' % (time_[5], startTime,openStartTime))

    while datetime.datetime.now() < openStartTime:
        time.sleep(float(timeSleep))

    print('队列活动名称:%s,开始执行报名任务' % time_[5])
    threading.Thread(target=main, args=(passwd1, activeId)).start()




    pass

def ActiveDeamon(passwd):
    global activeList
    """
        自动发现活动
    :param password:
    :return:
    """
    while True:
        huodong_id = get_activit(passwd['data'])
        for activity in huodong_id:


            # 遍历活动
            activityId = activity['activityId']
            name = activity['name']
            statusText = activity['statusText']


            passwd1 = {}
            passwd1['token'] = passwd['data']['token']
            passwd1['uid'] = passwd['data']['uid']

            if len(like) == 0:
                if name not in activeList:

                    threading.Thread(target=JoinActive, args=(passwd,passwd1, activityId)).start()
                    print('发现活动: %s,已添加到活动队列' % name)
                    activeList.append(name)
            else:
                for like_ in like:
                    if like_ in name:
                        if name not in activeList:
                            threading.Thread(target=JoinActive, args=(passwd,passwd1, activityId)).start()
                            print('发现活动: %s,已添加到活动队列' % name)
                            activeList.append(name)





        time.sleep(60)

# 发现活动报名关键词，如果为空则报名所有

if __name__ == '__main__':
    if os.path.exists('token'):
        with open('token', mode='r', encoding='utf-8') as f:
            datas = f.readlines()[0]
            data_s = json.loads(datas)
            account = data_s['account']
            pwd = data_s['pwd']
    else:
        account = input('请输入你的账号(手机号):')
        pwd = input('请输入你的密码:')
    passwd = Apply(account=account, pwd=pwd)
    passwd1 = {}

    threading.Thread(target=ActiveDeamon, args=(passwd,)).start()

