# -*- coding: utf-8 -*-
import os
import re
import csv
import time
import json
import random
import requests
from lxml import etree

cookie = '__yjs_duid=1_38f8fa4e81290bacc6c88e7f5b52fe181677902761364; Hm_lvt_a68414d98536efc52eeb879f984d8923=1677902762,1678068592,1678105348,1678192741; ds_session=65ueji01ddh3tmiqchk8kthgv1; uid=R-631284-a1a598ad0640996f90751f; Hm_lpvt_a68414d98536efc52eeb879f984d8923=1678350074'

# 钉钉
def dingd(data):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=a2cdec94a0be829eb65ffce2dce2226fe359d733c84a793acfcd866a8f2cba9c'
    headers = {"Content-Type": "application/json"}
    requests.post(url, data=json.dumps(data), headers=headers)
    return data


class Dazuqiu(object):
    def __init__(self):
        self.session = self.session()

    def session(self):
        session = requests.session()
        session.keep_alive = False
        session.adapters.DEFAULT_RETRIES = 10
        return session

    def dfilter(self):
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cookie': cookie}

        while True:
            time.sleep(random.randint(30, 100))
            res = self.session.get('https://live.dszuqiu.com/ajax/score/data?mt=0&nr=1&corner=1', headers=headers,
                                   timeout=30, verify=False)
            print('第一次请求响应状态码:', res.status_code)
            if res.status_code == 200:
                ids = json.loads(res.text)
                for i in ids['rs']:
                    id = i['id']
                    time.sleep(random.randint(2, 5))
                    # 四合一数据url
                    race_sp = 'https://www.dszuqiu.com/race_sp/' + id
                    res = self.session.get(race_sp, headers=headers, timeout=30, verify=False)
                    print('第二次请求响应状态码:', res.status_code)
                    # 现场数据url
                    race_xc = 'https://www.dszuqiu.com/race_xc/' + id
                    res2 = self.session.get(race_xc, headers=headers, timeout=30, verify=False)
                    print('第三次请求响应状态码:', res.status_code)
                    html = etree.HTML(res.text)
                    html2 = etree.HTML(res2.text)
                    try:
                        # 比赛名称
                        liansainame = html.xpath('//h3[@class="dsBreadcrumbs"]/a[3]/text()')[0].strip()
                        print(liansainame)
                        # 比赛球队
                        qiudui = html.xpath('//h3[@class="dsBreadcrumbs"]/text()')[0].strip()
                        # 指数趋势
                        zszoushi = html.xpath('//*[@id="race_part"]/div[3]/div/table/tbody/tr/td[5]/a/text()')[
                            0].strip()
                        # 半角球
                        banjiao = html.xpath('//*[@id="race_part"]/div[3]/div/table//tr/td[1]/text()')[0].strip().split(
                            ':')
                        banjiao = int(banjiao[0]) + int(banjiao[1])
                        # 半进球
                        banjin = html.xpath('//*[@id="race_part"]/div[3]/div/table//tr/td[3]/text()')[0].strip().split(
                            ':')
                        banjin = int(banjin[0]) + int(banjin[1])
                        # 40分角球
                        jiao_whole = html.xpath('//tbody[@id="sp_corner"]/tr')
                        jiao40 = []
                        for i in jiao_whole[::-1]:
                            td_quan_jiao = i.xpath('./td/text()')
                            if "40'" in td_quan_jiao[0].strip():
                                jiao40.append(td_quan_jiao[3])
                        # print(jiao40[0])

                        # 40分总进
                        jiao_whole = html.xpath('//tbody[@id="sp_corner"]/tr')
                        zong40 = []
                        zong = 0
                        for i in jiao_whole[::-1]:
                            td_quan_jiao = i.xpath('./td/text()')
                            if "40'" in td_quan_jiao[0].strip():
                                zong40.append(td_quan_jiao[1])
                                zong = zong40[0].split(':')
                                zong = zong + int(zong[0].strip()) + int(zong[1].strip())
                        # print(zong)

                        # 40分大小球大于值
                        size_whole = html.xpath('//tbody[@id="sp_half_daxiao"]/tr')
                        dayu40 = []
                        for i in size_whole[::-1]:  # enumerate 枚举
                            td_quan_daxiao = i.xpath('./td/text()')
                            if "40'" in td_quan_daxiao[0].strip():
                                dayu40.append(td_quan_daxiao[2])
                        # print(dayu40[0])

                        # 40分时角球指数
                        jiaozhi = html.xpath('//tbody[@id="sp_half_corner"]/tr')
                        jiaozhi40 = []
                        for i in jiaozhi[::-1]:
                            td_quan_jiao = i.xpath('./td/text()')
                            if "40'" in td_quan_jiao[0].strip():
                                jiaozhi40.append(td_quan_jiao[2])
                        # print(jiaozhi40[0])

                        # 指数条件过滤 -0.75 - 0.75
                        zhishu = \
                            html.xpath('//*[@id="race_part"]/div[3]/div/table/tbody/tr/td[5]/a/text()')[
                                0].strip().split('/')[
                                0].strip()
                        if -0.75 < float(zhishu) < 0.75:
                            # 35分让球比分条件过滤
                            rang_all_data = html.xpath('//tbody[@id="sp_rangfen"]/tr')
                            for sp in rang_all_data[::-1]:
                                all_rangfen = sp.xpath('./td/text()')
                                # print(all_rangfen)
                                if "35'" in all_rangfen[0].strip():
                                    if all_rangfen[1] not in '2 : 0  3 : 0  4 : 0  3 : 1  0 : 2  0 : 3  0 : 4  1 : 3':
                                        # 半场大小球在35分时第一条大值小于3.6
                                        size_half_data = html.xpath('//tbody[@id="sp_half_daxiao"]/tr')
                                        for sp in size_half_data[::-1]:
                                            size_half = sp.xpath('./td/text()')
                                            if "35'" in size_half[0].strip():
                                                if float(size_half[2]) < 3.6:  # 3.6设定

                                                    # 射正球门29分条件
                                                    f1 = 0
                                                    f2 = 0
                                                    for n in range(90):
                                                        zheng = re.findall(f'"x":{n},(.*?)"name"', html2[1])
                                                        if n < 30:  # 29分
                                                            if zheng != []:
                                                                fen = re.findall('info":"(.*?)"', zheng[0])
                                                                for i in fen:
                                                                    if int(i) > 1:
                                                                        f1 += int(i)
                                                        if n >= 30:
                                                            if zheng != []:
                                                                fen2 = re.findall('info":"(.*?)"', zheng[0])
                                                                for j in fen2:
                                                                    if int(j) > 1:
                                                                        f2 += int(j)

                                                    # 射偏球门29分条件
                                                    f3 = 0
                                                    f4 = 0
                                                    for n in range(90):
                                                        pian = re.findall(f'"x":{n},(.*?)"name"', html2[2])
                                                        if n < 30:  # 29分
                                                            if pian != []:
                                                                fen = re.findall('info":"(.*?)"', pian[0])
                                                                for i in fen:
                                                                    if int(i) > 2:
                                                                        f3 += int(i)
                                                        if n >= 30:
                                                            if pian != []:
                                                                fen2 = re.findall('info":"(.*?)"', pian[0])
                                                                for j in fen2:
                                                                    if int(j) > 1:
                                                                        f4 += int(j)

                                                    # 角球，25分-42分
                                                    jiao = html2.xpath(
                                                        '//span[@class="timeLineGoal" or @class="timeLineCorner"]/@title')
                                                    f5 = 0
                                                    for i in range(25, 43):
                                                        for j in jiao:
                                                            if str(i) in j and '角球' in j:
                                                                f5 += 1  # 1次设定

                                                    if f1 > 1 and f2 > f1 and f3 > 2 and f4 > f3 and f5 >= 1:
                                                        info = [race_sp, liansainame + '\t', qiudui + '\t',
                                                                zszoushi + '\t',
                                                                banjiao + '\t', banjin + '\t', jiao40[0] + '\t',
                                                                zong + '\t', dayu40[0] + '\t', jiaozhi40[0] + '\t']
                                                        data = {
                                                            'url': race_sp,
                                                            '联赛名字': liansainame,
                                                            '球队': qiudui,
                                                            '指数走势': zszoushi,
                                                            '半角球': banjiao,
                                                            '半进球': banjin,
                                                            '40分角球': jiao40[0],
                                                            '40分总进球': zong,
                                                            '40分时大小球大于值 ': dayu40[0],
                                                            '40分时角球指数 ': jiaozhi40[0]
                                                        }
                                                        print(data)
                                                        dingd(data)
                                                        if not os.path.exists(f'{liansainame}.csv'):
                                                            head = ['url', '联赛', '比赛球队', '指数走势', '半角球', '半进球', '40分角球',
                                                                    '40分总进球', '40分时大小球大于值 ', '40分时角球指数']
                                                            csvFile = open(f'{liansainame}.csv', 'a', newline='',
                                                                           encoding='utf-8-sig')
                                                            writer = csv.writer(csvFile)
                                                            writer.writerow(head)
                                                            csvFile.close()
                                                        else:
                                                            csvFile = open(f'{liansainame}.csv', 'a+', newline='',
                                                                           encoding='utf-8-sig')
                                                            writer = csv.writer(csvFile)
                                                            writer.writerow(info)
                                                            csvFile.close()
                    except Exception as e:
                        pass


if __name__ == '__main__':
    l = Dazuqiu()
    l.dfilter()
