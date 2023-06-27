# -*- coding: utf-8 -*-
import re
import time
import json
import requests
import pandas as pd
from lxml import etree
import concurrent.futures
from datetime import datetime

cookie = 'race_id=1148873; halfbt_daxiao=0; __yjs_duid=1_455c0fa31305a91ee21a40835c3cc0aa1681790104356; ds_session=sk9mf86b94mm50lcj6hvb3la44; Hm_lvt_a68414d98536efc52eeb879f984d8923=1687163224,1687317465; uid=R-631284-062f66e0064926c023587d; Hm_lpvt_a68414d98536efc52eeb879f984d8923=1687330118'


class Dszuqiu(object):

    def __init__(self):
        self.session = self.session()
        self.headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'Cookie': cookie,
            'Connection': 'close'}
        super().__init__()

    def session(self):
        session = requests.session()
        session.keep_alive = False
        session.adapters.DEFAULT_RETRIES = 10
        requests.packages.urllib3.disable_warnings()
        return session

    def monitor(self, data_dict):
        while True:
            for key, value in data_dict.items():
                url = key.replace('ss', 'baijia')
                bs_time = value.strip()

                bs_list = bs_time.split(' ')
                ymd = bs_list[0]
                ymd_list = ymd.split('/')
                y = int(ymd_list[0])
                m = int(ymd_list[1])
                d = int(ymd_list[2])
                oc = bs_list[1]
                oc_list = oc.split(':')
                o = int(oc_list[0])

                now_time = datetime.now()
                execute_at = datetime(y, m, d, o, 0, 0)
                time_delta = execute_at - now_time
                time_delta_seconds = time_delta.total_seconds()
                print(f"比赛链接:{url}  比赛时间:{bs_time}  距比赛开始时差:{time_delta_seconds}秒")
                if -3580 > time_delta_seconds > -3620 or -280 > time_delta_seconds > -320 or 200 > time_delta_seconds > 160:
                    crawl_result = []
                    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                        futures = concurrent.futures.as_completed(
                            [executor.submit(self.calculate, url)])
                        for future in concurrent.futures.as_completed(futures):
                            result = future.result()
                            if result:
                                crawl_result.append(future.result())

            time.sleep(30)

    def calculate(self, url):
        try:
            res = self.session.get(url, headers=self.headers, timeout=30, verify=False)
            html = etree.HTML(res.text)
            title = html.xpath('/html/head/title/text()')[0]
            if title.strip() == '用户登录 - DS足球':
                print('账号过期，请更换cookie！')
                exit()
            liansai = html.xpath('//h3[@class="dsBreadcrumbs"]/a[3]/text()')[0]
            qiudui = html.xpath('//h3[@class="dsBreadcrumbs"]/text()')[-1].strip()

            # 百家指数让球36
            ranglinshui36 = \
                html.xpath(
                    '//*[@id="baijia"]/div[1]/div/div[2]/table//tr[@onclick="request(8)"][1]/td[3]/text()')[
                    0]
            ranglinshui36 = float(ranglinshui36)
            rangchushui36 = \
                html.xpath(
                    '//*[@id="baijia"]/div[1]/div/div[2]/table//tr[@onclick="request(8)"][2]/td[2]/text()')[
                    0]
            rangchushui36 = float(rangchushui36)
            ranglinpan36 = \
                html.xpath(
                    '//*[@id="baijia"]/div[1]/div/div[2]/table//tr[@onclick="request(8)"][1]/td[4]/text()')[
                    0]
            if ',' in ranglinpan36:
                pan = ranglinpan36.split(',')
                p1 = pan[0]
                p2 = pan[1]
                ranglinpan36 = (float(p1) + float(p2)) / 2
            ranglinpan36 = float(ranglinpan36)
            rangchupan36 = \
                html.xpath(
                    '//*[@id="baijia"]/div[1]/div/div[2]/table//tr[@onclick="request(8)"][2]/td[3]/text()')[
                    0]
            if ',' in rangchupan36:
                pan = rangchupan36.split(',')
                p1 = pan[0]
                p2 = pan[1]
                rangchupan36 = (float(p1) + float(p2)) / 2
            rangchupan36 = float(rangchupan36)

            # 百家指数大小球36
            dalinshui36 = \
                html.xpath(
                    '//*[@id="baijia"]/div[2]/div/div[2]/table//tr[@onclick="request(8)"][1]/td[3]/text()')[
                    0]
            dalinshui36 = float(dalinshui36)
            dachushui36 = \
                html.xpath(
                    '//*[@id="baijia"]/div[2]/div/div[2]/table//tr[@onclick="request(8)"][2]/td[2]/text()')[
                    0]
            dachushui36 = float(dachushui36)
            dalinpan36 = \
                html.xpath(
                    '//*[@id="baijia"]/div[2]/div/div[2]/table//tr[@onclick="request(8)"][1]/td[4]/text()')[
                    0]
            if '/' in dalinpan36:
                pan = dalinpan36.split('/')
                p1 = pan[0]
                p2 = pan[1]
                dalinpan36 = (float(p1) + float(p2)) / 2
            dalinpan36 = float(dalinpan36)
            dachupan36 = \
                html.xpath(
                    '//*[@id="baijia"]/div[2]/div/div[2]/table//tr[@onclick="request(8)"][2]/td[3]/text()')[
                    0]
            if '/' in dachupan36:
                pan = dachupan36.split('/')
                p1 = pan[0]
                p2 = pan[1]
                dachupan36 = (float(p1) + float(p2)) / 2
            dachupan36 = float(dachupan36)


            if html.xpath('//*[@id="baiji a"]/div[1]/div/div[2]/table//tr[@onclick="request(3)"][1]/td[3]/text()'):
                # 百家指数让球S
                ranglinshuiS = \
                    html.xpath(
                        '//*[@id="baijia"]/div[1]/div/div[2]/table//tr[@onclick="request(3)"][1]/td[3]/text()')[
                        0]
                ranglinshuiS = float(ranglinshuiS)
                rangchushuiS = \
                    html.xpath(
                        '//*[@id="baijia"]/div[1]/div/div[2]/table//tr[@onclick="request(3)"][2]/td[2]/text()')[
                        0]
                rangchushuiS = float(rangchushuiS)
                ranglinpanS = \
                    html.xpath(
                        '//*[@id="baijia"]/div[1]/div/div[2]/table//tr[@onclick="request(3)"][1]/td[4]/text()')[
                        0]
                if ',' in ranglinpanS:
                    pan = ranglinpanS.split(',')
                    p1 = pan[0]
                    p2 = pan[1]
                    ranglinpanS = (float(p1) + float(p2)) / 2
                ranglinpanS = float(ranglinpanS)
                rangchupanS = \
                    html.xpath(
                        '//*[@id="baijia"]/div[1]/div/div[2]/table//tr[@onclick="request(3)"][2]/td[3]/text()')[
                        0]
                if ',' in rangchupanS:
                    pan = rangchupanS.split(',')
                    p1 = pan[0]
                    p2 = pan[1]
                    rangchupanS = (float(p1) + float(p2)) / 2
                rangchupanS = float(rangchupanS)

                # 百家指数大小球S
                dalinshuiS = \
                    html.xpath(
                        '//*[@id="baijia"]/div[2]/div/div[2]/table//tr[@onclick="request(3)"][1]/td[3]/text()')[
                        0]
                dalinshuiS = float(dalinshuiS)
                dachushuiS = \
                    html.xpath(
                        '//*[@id="baijia"]/div[2]/div/div[2]/table//tr[@onclick="request(3)"][2]/td[2]/text()')[
                        0]
                dachushuiS = float(dachushuiS)
                dalinpanS = \
                    html.xpath(
                        '//*[@id="baijia"]/div[2]/div/div[2]/table//tr[@onclick="request(3)"][1]/td[4]/text()')[
                        0]
                if '/' in dalinpanS:
                    pan = dalinpanS.split('/')
                    p1 = pan[0]
                    p2 = pan[1]
                    dalinpanS = (float(p1) + float(p2)) / 2
                dalinpanS = float(dalinpanS)
                dachupanS = \
                    html.xpath(
                        '//*[@id="baijia"]/div[2]/div/div[2]/table//tr[@onclick="request(3)"][2]/td[3]/text()')[
                        0]
                if '/' in dachupanS:
                    pan = dachupanS.split('/')
                    p1 = pan[0]
                    p2 = pan[1]
                    dachupanS = (float(p1) + float(p2)) / 2
                dachupanS = float(dachupanS)
            else:
                ranglinshuiS = ''
                rangchushuiS = ''
                ranglinpanS = ''
                rangchupanS = ''
                dalinshuiS = ''
                dachushuiS = ''
                dalinpanS = ''
                dachupanS = ''

            print(f"36让临水{ranglinshui36} 36让初水{rangchushui36} 36让临盘{ranglinpan36} 36让初盘{rangchupan36} S让临水{ranglinshuiS} S让初水{rangchushuiS} S让临盘{ranglinpanS} S让初盘{rangchupanS} 36大临水{dalinshui36} 36大初水{dachushui36} 36大临盘{dalinpan36} 36大初盘{dachupan36} S大临水{dalinshuiS} S大初水{dachushuiS} S大临盘{dalinpanS} S大初盘{dachupanS}")
            info = f"报警  \n比赛ID:{url.split('/')[-1]}  \n 比赛球队{qiudui} \n 36大临盘:{dalinpan36}"
            if rangchupan36 > ranglinpan36 and ranglinshui36 < 0.93 and dalinshui36 < 0.90 and ranglinpan36 < -0.4:
                print("满足条件一  ")
                self.send_dd(info)

            if rangchupan36 > ranglinpan36 and dalinpan36 > dachupan36 and ranglinpan36 < -0.4:
                print("满足条件二  ")
                self.send_dd(info)

            if rangchushui36 > ranglinshui36 and dachushui36 > dalinshui36:
                print("满足条件三  ")
                self.send_dd(info)

            if rangchupan36 > ranglinpan36 and dachushui36 > dalinshui36 and ranglinpan36 < -0.4:
                print("满足条件四  ")
                self.send_dd(info)

            return info
        except:
            pass

    def send_qq(self, msg: str):
        qqgid = '164808476'
        requests.get(
            'http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(str(qqgid), str(msg)))

    def send_dd(slef, msg: str):

        url = 'https://oapi.dingtalk.com/robot/send?access_token=7fbac5ead1bc9ecdc78644f58ae8e074376313d90a787b64a3b7fe2167ca8571'
        headers = {"Content-Type": "application/json"}
        data = {
            "msgtype": "text",
            "isAtAll": "True",
            "at": {"isAtAll": True},
            "text": {
                "content": msg
            }
        }

        requests.post(url, data=json.dumps(data), headers=headers)
        return print('钉钉推送成功！！！', data)

    def read_csv(self):
        df = pd.read_csv('DS未开始比赛.csv', usecols=['url', '比赛时间'], encoding='utf-8')
        # 将数据保存到字典中
        data_dict = {}
        for index, row in df.iterrows():
            data_dict[row['url']] = row['比赛时间']
        print(data_dict)
        return data_dict



if __name__ == '__main__':
    print('☞脚本已启动...')
    l = Dszuqiu()
    data_dict = l.read_csv()
    l.monitor(data_dict)
