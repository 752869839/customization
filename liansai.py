# -*- coding: utf-8 -*-
import os
import re
import csv
import time
import logging
import requests
from lxml import etree

logging.captureWarnings(True)
class Match(object):

    def __init__(self):
        self.session = self.session()
        self.headers = self.headers()

    def session(self):
        session = requests.session()
        session.keep_alive = False
        session.adapters.DEFAULT_RETRIES = 10
        return session

    def headers(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36',
            'Cookie':'homePupDivLayerbtcmchangename=1; Hm_lvt_4f816d475bb0b9ed640ae412d6b42cab=1622690809; sdc_session=1622690808632; __utma=63332592.676801720.1622690809.1622690809.1622690809.1; __utmc=63332592; __utmz=63332592.1622690809.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; isagree=1; motion_id=1622690856062_0.27120819607822555; usercheck=NjAxMTg4OTI1MWE5MTA5NzYzNTI4ZGIwOTc3OWFhOTY3MGNkOGFhNQ==; ck_user=bW44MzIwOTM=; ck_user2=bW44MzIwOTM=; ck_user_utf8=mn832093; ck_user_retime=1453632627; ck=NjAxMTg4OTI1MWE5MTA5NzYzNTI4ZGIwOTc3OWFhOTY3MGNkOGFhNQ==; tgw_l7_route=a962a8674da93f6ef39cd03ac55f6692; WT_FPC=id=undefined:lv=1622690875360:ss=1622690808631; sdc_userflag=1622690808633::1622690875363::7; Hm_lpvt_4f816d475bb0b9ed640ae412d6b42cab=1622690875; __utmb=63332592.6.10.1622690809; CLICKSTRN_ID=117.107.128.30-1622511393.354239::D391A84A029D8EF50A1037B7A1BF01E6'
        }
        return headers

    def match_data(self, sid, start_round, end_round, TM):
        url_list = [ 'https://liansai.500.com/index.php?c=match&a=getmatch&sid={}&round={}'.format(sid,rou) for rou in range(start_round,end_round + 1)]
        for index_url in url_list:
            response = self.session.get(index_url, headers=self.headers, timeout=30, verify=False)
            print(f'请求url:{response.url},响应状态码:{response.status_code}')
            # print(response.json())
            for key in response.json():
                fid = key['fid']
                touzhu_url = f'https://odds.500.com/fenxi/touzhu-{fid}.shtml'
                ouzhi_url = f'https://odds.500.com/fenxi/ouzhi-{fid}.shtml'
                time.sleep(TM)
                # 投注分析
                tresponse = self.session.get(touzhu_url, headers=self.headers, timeout=30, verify=False)
                print(f'请求url:{tresponse.url},响应状态码:{tresponse.status_code}')
                thtml = etree.HTML(tresponse.content.decode("gbk"))
                # print(tresponse.content.decode("gbk"))

                # 1
                tname = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[3]/td[1]/text()')[0]
                peilv = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[3]/td[2]/text()')[0]
                gailv = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[3]/td[3]/text()')[0]
                beidan = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[3]/td[4]/text()')[0]
                bifa = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[3]/td[5]/text()')[0]
                chengjiaojia = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[3]/td[6]/text()')[0]
                chengjiaoliang = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[3]/td[7]/text()')[0]
                zhuangjia = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[3]/td[8]/text()')[0]
                bifazhishu = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[3]/td[9]/text()')[0]
                lengre = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[3]/td[10]/text()')[0]
                yingkui = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[3]/td[11]/text()')[0]
                print(tname,peilv,gailv,beidan,bifa,chengjiaojia,chengjiaoliang,zhuangjia,bifazhishu,lengre,yingkui)

                # 2
                tname2 = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[4]/td[1]/text()')[0]
                peilv2 = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[4]/td[2]/text()')[0]
                gailv2 = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[4]/td[3]/text()')[0]
                beidan2 = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[4]/td[4]/text()')[0]
                bifa2 = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[4]/td[5]/text()')[0]
                chengjiaojia2 = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[4]/td[6]/text()')[0]
                chengjiaoliang2 = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[4]/td[7]/text()')[0]
                zhuangjia2 = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[4]/td[8]/text()')[0]
                bifazhishu2 = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[4]/td[9]/text()')[0]
                lengre2 = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[4]/td[10]/text()')[0]
                yingkui2 = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[4]/td[11]/text()')[0]
                print(tname2,peilv2,gailv2,beidan2,bifa2,chengjiaojia2,chengjiaoliang2,zhuangjia2,bifazhishu2,lengre2,yingkui2)

                # 3
                tname3 = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[5]/td[1]/text()')[0]
                peilv3 = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[5]/td[2]/text()')[0]
                gailv3 = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[5]/td[3]/text()')[0]
                beidan3 = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[5]/td[4]/text()')[0]
                bifa3 = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[5]/td[5]/text()')[0]
                chengjiaojia3 = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[5]/td[6]/text()')[0]
                chengjiaoliang3 = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[5]/td[7]/text()')[0]
                zhuangjia3 = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[5]/td[8]/text()')[0]
                bifazhishu3 = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[5]/td[9]/text()')[0]
                lengre3 = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[5]/td[10]/text()')[0]
                yingkui3 = thtml.xpath('//table[@class="pub_table pl_table_data  bif-yab"]/tbody/tr[5]/td[11]/text()')[0]
                print(tname3,peilv3,gailv3,beidan3,bifa3,chengjiaojia3,chengjiaoliang3,zhuangjia3,bifazhishu3,lengre3,yingkui3)

                # 百家欧赔
                oresponse = self.session.get(ouzhi_url, headers=self.headers, timeout=30, verify=False)
                print(f'请求url:{oresponse.url},响应状态码:{oresponse.status_code}')
                ohtml = etree.HTML(oresponse.content.decode("gbk"))
                # print(oresponse.content.decode("gbk"))

                #比分
                bifen = ohtml.xpath('//p[@class="odds_hd_bf"]/strong/text()')[0]
                rou = re.findall('round=([\s|\S]+)', index_url)[0]

                data = []

                if ohtml.xpath('//table[@id="datatb"]//tr[1]/td[@class="tb_plgs"]/@title'):
                    # 赔率公司 1
                    name = ohtml.xpath('//table[@id="datatb"]//tr[1]/td[@class="tb_plgs"]/@title')[0]
                    oupeisheng = ohtml.xpath('//table[@id="datatb"]//tr[1]/td[3]//tr[1]/td[1]/text()')[0]
                    oupeiping = ohtml.xpath('//table[@id="datatb"]//tr[1]/td[3]//tr[1]/td[2]/text()')[0]
                    oupeifu = ohtml.xpath('//table[@id="datatb"]//tr[1]/td[3]//tr[1]/td[3]/text()')[0]
                    gailvsheng = ohtml.xpath('//table[@id="datatb"]//tr[1]/td[4]//tr[1]/td[1]/text()')[0]
                    gailvping = ohtml.xpath('//table[@id="datatb"]//tr[1]/td[4]//tr[1]/td[2]/text()')[0]
                    gailvfu = ohtml.xpath('//table[@id="datatb"]//tr[1]/td[4]//tr[1]/td[3]/text()')[0]
                    fanhuanlv = ohtml.xpath('//table[@id="datatb"]//tr[1]/td[5]//tr[1]/td/text()')[0]
                    kailisheng = ohtml.xpath('//table[@id="datatb"]//tr[1]/td[6]//tr[1]/td[1]/text()')[0]
                    kailiping = ohtml.xpath('//table[@id="datatb"]//tr[1]/td[6]//tr[1]/td[2]/text()')[0]
                    kailifu = ohtml.xpath('//table[@id="datatb"]//tr[1]/td[6]//tr[1]/td[3]/text()')[0]
                    print(name,oupeisheng,oupeiping,oupeifu,gailvsheng,gailvping,gailvfu,fanhuanlv,kailisheng,kailiping,kailifu)

                    # 赔率公司 1
                    name2 = ohtml.xpath('//table[@id="datatb"]//tr[1]/td[@class="tb_plgs"]/@title')[0]
                    oupeisheng2 = ohtml.xpath('//table[@id="datatb"]//tr[1]/td[3]//tr[2]/td[1]/text()')[0]
                    oupeiping2 = ohtml.xpath('//table[@id="datatb"]//tr[1]/td[3]//tr[2]/td[2]/text()')[0]
                    oupeifu2 = ohtml.xpath('//table[@id="datatb"]//tr[1]/td[3]//tr[2]/td[3]/text()')[0]
                    gailvsheng2 = ohtml.xpath('//table[@id="datatb"]//tr[1]/td[4]//tr[2]/td[1]/text()')[0]
                    gailvping2 = ohtml.xpath('//table[@id="datatb"]//tr[1]/td[4]//tr[2]/td[2]/text()')[0]
                    gailvfu2 = ohtml.xpath('//table[@id="datatb"]//tr[1]/td[4]//tr[2]/td[3]/text()')[0]
                    fanhuanlv2 = ohtml.xpath('//table[@id="datatb"]//tr[1]/td[5]//tr[2]/td/text()')[0]
                    kailisheng2 = ohtml.xpath('//table[@id="datatb"]//tr[1]/td[6]//tr[2]/td[1]/text()')[0]
                    kailiping2 = ohtml.xpath('//table[@id="datatb"]//tr[1]/td[6]//tr[2]/td[2]/text()')[0]
                    kailifu2 = ohtml.xpath('//table[@id="datatb"]//tr[1]/td[6]//tr[2]/td[3]/text()')[0]
                    print(name2,oupeisheng2,oupeiping2,oupeifu2,gailvsheng2,gailvping2,gailvfu2,fanhuanlv2,kailisheng2,kailiping2,kailifu2)

                    gailvshengcha = str(round(float(str(gailvsheng).replace('%',''))-float(str(gailvsheng2).replace('%','')),2))+'%'
                    gailvfucha = str(round(float(str(gailvfu).replace('%', '')) - float(str(gailvfu2).replace('%', '')),2)) + '%'
                    fanhuanlvcha = str(round(float(str(fanhuanlv).replace('%', '')) - float(str(fanhuanlv2).replace('%', '')),2)) + '%'

                    data.extend([sid, rou, ouzhi_url, '', tname, peilv, gailv, beidan, bifa, chengjiaojia, chengjiaoliang, zhuangjia, bifazhishu, lengre, yingkui ,f'{tname}-{tname3} {bifen}','', name, oupeisheng,oupeisheng2, float(oupeisheng)-float(oupeisheng2),oupeiping,oupeiping2, oupeifu,oupeifu2,float(oupeifu)-float(oupeifu2), gailvsheng,gailvsheng2,gailvshengcha, gailvping,gailvping2, gailvfu,gailvfu2,gailvfucha, fanhuanlv,fanhuanlv2,fanhuanlvcha, kailisheng,kailisheng2,float(kailisheng)-float(kailisheng2), kailiping,kailiping2, kailifu,kailifu2,float(kailifu)-float(kailifu2)])
                else:
                    break

                if ohtml.xpath('//table[@id="datatb"]//tr[2]/td[@class="tb_plgs"]/@title'):
                    # 赔率公司 2
                    name3 = ohtml.xpath('//table[@id="datatb"]//tr[2]/td[@class="tb_plgs"]/@title')[0]
                    oupeisheng3 = ohtml.xpath('//table[@id="datatb"]//tr[2]/td[3]//tr[1]/td[1]/text()')[0]
                    oupeiping3 = ohtml.xpath('//table[@id="datatb"]//tr[2]/td[3]//tr[1]/td[2]/text()')[0]
                    oupeifu3 = ohtml.xpath('//table[@id="datatb"]//tr[2]/td[3]//tr[1]/td[3]/text()')[0]
                    gailvsheng3 = ohtml.xpath('//table[@id="datatb"]//tr[2]/td[4]//tr[1]/td[1]/text()')[0]
                    gailvping3 = ohtml.xpath('//table[@id="datatb"]//tr[2]/td[4]//tr[1]/td[2]/text()')[0]
                    gailvfu3 = ohtml.xpath('//table[@id="datatb"]//tr[2]/td[4]//tr[1]/td[3]/text()')[0]
                    fanhuanlv3 = ohtml.xpath('//table[@id="datatb"]//tr[2]/td[5]//tr[1]/td/text()')[0]
                    kailisheng3 = ohtml.xpath('//table[@id="datatb"]//tr[2]/td[6]//tr[1]/td[1]/text()')[0]
                    kailiping3 = ohtml.xpath('//table[@id="datatb"]//tr[2]/td[6]//tr[1]/td[2]/text()')[0]
                    kailifu3 = ohtml.xpath('//table[@id="datatb"]//tr[2]/td[6]//tr[1]/td[3]/text()')[0]
                    print(name3,oupeisheng3,oupeiping3,oupeifu3,gailvsheng3,gailvping3,gailvfu3,fanhuanlv3,kailisheng3,kailiping3,kailifu3)

                    # 赔率公司 2
                    name4 = ohtml.xpath('//table[@id="datatb"]//tr[2]/td[@class="tb_plgs"]/@title')[0]
                    oupeisheng4 = ohtml.xpath('//table[@id="datatb"]//tr[2]/td[3]//tr[2]/td[1]/text()')[0]
                    oupeiping4 = ohtml.xpath('//table[@id="datatb"]//tr[2]/td[3]//tr[2]/td[2]/text()')[0]
                    oupeifu4 = ohtml.xpath('//table[@id="datatb"]//tr[2]/td[3]//tr[2]/td[3]/text()')[0]
                    gailvsheng4 = ohtml.xpath('//table[@id="datatb"]//tr[2]/td[4]//tr[2]/td[1]/text()')[0]
                    gailvping4 = ohtml.xpath('//table[@id="datatb"]//tr[2]/td[4]//tr[2]/td[2]/text()')[0]
                    gailvfu4 = ohtml.xpath('//table[@id="datatb"]//tr[2]/td[4]//tr[2]/td[3]/text()')[0]
                    fanhuanlv4 = ohtml.xpath('//table[@id="datatb"]//tr[2]/td[5]//tr[2]/td/text()')[0]
                    kailisheng4 = ohtml.xpath('//table[@id="datatb"]//tr[2]/td[6]//tr[2]/td[1]/text()')[0]
                    kailiping4 = ohtml.xpath('//table[@id="datatb"]//tr[2]/td[6]//tr[2]/td[2]/text()')[0]
                    kailifu4 = ohtml.xpath('//table[@id="datatb"]//tr[2]/td[6]//tr[2]/td[3]/text()')[0]
                    print(name4,oupeisheng4,oupeiping4,oupeifu4,gailvsheng4,gailvping4,gailvfu4,fanhuanlv4,kailisheng4,kailiping4,kailifu4)

                    gailvshengcha4 = str(round(float(str(gailvsheng3).replace('%',''))-float(str(gailvsheng4).replace('%','')),2))+'%'
                    gailvfucha4 = str(round(float(str(gailvfu3).replace('%', '')) - float(str(gailvfu4).replace('%', '')),2)) + '%'
                    fanhuanlvcha4 = str(round(float(str(fanhuanlv3).replace('%', '')) - float(str(fanhuanlv4).replace('%', '')),2)) + '%'

                    data.extend(['', name3, oupeisheng3,oupeisheng4, float(oupeisheng3)-float(oupeisheng4),oupeiping3,oupeiping4, oupeifu3,oupeifu4,float(oupeifu3)-float(oupeifu4), gailvsheng3,gailvsheng4,gailvshengcha4, gailvping3,gailvping4, gailvfu3,gailvfu4,gailvfucha4, fanhuanlv3,fanhuanlv4,fanhuanlvcha4, kailisheng3,kailisheng4,float(kailisheng3)-float(kailisheng4), kailiping3,kailiping4, kailifu3,kailifu4,float(kailifu3)-float(kailifu4)])
                else:
                    pass

                if ohtml.xpath('//table[@id="datatb"]//tr[3]/td[@class="tb_plgs"]/@title'):
                    # 赔率公司 3
                    name5 = ohtml.xpath('//table[@id="datatb"]//tr[3]/td[@class="tb_plgs"]/@title')[0]
                    oupeisheng5 = ohtml.xpath('//table[@id="datatb"]//tr[3]/td[3]//tr[1]/td[1]/text()')[0]
                    oupeiping5 = ohtml.xpath('//table[@id="datatb"]//tr[3]/td[3]//tr[1]/td[2]/text()')[0]
                    oupeifu5 = ohtml.xpath('//table[@id="datatb"]//tr[3]/td[3]//tr[1]/td[3]/text()')[0]
                    gailvsheng5 = ohtml.xpath('//table[@id="datatb"]//tr[3]/td[4]//tr[1]/td[1]/text()')[0]
                    gailvping5 = ohtml.xpath('//table[@id="datatb"]//tr[3]/td[4]//tr[1]/td[2]/text()')[0]
                    gailvfu5 = ohtml.xpath('//table[@id="datatb"]//tr[3]/td[4]//tr[1]/td[3]/text()')[0]
                    fanhuanlv5 = ohtml.xpath('//table[@id="datatb"]//tr[3]/td[5]//tr[1]/td/text()')[0]
                    kailisheng5 = ohtml.xpath('//table[@id="datatb"]//tr[3]/td[6]//tr[1]/td[1]/text()')[0]
                    kailiping5 = ohtml.xpath('//table[@id="datatb"]//tr[3]/td[6]//tr[1]/td[2]/text()')[0]
                    kailifu5 = ohtml.xpath('//table[@id="datatb"]//tr[3]/td[6]//tr[1]/td[3]/text()')[0]
                    print(name5,oupeisheng5,oupeiping5,oupeifu5,gailvsheng5,gailvping5,gailvfu5,fanhuanlv5,kailisheng5,kailiping5,kailifu5)

                    # 赔率公司 3
                    name6 = ohtml.xpath('//table[@id="datatb"]//tr[3]/td[@class="tb_plgs"]/@title')[0]
                    oupeisheng6 = ohtml.xpath('//table[@id="datatb"]//tr[3]/td[3]//tr[2]/td[1]/text()')[0]
                    oupeiping6 = ohtml.xpath('//table[@id="datatb"]//tr[3]/td[3]//tr[2]/td[2]/text()')[0]
                    oupeifu6 = ohtml.xpath('//table[@id="datatb"]//tr[3]/td[3]//tr[2]/td[3]/text()')[0]
                    gailvsheng6 = ohtml.xpath('//table[@id="datatb"]//tr[3]/td[4]//tr[2]/td[1]/text()')[0]
                    gailvping6 = ohtml.xpath('//table[@id="datatb"]//tr[3]/td[4]//tr[2]/td[2]/text()')[0]
                    gailvfu6 = ohtml.xpath('//table[@id="datatb"]//tr[3]/td[4]//tr[2]/td[3]/text()')[0]
                    fanhuanlv6 = ohtml.xpath('//table[@id="datatb"]//tr[3]/td[5]//tr[2]/td/text()')[0]
                    kailisheng6 = ohtml.xpath('//table[@id="datatb"]//tr[3]/td[6]//tr[2]/td[1]/text()')[0]
                    kailiping6 = ohtml.xpath('//table[@id="datatb"]//tr[3]/td[6]//tr[2]/td[2]/text()')[0]
                    kailifu6 = ohtml.xpath('//table[@id="datatb"]//tr[3]/td[6]//tr[2]/td[3]/text()')[0]
                    print(name6,oupeisheng6,oupeiping6,oupeifu6,gailvsheng6,gailvping6,gailvfu6,fanhuanlv6,kailisheng6,kailiping6,kailifu6)

                    gailvshengcha6 = str(round(float(str(gailvsheng5).replace('%',''))-float(str(gailvsheng6).replace('%','')),2))+'%'
                    gailvfucha6 = str(round(float(str(gailvfu5).replace('%', '')) - float(str(gailvfu6).replace('%', '')),2)) + '%'
                    fanhuanlvcha6 = str(round(float(str(fanhuanlv5).replace('%', '')) - float(str(fanhuanlv6).replace('%', '')),2)) + '%'

                    data.extend(['', name5, oupeisheng5,oupeisheng6, float(oupeisheng5)-float(oupeisheng6),oupeiping5,oupeiping6, oupeifu5,oupeifu6,float(oupeifu5)-float(oupeifu6), gailvsheng5,gailvsheng6,gailvshengcha6, gailvping5,gailvping6, gailvfu5,gailvfu6,gailvfucha6, fanhuanlv5,fanhuanlv6,fanhuanlvcha6, kailisheng5,kailisheng6,float(kailisheng5)-float(kailisheng6), kailiping5,kailiping6, kailifu5,kailifu6,float(kailifu5)-float(kailifu6)])
                else:
                    pass

                if ohtml.xpath('//table[@id="datatb"]//tr[4]/td[@class="tb_plgs"]/@title'):
                    # 赔率公司 4
                    name7 = ohtml.xpath('//table[@id="datatb"]//tr[4]/td[@class="tb_plgs"]/@title')[0]
                    oupeisheng7 = ohtml.xpath('//table[@id="datatb"]//tr[4]/td[3]//tr[1]/td[1]/text()')[0]
                    oupeiping7 = ohtml.xpath('//table[@id="datatb"]//tr[4]/td[3]//tr[1]/td[2]/text()')[0]
                    oupeifu7 = ohtml.xpath('//table[@id="datatb"]//tr[4]/td[3]//tr[1]/td[3]/text()')[0]
                    gailvsheng7 = ohtml.xpath('//table[@id="datatb"]//tr[4]/td[4]//tr[1]/td[1]/text()')[0]
                    gailvping7 = ohtml.xpath('//table[@id="datatb"]//tr[4]/td[4]//tr[1]/td[2]/text()')[0]
                    gailvfu7 = ohtml.xpath('//table[@id="datatb"]//tr[4]/td[4]//tr[1]/td[3]/text()')[0]
                    fanhuanlv7 = ohtml.xpath('//table[@id="datatb"]//tr[4]/td[5]//tr[1]/td/text()')[0]
                    kailisheng7 = ohtml.xpath('//table[@id="datatb"]//tr[4]/td[6]//tr[1]/td[1]/text()')[0]
                    kailiping7 = ohtml.xpath('//table[@id="datatb"]//tr[4]/td[6]//tr[1]/td[2]/text()')[0]
                    kailifu7 = ohtml.xpath('//table[@id="datatb"]//tr[4]/td[6]//tr[1]/td[3]/text()')[0]
                    print(name7,oupeisheng7,oupeiping7,oupeifu7,gailvsheng7,gailvping7,gailvfu7,fanhuanlv7,kailisheng7,kailiping7,kailifu7)

                    # 赔率公司 4
                    name8 = ohtml.xpath('//table[@id="datatb"]//tr[4]/td[@class="tb_plgs"]/@title')[0]
                    oupeisheng8 = ohtml.xpath('//table[@id="datatb"]//tr[4]/td[3]//tr[2]/td[1]/text()')[0]
                    oupeiping8 = ohtml.xpath('//table[@id="datatb"]//tr[4]/td[3]//tr[2]/td[2]/text()')[0]
                    oupeifu8 = ohtml.xpath('//table[@id="datatb"]//tr[4]/td[3]//tr[2]/td[3]/text()')[0]
                    gailvsheng8 = ohtml.xpath('//table[@id="datatb"]//tr[4]/td[4]//tr[2]/td[1]/text()')[0]
                    gailvping8 = ohtml.xpath('//table[@id="datatb"]//tr[4]/td[4]//tr[2]/td[2]/text()')[0]
                    gailvfu8 = ohtml.xpath('//table[@id="datatb"]//tr[4]/td[4]//tr[2]/td[3]/text()')[0]
                    fanhuanlv8 = ohtml.xpath('//table[@id="datatb"]//tr[4]/td[5]//tr[2]/td/text()')[0]
                    kailisheng8 = ohtml.xpath('//table[@id="datatb"]//tr[4]/td[6]//tr[2]/td[1]/text()')[0]
                    kailiping8 = ohtml.xpath('//table[@id="datatb"]//tr[4]/td[6]//tr[2]/td[2]/text()')[0]
                    kailifu8 = ohtml.xpath('//table[@id="datatb"]//tr[4]/td[6]//tr[2]/td[3]/text()')[0]
                    print(name8,oupeisheng8,oupeiping8,oupeifu8,gailvsheng8,gailvping8,gailvfu8,fanhuanlv8,kailisheng8,kailiping8,kailifu8)

                    gailvshengcha8 = str(round(float(str(gailvsheng7).replace('%',''))-float(str(gailvsheng8).replace('%','')),2))+'%'
                    gailvfucha8 = str(round(float(str(gailvfu7).replace('%', '')) - float(str(gailvfu8).replace('%', '')),2)) + '%'
                    fanhuanlvcha8 = str(round(float(str(fanhuanlv7).replace('%', '')) - float(str(fanhuanlv8).replace('%', '')),2)) + '%'

                    data.extend(['', name7, oupeisheng7,oupeisheng8, float(oupeisheng7)-float(oupeisheng8),oupeiping7,oupeiping8, oupeifu7,oupeifu8,float(oupeifu7)-float(oupeifu8), gailvsheng7,gailvsheng8,gailvshengcha8, gailvping7,gailvping8, gailvfu7,gailvfu8,gailvfucha8, fanhuanlv7,fanhuanlv8,fanhuanlvcha8, kailisheng7,kailisheng8,float(kailisheng7)-float(kailisheng8), kailiping7,kailiping8, kailifu7,kailifu8,float(kailifu7)-float(kailifu8)])
                else:
                    pass

                if ohtml.xpath('//table[@id="datatb"]//tr[5]/td[@class="tb_plgs"]/@title'):
                    # 赔率公司 5
                    name9 = ohtml.xpath('//table[@id="datatb"]//tr[5]/td[@class="tb_plgs"]/@title')[0]
                    oupeisheng9 = ohtml.xpath('//table[@id="datatb"]//tr[5]/td[3]//tr[1]/td[1]/text()')[0]
                    oupeiping9 = ohtml.xpath('//table[@id="datatb"]//tr[5]/td[3]//tr[1]/td[2]/text()')[0]
                    oupeifu9 = ohtml.xpath('//table[@id="datatb"]//tr[5]/td[3]//tr[1]/td[3]/text()')[0]
                    gailvsheng9 = ohtml.xpath('//table[@id="datatb"]//tr[5]/td[4]//tr[1]/td[1]/text()')[0]
                    gailvping9 = ohtml.xpath('//table[@id="datatb"]//tr[5]/td[4]//tr[1]/td[2]/text()')[0]
                    gailvfu9 = ohtml.xpath('//table[@id="datatb"]//tr[5]/td[4]//tr[1]/td[3]/text()')[0]
                    fanhuanlv9 = ohtml.xpath('//table[@id="datatb"]//tr[5]/td[5]//tr[1]/td/text()')[0]
                    kailisheng9 = ohtml.xpath('//table[@id="datatb"]//tr[5]/td[6]//tr[1]/td[1]/text()')[0]
                    kailiping9 = ohtml.xpath('//table[@id="datatb"]//tr[5]/td[6]//tr[1]/td[2]/text()')[0]
                    kailifu9 = ohtml.xpath('//table[@id="datatb"]//tr[5]/td[6]//tr[1]/td[3]/text()')[0]
                    print(name9,oupeisheng9,oupeiping9,oupeifu9,gailvsheng9,gailvping9,gailvfu9,fanhuanlv9,kailisheng9,kailiping9,kailifu9)

                    # 赔率公司 5
                    name10 = ohtml.xpath('//table[@id="datatb"]//tr[5]/td[@class="tb_plgs"]/@title')[0]
                    oupeisheng10 = ohtml.xpath('//table[@id="datatb"]//tr[5]/td[3]//tr[2]/td[1]/text()')[0]
                    oupeiping10 = ohtml.xpath('//table[@id="datatb"]//tr[5]/td[3]//tr[2]/td[2]/text()')[0]
                    oupeifu10 = ohtml.xpath('//table[@id="datatb"]//tr[5]/td[3]//tr[2]/td[3]/text()')[0]
                    gailvsheng10 = ohtml.xpath('//table[@id="datatb"]//tr[5]/td[4]//tr[2]/td[1]/text()')[0]
                    gailvping10 = ohtml.xpath('//table[@id="datatb"]//tr[5]/td[4]//tr[2]/td[2]/text()')[0]
                    gailvfu10 = ohtml.xpath('//table[@id="datatb"]//tr[5]/td[4]//tr[2]/td[3]/text()')[0]
                    fanhuanlv10 = ohtml.xpath('//table[@id="datatb"]//tr[5]/td[5]//tr[2]/td/text()')[0]
                    kailisheng10 = ohtml.xpath('//table[@id="datatb"]//tr[5]/td[6]//tr[2]/td[1]/text()')[0]
                    kailiping10 = ohtml.xpath('//table[@id="datatb"]//tr[5]/td[6]//tr[2]/td[2]/text()')[0]
                    kailifu10 = ohtml.xpath('//table[@id="datatb"]//tr[5]/td[6]//tr[2]/td[3]/text()')[0]
                    print(name10,oupeisheng10,oupeiping10,oupeifu10,gailvsheng10,gailvping10,gailvfu10,fanhuanlv10,kailisheng10,kailiping10,kailifu10)

                    gailvshengcha10 = str(round(float(str(gailvsheng9).replace('%',''))-float(str(gailvsheng10).replace('%','')),2))+'%'
                    gailvfucha10 = str(round(float(str(gailvfu9).replace('%', '')) - float(str(gailvfu10).replace('%', '')),2)) + '%'
                    fanhuanlvcha10 = str(round(float(str(fanhuanlv9).replace('%', '')) - float(str(fanhuanlv10).replace('%', '')),2)) + '%'

                    data.extend(['', name9, oupeisheng9,oupeisheng10, float(oupeisheng9)-float(oupeisheng10),oupeiping9,oupeiping10, oupeifu9,oupeifu10,float(oupeifu9)-float(oupeifu10), gailvsheng9,gailvsheng10,gailvshengcha10, gailvping9,gailvping10, gailvfu9,gailvfu10,gailvfucha10, fanhuanlv9,fanhuanlv10,fanhuanlvcha10, kailisheng9,kailisheng10,float(kailisheng9)-float(kailisheng10), kailiping9,kailiping10, kailifu9,kailifu10,float(kailifu9)-float(kailifu10)])
                else:
                    pass

                if ohtml.xpath('//table[@id="datatb"]//tr[6]/td[@class="tb_plgs"]/@title'):
                    # 赔率公司 6
                    name11 = ohtml.xpath('//table[@id="datatb"]//tr[6]/td[@class="tb_plgs"]/@title')[0]
                    oupeisheng11 = ohtml.xpath('//table[@id="datatb"]//tr[6]/td[3]//tr[1]/td[1]/text()')[0]
                    oupeiping11 = ohtml.xpath('//table[@id="datatb"]//tr[6]/td[3]//tr[1]/td[2]/text()')[0]
                    oupeifu11 = ohtml.xpath('//table[@id="datatb"]//tr[6]/td[3]//tr[1]/td[3]/text()')[0]
                    gailvsheng11 = ohtml.xpath('//table[@id="datatb"]//tr[6]/td[4]//tr[1]/td[1]/text()')[0]
                    gailvping11 = ohtml.xpath('//table[@id="datatb"]//tr[6]/td[4]//tr[1]/td[2]/text()')[0]
                    gailvfu11 = ohtml.xpath('//table[@id="datatb"]//tr[6]/td[4]//tr[1]/td[3]/text()')[0]
                    fanhuanlv11 = ohtml.xpath('//table[@id="datatb"]//tr[6]/td[5]//tr[1]/td/text()')[0]
                    kailisheng11 = ohtml.xpath('//table[@id="datatb"]//tr[6]/td[6]//tr[1]/td[1]/text()')[0]
                    kailiping11 = ohtml.xpath('//table[@id="datatb"]//tr[6]/td[6]//tr[1]/td[2]/text()')[0]
                    kailifu11 = ohtml.xpath('//table[@id="datatb"]//tr[6]/td[6]//tr[1]/td[3]/text()')[0]
                    print(name11,oupeisheng11,oupeiping11,oupeifu11,gailvsheng11,gailvping11,gailvfu11,fanhuanlv11,kailisheng11,kailiping11,kailifu11)

                    # 赔率公司 6
                    name12 = ohtml.xpath('//table[@id="datatb"]//tr[6]/td[@class="tb_plgs"]/@title')[0]
                    oupeisheng12 = ohtml.xpath('//table[@id="datatb"]//tr[6]/td[3]//tr[2]/td[1]/text()')[0]
                    oupeiping12 = ohtml.xpath('//table[@id="datatb"]//tr[6]/td[3]//tr[2]/td[2]/text()')[0]
                    oupeifu12 = ohtml.xpath('//table[@id="datatb"]//tr[6]/td[3]//tr[2]/td[3]/text()')[0]
                    gailvsheng12 = ohtml.xpath('//table[@id="datatb"]//tr[6]/td[4]//tr[2]/td[1]/text()')[0]
                    gailvping12 = ohtml.xpath('//table[@id="datatb"]//tr[6]/td[4]//tr[2]/td[2]/text()')[0]
                    gailvfu12 = ohtml.xpath('//table[@id="datatb"]//tr[6]/td[4]//tr[2]/td[3]/text()')[0]
                    fanhuanlv12 = ohtml.xpath('//table[@id="datatb"]//tr[6]/td[5]//tr[2]/td/text()')[0]
                    kailisheng12 = ohtml.xpath('//table[@id="datatb"]//tr[6]/td[6]//tr[2]/td[1]/text()')[0]
                    kailiping12 = ohtml.xpath('//table[@id="datatb"]//tr[6]/td[6]//tr[2]/td[2]/text()')[0]
                    kailifu12 = ohtml.xpath('//table[@id="datatb"]//tr[6]/td[6]//tr[2]/td[3]/text()')[0]
                    print(name12,oupeisheng12,oupeiping12,oupeifu12,gailvsheng12,gailvping12,gailvfu12,fanhuanlv12,kailisheng12,kailiping12,kailifu12)

                    gailvshengcha12 = str(round(float(str(gailvsheng11).replace('%',''))-float(str(gailvsheng12).replace('%','')),2))+'%'
                    gailvfucha12 = str(round(float(str(gailvfu11).replace('%', '')) - float(str(gailvfu12).replace('%', '')),2)) + '%'
                    fanhuanlvcha12 = str(round(float(str(fanhuanlv11).replace('%', '')) - float(str(fanhuanlv12).replace('%', '')),2)) + '%'

                    data.extend(['', name11, oupeisheng11,oupeisheng12, float(oupeisheng11)-float(oupeisheng12),oupeiping11,oupeiping12, oupeifu11,oupeifu12,float(oupeifu11)-float(oupeifu12), gailvsheng11,gailvsheng12,gailvshengcha12, gailvping11,gailvping12, gailvfu11,gailvfu12,gailvfucha12, fanhuanlv11,fanhuanlv12,fanhuanlvcha12, kailisheng11,kailisheng12,float(kailisheng11)-float(kailisheng12), kailiping11,kailiping12, kailifu11,kailifu12,float(kailifu11)-float(kailifu12)])
                else:
                    pass

                if ohtml.xpath('//table[@id="datatb"]//tr[7]/td[@class="tb_plgs"]/@title'):
                    # 赔率公司 7
                    name13 = ohtml.xpath('//table[@id="datatb"]//tr[7]/td[@class="tb_plgs"]/@title')[0]
                    oupeisheng13 = ohtml.xpath('//table[@id="datatb"]//tr[7]/td[3]//tr[1]/td[1]/text()')[0]
                    oupeiping13 = ohtml.xpath('//table[@id="datatb"]//tr[7]/td[3]//tr[1]/td[2]/text()')[0]
                    oupeifu13 = ohtml.xpath('//table[@id="datatb"]//tr[7]/td[3]//tr[1]/td[3]/text()')[0]
                    gailvsheng13 = ohtml.xpath('//table[@id="datatb"]//tr[7]/td[4]//tr[1]/td[1]/text()')[0]
                    gailvping13 = ohtml.xpath('//table[@id="datatb"]//tr[7]/td[4]//tr[1]/td[2]/text()')[0]
                    gailvfu13 = ohtml.xpath('//table[@id="datatb"]//tr[7]/td[4]//tr[1]/td[3]/text()')[0]
                    fanhuanlv13 = ohtml.xpath('//table[@id="datatb"]//tr[7]/td[5]//tr[1]/td/text()')[0]
                    kailisheng13 = ohtml.xpath('//table[@id="datatb"]//tr[7]/td[6]//tr[1]/td[1]/text()')[0]
                    kailiping13 = ohtml.xpath('//table[@id="datatb"]//tr[7]/td[6]//tr[1]/td[2]/text()')[0]
                    kailifu13 = ohtml.xpath('//table[@id="datatb"]//tr[7]/td[6]//tr[1]/td[3]/text()')[0]
                    print(name13,oupeisheng13,oupeiping13,oupeifu13,gailvsheng13,gailvping13,gailvfu13,fanhuanlv13,kailisheng13,kailiping13,kailifu13)

                    # 赔率公司 7
                    name14 = ohtml.xpath('//table[@id="datatb"]//tr[7]/td[@class="tb_plgs"]/@title')[0]
                    oupeisheng14 = ohtml.xpath('//table[@id="datatb"]//tr[7]/td[3]//tr[2]/td[1]/text()')[0]
                    oupeiping14 = ohtml.xpath('//table[@id="datatb"]//tr[7]/td[3]//tr[2]/td[2]/text()')[0]
                    oupeifu14 = ohtml.xpath('//table[@id="datatb"]//tr[7]/td[3]//tr[2]/td[3]/text()')[0]
                    gailvsheng14 = ohtml.xpath('//table[@id="datatb"]//tr[7]/td[4]//tr[2]/td[1]/text()')[0]
                    gailvping14 = ohtml.xpath('//table[@id="datatb"]//tr[7]/td[4]//tr[2]/td[2]/text()')[0]
                    gailvfu14 = ohtml.xpath('//table[@id="datatb"]//tr[7]/td[4]//tr[2]/td[3]/text()')[0]
                    fanhuanlv14 = ohtml.xpath('//table[@id="datatb"]//tr[7]/td[5]//tr[2]/td/text()')[0]
                    kailisheng14 = ohtml.xpath('//table[@id="datatb"]//tr[7]/td[6]//tr[2]/td[1]/text()')[0]
                    kailiping14 = ohtml.xpath('//table[@id="datatb"]//tr[7]/td[6]//tr[2]/td[2]/text()')[0]
                    kailifu14 = ohtml.xpath('//table[@id="datatb"]//tr[7]/td[6]//tr[2]/td[3]/text()')[0]
                    print(name14,oupeisheng14,oupeiping14,oupeifu14,gailvsheng14,gailvping14,gailvfu14,fanhuanlv14,kailisheng14,kailiping14,kailifu14)

                    gailvshengcha14 = str(round(float(str(gailvsheng13).replace('%',''))-float(str(gailvsheng14).replace('%','')),2))+'%'
                    gailvfucha14 = str(round(float(str(gailvfu13).replace('%', '')) - float(str(gailvfu14).replace('%', '')),2)) + '%'
                    fanhuanlvcha14 = str(round(float(str(fanhuanlv13).replace('%', '')) - float(str(fanhuanlv14).replace('%', '')),2)) + '%'

                    data.extend(['', name13, oupeisheng13,oupeisheng14, float(oupeisheng13)-float(oupeisheng14),oupeiping13,oupeiping14, oupeifu13,oupeifu14,float(oupeifu13)-float(oupeifu14), gailvsheng13,gailvsheng14,gailvshengcha14, gailvping13,gailvping14, gailvfu13,gailvfu14,gailvfucha14, fanhuanlv13,fanhuanlv14,fanhuanlvcha14, kailisheng13,kailisheng14,float(kailisheng13)-float(kailisheng14), kailiping13,kailiping14, kailifu13,kailifu14,float(kailifu13)-float(kailifu14)])
                else:
                    pass

                if ohtml.xpath('//table[@id="datatb"]//tr[8]/td[@class="tb_plgs"]/@title'):
                    # 赔率公司 8
                    name15 = ohtml.xpath('//table[@id="datatb"]//tr[8]/td[@class="tb_plgs"]/@title')[0]
                    oupeisheng15 = ohtml.xpath('//table[@id="datatb"]//tr[8]/td[3]//tr[1]/td[1]/text()')[0]
                    oupeiping15 = ohtml.xpath('//table[@id="datatb"]//tr[8]/td[3]//tr[1]/td[2]/text()')[0]
                    oupeifu15 = ohtml.xpath('//table[@id="datatb"]//tr[8]/td[3]//tr[1]/td[3]/text()')[0]
                    gailvsheng15 = ohtml.xpath('//table[@id="datatb"]//tr[8]/td[4]//tr[1]/td[1]/text()')[0]
                    gailvping15 = ohtml.xpath('//table[@id="datatb"]//tr[8]/td[4]//tr[1]/td[2]/text()')[0]
                    gailvfu15 = ohtml.xpath('//table[@id="datatb"]//tr[8]/td[4]//tr[1]/td[3]/text()')[0]
                    fanhuanlv15 = ohtml.xpath('//table[@id="datatb"]//tr[8]/td[5]//tr[1]/td/text()')[0]
                    kailisheng15 = ohtml.xpath('//table[@id="datatb"]//tr[8]/td[6]//tr[1]/td[1]/text()')[0]
                    kailiping15 = ohtml.xpath('//table[@id="datatb"]//tr[8]/td[6]//tr[1]/td[2]/text()')[0]
                    kailifu15 = ohtml.xpath('//table[@id="datatb"]//tr[8]/td[6]//tr[1]/td[3]/text()')[0]
                    print(name15,oupeisheng15,oupeiping15,oupeifu15,gailvsheng15,gailvping15,gailvfu15,fanhuanlv15,kailisheng15,kailiping15,kailifu15)

                    # 赔率公司 8
                    name16 = ohtml.xpath('//table[@id="datatb"]//tr[8]/td[@class="tb_plgs"]/@title')[0]
                    oupeisheng16 = ohtml.xpath('//table[@id="datatb"]//tr[8]/td[3]//tr[2]/td[1]/text()')[0]
                    oupeiping16 = ohtml.xpath('//table[@id="datatb"]//tr[8]/td[3]//tr[2]/td[2]/text()')[0]
                    oupeifu16 = ohtml.xpath('//table[@id="datatb"]//tr[8]/td[3]//tr[2]/td[3]/text()')[0]
                    gailvsheng16 = ohtml.xpath('//table[@id="datatb"]//tr[8]/td[4]//tr[2]/td[1]/text()')[0]
                    gailvping16 = ohtml.xpath('//table[@id="datatb"]//tr[8]/td[4]//tr[2]/td[2]/text()')[0]
                    gailvfu16 = ohtml.xpath('//table[@id="datatb"]//tr[8]/td[4]//tr[2]/td[3]/text()')[0]
                    fanhuanlv16 = ohtml.xpath('//table[@id="datatb"]//tr[8]/td[5]//tr[2]/td/text()')[0]
                    kailisheng16 = ohtml.xpath('//table[@id="datatb"]//tr[8]/td[6]//tr[2]/td[1]/text()')[0]
                    kailiping16 = ohtml.xpath('//table[@id="datatb"]//tr[8]/td[6]//tr[2]/td[2]/text()')[0]
                    kailifu16 = ohtml.xpath('//table[@id="datatb"]//tr[8]/td[6]//tr[2]/td[3]/text()')[0]
                    print(name16,oupeisheng16,oupeiping16,oupeifu16,gailvsheng16,gailvping16,gailvfu16,fanhuanlv16,kailisheng16,kailiping16,kailifu16)

                    gailvshengcha16 = str(round(float(str(gailvsheng15).replace('%',''))-float(str(gailvsheng16).replace('%','')),2))+'%'
                    gailvfucha16 = str(round(float(str(gailvfu15).replace('%', '')) - float(str(gailvfu16).replace('%', '')),2)) + '%'
                    fanhuanlvcha16 = str(round(float(str(fanhuanlv15).replace('%', '')) - float(str(fanhuanlv16).replace('%', '')),2)) + '%'

                    data.extend(['', name15, oupeisheng15,oupeisheng16, float(oupeisheng15)-float(oupeisheng16),oupeiping15,oupeiping16, oupeifu15,oupeifu16,float(oupeifu15)-float(oupeifu16), gailvsheng15,gailvsheng16,gailvshengcha16, gailvping15,gailvping16, gailvfu15,gailvfu16,gailvfucha16, fanhuanlv15,fanhuanlv16,fanhuanlvcha16, kailisheng15,kailisheng16,float(kailisheng15)-float(kailisheng16), kailiping15,kailiping16, kailifu15,kailifu16,float(kailifu15)-float(kailifu16)])
                else:
                    pass

                if ohtml.xpath('//table[@id="datatb"]//tr[9]/td[@class="tb_plgs"]/@title'):
                    # 赔率公司 9
                    name17 = ohtml.xpath('//table[@id="datatb"]//tr[9]/td[@class="tb_plgs"]/@title')[0]
                    oupeisheng17 = ohtml.xpath('//table[@id="datatb"]//tr[9]/td[3]//tr[1]/td[1]/text()')[0]
                    oupeiping17 = ohtml.xpath('//table[@id="datatb"]//tr[9]/td[3]//tr[1]/td[2]/text()')[0]
                    oupeifu17 = ohtml.xpath('//table[@id="datatb"]//tr[9]/td[3]//tr[1]/td[3]/text()')[0]
                    gailvsheng17 = ohtml.xpath('//table[@id="datatb"]//tr[9]/td[4]//tr[1]/td[1]/text()')[0]
                    gailvping17 = ohtml.xpath('//table[@id="datatb"]//tr[9]/td[4]//tr[1]/td[2]/text()')[0]
                    gailvfu17 = ohtml.xpath('//table[@id="datatb"]//tr[9]/td[4]//tr[1]/td[3]/text()')[0]
                    fanhuanlv17 = ohtml.xpath('//table[@id="datatb"]//tr[9]/td[5]//tr[1]/td/text()')[0]
                    kailisheng17 = ohtml.xpath('//table[@id="datatb"]//tr[9]/td[6]//tr[1]/td[1]/text()')[0]
                    kailiping17 = ohtml.xpath('//table[@id="datatb"]//tr[9]/td[6]//tr[1]/td[2]/text()')[0]
                    kailifu17 = ohtml.xpath('//table[@id="datatb"]//tr[9]/td[6]//tr[1]/td[3]/text()')[0]
                    print(name17,oupeisheng17,oupeiping17,oupeifu17,gailvsheng17,gailvping17,gailvfu17,fanhuanlv17,kailisheng17,kailiping17,kailifu17)

                    # 赔率公司 9
                    name18 = ohtml.xpath('//table[@id="datatb"]//tr[9]/td[@class="tb_plgs"]/@title')[0]
                    oupeisheng18 = ohtml.xpath('//table[@id="datatb"]//tr[9]/td[3]//tr[2]/td[1]/text()')[0]
                    oupeiping18 = ohtml.xpath('//table[@id="datatb"]//tr[9]/td[3]//tr[2]/td[2]/text()')[0]
                    oupeifu18 = ohtml.xpath('//table[@id="datatb"]//tr[9]/td[3]//tr[2]/td[3]/text()')[0]
                    gailvsheng18 = ohtml.xpath('//table[@id="datatb"]//tr[9]/td[4]//tr[2]/td[1]/text()')[0]
                    gailvping18 = ohtml.xpath('//table[@id="datatb"]//tr[9]/td[4]//tr[2]/td[2]/text()')[0]
                    gailvfu18 = ohtml.xpath('//table[@id="datatb"]//tr[9]/td[4]//tr[2]/td[3]/text()')[0]
                    fanhuanlv18 = ohtml.xpath('//table[@id="datatb"]//tr[9]/td[5]//tr[2]/td/text()')[0]
                    kailisheng18 = ohtml.xpath('//table[@id="datatb"]//tr[9]/td[6]//tr[2]/td[1]/text()')[0]
                    kailiping18 = ohtml.xpath('//table[@id="datatb"]//tr[9]/td[6]//tr[2]/td[2]/text()')[0]
                    kailifu18 = ohtml.xpath('//table[@id="datatb"]//tr[9]/td[6]//tr[2]/td[3]/text()')[0]
                    print(name18,oupeisheng18,oupeiping18,oupeifu18,gailvsheng18,gailvping18,gailvfu18,fanhuanlv18,kailisheng18,kailiping18,kailifu18)

                    gailvshengcha18 = str(round(float(str(gailvsheng17).replace('%',''))-float(str(gailvsheng18).replace('%','')),2))+'%'
                    gailvfucha18 = str(round(float(str(gailvfu17).replace('%', '')) - float(str(gailvfu18).replace('%', '')),2)) + '%'
                    fanhuanlvcha18 = str(round(float(str(fanhuanlv17).replace('%', '')) - float(str(fanhuanlv18).replace('%', '')),2)) + '%'

                    data.extend(['', name17, oupeisheng17,oupeisheng18, float(oupeisheng17)-float(oupeisheng18),oupeiping17,oupeiping18, oupeifu17,oupeifu18,float(oupeifu17)-float(oupeifu18), gailvsheng17,gailvsheng18,gailvshengcha18, gailvping17,gailvping18, gailvfu17,gailvfu18,gailvfucha18, fanhuanlv17,fanhuanlv18,fanhuanlvcha18, kailisheng17,kailisheng18,float(kailisheng17)-float(kailisheng18), kailiping17,kailiping18, kailifu17,kailifu18,float(kailifu17)-float(kailifu18)])
                else:
                    pass

                if ohtml.xpath('//table[@id="datatb"]//tr[10]/td[@class="tb_plgs"]/@title'):
                    # 赔率公司 10
                    name19 = ohtml.xpath('//table[@id="datatb"]//tr[10]/td[@class="tb_plgs"]/@title')[0]
                    oupeisheng19 = ohtml.xpath('//table[@id="datatb"]//tr[10]/td[3]//tr[1]/td[1]/text()')[0]
                    oupeiping19 = ohtml.xpath('//table[@id="datatb"]//tr[10]/td[3]//tr[1]/td[2]/text()')[0]
                    oupeifu19 = ohtml.xpath('//table[@id="datatb"]//tr[10]/td[3]//tr[1]/td[3]/text()')[0]
                    gailvsheng19 = ohtml.xpath('//table[@id="datatb"]//tr[10]/td[4]//tr[1]/td[1]/text()')[0]
                    gailvping19 = ohtml.xpath('//table[@id="datatb"]//tr[10]/td[4]//tr[1]/td[2]/text()')[0]
                    gailvfu19 = ohtml.xpath('//table[@id="datatb"]//tr[10]/td[4]//tr[1]/td[3]/text()')[0]
                    fanhuanlv19 = ohtml.xpath('//table[@id="datatb"]//tr[10]/td[5]//tr[1]/td/text()')[0]
                    kailisheng19 = ohtml.xpath('//table[@id="datatb"]//tr[10]/td[6]//tr[1]/td[1]/text()')[0]
                    kailiping19 = ohtml.xpath('//table[@id="datatb"]//tr[10]/td[6]//tr[1]/td[2]/text()')[0]
                    kailifu19 = ohtml.xpath('//table[@id="datatb"]//tr[10]/td[6]//tr[1]/td[3]/text()')[0]
                    print(name19,oupeisheng19,oupeiping19,oupeifu19,gailvsheng19,gailvping19,gailvfu19,fanhuanlv19,kailisheng19,kailiping19,kailifu19)

                    # 赔率公司 10
                    name20 = ohtml.xpath('//table[@id="datatb"]//tr[10]/td[@class="tb_plgs"]/@title')[0]
                    oupeisheng20 = ohtml.xpath('//table[@id="datatb"]//tr[10]/td[3]//tr[2]/td[1]/text()')[0]
                    oupeiping20 = ohtml.xpath('//table[@id="datatb"]//tr[10]/td[3]//tr[2]/td[2]/text()')[0]
                    oupeifu20 = ohtml.xpath('//table[@id="datatb"]//tr[10]/td[3]//tr[2]/td[3]/text()')[0]
                    gailvsheng20 = ohtml.xpath('//table[@id="datatb"]//tr[10]/td[4]//tr[2]/td[1]/text()')[0]
                    gailvping20 = ohtml.xpath('//table[@id="datatb"]//tr[10]/td[4]//tr[2]/td[2]/text()')[0]
                    gailvfu20 = ohtml.xpath('//table[@id="datatb"]//tr[10]/td[4]//tr[2]/td[3]/text()')[0]
                    fanhuanlv20 = ohtml.xpath('//table[@id="datatb"]//tr[10]/td[5]//tr[2]/td/text()')[0]
                    kailisheng20 = ohtml.xpath('//table[@id="datatb"]//tr[10]/td[6]//tr[2]/td[1]/text()')[0]
                    kailiping20 = ohtml.xpath('//table[@id="datatb"]//tr[10]/td[6]//tr[2]/td[2]/text()')[0]
                    kailifu20 = ohtml.xpath('//table[@id="datatb"]//tr[10]/td[6]//tr[2]/td[3]/text()')[0]
                    print(name20,oupeisheng20,oupeiping20,oupeifu20,gailvsheng20,gailvping20,gailvfu20,fanhuanlv20,kailisheng20,kailiping20,kailifu20)

                    gailvshengcha20 = str(round(float(str(gailvsheng19).replace('%', '')) - float(str(gailvsheng20).replace('%', '')),2)) + '%'
                    gailvfucha20 = str(round(float(str(gailvfu19).replace('%', '')) - float(str(gailvfu20).replace('%', '')),2)) + '%'
                    fanhuanlvcha20 = str(round(float(str(fanhuanlv19).replace('%', '')) - float(str(fanhuanlv20).replace('%', '')),2)) + '%'

                    data.extend(['', name19, oupeisheng19,oupeisheng20, float(oupeisheng19)-float(oupeisheng20),oupeiping19,oupeiping20, oupeifu19,oupeifu20,float(oupeifu19)-float(oupeifu20), gailvsheng19,gailvsheng20,gailvshengcha20, gailvping19,gailvping20, gailvfu19,gailvfu20,gailvfucha20, fanhuanlv19,fanhuanlv20,fanhuanlvcha20, kailisheng19,kailisheng20,float(kailisheng19)-float(kailisheng20), kailiping19,kailiping20, kailifu19,kailifu20,float(kailifu19)-float(kailifu20)])


                # 存储
                info1 = ['', '', '', '', tname2, peilv2, gailv2, beidan2, bifa2, chengjiaojia2, chengjiaoliang2, zhuangjia2, bifazhishu2, lengre2, yingkui2,]
                info2 = ['', '', '', '', tname3, peilv3, gailv3, beidan3, bifa3, chengjiaojia3, chengjiaoliang3, zhuangjia3, bifazhishu3, lengre3, yingkui3]

                if not os.path.exists(f'{sid}-{start_round}-{end_round}.csv'):
                    head = ['联赛id', '轮数', '百家欧赔url', '', '球队名字 (百家欧赔)', '赔率 (百家欧赔)', '概率 (百家欧赔)', '北单(-1) (交易比例)', '必发 (交易比例)', '成交价 (必发成交)', '成交量 (必发成交)', '庄家盈亏 (必发成交)', '必发指数 (指数分析)', '冷热指数 (指数分析)', '盈亏指数 (指数分析)', '对局方比分',
                            '', '赔率公司定制 (定制一)', '胜 (及时欧赔)', '胜 (及时欧赔)', '差值', '平 (及时欧赔)', '平 (及时欧赔)', '负 (及时欧赔)', '负 (及时欧赔)', '差值', '胜 (及时概率)', '胜 (及时概率)', '差值', '平 (及时概率)', '平 (及时概率)', '负 (及时概率)', '负 (及时概率)', '差值', '值 (返还率)', '值 (返还率)', '返还率差' , '胜 (凯利指数)', '胜 (凯利指数)', '差值', '平 (凯利指数)', '平 (凯利指数)', '负 (凯利指数)', '负 (凯利指数)', '差值',
                            '', '赔率公司定制 (定制一)', '胜 (及时欧赔)', '胜 (及时欧赔)', '差值', '平 (及时欧赔)', '平 (及时欧赔)', '负 (及时欧赔)', '负 (及时欧赔)', '差值', '胜 (及时概率)', '胜 (及时概率)', '差值', '平 (及时概率)', '平 (及时概率)', '负 (及时概率)', '负 (及时概率)', '差值', '值 (返还率)', '值 (返还率)', '返还率差' , '胜 (凯利指数)', '胜 (凯利指数)', '差值', '平 (凯利指数)', '平 (凯利指数)', '负 (凯利指数)', '负 (凯利指数)', '差值',
                            '', '赔率公司定制 (定制一)', '胜 (及时欧赔)', '胜 (及时欧赔)', '差值', '平 (及时欧赔)', '平 (及时欧赔)', '负 (及时欧赔)', '负 (及时欧赔)', '差值', '胜 (及时概率)', '胜 (及时概率)', '差值', '平 (及时概率)', '平 (及时概率)', '负 (及时概率)', '负 (及时概率)', '差值', '值 (返还率)', '值 (返还率)', '返还率差' , '胜 (凯利指数)', '胜 (凯利指数)', '差值', '平 (凯利指数)', '平 (凯利指数)', '负 (凯利指数)', '负 (凯利指数)', '差值',
                            '', '赔率公司定制 (定制一)', '胜 (及时欧赔)', '胜 (及时欧赔)', '差值', '平 (及时欧赔)', '平 (及时欧赔)', '负 (及时欧赔)', '负 (及时欧赔)', '差值', '胜 (及时概率)', '胜 (及时概率)', '差值', '平 (及时概率)', '平 (及时概率)', '负 (及时概率)', '负 (及时概率)', '差值', '值 (返还率)', '值 (返还率)', '返还率差' , '胜 (凯利指数)', '胜 (凯利指数)', '差值', '平 (凯利指数)', '平 (凯利指数)', '负 (凯利指数)', '负 (凯利指数)', '差值',
                            '', '赔率公司定制 (定制一)', '胜 (及时欧赔)', '胜 (及时欧赔)', '差值', '平 (及时欧赔)', '平 (及时欧赔)', '负 (及时欧赔)', '负 (及时欧赔)', '差值', '胜 (及时概率)', '胜 (及时概率)', '差值', '平 (及时概率)', '平 (及时概率)', '负 (及时概率)', '负 (及时概率)', '差值', '值 (返还率)', '值 (返还率)', '返还率差' , '胜 (凯利指数)', '胜 (凯利指数)', '差值', '平 (凯利指数)', '平 (凯利指数)', '负 (凯利指数)', '负 (凯利指数)', '差值',
                            '', '赔率公司定制 (定制一)', '胜 (及时欧赔)', '胜 (及时欧赔)', '差值', '平 (及时欧赔)', '平 (及时欧赔)', '负 (及时欧赔)', '负 (及时欧赔)', '差值', '胜 (及时概率)', '胜 (及时概率)', '差值', '平 (及时概率)', '平 (及时概率)', '负 (及时概率)', '负 (及时概率)', '差值', '值 (返还率)', '值 (返还率)', '返还率差' , '胜 (凯利指数)', '胜 (凯利指数)', '差值', '平 (凯利指数)', '平 (凯利指数)', '负 (凯利指数)', '负 (凯利指数)', '差值',
                            '', '赔率公司定制 (定制一)', '胜 (及时欧赔)', '胜 (及时欧赔)', '差值', '平 (及时欧赔)', '平 (及时欧赔)', '负 (及时欧赔)', '负 (及时欧赔)', '差值', '胜 (及时概率)', '胜 (及时概率)', '差值', '平 (及时概率)', '平 (及时概率)', '负 (及时概率)', '负 (及时概率)', '差值', '值 (返还率)', '值 (返还率)', '返还率差' , '胜 (凯利指数)', '胜 (凯利指数)', '差值', '平 (凯利指数)', '平 (凯利指数)', '负 (凯利指数)', '负 (凯利指数)', '差值',
                            '', '赔率公司定制 (定制一)', '胜 (及时欧赔)', '胜 (及时欧赔)', '差值', '平 (及时欧赔)', '平 (及时欧赔)', '负 (及时欧赔)', '负 (及时欧赔)', '差值', '胜 (及时概率)', '胜 (及时概率)', '差值', '平 (及时概率)', '平 (及时概率)', '负 (及时概率)', '负 (及时概率)', '差值', '值 (返还率)', '值 (返还率)', '返还率差' , '胜 (凯利指数)', '胜 (凯利指数)', '差值', '平 (凯利指数)', '平 (凯利指数)', '负 (凯利指数)', '负 (凯利指数)', '差值',
                            '', '赔率公司定制 (定制一)', '胜 (及时欧赔)', '胜 (及时欧赔)', '差值', '平 (及时欧赔)', '平 (及时欧赔)', '负 (及时欧赔)', '负 (及时欧赔)', '差值', '胜 (及时概率)', '胜 (及时概率)', '差值', '平 (及时概率)', '平 (及时概率)', '负 (及时概率)', '负 (及时概率)', '差值', '值 (返还率)', '值 (返还率)', '返还率差' , '胜 (凯利指数)', '胜 (凯利指数)', '差值', '平 (凯利指数)', '平 (凯利指数)', '负 (凯利指数)', '负 (凯利指数)', '差值',
                            '', '赔率公司定制 (定制一)', '胜 (及时欧赔)', '胜 (及时欧赔)', '差值', '平 (及时欧赔)', '平 (及时欧赔)', '负 (及时欧赔)', '负 (及时欧赔)', '差值', '胜 (及时概率)', '胜 (及时概率)', '差值', '平 (及时概率)', '平 (及时概率)', '负 (及时概率)', '负 (及时概率)', '差值', '值 (返还率)', '值 (返还率)', '返还率差' , '胜 (凯利指数)', '胜 (凯利指数)', '差值', '平 (凯利指数)', '平 (凯利指数)', '负 (凯利指数)', '负 (凯利指数)', '差值',
                            ]
                    csvFile = open(f'{sid}-{start_round}-{end_round}.csv', 'a', newline='', encoding='utf-8-sig')
                    writer = csv.writer(csvFile)
                    writer.writerow(head)
                    csvFile.close()
                else:
                    csvFile = open(f'{sid}-{start_round}-{end_round}.csv', 'a+', newline='', encoding='utf-8-sig')
                    writer = csv.writer(csvFile)
                    writer.writerows([ data, info1, info2, []])
                    csvFile.close()


if __name__ == '__main__':
    ln = Match()
    year = str(input('请输入联赛ID:'))
    start_round , end_round = map(int, input('请输入轮数(多少轮到多少轮以空格分开):').split())
    TM = int(input('请设置爬取速度/s:'))
    ln.match_data(year, start_round, end_round, TM)