# -*- coding: utf-8 -*-
import os
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


class JH8(Selenium_Middleware):
    def __init__(self):
        self.session = self.session()
        self.headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'Connection': 'close'}
        super().__init__()


    def session(self):
        session = requests.session()
        session.keep_alive = False
        session.adapters.DEFAULT_RETRIES = 10
        requests.packages.urllib3.disable_warnings()
        return session

    def Getdata(self, ls_id, start_year, end_year):
        task_id = []
        api = [f"https://api-node.jihai8.com/api/data/schedule_odds?sclass_id={ls_id}&season={start_year}-{end_year}&sub_id=&round={id}" for id in range(1,37)]
        for url in api:
            res = requests.get(url, headers=self.headers, timeout=30, verify=False)
            if res.status_code == 200:
                schedule_id_list = res.json()["data"]["standard"]
                for schedule_id in schedule_id_list:
                    schedule_id = schedule_id["schedule_id"]
                    task_id.append(schedule_id)
        if len(task_id) == 0:
            api = [f"https://api-node.jihai8.com/api/data/schedule_odds?sclass_id={ls_id}&season={start_year}-{end_year}&sub_id=&round="]
            for url in api:
                res = requests.get(url, headers=self.headers, timeout=30, verify=False)
                if res.status_code == 200:
                    schedule_id_list = res.json()["data"]["standard"]
                    for schedule_id in schedule_id_list:
                        schedule_id = schedule_id["schedule_id"]
                        task_id.append(schedule_id)
        return task_id

    def Jiexi(self,task_id):
        for id in task_id:
            try:
                time.sleep(random.randint(5, 10))
                analysis_url = f'https://www.jihai8.com/zq/analysis_{id}.html'
                self.browser.get(analysis_url)
                if "您的访问频率过快，请稍等" or "Server error"  in self.browser.page_source:
                    while True:
                        time.sleep(10)
                        self.browser.refresh()
                        if "您的访问频率过快，请稍等" not in self.browser.page_source and "Server error" not in self.browser.page_source:
                            break
                # 分析
                self.browser.find_elements_by_xpath('//*[@id="porlet_4"]/div[1]/div[1]/span[1]')[0].click()
                index = etree.HTML(self.browser.page_source)
                date = index.xpath('//*[@id="__layout"]/div/section/div[2]/div/div[2]/div[1]/text()')[1].strip()
                bsqdz = index.xpath('//*[@id="__layout"]/div/section/div[2]/div/div[1]/div/a/span[2]/text()')[0].strip()
                bsqdy = index.xpath('//*[@id="__layout"]/div/section/div[2]/div/div[3]/div/a/span[1]/text()')[0].strip()
                bfz = index.xpath('//*[@id="__layout"]/div/section/div[2]/div/div[2]/div[2]/span[1]/b/text()')[0].strip()
                bfy = index.xpath('//*[@id="__layout"]/div/section/div[2]/div/div[2]/div[2]/span[3]/b/text()')[0].strip()
                he = int(bfz) + int(bfy)
                zjq = index.xpath('//*[@id="porlet_6"]/div[2]/table/tbody/tr[8]/td[4]/div/span[2]/text()')[0].strip()

                zds = index.xpath('//*[@id="porlet_4"]/div[2]/div/div[3]/span/b/text()')[0].strip().replace('%','')
                ying = index.xpath('//*[@id="porlet_4"]/div[2]/div/div[4]/span/b/text()')[0].strip().replace('%','')
                dql = index.xpath('//*[@id="porlet_4"]/div[2]/div/div[5]/span/b/text()')[0].strip().replace('%','')
                cjjq = index.xpath('//*[@id="porlet_4"]/div[2]/div/div[7]/span/b/text()')[0].strip()
                cjsq = index.xpath('//*[@id="porlet_4"]/div[2]/div/div[8]/span/b/text()')[0].strip()
                kds = index.xpath('//*[@id="porlet_4"]/div[3]/div/div[3]/span/b/text()')[0].strip().replace('%','')
                kying = index.xpath('//*[@id="porlet_4"]/div[3]/div/div[4]/span/b/text()')[0].strip().replace('%','')
                kdql = index.xpath('//*[@id="porlet_4"]/div[3]/div/div[5]/span/b/text()')[0].strip().replace('%','')
                kcjjq = index.xpath('//*[@id="porlet_4"]/div[3]/div/div[7]/span/b/text()')[0].strip()
                kcjsq = index.xpath('//*[@id="porlet_4"]/div[3]/div/div[8]/span/b/text()')[0].strip()
                print(analysis_url, date, bsqdz, bsqdy, bfz, bfy, he, zjq, zds, ying, dql, cjjq, cjsq, kds, kying, kdql, kcjjq, kcjsq)

                #必发
                time.sleep(random.randint(5, 10))
                bifa_url = f'https://www.jihai8.com/zq/bifa_{id}.html'
                self.browser.get(bifa_url)
                if "您的访问频率过快，请稍等" or "Server error"  in self.browser.page_source:
                    while True:
                        time.sleep(10)
                        self.browser.refresh()
                        if "您的访问频率过快，请稍等" not in self.browser.page_source and "Server error" not in self.browser.page_source:
                            break
                index2 = etree.HTML(self.browser.page_source)
                zhuz = index2.xpath('//*[@id="__layout"]/div/section/div[4]/div[1]/div/table/tbody/tr[1]/td[2]/text()')[0].strip()
                pingz = index2.xpath('//*[@id="__layout"]/div/section/div[4]/div[1]/div/table/tbody/tr[2]/td[2]/text()')[0].strip()
                kez = index2.xpath('//*[@id="__layout"]/div/section/div[4]/div[1]/div/table/tbody/tr[3]/td[2]/text()')[0].strip()
                zhuyk = index2.xpath('//*[@id="__layout"]/div/section/div[4]/div[1]/div/table/tbody/tr[1]/td[11]/text()')[0].strip()
                pingyk = index2.xpath('//*[@id="__layout"]/div/section/div[4]/div[1]/div/table/tbody/tr[2]/td[9]/text()')[0].strip()
                keyk = index2.xpath('//*[@id="__layout"]/div/section/div[4]/div[1]/div/table/tbody/tr[3]/td[9]/text()')[0].strip()
                zhulr = index2.xpath('//*[@id="__layout"]/div/section/div[4]/div[1]/div/table/tbody/tr[1]/td[12]/text()')[0].strip()
                pinglr = index2.xpath('//*[@id="__layout"]/div/section/div[4]/div[1]/div/table/tbody/tr[2]/td[10]/text()')[0].strip()
                kelr = index2.xpath('//*[@id="__layout"]/div/section/div[4]/div[1]/div/table/tbody/tr[3]/td[10]/text()')[0].strip()
                zhugm = index2.xpath('//*[@id="__layout"]/div/section/div[4]/div[1]/div/table/tbody/tr[1]/td[13]/text()')[0].strip()
                pinggm = index2.xpath('//*[@id="__layout"]/div/section/div[4]/div[1]/div/table/tbody/tr[2]/td[11]/text()')[0].strip()
                kegm = index2.xpath('//*[@id="__layout"]/div/section/div[4]/div[1]/div/table/tbody/tr[3]/td[11]/text()')[0].strip()
                zhucs = index2.xpath('//*[@id="__layout"]/div/section/div[4]/div[1]/div/table/tbody/tr[1]/td[14]/text()')[0].strip()
                pingcs = index2.xpath('//*[@id="__layout"]/div/section/div[4]/div[1]/div/table/tbody/tr[2]/td[12]/text()')[0].strip()
                kecs = index2.xpath('//*[@id="__layout"]/div/section/div[4]/div[1]/div/table/tbody/tr[3]/td[12]/text()')[0].strip()
                print(zhuz, pingz, kez, zhuyk, pingyk, keyk, zhulr, pinglr, kelr, zhugm, pinggm, kegm, zhucs, pingcs, kecs)

                # 欧指
                time.sleep(random.randint(5, 10))
                ouzhi_url = f'https://www.jihai8.com/zq/europe_{id}.html'
                self.browser.get(ouzhi_url)
                if "您的访问频率过快，请稍等" or "Server error"  in self.browser.page_source:
                    while True:
                        time.sleep(10)
                        self.browser.refresh()
                        if "您的访问频率过快，请稍等" not in self.browser.page_source and "Server error" not in self.browser.page_source:
                            break
                index3= etree.HTML(self.browser.page_source)
                zhukl = index3.xpath('//*[@id="__layout"]/div/section/div[4]/div[2]/div[3]/table/tbody/tr[2]/td[3]/div/span[1]/text()')[0].strip()
                pingkl = index3.xpath('//*[@id="__layout"]/div/section/div[4]/div[2]/div[3]/table/tbody/tr[2]/td[3]/div/span[2]/text()')[0].strip()
                kekl = index3.xpath('//*[@id="__layout"]/div/section/div[4]/div[2]/div[3]/table/tbody/tr[2]/td[3]/div/span[3]/text()')[0].strip()
                fanh = index3.xpath('//*[@id="__layout"]/div/section/div[4]/div[2]/div[3]/table/tbody/tr[2]/td[4]/text()')[0].strip()
                if "竞彩官方" in self.browser.page_source:
                    zhujc = index3.xpath('//*[@id="__layout"]/div/section/div[4]/div[2]/div[3]/table/tbody/tr[6]/td[1]/div/span[1]/text()')[0].strip()
                    pingjc = index3.xpath('//*[@id="__layout"]/div/section/div[4]/div[2]/div[3]/table/tbody/tr[6]/td[1]/div/span[2]/text()')[0].strip()
                    kejc = index3.xpath('//*[@id="__layout"]/div/section/div[4]/div[2]/div[3]/table/tbody/tr[6]/td[1]/div/span[3]/text()')[0].strip()
                    zhukl2 = index3.xpath('//*[@id="__layout"]/div/section/div[4]/div[2]/div[3]/table/tbody/tr[6]/td[3]/div/span[1]/text()')[0].strip()
                    pingkl2 = index3.xpath('//*[@id="__layout"]/div/section/div[4]/div[2]/div[3]/table/tbody/tr[6]/td[3]/div/span[2]/text()')[0].strip()
                    kekl2 = index3.xpath('//*[@id="__layout"]/div/section/div[4]/div[2]/div[3]/table/tbody/tr[6]/td[3]/div/span[3]/text()')[0].strip()
                    fanh2 = index3.xpath('//*[@id="__layout"]/div/section/div[4]/div[2]/div[3]/table/tbody/tr[6]/td[4]/text()')[0].strip()
                else:
                    zhujc = '0'
                    pingjc = '0'
                    kejc = '0'
                    zhukl2 = '0'
                    pingkl2 = '0'
                    kekl2 = '0'
                    fanh2 = '0'

                zhuam = index3.xpath('//*[@id="__layout"]/div/section/div[4]/div[2]/div[3]/table/tbody/tr[14]/td[3]/div/span[1]/text()')[0].strip()
                pingam = index3.xpath('//*[@id="__layout"]/div/section/div[4]/div[2]/div[3]/table/tbody/tr[14]/td[3]/div/span[2]/text()')[0].strip()
                keam = index3.xpath('//*[@id="__layout"]/div/section/div[4]/div[2]/div[3]/table/tbody/tr[14]/td[3]/div/span[3]/text()')[0].strip()
                fanh3 = index3.xpath('//*[@id="__layout"]/div/section/div[4]/div[2]/div[3]/table/tbody/tr[14]/td[4]/text()')[0].strip()
                print(zhukl, pingkl, kekl, fanh, zhujc, pingjc, kejc, zhukl2, pingkl2, kekl2, fanh2, zhuam, pingam, keam, fanh3)

                #总进
                time.sleep(random.randint(5, 10))
                zongjin_url = f'https://www.jihai8.com/zq/overdown_{id}.html'
                self.browser.get(zongjin_url)
                if "您的访问频率过快，请稍等" or "Server error"  in self.browser.page_source:
                    while True:
                        time.sleep(10)
                        self.browser.refresh()
                        if  "您的访问频率过快，请稍等" not in self.browser.page_source and "Server error" not in self.browser.page_source:
                            break
                index4= etree.HTML(self.browser.page_source)
                amdx = index4.xpath('//*[@id="__layout"]/div/section/div[4]/div/div[3]/table/tbody/tr[1]/td[4]/div/span[2]/text()')[0].strip()
                amkld = index4.xpath('//*[@id="__layout"]/div/section/div[4]/div/div[3]/table/tbody/tr[1]/td[5]/div/span[1]/text()')[0].strip()
                amklx = index4.xpath('//*[@id="__layout"]/div/section/div[4]/div/div[3]/table/tbody/tr[1]/td[5]/div/span[2]/text()')[0].strip()
                amfanh = index4.xpath('//*[@id="__layout"]/div/section/div[4]/div/div[3]/table/tbody/tr[1]/td[6]/text()')[0].strip()
                sbklid = index4.xpath('//*[@id="__layout"]/div/section/div[4]/div/div[3]/table/tbody/tr[4]/td[5]/div/span[1]/text()')[0].strip()
                sbklix = index4.xpath('//*[@id="__layout"]/div/section/div[4]/div/div[3]/table/tbody/tr[4]/td[5]/div/span[2]/text()')[0].strip()
                sbfanh = index4.xpath('//*[@id="__layout"]/div/section/div[4]/div/div[3]/table/tbody/tr[4]/td[6]/text()')[0].strip()
                lbkld = index4.xpath('//*[@id="__layout"]/div/section/div[4]/div/div[3]/table/tbody/tr[8]/td[5]/div/span[1]/text()')[0].strip()
                lbklx = index4.xpath('//*[@id="__layout"]/div/section/div[4]/div/div[3]/table/tbody/tr[8]/td[5]/div/span[2]/text()')[0].strip()
                lbfanh = index4.xpath('//*[@id="__layout"]/div/section/div[4]/div/div[3]/table/tbody/tr[8]/td[6]/text()')[0].strip()
                wlkld = index4.xpath('//*[@id="__layout"]/div/section/div[4]/div/div[3]/table/tbody/tr[12]/td[5]/div/span[1]/text()')[0].strip()
                wlklx = index4.xpath('//*[@id="__layout"]/div/section/div[4]/div/div[3]/table/tbody/tr[12]/td[5]/div/span[2]/text()')[0].strip()
                wlfanh= index4.xpath('//*[@id="__layout"]/div/section/div[4]/div/div[3]/table/tbody/tr[12]/td[6]/text()')[0].strip()
                print(amdx, amkld, amklx, amfanh, sbklid, sbklix, sbfanh, lbkld, lbklx, lbfanh, wlkld, wlklx, wlfanh)

                info = [analysis_url + '\t', date + '\t', bsqdz + '\t', bsqdy + '\t', bfz + '\t', bfy + '\t', str(he) + '\t', zjq + '\t', zds + '\t', ying + '\t', dql + '\t', cjjq + '\t', cjsq + '\t', kds + '\t', kying + '\t', kdql + '\t', kcjjq + '\t', kcjsq + '\t',
                zhuz + '\t', pingz + '\t', kez + '\t', zhuyk + '\t', pingyk + '\t', keyk + '\t', zhulr + '\t', pinglr + '\t', kelr + '\t', zhugm + '\t', pinggm + '\t', kegm + '\t', zhucs + '\t', pingcs + '\t', kecs + '\t',
                zhukl + '\t', pingkl + '\t', kekl + '\t', fanh + '\t', zhujc + '\t', pingjc + '\t', kejc + '\t', zhukl2 + '\t', pingkl2 + '\t', kekl2 + '\t', fanh2 + '\t', zhuam + '\t', pingam + '\t', keam + '\t', fanh3 + '\t',
                amdx + '\t', amkld + '\t', amklx + '\t', amfanh + '\t', sbklid + '\t', sbklix + '\t', sbfanh + '\t', lbkld + '\t', lbklx + '\t', lbfanh + '\t', wlkld + '\t', wlklx + '\t', wlfanh]
                # print(info)
                name = f'{start_year}-{end_year}比赛{ls_id}'
                if not os.path.exists(f'{name}.csv'):
                    head = ['url', '日期', '比赛双方', '比赛双方', '比分', '', '合', '总进球', '主队胜', '赢',
                            '大', '进', '失', '客队胜', '赢', '大', '进', '失', '主', '平', '负', '', '盈亏', '',
                            '', '冷热', '', '', '购买倾向', '', '', '出售倾向', '', '', '365凯利', '', '返还', ''
                            '', '竞彩', '', '' ,'竞彩凯利', '', '返还', '', '澳门', '', '返还', '澳门大小', '', '澳门凯利',
                            '返还', '', 'SB凯利', '返还', '', '立博凯利', '返还', '', '威廉希尔凯利', '']
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
                print(e)


    def run(self, ls_id, start_year, end_year):
        task_id = self.Getdata(ls_id, start_year, end_year)
        self.Jiexi(task_id)




if __name__ == '__main__':
    ls_id, start_year, end_year = map(int, input('请输入联赛id、爬取年份(多少年到多少年以空格分开):').split())
    l = JH8()
    l.run(ls_id, start_year, end_year)

