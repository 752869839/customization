# -*- coding: utf-8 -*-
import os
import re
import json
import time
import ddddocr
import requests
import schedule
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
        self.moren = 0
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

    def login(self):
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
                print('-------------------登录成功-------------------')
            self.bs_warning()
        except Exception as e:
            self.login()

    def bs_warning(self):
        new_window_driver = None  # 新的浏览器实例
        while True:
            warning_url = ['https://bifaw.com/bifaw/', 'https://bifaw.com/bifaw/result.php']
            for url in warning_url:
                self.driver.get(url)
                time.sleep(5)
                html = etree.HTML(self.driver.page_source)
                bisai = html.xpath('//table[@class="oddstable"]/tbody')
                if '你已经在别出登陆!' in self.driver.page_source or '你还没有登陆' in self.driver.page_source:
                    return self.login()
                if bisai == [] and '暂时没有比赛' in self.driver.page_source:
                    self.driver.refresh()
                    print(url,'：当前没有比赛!!!!!')
                for dd in bisai:
                    id = dd.xpath('parent::table/@id')[0]
                    比赛时间 = dd.xpath('tr[2]/th[1]/span[1]//text()')[0]
                    liansai = dd.xpath('tr[2]/th[1]/span[3]//text()')[0]
                    联赛 = re.sub(r'\(.*?\)', '', liansai)
                    主赛 = dd.xpath('tr[3]/td[1]/div[1]/span[1]//text()')[0]
                    客赛 = dd.xpath('tr[3]/td[1]/div[1]/span[2]//text()')[0]
                    bifen = dd.xpath('tr[3]/td[1]/span//text()[1]')[0]
                    try:
                        splitted = bifen.split(":")
                        主比分 = splitted[1].split("-")[0]
                        客比分 = splitted[1].split("-")[1]
                    except:
                        主比分 = ""
                        客比分 = ""
                    try:
                        主欧 = float(dd.xpath('tr[3]/td[4]//text()')[0].replace(',', ''))
                    except:
                        主欧 = self.moren
                    try:
                        和 = float(dd.xpath('tr[4]/td[3]//text()')[0].replace(',', ''))
                    except:
                        和 = self.moren
                    try:
                        客欧 = float(dd.xpath('tr[5]/td[3]//text()')[0].replace(',', ''))
                    except:
                        客欧 = self.moren
                    try:
                        主买家挂 = float(dd.xpath('tr[3]/td[3]//text()')[0].replace(',', ''))
                    except:
                        主买家挂 = self.moren
                    try:
                        主卖家 = float(dd.xpath('tr[3]/td[5]//text()')[0].replace(',', ''))
                    except:
                        主卖家 = self.moren
                    try:
                        主成交量 = float(dd.xpath('tr[3]/td[6]//text()')[0].replace(',', ''))
                    except:
                        主成交量 = self.moren
                    try:
                        客买家挂 = float(dd.xpath('tr[5]/td[2]//text()')[0].replace(',', ''))
                    except:
                        客买家挂 = self.moren
                    try:
                        客卖家 = float(dd.xpath('tr[5]/td[4]//text()')[0].replace(',', ''))
                    except:
                        客卖家 = self.moren
                    try:
                        客成交量 = float(dd.xpath('tr[5]/td[5]//text()')[0].replace(',', ''))
                    except:
                        客成交量 = self.moren
                    try:
                        必主 = float(dd.xpath('tr[3]/td[9]//text()')[0].replace(',', ''))
                    except:
                        必主 = self.moren
                    try:
                        赔主 = float(dd.xpath('tr[3]/td[10]//text()')[0].replace(',', ''))
                    except:
                        赔主 = self.moren
                    try:
                        盈主 = float(dd.xpath('tr[3]/td[11]//text()')[0].replace(',', ''))
                    except:
                        盈主 = self.moren
                    try:
                        必和 = float(dd.xpath('tr[4]/td[8]//text()')[0].replace(',', ''))
                    except:
                        必和 = self.moren
                    try:
                        赔和 = float(dd.xpath('tr[4]/td[9]//text()')[0].replace(',', ''))
                    except:
                        赔和 = self.moren
                    try:
                        盈和 = float(dd.xpath('tr[4]/td[10]//text()')[0].replace(',', ''))
                    except:
                        盈和 = self.moren
                    try:
                        必客 = float(dd.xpath('tr[5]/td[8]//text()')[0].replace(',', ''))
                    except:
                        必客 = self.moren
                    try:
                        赔客 = float(dd.xpath('tr[5]/td[9]//text()')[0].replace(',', ''))
                    except:
                        赔客 = self.moren
                    try:
                        盈客 = float(dd.xpath('tr[5]/td[10]//text()')[0].replace(',', ''))
                    except:
                        盈客 = self.moren
                    try:
                        指主 = float(dd.xpath('tr[3]/td[14]//text()')[0].replace(',', ''))
                    except:
                        指主 = self.moren
                    try:
                        指和 = float(dd.xpath('tr[4]/td[13]//text()')[0].replace(',', ''))
                    except:
                        指和 = self.moren
                    try:
                        指客 = float(dd.xpath('tr[5]/td[13]//text()')[0].replace(',', ''))
                    except:
                        指客 = self.moren
                    try:
                        差主 = float(dd.xpath('tr[3]/td[15]//text()')[0].replace(',', ''))
                    except:
                        差主 = self.moren
                    try:
                        差和 = float(dd.xpath('tr[4]/td[14]//text()')[0].replace(',', ''))
                    except:
                        差和 = self.moren
                    try:
                        差客 = float(dd.xpath('tr[5]/td[14]//text()')[0].replace(',', ''))
                    except:
                        差客 = self.moren
                    try:
                        热主 = float(dd.xpath('tr[3]/td[16]//text()')[0].replace(',', ''))
                    except:
                        热主 = self.moren
                    try:
                        热和 = float(dd.xpath('tr[4]/td[15]//text()')[0].replace(',', ''))
                    except:
                        热和 = self.moren
                    try:
                        热客 = float(dd.xpath('tr[5]/td[15]//text()')[0].replace(',', ''))
                    except:
                        热客 = self.moren
                    try:
                        大买 = float(dd.xpath('tr[7]/td[3]//text()')[0].replace(',', ''))
                    except:
                        大买 = self.moren
                    try:
                        大卖 = float(dd.xpath('tr[7]/td[5]//text()')[0].replace(',', ''))
                    except:
                        大卖 = self.moren
                    try:
                        大成交量 = float(dd.xpath('tr[7]/td[6]//text()')[0].replace(',', ''))
                    except:
                        大成交量 = self.moren
                    try:
                        小买 = float(dd.xpath('tr[8]/td[2]//text()')[0].replace(',', ''))
                    except:
                        小买 = self.moren
                    try:
                        小卖 = float(dd.xpath('tr[8]/td[4]//text()')[0].replace(',', ''))
                    except:
                        小卖 = self.moren
                    try:
                        小成交量 = float(dd.xpath('tr[8]/td[5]//text()')[0].replace(',', ''))
                    except:
                        小成交量 = self.moren
                    try:
                        大必 = float(dd.xpath('tr[7]/td[9]//text()')[0].replace(',', ''))
                    except:
                        大必 = self.moren
                    try:
                        大赔 = float(dd.xpath('tr[7]/td[10]//text()')[0].replace(',', ''))
                    except:
                        大赔 = self.moren
                    try:
                        大盈 = float(dd.xpath('tr[7]/td[11]//text()')[0].replace(',', ''))
                    except:
                        大盈 = self.moren
                    try:
                        小必 = float(dd.xpath('tr[8]/td[8]//text()')[0].replace(',', ''))
                    except:
                        小必 = self.moren
                    try:
                        小赔 = float(dd.xpath('tr[8]/td[9]//text()')[0].replace(',', ''))
                    except:
                        小赔 = self.moren
                    try:
                        小盈 = float(dd.xpath('tr[8]/td[10]//text()')[0].replace(',', ''))
                    except:
                        小盈 = self.moren
                    try:
                        大指 = float(dd.xpath('tr[8]/td[13]//text()')[0].replace(',', ''))
                    except:
                        大指 = self.moren
                    try:
                        大小盘 = float(dd.xpath('tr[8]/td[14]//text()')[0].replace(',', ''))
                    except:
                        大小盘 = self.moren
                    try:
                        小指 = float(dd.xpath('tr[8]/td[15]//text()')[0].replace(',', ''))
                    except:
                        小指 = self.moren
                    try:
                        大价位 = float(dd.xpath('tr[7]/td[4]//text()')[0].replace(',', ''))
                    except:
                        大价位 = self.moren
                    try:
                        小价位 = float(dd.xpath('tr[8]/td[3]//text()')[0].replace(',', ''))
                    except:
                        小价位 = self.moren

                    info = f"报警  \n联赛{联赛} \n当前时间{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')} \n比赛时间{比赛时间}  \n主赛{主赛}  \n客赛{客赛}  \n主比分{主比分}" \
                           f"  \n客比分{客比分}  \n主欧{主欧}  \n和{和}  \n客欧{客欧}  \n主买家挂{主买家挂}  \n主卖家{主卖家} " \
                           f" \n主成交量{主成交量}  \n客买家挂{客买家挂}  \n客卖家{客卖家}  \n客成交量{客成交量}  \n必主{必主}" \
                           f"  \n赔主{赔主}  \n盈主{盈主}  \n必和{必和}  \n赔和{赔和}  \n盈和{盈和}  \n必客{必客}  \n赔客{赔客}" \
                           f"  \n盈客{盈客}  \n指主{指主}  \n指和{指和}  \n指客{指客}  \n差主{差主}  \n差和{差和}  \n差客{差客} " \
                           f" \n热主{热主}  \n热和{热和}  \n热客{热客}  \n大买{大买}  \n大卖{大卖}  \n大成交量{大成交量}  \n小买{小买} " \
                           f" \n小卖{小卖}  \n小成交量{小成交量}  \n大必{大必}  \n大赔{大赔}  \n大盈{大盈}  \n小必{小必}  \n小赔{小赔}" \
                           f"  \n小盈{小盈}  \n大指{大指}  \n大小盘{大小盘}  \n小指{小指}  \n大价位{大价位}  \n小价位{小价位}"
                    print(info)
                    time_delta_seconds = self.time_difference(比赛时间)

                    current_time = datetime.now()
                    current_hour = current_time.hour
                    current_hour = int(current_hour) # 当前时间的整点数

                    print(f"距比赛开始时差:{time_delta_seconds}秒")
                    if 650 > time_delta_seconds > 580 or -160 > time_delta_seconds > -220:
                        # 告警条件1
                        if 大成交量 > 9000 and 大必 > 40 and 大赔 > 40 and 大小盘 < 3.75 and 大成交量 / 10000 * 大必 * 大价位 > 100 and (
                                大成交量 / 10000 * 大必 * 大价位) > (小成交量 / 10000 * 小必 * 小价位 * 2):
                            self.driver.find_elements_by_xpath(f'//table[@id={id}]/tbody/tr[9]/td/ul/li[8]')[0].click()
                            pic_link = self.switch_window(id)
                            self.send_dd(info + '告警条件1', pic_link)
                        # 告警条件2
                        if 主欧 < 2.1 and 主成交量 > 10000 and 热主 < 3 and 客买家挂 > 500 and 主卖家 < 100000:
                            self.driver.find_elements_by_xpath(f'//table[@id={id}]/tbody/tr[9]/td/ul/li[8]')[0].click()
                            pic_link = self.switch_window(id)
                            self.send_dd(info + '告警条件2', pic_link)
                        # 告警条件3
                        if 大成交量 > 30000 and 大小盘 < 3.9 and 大盈 > -80 and 大成交量 / 10000 * 大必 * 大价位 > 100 and (
                                大成交量 / 10000 * 大必 * 大价位) > (小成交量 / 10000 * 小必 * 小价位 * 2):
                            self.driver.find_elements_by_xpath(f'//table[@id={id}]/tbody/tr[9]/td/ul/li[8]')[0].click()
                            pic_link = self.switch_window(id)
                            self.send_dd(info + '大金大球', pic_link)
                        # 告警条件4
                        if 7000 > 大成交量 > 4000  and 大必 > 53 and 12 >= current_hour >= 6:
                            self.driver.find_elements_by_xpath(f'//table[@id={id}]/tbody/tr[9]/td/ul/li[8]')[0].click()
                            pic_link = self.switch_window(id)
                            self.send_dd(info + '美洲大球', pic_link)

                time.sleep(30)

    def switch_window(self, id):
        base_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "img")
        file = "{}.png".format(os.path.join(base_path, id))
        handles = self.driver.window_handles
        new_window_handle = handles[-1]
        self.driver.switch_to.window(new_window_handle)  # 切换新窗口
        time.sleep(2)  # 等待页面加载完成
        self.driver.get_screenshot_as_file(file)
        self.driver.close()  # 关闭新窗口
        self.driver.switch_to.window(handles[0])  # 切换回原始窗口
        pic_link = self.upload_pic(file)
        print(pic_link)
        return pic_link

    def upload_pic(self, file_path):
        url = "https://api.superbed.cn/upload"
        # 通过文件上传
        resp = requests.post(url, data={"token": "9197c3f05982441ea4c016cff339588b"},
                             files={"file": open(f"{file_path}", "rb")}, timeout=20)
        pic_link = resp.json()['url']
        return pic_link

    def time_difference(self, bs_time):
        dt = datetime.strptime(bs_time, "%m-%d %H:%M")
        year = dt.year
        month = dt.month
        day = dt.day
        hour = dt.hour
        minute = dt.minute
        second = dt.second
        now_time = datetime.now()
        execute_at = datetime(2023, month, day, hour, minute, second)
        time_delta = execute_at - now_time
        time_delta_seconds = time_delta.total_seconds()
        return time_delta_seconds

    def send_dd(slef, msg: str, pic_link):
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

        data_pic = {
            'msgtype': 'markdown',
            'markdown': {
                'title': '报警图片',
                'text': f'![报警图片]({pic_link})'
            }
        }
        requests.post(url, data=json.dumps(data), headers=headers)
        time.sleep(2)
        res = requests.post(url, json=data_pic, headers=headers)
        print(res.status_code)
        return print('钉钉推送消息成功！！！')

    def get_verifyCode(self, imgContent):
        ocr = ddddocr.DdddOcr()
        img = Image.open(BytesIO(imgContent))
        res = ocr.classification(img)
        return res


# def my_task():
#     l = BIFAW()
#     l.login()
#
# schedule.every().hour.do(my_task)
# # 立即运行所有过期但尚未执行的任务
# schedule.run_all()
# while True:
#     schedule.run_pending()
#     time.sleep(1)

if __name__ == '__main__':
    l = BIFAW()
    l.login()
