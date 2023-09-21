# -*- coding: utf-8 -*-
import re
import os
import csv
import time
import ddddocr
import requests
from PIL import Image
from lxml import etree
from io import BytesIO
from selenium import webdriver
from datetime import datetime, timedelta


class BIFAW(object):

    def __init__(self):
        super().__init__()
        self.chromeOptions = self.get_options()
        self.driver = self.get_driver()
        self.headers = {
            "authority": "bifaw.com",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "zh-CN,zh;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://bifaw.com",
            "referer": "https://bifaw.com/bifaw/result.php",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }

    def get_options(self):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument('--headless')
        chromeOptions.add_argument('--disable-gpu')
        chromeOptions.add_argument('window-size=1920,1080')
        chromeOptions.add_argument("--no-sandbox")
        return chromeOptions

    def get_driver(self):
        driver = webdriver.Chrome(chrome_options=self.chromeOptions)
        driver.set_page_load_timeout(10)
        # driver.set_script_timeout(10)
        return driver

    def creat_session(self):
        # 获取页面的 cookie
        cookies = self.driver.get_cookies()
        # 创建一个 session，并设置页面的 cookie
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])
        return session

    def login(self, start_date, end_date):
        initial_url = 'https://bifaw.com/bifaw/result.php'
        self.driver.get(initial_url)
        session = self.creat_session()
        print('-------------------开始登录------------------')
        self.driver.find_element_by_xpath('//*[@id="txtUsername"]').send_keys('13983209352')
        self.driver.find_element_by_xpath('//*[@id="txtPassword"]').send_keys('11223344o')
        response = etree.HTML(self.driver.page_source)
        img_url = 'https://bifaw.com' + response.xpath('//*[@id="vdimgck"]/@src')[0]

        # 使用 session 发送 GET 请求获取验证码图片的内容
        response = session.get(img_url)
        with open("captcha.png", "wb") as file:
            file.write(response.content)

        code = self.get_verifyCode(response.content)
        print(f'验证码识别结果：{code}')
        self.driver.find_element_by_xpath('//*[@id="vdcode"]').send_keys(code)
        self.driver.find_elements_by_xpath('//*[@id="submitImage"]')[0].click()
        time.sleep(5)
        try:
            if '你好:13983209352' in self.driver.page_source:
                print('------------------登录成功-------------------')
            self.analysis_data(start_date, end_date)
        except Exception as e:
            print(f'{e}--------------识别错误请重新运行/任务运行完毕---------------')

    def analysis_data(self, start, end):
        session = self.creat_session()

        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")
        bisai_time = start_date
        while True:
            bisai_time = bisai_time.strftime("%Y-%m-%d")
            # 定位 input 标签元素
            input_element = self.driver.find_element_by_xpath("//input[@id='matchdate']")
            # 获取当前 input 元素的 value 属性值
            current_date = input_element.get_attribute("value")
            print("当前日期：", current_date)
            # 使用 Javascript 替换 input 元素的 value 属性值
            self.driver.execute_script("arguments[0].setAttribute('value', arguments[1])", input_element, bisai_time)
            # 再次获取 input 元素的 value 属性值，验证是否被替换
            updated_value = input_element.get_attribute("value")
            print("更新后的日期：", updated_value)
            time.sleep(1)
            self.driver.find_elements_by_xpath('//*[@id="abf_header"]/ul/li[7]/input')[0].click()
            time.sleep(3)
            html = etree.HTML(self.driver.page_source)
            bisai = html.xpath('//table[@class="oddstable"]/tbody')
            for dd in bisai:
                time_only = dd.xpath('tr[2]/th[1]/span[1]//text()')[0]
                time_only = time_only[6:]
                liansai = dd.xpath('tr[2]/th[1]/span[3]//text()')[0]
                liansai = re.sub(r'\(.*?\)', '', liansai)
                zhusai = dd.xpath('tr[3]/td[1]/div[1]/span[1]//text()')[0]
                kesai = dd.xpath('tr[3]/td[1]/div[1]/span[2]//text()')[0]
                bifen = dd.xpath('tr[3]/td[1]/span//text()[1]')[0]
                try:
                    splitted = bifen.split(":")
                    part1 = splitted[1].split("-")[0]
                    part2 = splitted[1].split("-")[1]
                except:
                    part1 = ""
                    part2 = ""
                zhuou = dd.xpath('tr[3]/td[4]//text()')[0]
                he = dd.xpath('tr[4]/td[3]//text()')[0]
                keou = dd.xpath('tr[5]/td[3]//text()')[0]
                zhujiamaigua = dd.xpath('tr[3]/td[3]//text()')[0]
                zhumaijia = dd.xpath('tr[3]/td[5]//text()')[0]
                zhuchengjiao = dd.xpath('tr[3]/td[6]//text()')[0]
                kemaijiagua = dd.xpath('tr[5]/td[2]//text()')[0]
                kemaijia = dd.xpath('tr[5]/td[4]//text()')[0]
                kechengjiao = dd.xpath('tr[5]/td[5]//text()')[0]
                bizhu = dd.xpath('tr[3]/td[9]//text()')[0]
                peizhu = dd.xpath('tr[3]/td[10]//text()')[0]
                yingzhu = dd.xpath('tr[3]/td[11]//text()')[0]
                bihe = dd.xpath('tr[4]/td[8]//text()')[0]
                peihe = dd.xpath('tr[4]/td[9]//text()')[0]
                yinghe = dd.xpath('tr[4]/td[10]//text()')[0]
                bike = dd.xpath('tr[5]/td[8]//text()')[0]
                peike = dd.xpath('tr[5]/td[9]//text()')[0]
                yingke = dd.xpath('tr[5]/td[10]//text()')[0]
                zhizhu = dd.xpath('tr[3]/td[14]//text()')[0]
                zhihe = dd.xpath('tr[4]/td[13]//text()')[0]
                zhike = dd.xpath('tr[5]/td[13]//text()')[0]
                chazhu = dd.xpath('tr[3]/td[15]//text()')[0]
                chahe = dd.xpath('tr[4]/td[14]//text()')[0]
                chake = dd.xpath('tr[5]/td[14]//text()')[0]
                rezhu = dd.xpath('tr[3]/td[16]//text()')[0]
                rehe = dd.xpath('tr[4]/td[15]//text()')[0]
                reke = dd.xpath('tr[5]/td[15]//text()')[0]
                damai = dd.xpath('tr[7]/td[3]//text()')[0]
                damai2 = dd.xpath('tr[7]/td[5]//text()')[0]
                dachengjiao = dd.xpath('tr[7]/td[6]//text()')[0]
                xiaomai = dd.xpath('tr[8]/td[2]//text()')[0]
                xiaomai2 = dd.xpath('tr[8]/td[4]//text()')[0]
                xiaochengjiao = dd.xpath('tr[8]/td[5]//text()')[0]
                dabi = dd.xpath('tr[7]/td[9]//text()')[0]
                dapei = dd.xpath('tr[7]/td[10]//text()')[0]
                daying = dd.xpath('tr[7]/td[11]//text()')[0]
                xiaobi = dd.xpath('tr[8]/td[8]//text()')[0]
                xiaopei = dd.xpath('tr[8]/td[9]//text()')[0]
                xiaoying = dd.xpath('tr[8]/td[10]//text()')[0]
                dazhi = dd.xpath('tr[8]/td[13]//text()')[0]
                daxiaopan = dd.xpath('tr[8]/td[14]//text()')[0]
                xiaozhi = dd.xpath('tr[8]/td[15]//text()')[0]
                info = [bisai_time, time_only + '\t', liansai + '\t', zhusai + '\t', kesai + '\t', part1 + '\t',
                        part2 + '\t',
                        zhuou + '\t', he + '\t', keou + '\t', zhujiamaigua + '\t', zhumaijia + '\t',
                        zhuchengjiao + '\t', kemaijiagua + '\t', kemaijia + '\t', kechengjiao + '\t', bizhu + '\t',
                        peizhu + '\t',
                        yingzhu + '\t', bihe + '\t', peihe + '\t', yinghe + '\t',
                        bike + '\t', peike + '\t', yingke + '\t', zhizhu + '\t', zhihe + '\t',
                        zhike + '\t', chazhu + '\t', chahe + '\t', chake + '\t', rezhu + '\t',
                        rehe + '\t', reke + '\t', damai + '\t', damai2 + '\t', dachengjiao + '\t',
                        xiaomai + '\t', xiaomai2 + '\t', xiaochengjiao + '\t',
                        dabi + '\t', dapei + '\t', daying + '\t', xiaobi + '\t', xiaopei + '\t',
                        xiaoying + '\t', dazhi + '\t', daxiaopan + '\t', xiaozhi + '\t']

                print(info)
                self.save_info(info)
            url = "https://bifaw.com/bifaw/serveodds.php"
            year, month, day = bisai_time.split("-")
            data = {
                "year": year,
                "month": month,
                "day": day,
                "page": "1",
                "fff": "4"
            }
            response = session.post(url, headers=self.headers, data=data)
            response.encoding = 'utf-8-sig'
            jiekou_data = response.json()
            if jiekou_data == []:
                bisai_time = datetime.strptime(bisai_time, "%Y-%m-%d")
                # 判断是否达到结束日期
                if bisai_time > end_date:
                    break
                bisai_time += timedelta(days=1)
                continue
            for key, value in jiekou_data.items():
                info = value['info'].split(',')
                zhu = info[4]
                ke = info[5]
                try:
                    match = value['macth'].split(',')
                    zhumai = match[-6]
                    zhumai2 = match[-5]
                    kemai = match[-4]
                    kemai2 = match[-3]
                except:
                    zhumai = ''
                    zhumai2 = ''
                    kemai = ''
                    kemai2 = ''
                try:
                    ou = value['ou'][0].split(',')
                    damai = ou[-4]
                    damai2 = ou[-3]
                except:
                    damai = ''
                    damai2 = ''

                info = [zhu, ke, zhumai, zhumai2, kemai, kemai2, damai, damai2]
                print(info)
                self.save_jiekou(info)

            bisai_time = datetime.strptime(bisai_time, "%Y-%m-%d")
            # 判断是否达到结束日期
            if bisai_time > end_date:
                break
            bisai_time += timedelta(days=1)
            time.sleep(5)


    def save_info(self, info):
        name = '必发数据XLS'
        if not os.path.exists(f'{name}.csv'):
            head = ['日期', '比赛时间', '联赛', '主', '客', '比分', '比分', '主欧', '和', '客欧', '主买家挂', '主卖家',
                    '主成交量', '客买家挂', '客卖家', '客成交量', '必主', '赔主', '盈主', '必和',
                    '赔和', '盈和', '必客', '赔客', '盈客', '指主', '指和', '指客', '差主',
                    '差和', '差客', '热主', '热和', '热客', '大买', '大卖', '大成交量',
                    '小买', '小卖', '小成交量', '大必', '大赔', '大盈',
                    '小必', '小赔', '小盈', '大指', '大小盘', '小指']
            csvFile = open(f'{name}.csv', 'a', newline='', encoding='utf-8-sig')
            writer = csv.writer(csvFile)
            writer.writerow(head)
            csvFile.close()
        else:
            csvFile = open(f'{name}.csv', 'a+', newline='', encoding='utf-8-sig')
            writer = csv.writer(csvFile)
            writer.writerow(info)
            csvFile.close()

    def save_jiekou(self, info):
        name = '必发数据XLS接口'
        if not os.path.exists(f'{name}.csv'):
            head = ['主', '客', '主买', '主卖', '客买', '客卖', '大买', '大卖']
            csvFile = open(f'{name}.csv', 'a', newline='', encoding='utf-8-sig')
            writer = csv.writer(csvFile)
            writer.writerow(head)
            csvFile.close()
        else:
            csvFile = open(f'{name}.csv', 'a+', newline='', encoding='utf-8-sig')
            writer = csv.writer(csvFile)
            writer.writerow(info)
            csvFile.close()

    def get_verifyCode(self, imgContent):
        ocr = ddddocr.DdddOcr()
        img = Image.open(BytesIO(imgContent))
        res = ocr.classification(img)
        return res


if __name__ == '__main__':
    l = BIFAW()
    start_date, end_date = map(str, input('请输入开始日期和终止日期(以空格分开):').split())
    l.login(start_date, end_date)
