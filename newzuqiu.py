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


class Dszuqiu(Selenium_Middleware):
    def __init__(self):
        self.session = self.session()
        super().__init__()

    def session(self):
        session = requests.session()
        session.keep_alive = False
        session.adapters.DEFAULT_RETRIES = 10
        return session

    def nextPage(self):
        self.browser.find_element_by_link_text('下一页 »').click()

    def biaodan(self, start_page, end_page):
        index_url = "https://www.dszuqiu.com/diary"
        self.browser.get(index_url)
        time.sleep(1)
        self.browser.find_elements_by_xpath('//*[@id="pjax-container"]/div/div/div[1]/div[2]/ul[1]/li[5]/a')[0].click()
        time.sleep(1)
        self.browser.find_elements_by_xpath('//*[@id="pankou-list-filter"]/ul/li[3]/a')[0].click()
        time.sleep(1)
        self.browser.find_elements_by_xpath('//*[@id="corner-list-filter"]/form/div[2]/div/div[2]/button')[0].click()
        time.sleep(5)
        for num in range(start_page, end_page+1):
            in_url = f'https://www.dszuqiu.com/diary/p.{num}'
            print(f'当前采集页数:{in_url}')
            self.browser.get(in_url)
            html = etree.HTML(self.browser.page_source)
            xi = html.xpath('//*[@id="diary_info"]/table/tbody/tr/td[17]/a/@href')
            for x in xi:
                id = re.findall('/race/([\s|\S]+)', x)[0]
                url = 'http://www.dszuqiu.com/race_ss/' + id
                self.browser.get(url)
                fhtml = etree.HTML(self.browser.page_source)
                # 延迟秒数
                time.sleep(random.randint(1,3))
                try:
                    # 比赛球队
                    qiudui = fhtml.xpath('//h3[@class="dsBreadcrumbs"]/text()')[-1].strip()
                    # 指数趋势
                    zhishu = fhtml.xpath('//*[@id="race_part"]/div[2]/div/table/tbody/tr/td[5]/a/text()')[0].strip()
                    # 进球分布主
                    try:
                        jinzhu1 = fhtml.xpath(
                            '/html/body/div/main/div/div/div/div[2]/div/div[1]/div[2]/div/div[1]/table/tbody/tr/td[1]/text()')[
                            0].strip()
                        jinzhu2 = fhtml.xpath(
                            '/html/body/div/main/div/div/div/div[2]/div/div[1]/div[2]/div/div[1]/table/tbody/tr/td[2]/text()')[
                            0].strip()
                        jinzhu3 = fhtml.xpath(
                            '/html/body/div/main/div/div/div/div[2]/div/div[1]/div[2]/div/div[1]/table/tbody/tr/td[3]/text()')[
                            0].strip()
                        jinzhu4 = fhtml.xpath(
                            '/html/body/div/main/div/div/div/div[2]/div/div[1]/div[2]/div/div[1]/table/tbody/tr/td[4]/text()')[
                            0].strip()
                        jinzhu5 = fhtml.xpath(
                            '/html/body/div/main/div/div/div/div[2]/div/div[1]/div[2]/div/div[1]/table/tbody/tr/td[5]/text()')[
                            0].strip()
                        jinzhu6 = fhtml.xpath(
                            '/html/body/div/main/div/div/div/div[2]/div/div[1]/div[2]/div/div[1]/table/tbody/tr/td[6]/text()')[
                            0].strip()
                        jinzhu = jinzhu1 + ' ' + jinzhu2 + ' ' + jinzhu3 + ' ' + jinzhu4 + ' ' + jinzhu5 + ' ' + jinzhu6
                    except:
                        jinzhu = ''
                    # 进球分布客
                    try:
                        jinke1 = fhtml.xpath(
                            '/html/body/div/main/div/div/div/div[2]/div/div[1]/div[2]/div/div[2]/table/tbody/tr/td[1]/text()')[
                            0].strip()
                        jinke2 = fhtml.xpath(
                            '/html/body/div/main/div/div/div/div[2]/div/div[1]/div[2]/div/div[2]/table/tbody/tr/td[2]/text()')[
                            0].strip()
                        jinke3 = fhtml.xpath(
                            '/html/body/div/main/div/div/div/div[2]/div/div[1]/div[2]/div/div[2]/table/tbody/tr/td[3]/text()')[
                            0].strip()
                        jinke4 = fhtml.xpath(
                            '/html/body/div/main/div/div/div/div[2]/div/div[1]/div[2]/div/div[2]/table/tbody/tr/td[4]/text()')[
                            0].strip()
                        jinke5 = fhtml.xpath(
                            '/html/body/div/main/div/div/div/div[2]/div/div[1]/div[2]/div/div[2]/table/tbody/tr/td[5]/text()')[
                            0].strip()
                        jinke6 = fhtml.xpath(
                            '/html/body/div/main/div/div/div/div[2]/div/div[1]/div[2]/div/div[2]/table/tbody/tr/td[6]/text()')[
                            0].strip()
                        jinke = jinke1 + ' ' + jinke2 + ' ' + jinke3 + ' ' + jinke4 + ' ' + jinke5 + ' ' + jinke6
                    except:
                        jinke = ''
                    # 主客
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

                    info = [url, qiudui + '\t', zhishu + '\t', jinzhu + '\t',
                            jinke + '\t',
                            zhukezhu + '\t', zhukeke + '\t', zhukejsz + '\t', zhukejsk + '\t', zhukepz + '\t',
                            zhukepk + '\t', zhukezs + '\t', zhukeks + '\t',
                            quanjinzhu + '\t', quanjinke + '\t', quanshengjsz + '\t', quanshengjsk + '\t',
                            quanyingpz + '\t', quanyingpk + '\t', quanzs + '\t', quanks + '\t']
                    print(info)
                    name = f'{datetime.utcnow().strftime("%Y%m%d")}'
                    if not os.path.exists(f'{name}.csv'):
                        head = ['url', '比赛球队', '指数走势',  '进球分布主', '进球分布客',
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
                except:
                    pass

if __name__ == '__main__':
    start_page, end_page = map(int, input('请输入爬取页数(多少页到多少页以空格分开):').split())
    lz = Dszuqiu()
    lz.biaodan(start_page, end_page)
