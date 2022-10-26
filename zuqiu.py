# -*- coding: utf-8 -*-
import os
import re
import csv
import time
import random
import requests
from lxml import etree
from datetime import datetime
from selenium import webdriver
# from chaojiying import Chaojiying_Client

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


requests.packages.urllib3.disable_warnings()


class Dszuqiu(Selenium_Middleware):
    def __init__(self):
        self.session = self.session()
        self.headers = self.headers()
        self.headers2 = self.headers2()
        super().__init__()

    def session(self):
        session = requests.session()
        session.keep_alive = False
        session.adapters.DEFAULT_RETRIES = 10
        return session

    def headers(self):
        headers = {
            "User-Agent": random.choice([
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
                "Opera/8.0 (Windows NT 5.1; U; en)",
                "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
                "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
                "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
                "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10 Gecko / 20100922Ubuntu / 10.10(maverick)Firefox / 3.6.10",
                # Safari
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
                # chrome
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
                "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
                # 360
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
                "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",  # 淘宝浏览器
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
                # 猎豹浏览器
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
                "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
                "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
                # QQ浏览器
                "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
                "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
                # sogou浏览器
                "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
                # maxthon浏览器
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
                # UC浏览器
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
            ]),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers

    def headers2(self):
        headers2 = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cookie': ''
        }
        return headers2

    def login(self):
        login_url = 'https://www.dszuqiu.com/w_login'
        captcha_url = 'https://www.dszuqiu.com/captcha'
        resp = self.session.get(captcha_url, headers=self.headers, timeout=30, verify=False)
        print(resp.status_code)
        path = os.path.dirname(os.path.abspath(__file__))
        open(f"{path}/img/football.png", 'wb').write(resp.content)
        im = open(f'{path}/img/football.png', 'rb').read()
        chaojiying = Chaojiying_Client()
        code = chaojiying.PostPic(im, 1006)
        result = code["pic_str"].lower()
        print('验证码识别结果为:', result)
        data = {
            "zhanghu": 'foreign.trade1@cibsc.biz',
            "password": '11223344o',
            "captcha_input": result,
            "rememberMe": '1',
            "is_ajax": '1'
        }
        response = self.session.post(login_url, headers=self.headers, data=data)
        print(response.status_code)
        cookie = requests.utils.dict_from_cookiejar(self.session.cookies)
        return cookie

    def biaodan(self, start_page, end_page):
        for page in range(start_page, end_page):
            index_url = f"https://www.dszuqiu.com/league/40/p.{page}?type=ended_race"
            res = self.session.get(index_url, headers=self.headers, timeout=30, verify=False)
            print('第一次请求:', res.status_code)
            if res.status_code == 200:
                html = etree.HTML(res.text)
                xi = html.xpath('//section[@id="ended"]//tbody/tr/td/a[@title="析"]/@href')
                for x in xi:
                    id = re.findall('/race/([\s|\S]+)', x)[0]
                    print(id)
                    url = 'http://www.dszuqiu.com/race_ss/' + id
                    response = self.session.get(url, headers=self.headers, timeout=30, verify=False)
                    time.sleep(1)
                    print('第二次请求:', response.status_code)
                    dhtml = etree.HTML(response.text)
                    # 比赛球队
                    qiudui = dhtml.xpath('//h3[@class="dsBreadcrumbs"]/text()')[-1].strip()
                    # 指数趋势
                    zhishu = dhtml.xpath('//*[@id="race_part"]/div[3]/div/table/tbody/tr/td[5]/a/text()')[0].strip()
                    # 半角球全
                    jiao1 = dhtml.xpath('//*[@id="race_part"]/div[3]/div/table/tbody/tr/td[1]/text()')[0].strip()
                    jiao2 = dhtml.xpath('//*[@id="race_part"]/div[3]/div/table/tbody/tr/td[2]/text()')[0].strip()
                    jiaoquan = jiao1 + ' ' + jiao2
                    # 半进球全
                    jin1 = dhtml.xpath('//*[@id="race_part"]/div[3]/div/table/tbody/tr/td[3]/text()')[0].strip()
                    jin2 = dhtml.xpath('//*[@id="race_part"]/div[3]/div/table/tbody/tr/td[4]/text()')[0].strip()
                    jinquan = jin1 + ' ' + jin2
                    # 进球分布主
                    try:
                        jinzhu1 = dhtml.xpath(
                            '/html/body/div/main/div/div/div/div[2]/div/div[1]/div[2]/div/div[1]/table/tbody/tr/td[1]/text()')[
                            0].strip()
                        jinzhu2 = dhtml.xpath(
                            '/html/body/div/main/div/div/div/div[2]/div/div[1]/div[2]/div/div[1]/table/tbody/tr/td[2]/text()')[
                            0].strip()
                        jinzhu3 = dhtml.xpath(
                            '/html/body/div/main/div/div/div/div[2]/div/div[1]/div[2]/div/div[1]/table/tbody/tr/td[3]/text()')[
                            0].strip()
                        jinzhu4 = dhtml.xpath(
                            '/html/body/div/main/div/div/div/div[2]/div/div[1]/div[2]/div/div[1]/table/tbody/tr/td[4]/text()')[
                            0].strip()
                        jinzhu5 = dhtml.xpath(
                            '/html/body/div/main/div/div/div/div[2]/div/div[1]/div[2]/div/div[1]/table/tbody/tr/td[5]/text()')[
                            0].strip()
                        jinzhu6 = dhtml.xpath(
                            '/html/body/div/main/div/div/div/div[2]/div/div[1]/div[2]/div/div[1]/table/tbody/tr/td[6]/text()')[
                            0].strip()
                        jinzhu = jinzhu1 + ' ' + jinzhu2 + ' ' + jinzhu3 + ' ' + jinzhu4 + ' ' + jinzhu5 + ' ' + jinzhu6
                    except:
                        jinzhu = ''
                    # 进球分布客
                    try:
                        jinke1 = dhtml.xpath(
                            '/html/body/div/main/div/div/div/div[2]/div/div[1]/div[2]/div/div[2]/table/tbody/tr/td[1]/text()')[
                            0].strip()
                        jinke2 = dhtml.xpath(
                            '/html/body/div/main/div/div/div/div[2]/div/div[1]/div[2]/div/div[2]/table/tbody/tr/td[2]/text()')[
                            0].strip()
                        jinke3 = dhtml.xpath(
                            '/html/body/div/main/div/div/div/div[2]/div/div[1]/div[2]/div/div[2]/table/tbody/tr/td[3]/text()')[
                            0].strip()
                        jinke4 = dhtml.xpath(
                            '/html/body/div/main/div/div/div/div[2]/div/div[1]/div[2]/div/div[2]/table/tbody/tr/td[4]/text()')[
                            0].strip()
                        jinke5 = dhtml.xpath(
                            '/html/body/div/main/div/div/div/div[2]/div/div[1]/div[2]/div/div[2]/table/tbody/tr/td[5]/text()')[
                            0].strip()
                        jinke6 = dhtml.xpath(
                            '/html/body/div/main/div/div/div/div[2]/div/div[1]/div[2]/div/div[2]/table/tbody/tr/td[6]/text()')[
                            0].strip()
                        jinke = jinke1 + ' ' + jinke2 + ' ' + jinke3 + ' ' + jinke4 + ' ' + jinke5 + ' ' + jinke6
                    except:
                        jinke = ''
                    # 主客
                    self.browser.get(url)
                    fhtml = etree.HTML(self.browser.page_source)
                    zhukezhu = fhtml.xpath('//*[@id="history_table"]/table/tbody/tr[1]/td[3]/text()')[0].strip()
                    zhukeke = fhtml.xpath('//*[@id="history_table"]/table/tbody/tr[3]/td[3]/text()')[0].strip()
                    zhukejsz = fhtml.xpath('//*[@id="history_table"]/table/tbody/tr[1]/td[8]//text()')
                    zhukejsz = ''.join(zhukejsz)
                    zhukejsk = fhtml.xpath('//*[@id="history_table"]/table/tbody/tr[3]/td[8]//text()')
                    zhukejsk = ''.join(zhukejsk)
                    zhukepz = fhtml.xpath('//*[@id="history_table"]/table/tbody/tr[1]/td[6]//text()')
                    zhukepz = ''.join(zhukepz)
                    zhukepk = fhtml.xpath('//*[@id="history_table"]/table/tbody/tr[3]/td[6]//text()')
                    zhukepk = ''.join(zhukepk)
                    zhukezs = fhtml.xpath('//*[@id="history_table"]/table/tbody/tr[1]/td[7]//text()')
                    zhukezs = ''.join(zhukezs)
                    zhukeks = fhtml.xpath('//*[@id="history_table"]/table/tbody/tr[3]/td[7]//text()')
                    zhukeks = ''.join(zhukeks)
                    # 全部
                    self.browser.find_elements_by_xpath('//*[@id="tabid1"]')[0].click()
                    ghtml = etree.HTML(self.browser.page_source)
                    quanjinzhu = ghtml.xpath('//*[@id="history_table"]/table/tbody/tr[1]/td[3]/text()')[0].strip()
                    quanjinke = ghtml.xpath('//*[@id="history_table"]/table/tbody/tr[3]/td[3]/text()')[0].strip()
                    quanshengjsz = ghtml.xpath('//*[@id="history_table"]/table/tbody/tr[1]/td[8]//text()')
                    quanshengjsz = ''.join(quanshengjsz)
                    quanshengjsk = ghtml.xpath('//*[@id="history_table"]/table/tbody/tr[3]/td[8]//text()')
                    quanshengjsk = ''.join(quanshengjsk)
                    quanyingpz = ghtml.xpath('//*[@id="history_table"]/table/tbody/tr[1]/td[6]//text()')
                    quanyingpz = ''.join(quanyingpz)
                    quanyingpk = ghtml.xpath('//*[@id="history_table"]/table/tbody/tr[3]/td[6]//text()')
                    quanyingpk = ''.join(quanyingpk)
                    quanzs = ghtml.xpath('//*[@id="history_table"]/table/tbody/tr[1]/td[7]//text()')
                    quanzs = ''.join(quanzs)
                    quanks = ghtml.xpath('//*[@id="history_table"]/table/tbody/tr[3]/td[7]//text()')
                    quanks = ''.join(quanks)

                    info = [url, qiudui + '\t', zhishu + '\t', jiaoquan + '\t', jinquan + '\t', jinzhu + '\t',
                            jinke + '\t',
                            zhukezhu + '\t', zhukeke + '\t', zhukejsz + '\t', zhukejsk + '\t', zhukepz + '\t',
                            zhukepk + '\t', zhukezs + '\t', zhukeks + '\t',
                            quanjinzhu + '\t', quanjinke + '\t', quanshengjsz + '\t', quanshengjsk + '\t',
                            quanyingpz + '\t', quanyingpk + '\t', quanzs + '\t', quanks + '\t']
                    print(info)
                    name = datetime.utcnow().strftime("%Y%m%d")
                    if not os.path.exists(f'{name}.csv'):
                        head = ['url', '比赛球队', '指数走势', '半角球全', '半进球全', '进球分布主', '进球分布客',
                                '主客进球主', '主客进球客', '主客净胜主', '主客净胜客', '主客赢盘主', '主客赢盘客', '主客主胜', '主客客胜',
                                '全进球主', '全进球客', '全净胜主', '全净胜客', '全赢盘主', '全赢盘客', '全主胜', '全客胜']
                        csvFile = open(f'{name}.csv', 'a', newline='', encoding='utf-8-sig')
                        writer = csv.writer(csvFile)
                        writer.writerow(head)
                        csvFile.close()
                    else:
                        csvFile = open(f'{name}.csv', 'a+', newline='', encoding='utf-8-sig')
                        writer = csv.writer(csvFile)
                        writer.writerow(info)
                        csvFile.close()


if __name__ == '__main__':
    start_page, end_page = map(int, input('请输入爬取页数(多少页到多少页以空格分开):').split())
    lz = Dszuqiu()
    lz.biaodan(start_page, end_page)
