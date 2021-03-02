# -*- coding: utf-8 -*-
import os
import re
import csv
import time
import requests
from lxml import etree
from mylog import _logger
from chaojiying import Chaojiying_Client


logger = _logger()
class Football(object):
    def __init__(self):
        self.session = self.session()
        self.headers = self.headers()

    def session(self):
        session = requests.session()
        session.keep_alive = False
        session.adapters.DEFAULT_RETRIES = 10
        return session

    """
    Cookie已经注释掉,采用login()登陆函数模拟登陆成功,再通过session维持会话状态,
    如需要采用手动添加cookie的方式,可将整个login()函数注释掉,打开请求头中Cookie,将
    其换成浏览器中最新cookie信息即可
    """
    def headers(self):
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/78.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            #'Cookie':'uid=R-570329-33aa83de060094016f3d09; ds_session=n0411e3fo3i0n6sas7so42ks10; Hm_lvt_a68414d98536efc52eeb879f984d8923=1611208544,1611216752,1611371703,1611375529; Hm_lpvt_a68414d98536efc52eeb879f984d8923=1611537976'
        }
        return headers


    #自动登录
    def login(self):
        login_url = 'https://www.dszuqiu.com/w_login'
        captcha_url = 'https://www.dszuqiu.com/captcha'
        resp = self.session.get(captcha_url, headers=self.headers, timeout=30, verify=False)
        logger.info(resp.status_code)
        path = os.path.dirname(os.path.abspath(__file__))
        open(f"{path}/img/football.png", 'wb').write(resp.content)
        im = open(f'{path}/img/football.png', 'rb').read()
        chaojiying = Chaojiying_Client()
        code = chaojiying.PostPic(im, 1006)
        result = code["pic_str"].lower()
        logger.info('验证码识别结果为:')
        logger.info(result)
        #表单
        data = {
                "zhanghu": 'foreign.trade1@cibsc.biz',
                "password": '11223344o',
                "captcha_input": result,
                "rememberMe": '1',
                "is_ajax": '1'
                }
        response = self.session.post(login_url, headers=self.headers, data=data)
        logger.info(response.status_code)
        cookie = requests.utils.dict_from_cookiejar(self.session.cookies)
        return cookie

    #数据获取及存储
    def race(self):
        index_url = ['https://www.dszuqiu.com/league/{}/p.{}?type=ended_race'.format(id, page) for page in range(start_page, end_page + 1)]

        for url in index_url:
            response = self.session.get(url,headers=self.headers,timeout=30,verify=False)
            logger.info(response.status_code)
            html = etree.HTML(response.text)
            href_list = html.xpath('//section[@id="ended"]//a[text()="析"]/@href')
            try:
                match_name = html.xpath('//*[@class="dsBreadcrumbs2"]/text()')[-1].strip()
                for href in href_list:
                    #四合一数据url
                    race_sp = f'https://www.dszuqiu.com/race_sp/' + href.split('/')[-1]
                    #现场数据url
                    race_xc = f'https://www.dszuqiu.com/race_xc/' + href.split('/')[-1]

                    #四合一数据请求
                    race_sp_response = self.session.get(race_sp, headers=self.headers, timeout=30, verify=False)
                    time.sleep(TM)
                    logger.info(race_sp_response.status_code)
                    # logger.info(race_sp_response.text)
                    html = etree.HTML(race_sp_response.text)

                    try:
                        ball_name = html.xpath('//h3[@class="dsBreadcrumbs"]/text()')[-1].strip()
                    except Exception as e:
                        logger.info('cookie失效请重新替换cookie!启动')
                        logger.warning(e)

                    # 让球全场
                    rang_whole = html.xpath('//tbody[@id="sp_rangfen"]/tr')
                    ball_rang_quan = ''
                    for i in rang_whole[::-1]:
                        td_rangfen = i.xpath('./td/text()')
                        if "{}'".format(rang_whole_minute) in td_rangfen[0].strip():
                            ball_rang_quan += td_rangfen[3]
                            break
                        else:
                            ball_rang_quan += " "

                    # 让球半场
                    rang_half = html.xpath('//tbody[@id="sp_half_rangfen"]/tr')
                    ball_ban_rang = ''
                    for i in rang_half[::-1]:
                        td_half_rangfen = i.xpath('./td/text()')
                        if "{}'".format(rang_half_minute) in td_half_rangfen[0].strip():
                            ball_ban_rang += td_half_rangfen[3]
                            break
                        else:
                            ball_ban_rang += " "

                    # 大小球全场
                    size_whole = html.xpath('//tbody[@id="sp_daxiao"]/tr')
                    ball_quan_daxiao = ''
                    for i in size_whole[::-1]:  # enumerate 枚举
                        td_quan_daxiao = i.xpath('./td/text()')
                        if "{}'".format(size_whole_minute) in td_quan_daxiao[0].strip():
                            ball_quan_daxiao += td_quan_daxiao[2]
                            break
                        else:
                            ball_quan_daxiao += " "

                    # 大小球半场
                    size_half = html.xpath('//tbody[@id="sp_half_daxiao"]/tr')
                    ball_ban_daxiao = ''
                    for i in size_half[::-1]:
                        td_size_half_minute = i.xpath('./td/text()')
                        if "{}'".format(size_half_minute) in td_size_half_minute[0].strip():
                            ball_ban_daxiao += td_size_half_minute[2]
                            break
                        else:
                            ball_ban_daxiao += " "

                    # 角球全场
                    jiao_whole = html.xpath('//tbody[@id="sp_corner"]/tr')
                    ball_quan_jiao = ''
                    for i in jiao_whole[::-1]:
                        td_quan_jiao = i.xpath('./td/text()')
                        if "{}'".format(jiao_whole_minute) in td_quan_jiao[0].strip():
                            ball_quan_jiao += td_quan_jiao[2]
                            break
                        else:
                            ball_quan_jiao += " "

                    # 角球半场
                    jiao_half = html.xpath('//tbody[@id="sp_half_corner"]/tr')
                    ball_ban_jiao = ''
                    for i in jiao_half[::-1]:
                        td_jiao_half_minute = i.xpath('./td/text()')
                        if "{}'".format(jiao_half_minute) in td_jiao_half_minute[0].strip():
                            ball_ban_jiao += td_jiao_half_minute[2]
                            break
                        else:
                            ball_ban_jiao += " "

                    #现场数据请求
                    race_xc_response = self.session.get(race_xc, headers=self.headers, timeout=30, verify=False)
                    logger.info(race_xc_response.status_code)

                    race_xc_html = race_xc_response.text.split('chart_options.series = ')

                    # 射正球门1
                    zheng = re.findall(f'"x":{zheng_minute},(.*?)"name"', race_xc_html[1])
                    if zheng == []:
                        zheng_minute_bak = zheng_minute
                        while True:
                            zheng_minute_bak = zheng_minute_bak - 1
                            zheng = re.findall(f'"x":{zheng_minute_bak},(.*?)"name"', race_xc_html[1])
                            if zheng != []:
                                break
                            # print('zheng_minute_bak',zheng_minute_bak)
                        if len(zheng) == 1:
                            zheng_front = re.findall('y":(.*?),"marker', zheng[0])[0]
                            zheng_back = re.findall('info":"(.*?)"', zheng[0])[0]
                        elif len(zheng) > 1:
                            zheng_front = re.findall('y":(.*?),"marker', zheng[0])[0]
                            zheng_back = re.findall('info":"(.*?)"', zheng[0])[0]
                            zheng_front_bak = re.findall('y":(.*?),"marker', zheng[-1])[0]
                            zheng_back_bak = re.findall('info":"(.*?)"', zheng[-1])[0]

                    else:
                        if len(zheng) == 1:
                            zheng_front = re.findall('y":(.*?),"marker', zheng[0])[0]
                            zheng_back = re.findall('info":"(.*?)"', zheng[0])[0]
                        elif len(zheng) > 1:
                            zheng_front = re.findall('y":(.*?),"marker', zheng[0])[0]
                            zheng_back = re.findall('info":"(.*?)"', zheng[0])[0]
                            zheng_front_bak = re.findall('y":(.*?),"marker', zheng[-1])[0]
                            zheng_back_bak = re.findall('info":"(.*?)"', zheng[-1])[0]

                    szqm = f'{zheng_front}比{zheng_back}'

                    try:
                        szqm_bak = f'{zheng_front_bak}比{zheng_back_bak}'
                        if int(zheng_front) + int(zheng_back) > int(zheng_front_bak) + int(zheng_back_bak):
                            szqm = szqm
                        elif int(zheng_front) + int(zheng_back) < int(zheng_front_bak) + int(zheng_back_bak):
                            szqm = szqm_bak
                    except:
                        pass

                    # 射正球门2
                    zheng2 = re.findall(f'"x":{zheng_minute2},(.*?)"name"', race_xc_html[1])
                    if zheng2 == []:
                        zheng_minute2_bak = zheng_minute2
                        while True:
                            zheng_minute2_bak = zheng_minute2_bak - 1
                            zheng2 = re.findall(f'"x":{zheng_minute2_bak},(.*?)"name"', race_xc_html[1])
                            if zheng2 != []:
                                break
                            # print('zheng_minute2_bak',zheng_minute2_bak)
                        if len(zheng2) == 1:
                            zheng_front2 = re.findall('y":(.*?),"marker', zheng2[0])[0]
                            zheng_back2 = re.findall('info":"(.*?)"', zheng2[0])[0]
                        elif len(zheng2) > 1:
                            zheng_front2 = re.findall('y":(.*?),"marker', zheng2[0])[0]
                            zheng_back2 = re.findall('info":"(.*?)"', zheng2[0])[0]
                            zheng_front2_bak = re.findall('y":(.*?),"marker', zheng2[-1])[0]
                            zheng_back2_bak = re.findall('info":"(.*?)"', zheng2[-1])[0]

                    else:
                        if len(zheng2) == 1:
                            zheng_front2 = re.findall('y":(.*?),"marker', zheng2[0])[0]
                            zheng_back2 = re.findall('info":"(.*?)"', zheng2[0])[0]
                        elif len(zheng2) > 1:
                            zheng_front2 = re.findall('y":(.*?),"marker', zheng2[0])[0]
                            zheng_back2 = re.findall('info":"(.*?)"', zheng2[0])[0]
                            zheng_front2_bak = re.findall('y":(.*?),"marker', zheng2[-1])[0]
                            zheng_back2_bak = re.findall('info":"(.*?)"', zheng2[-1])[0]

                    szqm2 = f'{zheng_front2}比{zheng_back2}'

                    try:
                        szqm2_bak = f'{zheng_front2_bak}比{zheng_back2_bak}'
                        if int(zheng_front2) + int(zheng_back2) > int(zheng_front2_bak) + int(zheng_back2_bak):
                            szqm2 = szqm2
                        elif int(zheng_front2) + int(zheng_back2) < int(zheng_front2_bak) + int(zheng_back2_bak):
                            szqm2 = szqm2_bak
                    except:
                        pass

                    #射偏球门1
                    pian = re.findall(f'"x":{pian_minute},(.*?)"name"', race_xc_html[2])
                    if pian == []:
                        pian_minute_bak = pian_minute
                        while True:
                            pian_minute_bak = pian_minute_bak - 1
                            pian = re.findall(f'"x":{pian_minute_bak},(.*?)"name"', race_xc_html[2])
                            if pian != []:
                                break
                            # print('pian_minute_bak',pian_minute_bak)
                        if len(pian) == 1:
                            pian_front = re.findall('y":(.*?),"marker', pian[0])[0]
                            pian_back = re.findall('info":"(.*?)"', pian[0])[0]
                        elif len(pian) > 1:
                            pian_front = re.findall('y":(.*?),"marker', pian[0])[0]
                            pian_back = re.findall('info":"(.*?)"', pian[0])[0]
                            pian_front_bak = re.findall('y":(.*?),"marker', pian[-1])[0]
                            pian_back_bak = re.findall('info":"(.*?)"', pian[-1])[0]

                    else:
                        if len(pian) == 1:
                            pian_front = re.findall('y":(.*?),"marker', pian[0])[0]
                            pian_back = re.findall('info":"(.*?)"', pian[0])[0]
                        elif len(pian) > 1:
                            pian_front = re.findall('y":(.*?),"marker', pian[0])[0]
                            pian_back = re.findall('info":"(.*?)"', pian[0])[0]
                            pian_front_bak = re.findall('y":(.*?),"marker', pian[-1])[0]
                            pian_back_bak = re.findall('info":"(.*?)"', pian[-1])[0]

                    spqm = f'{pian_front}比{pian_back}'

                    try:
                        spqm_bak = f'{pian_front_bak}比{pian_back_bak}'
                        if int(pian_front) + int(pian_back) > int(pian_front_bak) + int(pian_back_bak):
                            spqm = spqm
                        elif int(pian_front) + int(pian_back) < int(pian_front_bak) + int(pian_back_bak):
                            spqm = spqm_bak
                    except:
                        pass

                    # 射偏球门2
                    pian2 = re.findall(f'"x":{pian_minute2},(.*?)"name"', race_xc_html[2])
                    if pian2 == []:
                        pian_minute2_bak = pian_minute2
                        while True:
                            pian_minute2_bak = pian_minute2_bak - 1
                            pian2 = re.findall(f'"x":{pian_minute2_bak},(.*?)"name"', race_xc_html[2])
                            if pian2 != []:
                                break
                            # print('pian_minute2_bak',pian_minute2_bak)

                        if len(pian2) == 1:
                            pian_front2 = re.findall('y":(.*?),"marker', pian2[0])[0]
                            pian_back2 = re.findall('info":"(.*?)"', pian2[0])[0]
                        elif len(pian2) > 1:
                            pian_front2 = re.findall('y":(.*?),"marker', pian2[0])[0]
                            pian_back2 = re.findall('info":"(.*?)"', pian2[0])[0]
                            pian_front2_bak = re.findall('y":(.*?),"marker', pian2[-1])[0]
                            pian_back2_bak = re.findall('info":"(.*?)"', pian2[-1])[0]

                    else:
                        if len(pian2) == 1:
                            pian_front2 = re.findall('y":(.*?),"marker', pian2[0])[0]
                            pian_back2 = re.findall('info":"(.*?)"', pian2[0])[0]
                        elif len(pian2) > 1:
                            pian_front2 = re.findall('y":(.*?),"marker', pian2[0])[0]
                            pian_back2 = re.findall('info":"(.*?)"', pian2[0])[0]
                            pian_front2_bak = re.findall('y":(.*?),"marker', pian2[-1])[0]
                            pian_back2_bak = re.findall('info":"(.*?)"', pian2[-1])[0]

                    spqm2 = f'{pian_front2}比{pian_back2}'

                    try:
                        spqm2_bak = f'{pian_front2_bak}比{pian_back2_bak}'
                        if int(pian_front2) + int(pian_back2) > int(pian_front2_bak) + int(pian_back2_bak):
                            spqm2 = spqm2
                        elif int(pian_front2) + int(pian_back2) < int(pian_front2_bak) + int(pian_back2_bak):
                            spqm2 = spqm2_bak
                    except:
                        pass

                    #危险进攻1
                    weixian = re.findall(f'"x":{weixian_minute},(.*?)"name"', race_xc_html[3])
                    if weixian == []:
                        weixian_minute_bak = weixian_minute
                        while True:
                            weixian_minute_bak = weixian_minute_bak - 1
                            weixian = re.findall(f'"x":{weixian_minute_bak},(.*?)"name"', race_xc_html[3])
                            if weixian != []:
                                break
                            # print('weixian_minute_bak',weixian_minute_bak)

                        if len(weixian) == 1:
                            weixian_front = re.findall('y":(.*?),"marker', weixian[0])[0]
                            weixian_back = re.findall('info":"(.*?)"', weixian[0])[0]
                        elif len(weixian) > 1:
                            weixian_front = re.findall('y":(.*?),"marker', weixian[0])[0]
                            weixian_back = re.findall('info":"(.*?)"', weixian[0])[0]
                            weixian_front_bak = re.findall('y":(.*?),"marker', weixian[-1])[0]
                            weixian_back_bak = re.findall('info":"(.*?)"', weixian[-1])[0]
                    else:
                        if len(weixian) == 1:
                            weixian_front = re.findall('y":(.*?),"marker', weixian[0])[0]
                            weixian_back = re.findall('info":"(.*?)"', weixian[0])[0]
                        elif len(weixian) > 1:
                            weixian_front = re.findall('y":(.*?),"marker', weixian[0])[0]
                            weixian_back = re.findall('info":"(.*?)"', weixian[0])[0]
                            weixian_front_bak = re.findall('y":(.*?),"marker', weixian[-1])[0]
                            weixian_back_bak = re.findall('info":"(.*?)"', weixian[-1])[0]

                    wxjg = f'{weixian_front}比{weixian_back}'

                    try:
                        wxjg_bak = f'{weixian_front_bak}比{weixian_back_bak}'
                        if int(weixian_front) + int(weixian_back) > int(weixian_front_bak) + int(weixian_back_bak):
                            wxjg = wxjg
                        elif int(weixian_front) + int(weixian_back) < int(weixian_front_bak) + int(weixian_back_bak):
                            wxjg = wxjg_bak
                    except:
                        pass

                    # 危险进攻2
                    weixian2 = re.findall(f'"x":{weixian_minute2},(.*?)"name"', race_xc_html[3])
                    if weixian2 == []:
                        weixian_minute2_bak = weixian_minute2
                        while True:
                            weixian_minute2_bak = weixian_minute2_bak - 1
                            weixian2 = re.findall(f'"x":{weixian_minute2_bak},(.*?)"name"', race_xc_html[3])
                            if weixian2 != []:
                                break
                            # print('weixian_minute2_bak',weixian_minute2_bak)

                        if len(weixian2) == 1:
                            weixian_front2 = re.findall('y":(.*?),"marker', weixian2[0])[0]
                            weixian_back2 = re.findall('info":"(.*?)"', weixian2[0])[0]
                        elif len(weixian2) > 1:
                            weixian_front2 = re.findall('y":(.*?),"marker', weixian2[0])[0]
                            weixian_back2 = re.findall('info":"(.*?)"', weixian2[0])[0]
                            weixian_front2_bak = re.findall('y":(.*?),"marker', weixian2[-1])[0]
                            weixian_back2_bak = re.findall('info":"(.*?)"', weixian2[-1])[0]
                    else:
                        if len(weixian2) == 1:
                            weixian_front2 = re.findall('y":(.*?),"marker', weixian2[0])[0]
                            weixian_back2 = re.findall('info":"(.*?)"', weixian2[0])[0]
                        elif len(weixian2) > 1:
                            weixian_front2 = re.findall('y":(.*?),"marker', weixian2[0])[0]
                            weixian_back2 = re.findall('info":"(.*?)"', weixian2[0])[0]
                            weixian_front2_bak = re.findall('y":(.*?),"marker', weixian2[-1])[0]
                            weixian_back2_bak = re.findall('info":"(.*?)"', weixian2[-1])[0]

                    wxjg2 = f'{weixian_front2}比{weixian_back2}'

                    try:
                        wxjg2_bak = f'{weixian_front2_bak}比{weixian_back2_bak}'
                        if int(weixian_front2) + int(weixian_back2) > int(weixian_front2_bak) + int(weixian_back2_bak):
                            wxjg2 = wxjg2
                        elif int(weixian_front2) + int(weixian_back2) < int(weixian_front2_bak) + int(weixian_back2_bak):
                            wxjg2 = wxjg2_bak
                    except:
                        pass

                    #角球进球信息
                    ball_html = etree.HTML(race_xc_response.text)
                    ball_info = ball_html.xpath('//span[@class="timeLineGoal" or @class="timeLineCorner"]/@title')
                    jiao_ball = ''
                    jin_ball = ''
                    for ball in ball_info:
                        if '35' in ball or '36' in ball or '37' in ball or '38' in ball or '39' in ball or '40' in ball or '41' in ball or '42' in ball or '43' in ball or '44' in ball or '45' in ball :
                            if '角球' in ball and '上半场角球' not in jiao_ball:
                                jiao_ball +=  '上半场角球: '  + '\n' + ball + '\n'
                            elif '角球' in ball:
                                jiao_ball +=  ball + '\n'
                            if '进球' in ball and '上半场进球' not in jin_ball:
                                jin_ball += '上半场进球: ' + '\n' + ball + '\n'
                            elif '进球' in ball:
                                jin_ball += ball + '\n'
                        if  '85' in ball or '86' in ball or '87' in ball or '88' in ball or '89' in ball or '90' in ball:
                            if '角球' in ball and '下半场角球' not in jiao_ball:
                                jiao_ball += '下半场角球: ' + '\n' + ball + '\n'
                            elif '角球' in ball:
                                jiao_ball += ball + '\n'
                            if '进球' in ball and '下半场进球' not in jin_ball:
                                jin_ball += '下半场进球: ' + '\n' + ball  + '\n'
                            elif '进球' in ball:
                                jin_ball += ball + '\n'

                    #比赛日期
                    match_time = ball_html.xpath('//span[@class="analysisRaceTime"]/text()')[0].strip()
                    #盘口走势
                    just_move = ball_html.xpath('//a[@href="javascript:void(0)"]/text()')[0].strip().replace('/','//')

                    info = [ball_name, race_xc, match_time, just_move, rang_half_minute, ball_ban_rang,
                            size_half_minute, ball_ban_daxiao, jiao_half_minute, ball_ban_jiao, rang_whole_minute,
                            ball_rang_quan, size_whole_minute, ball_quan_daxiao, jiao_whole_minute, ball_quan_jiao,
                            zheng_minute, szqm, pian_minute, spqm, weixian_minute, wxjg, zheng_minute2, szqm2, pian_minute2, spqm2,
                             weixian_minute2, wxjg2, jiao_ball, jin_ball]

                    logger.info(info)
                    if not os.path.exists(f'{match_name}.csv'):
                        head = ['球队', '链接', '比赛日期', '盘口走势', '分钟', '半场让球', '分钟', '半场大小球', '分钟', '半场角球', '分钟', '全场让球',
                                '分钟', '全场大小球', '分钟', '全场角球', '分钟', '射正球门', '分钟', '射偏球门', '分钟', '危险进攻','分钟', '射正球门',
                                '分钟', '射偏球门', '分钟', '危险进攻',  '角球信息', '进球信息']
                        csvFile = open(f'{match_name}.csv', 'a', newline='', encoding='utf-8-sig')
                        writer = csv.writer(csvFile)
                        writer.writerow(head)
                        csvFile.close()
                    else:
                        csvFile = open(f'{match_name}.csv', 'a+', newline='', encoding='utf-8-sig')
                        writer = csv.writer(csvFile)
                        writer.writerow(info)
                        csvFile.close()
            except:
                pass

        return None


if __name__ == '__main__':
    execute = Football()
    id = input('请输入联赛id:')
    start_page, end_page = map(int, input('设置开始和结束页,空格隔开:').split())
    rang_whole_minute, size_whole_minute, jiao_whole_minute = map(int, input('设置全场分钟,空格隔开(让球|大小球|角球):').split())
    rang_half_minute, size_half_minute, jiao_half_minute = map(int, input('设置半场分钟,空格隔开(让球|大小球|角球):').split())
    zheng_minute, zheng_minute2, pian_minute, pian_minute2, weixian_minute, weixian_minute2 = map(int, input('设置射正(两个值)、射偏(2个值)、危险进攻(2个值),空格隔开(射正|射正|射偏|射偏|危险进攻|危险进攻):').split())
    TM = int(input('请设置爬取速度/s:'))
    execute.login()
    execute.race()




