# -*- coding: utf-8 -*-
import os
import re
import csv
import time
import random
import requests
from lxml import etree
from selenium import webdriver


class Selenium_Middleware(object):

    def __init__(self):
        self.chromeOptions = self.get_chrome()
        self.browser = self.get_browser()

    def get_chrome(self):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument('--headless')
        chromeOptions.add_argument('--disable-gpu')
        chromeOptions.add_argument('window-size=1280,800')
        chromeOptions.add_argument("--no-sandbox")
        chromeOptions.add_argument('blink-settings=imagesEnabled=false')
        return chromeOptions

    def get_browser(self):
        browser = webdriver.Chrome(chrome_options=self.chromeOptions)
        browser.set_page_load_timeout(10)
        browser.set_script_timeout(10)
        return browser


cookie = '__yjs_duid=1_455c0fa31305a91ee21a40835c3cc0aa1681790104356; uid=R-631284-858337390643e157637505; ds_session=2agi0akd80cp9f015ifm43vlq0; Hm_lvt_a68414d98536efc52eeb879f984d8923=1681790107,1681884408; Hm_lpvt_a68414d98536efc52eeb879f984d8923=1681897089'


class Dszuqiu(Selenium_Middleware):
    def __init__(self):
        self.session = self.session()
        super().__init__()

    def session(self):
        session = requests.session()
        session.keep_alive = False
        session.adapters.DEFAULT_RETRIES = 10
        requests.packages.urllib3.disable_warnings()
        return session

    def biaodan(self, date, start_page, end_page):
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cookie': cookie}
        # index_url = f"https://www.dszuqiu.com/diary/{date}"
        # self.browser.get(index_url)
        # time.sleep(1)
        # self.browser.find_elements_by_xpath('//*[@id="pjax-container"]/div/div/div[1]/div[2]/ul[1]/li[5]/a')[
        #     0].click()
        # time.sleep(1)
        # self.browser.find_elements_by_xpath('//*[@id="pankou-list-filter"]/ul/li[3]/a')[0].click()
        # time.sleep(1)
        # self.browser.find_elements_by_xpath('//*[@id="corner-list-filter"]/form/div[2]/div/div[1]/a[1]')[0].click()
        # time.sleep(1)
        # self.browser.find_elements_by_xpath('//*[@id="corner-list-filter"]/form/div[2]/div/div[2]/button')[0].click()
        # time.sleep(5)
        # 下滑
        # for i in range(10):
        #     time.sleep(2)
        #     self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        for num in range(start_page, end_page + 1):
            in_url = f'https://www.dszuqiu.com/diary/{date}/p.{num}'
            print(f'当前采集页数:{in_url}')
            self.browser.get(in_url)
            html = etree.HTML(self.browser.page_source)
            xi = html.xpath('//*[@id="diary_info"]/table/tbody/tr/td[12]/a/@href')
            for x in xi:
                if 'race_sp' in x:
                    id = re.findall('/race_sp/([\s|\S]+)', x)[0]
                else:
                    id = re.findall('/race/([\s|\S]+)', x)[0]
                url_sp = 'https://www.dszuqiu.com/race_sp/' + id
                response = self.session.get(url_sp, headers=headers, timeout=30, verify=False)
                # 延迟秒数
                time.sleep(random.randint(3, 7))
                print('第二次请求:', response.status_code)
                chtml = etree.HTML(response.text)
                try:
                    rq_list = []
                    rq = chtml.xpath('//tbody[@id="sp_rangfen"]/tr')
                    rq_lenght = len(rq)
                    for index in range(0, rq_lenght):
                        poster = rq[index]
                        result = poster.xpath(
                            'td[@class="text-center red-color" or @class="text-center red-color xh-highlight"]/text()')[
                            0]
                        if result == "-":
                            r1 = poster.xpath('td[3]/text()')[0]
                            rq_list.append(r1)
                    rq1 = rq_list[0]
                    try:
                        rq2 = rq_list[1]
                    except:
                        rq2 = '0'
                except:
                    rq1 = ''
                    rq2 = ''
                try:
                    dxq_list = []
                    dxq = chtml.xpath('//tbody[@id="sp_daxiao"]/tr')
                    dxq_lenght = len(dxq)
                    for index in range(0, dxq_lenght):
                        poster = dxq[index]
                        result = poster.xpath(
                            'td[@class="text-center red-color" or @class="text-center red-color xh-highlight"]/text()')[
                            0]
                        if result == "-":
                            r1 = poster.xpath('td[3]/text()')[0]
                            dxq_list.append(r1)
                    dxq1 = dxq_list[0]
                    try:
                        dxq2 = dxq_list[1]
                    except:
                        dxq2 = '0'
                except:
                    dxq1 = ''
                    dxq2 = ''
                url_ss = 'https://www.dszuqiu.com/race_ss/' + id
                # response = self.session.get(url_ss, headers=headers, timeout=30, verify=False)
                self.browser.get(url_ss)
                # 延迟秒数
                time.sleep(random.randint(2, 6))
                print('第二次请求:', response.status_code)
                dhtml = etree.HTML(self.browser.page_source)
                try:
                    # 比赛球队
                    saishi = dhtml.xpath('//h3[@class="dsBreadcrumbs"]/a[3]/text()')[0].strip()
                    qiudui = dhtml.xpath('//h3[@class="dsBreadcrumbs"]/text()')[-1].strip()
                    shijian = dhtml.xpath('//span[@class="analysisRaceTime"]/text()')[0].strip()
                    try:
                        bifens = dhtml.xpath('//*[@id="race_part"]/div[3]/div/table/tbody/tr/td[4]/text()')[0].strip()
                        bifen = bifens.split(':')
                        bifen1 = bifen[0]
                        bifen2 = bifen[1]
                        bifenhe = int(bifen1) + int(bifen2)
                    except:
                        bifen1 = ''
                        bifen2 = ''
                        bifenhe = ''
                    # print(saishi,qiudui,shijian,bifen)
                    # 指数趋势
                    try:
                        zhishu = dhtml.xpath('//*[@id="race_part"]/div[3]/div/table/tbody/tr/td[5]/a/text()')[0].strip()
                        zhishu = zhishu.split('/')
                        rqzhishu = zhishu[0].strip()
                        jqzhishu = zhishu[2].strip()
                        dxzhishu = zhishu[1].strip()
                    except:
                        zhishu = dhtml.xpath('//*[@id="race_part"]/div[2]/div/table/tbody/tr/td[5]/a/text()')[0].strip()
                        zhishu = zhishu.split('/')
                        rqzhishu = zhishu[0].strip()
                        jqzhishu = zhishu[2].strip()
                        dxzhishu = zhishu[1].strip()
                    # print(rqzhishu,jqzhishu,dxzhishu)
                    # 总进球均
                    zjjun = dhtml.xpath('//*[@id="history_table"]/table/tbody/tr[5]/td[3]//text()')
                    zjjunlen = len(zjjun)
                    if zjjunlen == 3:
                        zjjun = zjjun[2].strip().replace('/', '')
                    if zjjunlen == 2:
                        zjjun = zjjun[1].strip().replace('/', '')
                    if zjjunlen == 1:
                        zjjun = zjjun[0].split('/')
                        zjjun = zjjun[1].strip()
                    # print(zjjun)
                    # 失球主
                    sqzhu = dhtml.xpath('//*[@id="history_table"]/table/tbody/tr[1]/td[4]//text()')
                    sqzhulen = len(sqzhu)
                    if sqzhulen == 3:
                        sqzhu = sqzhu[2].strip()
                    if sqzhulen == 2:
                        sqzhu = sqzhu[1].strip()
                    if sqzhulen == 1:
                        sqzhu = sqzhu[0].split('/')
                        sqzhu = sqzhu[1].strip()
                    # print(sqzhu)
                    # 失球客
                    sqke = dhtml.xpath('//*[@id="history_table"]/table/tbody/tr[3]/td[4]//text()')
                    sqkelen = len(sqke)
                    if sqkelen == 3:
                        sqke = sqke[2].strip()
                    if sqkelen == 2:
                        sqke = sqke[1].strip()
                    if sqkelen == 1:
                        sqke = sqke[0].split('/')
                        sqke = sqke[1].strip()
                    # print(sqke)
                    # 大球主
                    dqzhu = dhtml.xpath('//*[@id="history_table"]/table/tbody/tr[1]/td[5]//text()')
                    dqzhulen = len(dqzhu)
                    if dqzhulen == 3:
                        dqzhu = dqzhu[2].strip().replace('%', '').replace('/', '')
                    if dqzhulen == 2:
                        dqzhu = dqzhu[1].strip().replace('%', '').replace('/', '')
                    if dqzhulen == 1:
                        dqzhu = dqzhu[0].split('/')
                        dqzhu = dqzhu[1].strip().replace('%', '').replace('/', '')
                    # print(dqzhu)
                    # 大球客
                    dqke = dhtml.xpath('//*[@id="history_table"]/table/tbody/tr[3]/td[5]//text()')
                    dqkelen = len(dqke)
                    if dqkelen == 3:
                        dqke = dqke[2].strip().replace('%', '').replace('/', '')
                    if dqkelen == 2:
                        dqke = dqke[1].strip().replace('%', '').replace('/', '')
                    if dqkelen == 1:
                        dqke = dqke[0].split('/')
                        dqke = dqke[1].strip().replace('%', '').replace('/', '')
                    # print(dqke)
                    # 静胜球
                    jsqiu = dhtml.xpath('//*[@id="history_table"]/table/tbody/tr[1]/td[8]//text()')
                    jsqiulen = len(jsqiu)
                    if jsqiulen == 3:
                        jsqiu = jsqiu[2].strip().replace('+', '').replace('/', '')
                    if jsqiulen == 2:
                        jsqiu = jsqiu[1].strip().replace('+', '').replace('/', '')
                    if jsqiulen == 1:
                        jsqiu = jsqiu[0].split('/')
                        jsqiu = jsqiu[1].strip().replace('+', '').replace('/', '')
                    # print(jsqiu)
                    jsqiu2 = dhtml.xpath('//*[@id="history_table"]/table/tbody/tr[3]/td[8]//text()')
                    jsqiulen2 = len(jsqiu2)
                    if jsqiulen2 == 3:
                        jsqiu2 = jsqiu2[2].strip().replace('+', '').replace('/', '')
                    if jsqiulen2 == 2:
                        jsqiu2 = jsqiu2[1].strip().replace('+', '').replace('/', '')
                    if jsqiulen2 == 1:
                        jsqiu2 = jsqiu2[0].split('/')
                        jsqiu2 = jsqiu2[1].strip().replace('+', '').replace('/', '')
                    # print(jsqiu2)
                    jsqiu3 = dhtml.xpath('//*[@id="history_table"]/table/tbody/tr[1]/td[11]//text()')
                    jsqiulen3 = len(jsqiu3)
                    if jsqiulen3 == 3:
                        jsqiu3 = jsqiu3[2].strip().replace('+', '').replace('/', '')
                    if jsqiulen3 == 2:
                        jsqiu3 = jsqiu3[1].strip().replace('+', '').replace('/', '')
                    if jsqiulen3 == 1:
                        jsqiu3 = jsqiu3[0].split('/')
                        jsqiu3 = jsqiu3[1].strip().replace('+', '').replace('/', '')
                    # print(jsqiu3)
                    jsqiu4 = dhtml.xpath('//*[@id="history_table"]/table/tbody/tr[3]/td[11]//text()')
                    jsqiulen4 = len(jsqiu4)
                    if jsqiulen4 == 3:
                        jsqiu4 = jsqiu4[2].strip().replace('+', '').replace('/', '')
                    if jsqiulen4 == 2:
                        jsqiu4 = jsqiu4[1].strip().replace('+', '').replace('/', '')
                    if jsqiulen4 == 1:
                        jsqiu4 = jsqiu4[0].split('/')
                        jsqiu4 = jsqiu4[1].strip().replace('+', '').replace('/', '')
                    # print(jsqiu4)
                    # 让球赢盘
                    rqypan = dhtml.xpath('//*[@id="history_table"]/table/tbody/tr[1]/td[6]//text()')
                    rqypanlen = len(rqypan)
                    if rqypanlen == 3:
                        rqypan = rqypan[2].strip().replace('%', '').replace('/', '')
                    if rqypanlen == 2:
                        rqypan = rqypan[1].strip().replace('%', '').replace('/', '')
                    if rqypanlen == 1:
                        rqypan = rqypan[0].split('/')
                        rqypan = rqypan[1].strip().replace('%', '').replace('/', '')
                    # print(rqypan)
                    rqypan2 = dhtml.xpath('//*[@id="history_table"]/table/tbody/tr[3]/td[6]//text()')
                    rqypanlen2 = len(rqypan2)
                    if rqypanlen2 == 3:
                        rqypan2 = rqypan2[2].strip().replace('%', '').replace('/', '')
                    if rqypanlen2 == 2:
                        rqypan2 = rqypan2[1].strip().replace('%', '').replace('/', '')
                    if rqypanlen2 == 1:
                        rqypan2 = rqypan2[0].split('/')
                        rqypan2 = rqypan2[1].strip().replace('%', '').replace('/', '')
                    # print(rqypan2)
                    # 胜
                    sheng = dhtml.xpath('//*[@id="history_table"]/table/tbody/tr[1]/td[7]//text()')
                    shenglen = len(sheng)
                    if shenglen == 3:
                        sheng = sheng[1].strip().replace('%', '').replace('/', '')
                    if shenglen == 2:
                        sheng = sheng[1].strip().replace('%', '').replace('/', '')
                    if shenglen == 1:
                        sheng = sheng[0].split('/')
                        sheng = sheng[1].strip().replace('%', '').replace('/', '')
                    # print(sheng)
                    sheng2 = dhtml.xpath('//*[@id="history_table"]/table/tbody/tr[3]/td[7]//text()')
                    shenglen2 = len(sheng2)
                    if shenglen2 == 3:
                        sheng2 = sheng2[2].strip().replace('%', '').replace('/', '')
                    if shenglen2 == 2:
                        sheng2 = sheng2[1].strip().replace('%', '').replace('/', '')
                    if shenglen2 == 1:
                        sheng2 = sheng2[0].split('/')
                        sheng2 = sheng2[1].strip().replace('%', '').replace('/', '')
                    # print(sheng2)
                    # 角球
                    jiao = dhtml.xpath('//*[@id="history_table"]/table/tbody/tr[5]/td[9]//text()')
                    jiaolen = len(jiao)
                    jiaoban = None
                    jiaoquan = None
                    if jiaolen == 3:
                        jiaoban = jiao[0].strip().replace('/', '')
                        jiaoquan = jiao[2].strip().replace('/', '')
                    if jiaolen == 2:
                        jiaoban = jiao[0].strip().replace('/', '')
                        jiaoquan = jiao[1].strip().replace('/', '')
                    if jiaolen == 1:
                        jiao = jiao[0].split('/')
                        jiaoban = jiao[0].strip().replace('/', '')
                        jiaoquan = jiao[1].strip().replace('/', '')

                    # 主进
                    zhujin = dhtml.xpath('//*[@id="history_table"]/table/tbody/tr[1]/td[3]//text()')
                    zhujinlen = len(zhujin)
                    if zhujinlen == 3:
                        zhujin = zhujin[2].strip().replace('%', '').replace('/', '')
                    if zhujinlen == 2:
                        zhujin = zhujin[1].strip().replace('%', '').replace('/', '')
                    if zhujinlen == 1:
                        zhujin = zhujin[0].split('/')
                        zhujin = zhujin[1].strip().replace('%', '').replace('/', '')

                    # 主全进
                    zhuqj = dhtml.xpath('//*[@id="history_table"]/table/tbody/tr[2]/td[2]//text()')
                    zhuqjlen = len(zhuqj)
                    if zhuqjlen == 3:
                        zhuqj = zhuqj[2].strip().replace('%', '').replace('/', '')
                    if zhuqjlen == 2:
                        zhuqj = zhuqj[1].strip().replace('%', '').replace('/', '')
                    if zhuqjlen == 1:
                        zhuqj = zhuqj[0].split('/')
                        zhuqj = zhuqj[1].strip().replace('%', '').replace('/', '')

                    # 客进
                    kejin = dhtml.xpath('//*[@id="history_table"]/table/tbody/tr[3]/td[3]//text()')
                    kejinlen = len(kejin)
                    if kejinlen == 3:
                        kejin = kejin[2].strip().replace('%', '').replace('/', '')
                    if kejinlen == 2:
                        kejin = kejin[1].strip().replace('%', '').replace('/', '')
                    if kejinlen == 1:
                        kejin = kejin[0].split('/')
                        kejin = kejin[1].strip().replace('%', '').replace('/', '')

                    # 客全进
                    keqj = dhtml.xpath('//*[@id="history_table"]/table/tbody/tr[4]/td[2]//text()')
                    keqjlen = len(keqj)
                    if keqjlen == 3:
                        keqj = keqj[2].strip().replace('%', '').replace('/', '')
                    if keqjlen == 2:
                        keqj = keqj[1].strip().replace('%', '').replace('/', '')
                    if keqjlen == 1:
                        keqj = keqj[0].split('/')
                        keqj = keqj[1].strip().replace('%', '').replace('/', '')

                    url_baijia = 'https://www.dszuqiu.com/race_baijia/' + id
                    self.browser.get(url_baijia)
                    # 延迟秒数
                    time.sleep(random.randint(3, 7))
                    print('第二次请求:', response.status_code)
                    fhtml = etree.HTML(self.browser.page_source)
                    # 百家指数让球
                    rang36jizhu = fhtml.xpath('//*[@id="baijia"]/div[1]/div/div[2]/table/tbody/tr[1]/td[3]/text()')[0]
                    rang36jirang = fhtml.xpath('//*[@id="baijia"]/div[1]/div/div[2]/table/tbody/tr[1]/td[4]/text()')[
                        0].replace('+', '')
                    rang36chuzhu = fhtml.xpath('//*[@id="baijia"]/div[1]/div/div[2]/table/tbody/tr[2]/td[2]/text()')[0]
                    rang36churang = fhtml.xpath('//*[@id="baijia"]/div[1]/div/div[2]/table/tbody/tr[2]/td[3]/text()')[
                        0].replace('+', '')

                    # 百家指数大小球
                    daxiao36jidayu = \
                        fhtml.xpath(
                            '//*[@id="baijia"]/div[2]/div/div[2]/table//tr[@onclick="request(8)"][1]/td[3]/text()')[
                            0]
                    daxiao36jidaxiao = \
                        fhtml.xpath(
                            '//*[@id="baijia"]/div[2]/div/div[2]/table//tr[@onclick="request(8)"][1]/td[4]/text()')[
                            0]
                    daxiao36chudayu = \
                        fhtml.xpath(
                            '//*[@id="baijia"]/div[2]/div/div[2]/table//tr[@onclick="request(8)"][2]/td[2]/text()')[
                            0]
                    daxiao36chudaxiao = \
                        fhtml.xpath(
                            '//*[@id="baijia"]/div[2]/div/div[2]/table//tr[@onclick="request(8)"][2]/td[3]/text()')[
                            0]
                    try:
                        daxiaoS = fhtml.xpath(
                            '//*[@id="baijia"]/div[2]/div/div[2]/table//tr[@onclick="request(3)"][2]/td[2]/text()')[0]
                    except:
                        daxiaoS = '-'

                    try:
                        daxiao10 = fhtml.xpath(
                            '//*[@id="baijia"]/div[2]/div/div[2]/table//tr[@onclick="request(22)"][2]/td[2]/text()')[0]
                    except:
                        daxiao10 = '-'

                    try:
                        daxiaoyi = fhtml.xpath(
                            '//*[@id="baijia"]/div[2]/div/div[2]/table//tr[@onclick="request(12)"][2]/td[2]/text()')[0]
                    except:
                        daxiaoyi = '-'

                    try:
                        daxiaowei = fhtml.xpath(
                            '//*[@id="baijia"]/div[2]/div/div[2]/table//tr[@onclick="request(14)"][2]/td[2]/text()')[0]
                    except:
                        daxiaowei = '-'

                    try:
                        daxiaoming = fhtml.xpath(
                            '//*[@id="baijia"]/div[2]/div/div[2]/table//tr[@onclick="request(17)"][2]/td[2]/text()')[0]
                    except:
                        daxiaoming = '-'

                    try:
                        daxiaowei2 = fhtml.xpath(
                            '//*[@id="baijia"]/div[2]/div/div[2]/table//tr[@onclick="request(9)"][2]/td[2]/text()')[0]
                    except:
                        daxiaowei2 = '-'

                    try:
                        daxiaoli_cdy = fhtml.xpath(
                            '//*[@id="baijia"]/div[2]/div/div[2]/table//tr[@onclick="request(31)"][2]/td[2]/text()')[0]
                    except:
                        daxiaoli_cdy = '-'

                    try:
                        daxiaoli_cdx = fhtml.xpath(
                            '//*[@id="baijia"]/div[2]/div/div[2]/table//tr[@onclick="request(31)"][2]/td[3]/text()')[0]
                    except:
                        daxiaoli_cdx = '-'


                    try:
                        daxiaoli_jdy = fhtml.xpath(
                            '//*[@id="baijia"]/div[2]/div/div[2]/table//tr[@onclick="request(31)"][1]/td[@class="text-center"][2]/text()')[0]
                    except:
                        daxiaoli_jdy = '-'

                    try:
                        daxiaoli_jdx = fhtml.xpath(
                            '//*[@id="baijia"]/div[2]/div/div[2]/table//tr[@onclick="request(31)"][1]/td[@class="text-center"][3]/text()')[0]
                    except:
                        daxiaoli_jdx = '-'



                    try:
                        daxiaoying = fhtml.xpath(
                            '//*[@id="baijia"]/div[2]/div/div[2]/table//tr[@onclick="request(35)"][2]/td[2]/text()')[0]
                    except:
                        daxiaoying = '-'

                    try:
                        daxiaoli2 = fhtml.xpath(
                            '//*[@id="baijia"]/div[2]/div/div[2]/table//tr[@onclick="request(4)"][2]/td[2]/text()')[0]
                    except:
                        daxiaoli2 = '-'

                    info = [url_ss, saishi + '\t', qiudui + '\t', shijian + '\t', bifen1 + '\t', bifen2 + '\t',
                            str(bifenhe) + '\t', rqzhishu + '\t', rq1 + '\t', rq2 + '\t', jqzhishu + '\t',
                            dxzhishu + '\t',
                            zjjun + '\t', sqzhu + '\t', sqke + '\t', dqzhu + '\t', dqke + '\t',
                            jsqiu + '\t', jsqiu2 + '\t', dxq1 + '\t', dxq2 + '\t',
                            rqypan + '\t',
                            rqypan2 + '\t', sheng + '\t', sheng2 + '\t', jiaoban + '\t', jiaoquan + '\t',
                            zhujin + '\t', zhuqj + '\t', kejin + '\t', keqj + '\t', rang36jizhu + '\t',
                            rang36jirang + '\t', rang36chuzhu + '\t', rang36churang + '\t',
                            daxiao36jidayu + '\t', daxiao36jidaxiao + '\t', daxiao36chudayu + '\t',
                            daxiao36chudaxiao + '\t', daxiaoS + '\t', daxiao10 + '\t', daxiaoyi + '\t', daxiaowei + '\t',
                            daxiaoming + '\t', daxiaowei2 + '\t', daxiaoli_cdy + '\t', daxiaoying + '\t', daxiaoli2 + '\t', jsqiu3 + '\t', jsqiu4 + '\t', daxiaoli_cdx + '\t', daxiaoli_jdy + '\t', daxiaoli_jdx]
                    print(info)
                    name = f'DS已经完成比赛{date}'
                    if not os.path.exists(f'{name}.csv'):
                        head = ['url', '赛事', '比赛球队', '比赛时间', '比分', '比分', '总球', '让球', '主让', '客让',
                                '角球', '大小球', '总进球均', '主失球', '客失球', '主大球', '客大球', '主净胜', '客净胜', '大小盘口', '大小盘2', '让球盘口', '让球盘口2', '主胜', '客胜', '角球半', '角球全',
                                '主进', '主全进', '客进', '客全进', '让球36即主队', '让球36即让球', '让球36初主队', '让球36初让球',
                                '大小球36即主队', '大小球36即让球', '大小球36初主队', '大小球36初让球', '大小S初', '大小10初',
                                '大小易初', '大小韦初', '大小明初', '大小威初', '大小利初大于', '大小盈初', '大小立初', '净胜球主', '净胜球客', '大小利初大小', '大小利即大于', '大小利即大小']
                        csvFile = open(f'{name}.csv', 'a', newline='', encoding='utf-8-sig')
                        writer = csv.writer(csvFile)
                        writer.writerow(head)
                        csvFile.close()
                    else:
                        csvFile = open(f'{name}.csv', 'a+', newline='', encoding='utf-8-sig')
                        writer = csv.writer(csvFile)
                        writer.writerow(info)
                        csvFile.close()
                except Exception as e:
                    pass


if __name__ == '__main__':
    date, start_page, end_page = map(int, input('请输入日期、爬取页数(多少页到多少页以空格分开):').split())
    lz = Dszuqiu()
    lz.biaodan(date, start_page, end_page)
