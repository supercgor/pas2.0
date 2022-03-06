# -*- coding: utf-8
# hi
import sys
import warnings
from configparser import ConfigParser
from time import localtime, strftime

from selenium.webdriver.chrome.options import Options

from func import *

warnings.filterwarnings('ignore')


def sys_path(browser):
    path = f'./{browser}/bin/'
    if sys.platform.startswith('win'):
        return path + f'{browser}.exe'
    elif sys.platform.startswith('linux'):
        return path + f'{browser}'
    elif sys.platform.startswith('darwin'):
        return path + f'{browser}'
    else:
        raise Exception('暂不支持该系统')


def go():
    player_conf = ConfigParser()
    player_conf.read("player.ini", encoding='utf8')
    player_num = len(player_conf.sections())
    conf = ConfigParser()
    conf.read("config.ini", encoding='utf8')
    now_time = str(strftime("%Y-%m-%d", localtime()))

    campus = conf['common']['campus']

    habitation, district, street = dict(conf['in']).values()

    destination = conf['out']['destination']

    capture = conf.getboolean('capture', '是否需要备案历史截图')
    path = conf['capture']['截图保存路径']

    wechat = conf.getboolean('wechat', '是否需要微信通知')

    working_markdown = False

    for i in range(player_num):

        print("第" + str(player_num + 1) + "位同學開始報備")

        working_player = "player_" + str(i + 1)

        studentID, mail, pwd, phoneNum, before_time, reason, detail, track = dict(player_conf[working_player]).values()

        if before_time == now_time:
            print("今天已經報備過了!")

        run(driver_pjs, studentID, pwd, campus, mail, phoneNum, reason, detail, destination,
            track, habitation, district, street, capture, path, wechat, "")

        player_conf.set(working_player, 'time', now_time)

        working_markdown = True

    if working_markdown:
        player_conf.write(open('player.ini', 'w'))


if __name__ == '__main__':

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    driver_pjs = webdriver.Chrome(executable_path="chromedriver.exe")

    print('Driver Launched\n')

    go()

    driver_pjs.quit()
