# -*- coding: utf-8 -*-
import time
import json
import requests
from lxml import etree
from datetime import datetime

cookie = 'race_id=1148873; halfbt_daxiao=0; __yjs_duid=1_455c0fa31305a91ee21a40835c3cc0aa1681790104356; ds_session=sk9mf86b94mm50lcj6hvb3la44; Hm_lvt_a68414d98536efc52eeb879f984d8923=1687163224,1687317465; uid=R-631284-062f66e0064926c023587d; Hm_lpvt_a68414d98536efc52eeb879f984d8923=1687330118'


class Dazuqiu(object):

    def __init__(self):
        self.session = self.session()
        self.headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'Cookie': cookie,
            'Connection': 'close'}
        super().__init__()

    def session(self):
        session = requests.session()
        session.keep_alive = False
        session.adapters.DEFAULT_RETRIES = 10
        requests.packages.urllib3.disable_warnings()
        return session

    def monitor(self, O, M , ID: str, dx: float, dy: float, TM: int):
        while True:
            url = f"https://www.dszuqiu.com/race_sp/{ID}"
            res = self.session.get(url, headers=self.headers, timeout=30, verify=False)
            html = etree.HTML(res.text)
            title = html.xpath('/html/head/title/text()')[0]
            liansai = html.xpath('//h3[@class="dsBreadcrumbs"]/a[3]/text()')[0]
            qiudui = html.xpath('//h3[@class="dsBreadcrumbs"]/text()')[-1].strip()
            if title.strip() == '用户登录 - DS足球':
                print('账号过期，请更换cookie！')
                exit()

            # 四合一大小球全场
            size_whole = html.xpath('//tbody[@id="sp_daxiao"]/tr')
            for tr in size_whole[::-1]:
                td_daxiao = tr.xpath('./td/text()')
                try:
                    bisai_time = datetime.strptime(td_daxiao[5], '%m/%d %H:%M').strftime("%H:%M")
                    m_time = str(O) + ':' + str(M)
                    monitor_time = datetime.strptime(m_time, '%H:%M').strftime("%H:%M")
                    print(f"比赛时间：{bisai_time}，监控时间：{monitor_time}，比赛分钟数：{td_daxiao[0]}，大小球值：{td_daxiao[3]}，大于值：{td_daxiao[2]}")
                    if bisai_time >= monitor_time:
                        if dx == float(td_daxiao[3]) and float(td_daxiao[2]) > dy:
                            info = f"报警  \n比赛ID:{ID} \n 联赛:{liansai} \n 比赛球队{qiudui} \n 大小球:{dx} \n 大于:{dy}"
                            print(info)
                            return  self.send_dd(info)
                        else:
                            if "90" in td_daxiao[0]:
                                return print("本场比赛没有符合条件！退出监控！")
                except:
                    pass
            time.sleep(TM)

    def send_qq(self, msg: str):
        qqgid = '164808476'
        requests.get(
            'http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(str(qqgid), str(msg)))

    def send_dd(slef, msg: str):

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

        requests.post(url, data=json.dumps(data), headers=headers)
        return  print('钉钉推送成功！！！',data)

    def task_run(self, O, M , ID, dx, dy, TM):
        now_time = datetime.now()
        execute_at = datetime(now_time.year, now_time.month, now_time.day, O, M, 0)
        delta = execute_at - datetime.now()
        print(f'于{delta.total_seconds()}秒后执行任务！')
        time.sleep(delta.total_seconds())
        self.monitor(O, M ,ID, dx, dy, TM)



if __name__ == '__main__':
    ID = input('请输入比赛ID:')
    o, m = map(int, input('请输入定时时间例如09 10,空格隔开:').split())
    dx, dy = map(float, input('请输入大小球和大于值,空格隔开:').split())
    TM = int(input('请设置多少秒刷新一次/s:'))
    print('☞脚本已启动...')
    l = Dazuqiu()
    l.task_run(o, m, ID, dx, dy, TM)
