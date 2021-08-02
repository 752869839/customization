# -*- coding: utf-8 -*-
import os
import csv
import time
import json
import random
import smtplib
import requests
from lxml import etree
from email.utils import COMMASPACE
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# from chaojiying import Chaojiying_Client


COOKIE = 'Hm_lvt_a68414d98536efc52eeb879f984d8923=1627524896; __cf_bm=3485eab8ac5c2e832cb374af6992d76a92ba690f-1627637053-1800-AdEz06fFmfkjprIHs2f0vh28TgK7aUIRQJFWVIWuwG407JMaDhX0sPbQuiedr9u8fWT/slmnN8gkB0LuJtTqP43d7R2zs7tav3bS1XmV5GPaubDEJGIz8M1yqyAFHtYqlw==; ds_session=d5nor4ka92fds8cf2l5o1o03j4; uid=R-570329-f11809f206103c71c44b41; Hm_lpvt_a68414d98536efc52eeb879f984d8923=1627638495'

USERAGENT = [
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
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",  # sogou浏览器
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
            # maxthon浏览器
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
            # UC浏览器
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
        ]


# email
SMTP_SERVER = 'smtp.exmail.qq.com'
SMTP_PORT = 465
SENDER = 'account@cibsc.biz'
ACCOUNT_INFO = {'username':'account@cibsc.biz', 'password':'11223344Oo'}

def send_mail(receivers, subject, text, smtp_server=SMTP_SERVER, smtp_port=SMTP_PORT, sender=SENDER, account_info=ACCOUNT_INFO):
    """
    :param receivers:接收邮箱列表
    :param subject:发送邮件主题
    :param text:发送邮件正文
    :param filename:发送邮件附件
    :param smtp_server:smtp服务器地址
    :param smtp_port:smtp TLS/STARTTLS 端口
    :param sender:发送者
    :param account_info:发送者邮箱账号密码
    :return:
    """

    # 正文
    msg_root = MIMEMultipart()    # 创建一个带附件的实例
    msg_root['SUBJECT'] = subject
    msg_root['To'] = COMMASPACE.join(receivers)
    msg_text = MIMEText(text, 'html', 'utf-8')
    msg_root.attach(msg_text)

    smtp = smtplib.SMTP_SSL(f'{smtp_server}:{smtp_port}')
    smtp.login(account_info['username'], account_info['password'])
    smtp.sendmail(sender, receivers, msg_root.as_string())
    smtp.close()


requests.packages.urllib3.disable_warnings()  #忽略requests https警告

# 钉钉
def dingd(message):

    url = 'https://oapi.dingtalk.com/robot/send?access_token=a2cdec94a0be829eb65ffce2dce2226fe359d733c84a793acfcd866a8f2cba9c'
    headers = {"Content-Type": "application/json"}
    data = message
    requests.post(url, data=json.dumps(data), headers=headers)
    
    return data

task = []
class Dszuqiu(object):
    def __init__(self):
        self.session = self.session()
        self.headers = self.headers()
        self.headers2 = self.headers2()

    def session(self):
        session = requests.session()
        session.keep_alive = False
        session.adapters.DEFAULT_RETRIES = 10
        return session

    def headers(self):
        headers = {
            "User-Agent": random.choice(USERAGENT),
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
            'Cookie': COOKIE
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
        print('验证码识别结果为:',result)
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


    def get_state(self, array):
        for i in array:
            i_next = array[array.index(i) + 1]  # i相邻的下一个元素
            if isinstance(i, dict) and isinstance(i_next, dict):
                return i


    def gain(self,interval,way):
        while True:
            index_url = "https://live.dszuqiu.com/ajax/score/data?mt=0&nr=1"
            try:
                res = requests.get(index_url, headers=self.headers, timeout=30, verify=False)
                print('第一次请求响应状态码:',res.status_code)
                if res.status_code == 200:
                    # index_html = etree.HTML(res.text)
                    # live_match = index_html.xpath('//*[@id="on"]/tr')
                    # print(live_match)
                    # for live in live_match:
                    #     match_minute = live.xpath('./td[3]/span/text()')[0]
                    #     match_minute = int(str(match_minute).replace("'", ""))
                    #     print(match_minute)
                    #     if match_minute > 30 :
                    #         id = live.xpath('./@rid')[0]
    
                    match_num = len(res.json()['rs'])
                    # print(res.json()['rs'][4]['status'])
                    for i in range(0,match_num):
                        match_status = res.json()['rs'][i]['status']
                        if match_status in "未 半 全":
                            continue
                        elif int(match_status) > 30 :
                            print('比赛时间:',match_status)
                            # self.login()
                            id = res.json()['rs'][i]['id']
                            race_sp_url = f'https://www.dszuqiu.com/race_sp/{id}'
                            self.headers2['Cookie'] = f'race_id={id}; '+ COOKIE
                            race_response = self.session.get(race_sp_url, headers=self.headers2, timeout=30, verify=False)
                            print('第二次请求响应状态码:',race_response.status_code)
                            if race_response.status_code == 200:
                                race_html = etree.HTML(race_response.text)
    
                                try:
                                    match_country= race_html.xpath('//h3[@class="dsBreadcrumbs"]/a[3]/text()')[0]
                                    match_name = race_html.xpath('//h3[@class="dsBreadcrumbs"]/text()')[-1].strip()
                                except:
                                    match_country = race_html.xpath('//h3[@class="dsBreadcrumbs"]/a[3]/text()')[0]
                                    match_name = race_html.xpath('//h3[@class="dsBreadcrumbs"]/text()')[-1].strip()
                                    send_mail(['14302642@qq.com'], 'cookie过期', '您的cookie已过期,请更换cookie后,重新启动足球监控预警程序!')
                                    print('cookie过期邮件发送成功')
    
                                # 让球全场
                                rang_all_data = race_html.xpath('//tbody[@id="sp_rangfen"]/tr')
                                quan = []
                                for sp in rang_all_data[::-1]:
                                    all_rangfen = sp.xpath('./td/text()')
                                    for minute in range(70, 86):
                                        if f"{minute}'" in all_rangfen[0].strip():
                                            if sp.xpath('./td/@class')[3] == "text-center redTD":
                                                quan.append({'date': all_rangfen[5], 'minute': minute})
                                            else:
                                                quan.append('-')
    
                                # 让球全场的半场
                                rang_all_data = race_html.xpath('//tbody[@id="sp_rangfen"]/tr')
                                quan2 = []
                                for sp in rang_all_data[::-1]:
                                    all_rangfen = sp.xpath('./td/text()')
                                    for minute in range(30, 43):
                                        if f"{minute}'" in all_rangfen[0].strip():
                                            if sp.xpath('./td/@class')[3] == "text-center redTD":
                                                quan2.append({'date': all_rangfen[5], 'minute': minute})
                                            else:
                                                quan2.append('-')
                                                
                                # 让球半场
                                rang_half_data = race_html.xpath('//tbody[@id="sp_half_rangfen"]/tr')
                                ban = []
                                for sp in rang_half_data[::-1]:
                                    half_rangfen = sp.xpath('./td/text()')
                                    for minute in range(30, 43):
                                        if f"{minute}'"in half_rangfen[0].strip():
                                            if sp.xpath('./td/@class')[3] == "text-center redTD":
                                                ban.append({'date': half_rangfen[5], 'minute': minute})
                                            else:
                                                ban.append('-')
                                if way == 1:
                                    # 判断全场下半场连续红
                                    result = self.get_state(quan)
                                    if type(result) == dict:
        
                                        # 大小球全场
                                        size_all_data = race_html.xpath('//tbody[@id="sp_daxiao"]/tr')
                                        quan_daxiao = ''
                                        for i in size_all_data[::-1]:  # enumerate 枚举
                                            td_quan_daxiao = i.xpath('./td/text()')
                                            if f"{result['minute']}'" in td_quan_daxiao[0].strip():
                                                quan_daxiao += td_quan_daxiao[2]
                                                break
                                        try:
                                            message_all = f'比赛链接：{race_sp_url}\n比赛双方：{match_country}-{match_name}\n日期：{result["date"]}\n分钟：{result["minute"]}\n大小球：{quan_daxiao}'
                                            print(message_all)
                                            verify = f'{match_name}-全下'
                                            if verify not in task:
                                                send_mail(['14302642@qq.com'], f'全场预警邮件-{match_country}-{match_name}',message_all)
                                                task.append(verify)
                                                print('预警邮件发送成功!')
                                        except Exception as e:
                                            print(e)
    
                                    # 判断全场的上半场场连续红
                                    result = self.get_state(quan2)
                                    if type(result) == dict:
        
                                        # 大小球全场
                                        size_all_data = race_html.xpath('//tbody[@id="sp_daxiao"]/tr')
                                        quan_daxiao = ''
                                        for i in size_all_data[::-1]:  # enumerate 枚举
                                            td_quan_daxiao = i.xpath('./td/text()')
                                            if f"{result['minute']}'" in td_quan_daxiao[0].strip():
                                                quan_daxiao += td_quan_daxiao[2]
                                                break
                                        try:
                                            message_all = f'比赛链接：{race_sp_url}\n比赛双方：{match_country}-{match_name}\n日期：{result["date"]}\n分钟：{result["minute"]}\n大小球：{quan_daxiao}'
                                            print(message_all)
                                            verify = f'{match_name}-全上'
                                            if verify not in task:
                                                send_mail(['14302642@qq.com'], f'全场的半场预警邮件-{match_country}-{match_name}', message_all)
                                                task.append(verify)
                                                print('预警邮件发送成功!')
                                        except Exception as e:
                                            print(e)
        
                                    # 判断半场连续红
                                    result = self.get_state(ban)
                                    if type(result) == dict:
        
                                       # 大小球半场
                                        size_half_data = race_html.xpath('//tbody[@id="sp_half_daxiao"]/tr')
                                        ban_daxiao = ''
                                        for i in size_half_data[::-1]:
                                            td_size_half_minute = i.xpath('./td/text()')
                                            if f"{result['minute']}'" in td_size_half_minute[0].strip():
                                                ban_daxiao += td_size_half_minute[2]
                                                break
                                        try:
                                            message_half = f'比赛链接：{race_sp_url}\n比赛双方：{match_country}-{match_name}\n日期：{result["date"]}\n分钟：{result["minute"]}\n大小球：{ban_daxiao}'
                                            print(message_half)
                                            verify = f'{match_name}-半'
                                            if verify not in task:
                                                send_mail(['14302642@qq.com'], f'半场预警邮件-{match_country}-{match_name}',message_half)
                                                task.append(verify)
                                                print('预警邮件发送成功!')
                                        except Exception as e:
                                            print(e)

                                if way == 2:
                                    # 判断全场下半场连续红
                                    result = self.get_state(quan)
                                    if type(result) == dict:
        
                                        # 大小球全场
                                        size_all_data = race_html.xpath('//tbody[@id="sp_daxiao"]/tr')
                                        quan_daxiao = ''
                                        for i in size_all_data[::-1]:  # enumerate 枚举
                                            td_quan_daxiao = i.xpath('./td/text()')
                                            if f"{result['minute']}'" in td_quan_daxiao[0].strip():
                                                quan_daxiao += td_quan_daxiao[2]
                                                break
                                        try:
                                            message_all = f'比赛链接：{race_sp_url}\n比赛双方：{match_country}-{match_name}\n日期：{result["date"]}\n分钟：{result["minute"]}\n大小球：{quan_daxiao}'
                                            print(message_all)
                                            data = {
                                                "msgtype": "text",
                                                "isAtAll": "True",
                                                "at": {"isAtAll": True},
                                                "text": {
                                                    "content": message_all
                                                 }
                                            }
                                            
                                            verify = f'{match_name}-全下'
                                            if verify not in task:
                                                dingd(data)
                                                task.append(verify)
                                                print('预警钉钉消息发送成功!')
                                        except Exception as e:
                                            print(e)
    
                                    # 判断全场的上半场场连续红
                                    result = self.get_state(quan2)
                                    if type(result) == dict:
        
                                        # 大小球全场
                                        size_all_data = race_html.xpath('//tbody[@id="sp_daxiao"]/tr')
                                        quan_daxiao = ''
                                        for i in size_all_data[::-1]:  # enumerate 枚举
                                            td_quan_daxiao = i.xpath('./td/text()')
                                            if f"{result['minute']}'" in td_quan_daxiao[0].strip():
                                                quan_daxiao += td_quan_daxiao[2]
                                                break
                                        try:
                                            message_all = f'比赛链接：{race_sp_url}\n比赛双方：{match_country}-{match_name}\n日期：{result["date"]}\n分钟：{result["minute"]}\n大小球：{quan_daxiao}'
                                            print(message_all)
                                            data = {
                                                "msgtype": "text",
                                                "isAtAll": "True",
                                                "at": {"isAtAll": True},
                                                "text": {
                                                    "content": message_all
                                                }
                                            }

                                            verify = f'{match_name}-全上'
                                            if verify not in task:
                                                dingd(data)
                                                task.append(verify)
                                                print('预警钉钉消息发送成功!')
                                        except Exception as e:
                                            print(e)
    
                                    # 判断半场连续红
                                    result = self.get_state(ban)
                                    if type(result) == dict:
        
                                        # 大小球半场
                                        size_half_data = race_html.xpath('//tbody[@id="sp_half_daxiao"]/tr')
                                        ban_daxiao = ''
                                        for i in size_half_data[::-1]:
                                            td_size_half_minute = i.xpath('./td/text()')
                                            if f"{result['minute']}'" in td_size_half_minute[0].strip():
                                                ban_daxiao += td_size_half_minute[2]
                                                break
                                        try:
                                            message_half = f'比赛链接：{race_sp_url}\n比赛双方：{match_country}-{match_name}\n日期：{result["date"]}\n分钟：{result["minute"]}\n大小球：{ban_daxiao}'
                                            print(message_half)
                                            data = {
                                                "msgtype": "text",
                                                "isAtAll": "True",
                                                "at": {"isAtAll": True},
                                                "text": {
                                                    "content": message_half
                                                }
                                            }

                                            verify = f'{match_name}-半'
                                            if verify not in task:
                                                dingd(data)
                                                task.append(verify)
                                                print('预警钉钉消息发送成功!')
                                        except Exception as e:
                                            print(e)
    
            except Exception as e:
                print(e)
                
            time.sleep(interval)


if __name__ == '__main__':
    lz = Dszuqiu()
    way = int(input('请选择预警方式 1 邮箱预警 2 钉钉预警 :'))
    interval = int(input('请设置预警间隔/s:'))
    lz.gain(interval,way)

