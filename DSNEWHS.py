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
        index_url = f"https://www.dszuqiu.com/diary/{date}"
        self.browser.get(index_url)
        time.sleep(1)
        self.browser.find_elements_by_xpath('//*[@id="pjax-container"]/div/div/div[1]/div[2]/ul[1]/li[5]/a')[
            0].click()
        time.sleep(1)
        self.browser.find_elements_by_xpath('//*[@id="pankou-list-filter"]/ul/li[3]/a')[0].click()
        time.sleep(1)
        self.browser.find_elements_by_xpath('//*[@id="corner-list-filter"]/form/div[2]/div/div[2]/button')[
            0].click()
        time.sleep(5)
        for num in range(start_page, end_page + 1):
            in_url = f'https://www.dszuqiu.com/diary/{date}/p.{num}'
            print(f'当前采集页数:{in_url}')
            self.browser.get(in_url)
            html = etree.HTML(self.browser.page_source)
            xi = html.xpath('//*[@id="diary_info"]/table/tbody/tr/td[12]/a/@href')
            print(xi)
            for x in xi:
                id = re.findall('/race/([\s|\S]+)', x)[0]
                url_sp = 'https://www.dszuqiu.com/race_sp/' + id
                response = self.session.get(url_sp, headers=headers, timeout=30, verify=False)
                # 延迟秒数
                time.sleep(random.randint(2, 10))
                print('第二次请求:', response.status_code)
                chtml = etree.HTML(response.text)
                rq_list = []
                rq = chtml.xpath('//tbody[@id="sp_rangfen"]/tr')
                rq_lenght = len(rq)
                for index in range(0, rq_lenght):
                    poster = rq[index]
                    result = poster.xpath('td[@class="text-center red-color" or @class="text-center red-color xh-highlight"]/text()')[0]
                    if result == "-":
                        r1 = poster.xpath('td[3]/text()')[0]
                        rq_list.append(r1)
                rq1 = rq_list[0]
                try:
                    rq2 = rq_list[1]
                except:
                    rq2 = '0'

                dxq_list = []
                dxq = chtml.xpath('//tbody[@id="sp_daxiao"]/tr')
                dxq_lenght = len(dxq)
                for index in range(0, dxq_lenght):
                    poster = dxq[index]
                    result = poster.xpath('td[@class="text-center red-color" or @class="text-center red-color xh-highlight"]/text()')[0]
                    if result == "-":
                        r1 = poster.xpath('td[3]/text()')[0]
                        dxq_list.append(r1)
                dxq1 = dxq_list[0]
                try:
                    dxq2 = dxq_list[1]
                except:
                    dxq2 = '0'
                try:
                    url_ss = 'https://www.dszuqiu.com/race_ss/' + id
                    # response = self.session.get(url_ss, headers=headers, timeout=30, verify=False)
                    self.browser.get(url_ss)
                    # 延迟秒数
                    time.sleep(random.randint(2,10))
                    print('第二次请求:', response.status_code)
                    dhtml = etree.HTML(self.browser.page_source)
                    # try:
                    # 比赛球队
                    saishi = dhtml.xpath('//h3[@class="dsBreadcrumbs"]/a[3]/text()')[0].strip()
                    qiudui = dhtml.xpath('//h3[@class="dsBreadcrumbs"]/text()')[-1].strip()
                    shijian = dhtml.xpath('//span[@class="analysisRaceTime"]/text()')[0].strip()
                    bifen = dhtml.xpath('//*[@id="race_part"]/div[3]/div/table/tbody/tr/td[4]/text()')[0].strip()
                    bifen = bifen.split(':')
                    bifen = int(bifen[0]) + int(bifen[1])
                    # print(saishi,qiudui,shijian,bifen)
                    # 指数趋势
                    zhishu = dhtml.xpath('//*[@id="race_part"]/div[3]/div/table/tbody/tr/td[5]/a/text()')[0].strip()
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
                        dqzhu = dqzhu[2].strip().replace('%', '')
                    if dqzhulen == 2:
                        dqzhu = dqzhu[1].strip().replace('%', '')
                    if dqzhulen == 1:
                        dqzhu = dqzhu[0].split('/')
                        dqzhu = dqzhu[1].strip().replace('%', '')
                    # print(dqzhu)
                    # 大球客
                    dqke = dhtml.xpath('//*[@id="history_table"]/table/tbody/tr[3]/td[5]//text()')
                    dqkelen = len(dqke)
                    if dqkelen == 3:
                        dqke = dqke[2].strip().replace('%', '')
                    if dqkelen == 2:
                        dqke = dqke[1].strip().replace('%', '')
                    if dqkelen == 1:
                        dqke = dqke[0].split('/')
                        dqke = dqke[1].strip().replace('%', '')
                    # print(dqke)
                    # 静胜球
                    jsqiu = dhtml.xpath('//*[@id="history_table"]/table/tbody/tr[1]/td[8]//text()')
                    jsqiulen = len(jsqiu)
                    if jsqiulen == 3:
                        jsqiu = jsqiu[2].strip().replace('+', '')
                    if jsqiulen == 2:
                        jsqiu = jsqiu[1].strip().replace('+', '')
                    if jsqiulen == 1:
                        jsqiu = jsqiu[0].split('/')
                        jsqiu = jsqiu[1].strip().replace('+', '')
                    # print(jsqiu)
                    jsqiu2 = dhtml.xpath('//*[@id="history_table"]/table/tbody/tr[3]/td[8]//text()')
                    jsqiulen2 = len(jsqiu2)
                    if jsqiulen2 == 3:
                        jsqiu2 = jsqiu2[2].strip().replace('+', '')
                    if jsqiulen2 == 2:
                        jsqiu2 = jsqiu2[1].strip().replace('+', '')
                    if jsqiulen2 == 1:
                        jsqiu2 = jsqiu2[0].split('/')
                        jsqiu2 = jsqiu2[1].strip().replace('+', '')
                    # print(jsqiu2)
                    # 让球赢盘
                    rqypan = dhtml.xpath('//*[@id="history_table"]/table/tbody/tr[1]/td[6]//text()')
                    rqypanlen = len(rqypan)
                    if rqypanlen == 3:
                        rqypan = rqypan[2].strip().replace('%', '')
                    if rqypanlen == 2:
                        rqypan = rqypan[1].strip().replace('%', '')
                    if rqypanlen == 1:
                        rqypan = rqypan[0].split('/')
                        rqypan = rqypan[1].strip().replace('%', '')
                    # print(rqypan)
                    rqypan2 = dhtml.xpath('//*[@id="history_table"]/table/tbody/tr[3]/td[6]//text()')
                    rqypanlen2 = len(rqypan2)
                    if rqypanlen2 == 3:
                        rqypan2 = rqypan2[2].strip().replace('%', '')
                    if rqypanlen2 == 2:
                        rqypan2 = rqypan2[1].strip().replace('%', '')
                    if rqypanlen2 == 1:
                        rqypan2 = rqypan2[0].split('/')
                        rqypan2 = rqypan2[1].strip().replace('%', '')
                    # print(rqypan2)
                    # 胜
                    sheng = dhtml.xpath('//*[@id="history_table"]/table/tbody/tr[1]/td[7]//text()')
                    shenglen = len(sheng)
                    if shenglen == 3:
                        sheng = sheng[1].strip().replace('%', '')
                    if shenglen == 2:
                        sheng = sheng[1].strip().replace('%', '')
                    if shenglen == 1:
                        sheng = sheng[0].split('/')
                        sheng = sheng[1].strip().replace('%', '')
                    # print(sheng)
                    sheng2 = dhtml.xpath('//*[@id="history_table"]/table/tbody/tr[3]/td[7]//text()')
                    shenglen2 = len(sheng2)
                    if shenglen2 == 3:
                        sheng2 = sheng2[2].strip().replace('%', '')
                    if shenglen2 == 2:
                        sheng2 = sheng2[1].strip().replace('%', '')
                    if shenglen2 == 1:
                        sheng2 = sheng2[0].split('/')
                        sheng2 = sheng2[1].strip().replace('%', '')
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
                        jiaoban = jiao[0].strip()
                        jiaoquan = jiao[1].strip()

                    info = [url_ss, saishi + '\t', qiudui + '\t', shijian + '\t', bifen + '\t',
                            rqzhishu + '\t', rq1 + '\t', rq2 + '\t', jqzhishu + '\t', dxzhishu + '\t',
                                zjjun + '\t', sqzhu + '\t', sqke + '\t', dqzhu + '\t', dqke + '\t',
                            jsqiu + '\t', jsqiu2 + '\t', dxq1 + '\t', dxq2 + '\t', rqypan + '\t',
                            rqypan2 + '\t', sheng + '\t', sheng2 + '\t', jiaoban + '\t', jiaoquan]
                    print(info)
                    name = f'DS比赛统计{date}'
                    if not os.path.exists(f'{name}.csv'):
                        head = ['url', '赛事', '比赛球队', '比赛时间', '比分', '让球', '让球数据1', '让球数据2',
                                '角球', '大小球', '总进球均', '失球主', '失球客', '大球主', '大球客', '净胜球1',
                                '净胜球2', '大小球盘1', '大小球盘2', '让球赢盘1', '让球赢盘2', '胜1', '胜2', '角球半', '角球全']
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
