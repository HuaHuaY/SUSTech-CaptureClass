'''
Changed from "https://github.com/YoungWilliamZ/SUSTC-Qiangke/tree/master/python_version/SUSTC-qiangke.py"
'''

from datetime import datetime
from getpass import getpass
from json import dump, load
from os import path, system
from random import random
from re import findall, split
from time import sleep

from requests import Session

infor = ("Name", "Id", "Value")
logInData = {}
classJsonName = "captureClassList.json"
classList = []  # 抢课列表
is_random_delay = True  # 默认使用随机延迟
delay = 0.0  # 抢课失败后延迟，单位为秒
session = Session()


# 预先设置
def config():
    # 输入CAS账号密码
    logInData['username'] = input("请输入您的CAS账号：").strip()
    logInData['password'] = getpass("请输入您的CAS密码：").strip()
    logInData['_eventId'] = 'submit'

    # 登录验证密码正确性
    while len(findall('请输入您的用户名和密码.', logIn().text)) != 0:
        logInData['password'] = getpass("密码错误！请重新输入密码：").strip()

    if path.exists(classJsonName) and path.isfile(classJsonName):
        print("检索到JSON课程配置文件")
        global classList
        with open(classJsonName, "r", encoding="utf8") as f:
            classList = load(f)["classList"]
    else:
        p = tuple(split("[, ]", input(
            '\n请输入待抢课程名称、id与分类号，以逗号分隔，名字任取，\n本学期计划分类号为1，专业内跨年级为2，其他为0，\n如" IELTS,201920201001718,0 "：').strip()))
        classList.append({infor[0]: p[0], infor[1]: p[1], infor[2]: p[2]})
        while(int(input("请问是否继续添加课程，不需要请输入0，需要请输入1：")) != 0):
            p = tuple(split("[, ]", input("请输入待抢课程名称、id与分类号：").strip()))
            classList.append({infor[0]: p[0], infor[1]: p[1], infor[2]: p[2]})

        if int(input("是否需要保存课程配置到class.json文件，不需要请输入0，需要请输入1：")) != 0:
            with open(classJsonName, "w") as f:
                dump({"classList": classList}, f)

    global delay, is_random_delay
    if int(input("\n请问是否需要固定抢课失败延迟，不需要请输入0，需要请输入1：")) != 0:
        delay = int(input("请以毫秒为单位，输入抢课失败后延迟：")) / 1000.0
        is_random_delay = False
    print()


def logIn():
    # CAS登录并跳转教务系统
    response = session.get(
        'https://cas.sustech.edu.cn/cas/login')
    if 'execution' not in logInData:
        logInData['execution'] = findall('on" value="(.+?)"', response.text)[0]
    session.post(
        'https://cas.sustech.edu.cn/cas/login?service=http%3A%2F%2Fjwxt.sustech.edu.cn%2Fjsxsd%2F', logInData)

    # 查询选课页面链接
    return session.get(
        'http://jwxt.sustech.edu.cn/jsxsd/xsxk/xklc_list?Ves632DSdyV=NEW_XSD_PYGL')


def wait():
    system("cls")
    now = datetime.now()
    while now.hour*60 + now.minute < 12*60+55:
        print("当前时间为 %d:%d:%d，" % (now.hour, now.minute, now.second), end="")
        print("距下午1点还有 %d:%d:%d" %
              ((13*60*60 - now.hour*60*60 - now.minute*60 - now.second) / 3600,
               (13*60*60 - now.hour*60*60 - now.minute*60 - now.second) % 3600 / 60,
                  (13*60*60 - now.hour*60*60 - now.minute*60 - now.second) % 60))
        sleep(0.9)
        system("cls")
        now = datetime.now()
        if now.hour*60 + now.minute >= 12*60+55:
            print("时间已过12:55，开始准备抢课\n")


def start():
    key = findall('href="(.+)" target="blank">进入选课', logIn().text)
    while(len(key) == 0):
        print("选课系统暂时关闭，即将重试！")
        key = findall('href="(.+)" target="blank">进入选课', logIn().text)
        now = datetime.now()
        if now.hour*60 + now.minute < 12*60+59:
            sleep(20)

    k = key[0]

    # 这里前后cookies打印结果未发生变化，但是若省去这条get则选课失败，提示“当前账号已在别处登录，请重新登录进入选课！”
    session.get('http://jwxt.sustech.edu.cn' + k)

    print("CAS验证成功")
    print("教务系统启动")
    print("开始抢课")


def rush_all(classList):
    count = 1
    while len(classList) > 0:
        print('\n开始第 %d 次喵喵喵' % count)
        count += 1
        for p in classList:
            if rush(p):
                classList.remove(p)


def rush(p):
    print(p)
    print('正在抢 %s' % p[infor[0]])
    if p[infor[2]] == '1':
        response = session.get(
            "http://jwxt.sustech.edu.cn/jsxsd/xsxkkc/bxqjhxkOper?jx0404id=%s&xkzy=&trjf=" % p[infor[1]])
    elif p[infor[2]] == '2':
        response = session.get(
            "http://jwxt.sustech.edu.cn/jsxsd/xsxkkc/knjxkOper?jx0404id=%s&xkzy=&trjf=" % p[infor[1]])
    else:
        response = session.get(
            "http://jwxt.sustech.edu.cn/jsxsd/xsxkkc/fawxkOper?jx0404id=%s&xkzy=&trjf=" % p[infor[1]])
    result = str(response.content, 'utf-8')
    if result.find("true", 0, len(result)) >= 1:
        print("抢到 " + p[infor[0]] + " 啦")
        return True

    global delay
    print(result + "继续加油!", end="")
    if is_random_delay:
        delay = random() / 10
    if delay != 0.0:
        print("等待%fs" % delay, end="")
        sleep(delay)
    print()
    return False


def main():
    config()
    wait()
    start()
    rush_all(classList)
    session.close()


if __name__ == '__main__':
    main()
