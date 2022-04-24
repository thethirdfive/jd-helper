# -*- coding=utf-8 -*-
from time import sleep
import requests
import sys
import config
import AES_SECRET
import zipfile
import pandas as pd
from bs4 import BeautifulSoup
import AES_SECRET

service = None  # 客服
taskid = None  # 导出表格文件id
filename = []  # 导出的文件名称
passwd = None  # 文件密码
kf_name = {
    'hesong-sansan': '丁沪婉',
    'hesong-leixuan': '雷轩',
    '鹤松医药011': '季雅囡',
    '鹤松医药008': '兜底组008',
    '鹤松009': '兜底组009',
    '闻毓': '闻毓',
    'tsurumatsu': 'tsurumatsu'
}
# 客服值班表
kf_zbb = {
    '2022-04-22': '季雅囡',
    '2022-04-23': '雷轩',
    '2022-04-24': '丁沪婉',
    '2022-04-25': '季雅囡',
    '2022-04-26': '雷轩',
    '2022-04-27': '丁沪婉',
    '2022-04-28': '季雅囡',
    '2022-04-29': '雷轩',
    '2022-04-30': '丁沪婉'
}
kfs = []  # 客服人员
sale = {
    '销售额': 0,
    '订单总数': 0,
    '取消订单数': 0
}  # 销售情况
week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]


def waiterSession(pageSize, startTime, endTime):
    '''客服管家->咚咚查询->客户咨询查询
    https://kf.jd.com/waiterSession/queryList.action?page=1&pageSize=15&startTime=2022-04-21&endTime=2022-04-21
    '''
    url = 'https://kf.jd.com/waiterSession/queryList.action'
    headers = {
        'Connection': config.Connection,
        'Cookie': config.cookie,
        'User-Agent': config.ua,
        'sec-ch-ua': config.sec_ch_ua,
        'sec-ch-ua-mobile': config.sec_ch_ua_mobile,
        'Sec-Fetch-Site': config.Sec_Fetch_Site,
        'Sec-Fetch-Mode': config.sec_ch_ua_mobile,
        'Sec-Fetch-Dest': config.Sec_Fetch_Dest,
        'Host': config.Host,
        'Accept-Encoding': config.AcceptEncoding,
        'Accept-Language': config.AcceptLanguage,
        'Accept': config.Accept
    }
    payload = {
        'page': 1,
        'pageSize': pageSize,
        'startTime': startTime,
        'endTime': endTime,
    }
    r = requests.get(url, params=payload, headers=headers)
    if r.status_code == 200:
        r.encoding = 'utf-8'
        res = r.json()
        df = pd.json_normalize(res['waiterSessionList'])
        #df = pd.json_normalize(res['waiterSessionList']).loc[:,['service','sessionTypeDesc','customerMsgNum','waiterMsgNum']]
        kfsum = df['service'].value_counts()
        for kf in kfsum.index:
            kfs.append(kf)
            print("{}接待{}人".format(kf_name[kf], kfsum[kf]))


def orderDetail(pageSize, startTime, endTime):
    '''客服管家->咚咚查询->促成订单查询
    https://kf.jd.com/orderDetail/queryList.action?page=1&pageSize=15&startTime=2022-4-21&endTime=2022-4-21
    '''
    url = 'https://kf.jd.com/orderDetail/queryList.action'
    headers = {
        'Connection': config.Connection,
        'Cookie': config.cookie,
        'User-Agent': config.ua,
        'sec-ch-ua': config.sec_ch_ua,
        'sec-ch-ua-mobile': config.sec_ch_ua_mobile,
        'Sec-Fetch-Site': config.Sec_Fetch_Site,
        'Sec-Fetch-Mode': config.sec_ch_ua_mobile,
        'Sec-Fetch-Dest': config.Sec_Fetch_Dest,
        'Host': config.Host,
        'Accept-Encoding': config.AcceptEncoding,
        'Accept-Language': config.AcceptLanguage,
        'Accept': config.Accept
    }
    payload = {
        'page': 1,
        'pageSize': pageSize,
        'startTime': startTime,
        'endTime': endTime,

    }
    r = requests.get(url, params=payload, headers=headers)
    if r.status_code == 200:
        r.encoding = 'utf-8'
        res = r.json()
        if(res['totalRecordNum'] != 0):
            df = pd.json_normalize(res['orderDetailList'])
            kfsum = df['service'].value_counts()
            for kf in kfsum.index:
                print("{}促成{}单".format(kf_name[kf], kfsum[kf]))


def workload(startTime, endTime, servicePin):
    '''客服管家->客服个人工作数据->工作量（前日一天）
    https://kf.jd.com/waiterPerson/workload/queryList?page=1&pageSize=15&startTime=2022-04-21&endTime=2022-04-21&transferType=1&servicePin=hesong-sansan&type=1
    '''
    url = 'https://kf.jd.com/waiterPerson/workload/queryList'
    headers = {
        'Connection': config.Connection,
        'Cookie': config.cookie,
        'User-Agent': config.ua,
        'sec-ch-ua': config.sec_ch_ua,
        'sec-ch-ua-mobile': config.sec_ch_ua_mobile,
        'Sec-Fetch-Site': config.Sec_Fetch_Site,
        'Sec-Fetch-Mode': config.sec_ch_ua_mobile,
        'Sec-Fetch-Dest': config.Sec_Fetch_Dest,
        'Host': config.Host,
        'Accept-Encoding': config.AcceptEncoding,
        'Accept-Language': config.AcceptLanguage,
        'Accept': config.Accept
    }
    payload = {
        'page': 1,
        'pageSize': 15,
        'startTime': startTime,
        'endTime': endTime,
        'servicePin': servicePin,
        'type': 1,
        'transferType': 1
    }
    r = requests.get(url, params=payload, headers=headers)
    if r.status_code == 200:
        r.encoding = 'utf-8'
        res = r.json()
        print("{}在线时长：{}小时".format(
            kf_name[servicePin], res['totalDetail']['onlineTime']))


def doSave(startDate, endDate):
    '''创建导出任务 /exportCenter/doSave.action
    https://export.shop.jd.com/exportCenter/doSave.action
    '''
    url = 'https://export.shop.jd.com/exportCenter/doSave.action'
    headers = {
        'Connection': config.Connection,
        'Cookie': config.cookie,
        'User-Agent': config.ua,
        'sec-ch-ua': config.sec_ch_ua,
        'sec-ch-ua-mobile': config.sec_ch_ua_mobile,
        'Sec-Fetch-Site': config.Sec_Fetch_Site_export,
        'Sec-Fetch-Mode': config.sec_ch_ua_mobile,
        'Sec-Fetch-Dest': config.Sec_Fetch_Dest,
        'Host': config.Host_export,
        'Accept-Encoding': config.AcceptEncoding,
        'Accept-Language': config.AcceptLanguage,
        'Accept': config.Accept_export,
        'Content-Type': config.ContentType_export
    }
    taskDataParam = '{{"startDate":"{}","endDate":"{}","exportTaskType":0}}'.format(
        startDate, endDate)
    payload = {
        "exportType": 0,
        "taskDataParam": taskDataParam
    }
    r = requests.post(url=url, data=payload, headers=headers)
    if r.status_code == 200:
        r.encoding = 'utf-8'
        res = r.json()
        if(res['success']):
            print("创建导出任务完成！")


def list():
    '''导出列表->获取最新的导出文件ID
    https://export.shop.jd.com/exportCenter/list
    '''
    url = 'https://export.shop.jd.com/exportCenter/list'
    headers = {
        'Connection': config.Connection,
        'Cookie': config.cookie,
        'User-Agent': config.ua,
        'sec-ch-ua': config.sec_ch_ua,
        'sec-ch-ua-mobile': config.sec_ch_ua_mobile,
        'Sec-Fetch-Site': config.Sec_Fetch_Site_export,
        'Sec-Fetch-Mode': config.sec_ch_ua_mobile,
        'Sec-Fetch-Dest': config.Sec_Fetch_Dest,
        'Host': config.Host_export,
        'Accept-Encoding': config.AcceptEncoding,
        'Accept-Language': config.AcceptLanguage,
        'Accept': config.Accept_export,
        'Content-Type': config.ContentType_export
    }
    payload = {
        "page": 1,
        "exportTaskType": 0
    }
    r = requests.post(url=url, data=payload, headers=headers)
    if r.status_code == 200:
        r.encoding = 'utf-8'
        res = r.json()
        global taskid
        taskid = res['pageModel']['itemList'][0]['id']
        print("获取最新的导出文件ID:{}".format(taskid))


def export(id):
    '''下载导出文件 exportCenter/export.action
    https://export.shop.jd.com/exportCenter/export.action?taskId=40823102
    '''
    url = 'https://export.shop.jd.com/exportCenter/export.action'
    headers = {
        'Connection': config.Connection,
        'Cookie': config.cookie,
        'User-Agent': config.ua,
        'sec-ch-ua': config.sec_ch_ua,
        'sec-ch-ua-mobile': config.sec_ch_ua_mobile,
        'Sec-Fetch-Site': config.Sec_Fetch_Site_export,
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Host': config.Host_export,
        'Accept-Encoding': config.AcceptEncoding,
        'Accept-Language': config.AcceptLanguage,
        # 'Upgrade-Insecure-Requests': 1,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    payload = {
        "taskId": id
    }
    r = requests.get(url=url, params=payload, headers=headers)
    if r.status_code == 200:
        with open('downloads/{}.zip'.format(id), 'wb') as filedownload:
            filedownload.write(r.content)
            filedownload.close()
        passwd = input("请输入收到的解压密码:")
        try:
            zfile = zipfile.ZipFile('downloads/{}.zip'.format(id), 'r')
            global filename
            filename = zfile.namelist()
            print(filename)
            zfile.extractall('downloads/{}/'.format(id),
                             pwd=passwd.encode('utf-8'))
            print("导出表格文件完成")

        except:
            print("解压密码错误！")


def sendPassword(id):
    '''发送短信验证码
    https://export.shop.jd.com/exportCenter/sendPassword.action
    '''
    url = 'https://export.shop.jd.com/exportCenter/sendPassword.action'
    headers = {
        'Connection': config.Connection,
        'Cookie': config.cookie,
        'User-Agent': config.ua,
        'sec-ch-ua': config.sec_ch_ua,
        'sec-ch-ua-mobile': config.sec_ch_ua_mobile,
        'Sec-Fetch-Site': config.Sec_Fetch_Site_export,
        'Sec-Fetch-Mode': config.sec_ch_ua_mobile,
        'Sec-Fetch-Dest': config.Sec_Fetch_Dest,
        'Host': config.Host_export,
        'Accept-Encoding': config.AcceptEncoding,
        'Accept-Language': config.AcceptLanguage,
        'Accept': config.Accept_export,
        'Content-Type': config.ContentType_export
    }
    payload = {
        "taskId": id,
        "exportTaskType": 0
    }

    r = requests.post(url=url, data=payload, headers=headers)
    if r.status_code == 200:
        r.encoding = 'utf-8'
        res = r.json()
        if(res['success']):
            print("发送验证码完成，返回:{}".format(res['data']))


def getOrderDetail(orderId):
    '''获取订单详情页的accesskey
    https://neworder.shop.jd.com/order/orderDetail?orderId=242825972327
    '''
    url = 'https://neworder.shop.jd.com/order/orderDetail'
    headers = {
        'Connection': config.Connection,
        'Cookie': config.cookie,
        'User-Agent': config.ua,
        'sec-ch-ua': config.sec_ch_ua,
        'sec-ch-ua-mobile': config.sec_ch_ua_mobile,
        'Sec-Fetch-Site': config.Sec_Fetch_Site_export,
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Host': 'neworder.shop.jd.com',
        'Accept-Encoding': config.AcceptEncoding,
        'Accept-Language': config.AcceptLanguage,
        # 'Upgrade-Insecure-Requests': 1,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    payload = {
        "orderId": orderId
    }
    r = requests.get(url=url, params=payload, headers=headers)
    if r.status_code == 200:
        try:
            soup = BeautifulSoup(r.content, 'lxml')
            viewOrderPhone = soup.find(id="viewOrderPhone")
            return viewOrderPhone.attrs['accesskey'][0]
        except:
            print("获取accesskey错误!")
            return ""
    else:
        return ""


def phoneSensltiveInfo(orderId, accessKey):
    '''查询手机号码
    https://neworder.shop.jd.com/order/json/phoneSensltiveInfo
    '''
    url = 'https://neworder.shop.jd.com/order/json/phoneSensltiveInfo'
    headers = {
        'Connection': config.Connection,
        'Cookie': config.cookie,
        'User-Agent': config.ua,
        'sec-ch-ua': config.sec_ch_ua,
        'sec-ch-ua-mobile': config.sec_ch_ua_mobile,
        'Sec-Fetch-Site': config.Sec_Fetch_Site_export,
        'Sec-Fetch-Mode': config.sec_ch_ua_mobile,
        'Sec-Fetch-Dest': config.Sec_Fetch_Dest,
        'Host': 'neworder.shop.jd.com',
        'Accept-Encoding': config.AcceptEncoding,
        'Accept-Language': config.AcceptLanguage,
        'Accept': config.Accept_export,
        'Content-Type': config.ContentType_export
    }
    payload = {
        'orderId': orderId,
        'emergencyContact': '',
        'accessKey': accessKey,
        'accessType': 0,
        'token': '',
        "state": 'success'
    }
    r = requests.post(url=url, data=payload, headers=headers)
    if r.status_code == 200:
        try:
            r.encoding = 'utf-8'
            res = r.json()
            mobile = res['model']['mobile']
            aes_secret = AES_SECRET.AES_ENCRYPT()
            return aes_secret.decrypt(mobile).decode()
        except:
            print("获取手机号码错误！")
            return ""
    else:
        return ""


#########################################################

def run_kefu_tj():
    '''每天统计客服工作情况

    '''
    waiterSession(100, config.yesterday, config.yesterday)
    sleep(config.duration)
    orderDetail(100, config.yesterday, config.yesterday)
    sleep(config.duration)
    for kfpin in kfs:
        workload(config.yesterday, config.yesterday, kfpin)
        sleep(config.duration)

    print("今日[{}]勤務中:{}, Doryoku!\n\n".format(
        week_list[config.today.weekday()], kf_zbb[str(config.today)]))


def run_dingdan_tj():
    '''每天统计销售情况并获取订单客户手机号码
    '''
    doSave("{}{}".format(config.yesterday, " 00:00:00"),
           "{}{}".format(config.yesterday, " 23:59:59"))
    sleep(config.duration)
    list()
    sleep(config.duration)
    sendPassword(taskid)
    sleep(config.duration)
    export(taskid)
    sleep(config.duration) # 等待文件缓冲
    df = pd.read_csv('./downloads/{}/{}'.format(taskid,
                     filename[0]), encoding='gbk')
    sale['销售额'] = int(df['京东价'].sum())
    sale['订单总数'] = df.shape[0]
    for index, row in df.iterrows():
        if('删除' in row['订单状态']):
            sale['取消订单数'] = sale['取消订单数'] + 1
        print('订单号:', row['订单号'])
        accesskey = getOrderDetail(row['订单号'])
        print('accesskey:', accesskey)
        sleep(config.duration)
        phoneNumber = phoneSensltiveInfo(row['订单号'], accesskey)
        print('phoneNumber:', phoneNumber)
        sleep(config.duration)
        df.loc[index, '联系电话'] = phoneNumber  # 更新手机号码
    df.to_excel('E:/客服销售表/temp/{}_{}值班客服销售表.xlsx'.format(str(config.yesterday), kf_zbb[str(config.yesterday)]), columns=[
                '订单号', '商品ID', '商品名称', '订购数量', '支付方式', '下单时间', '京东价', '订单金额', '结算金额', '余额支付', '应付金额', '订单状态', '订单类型', '下单帐号', '客户姓名', '客户地址', '联系电话', '订单备注'])
    print("\n\n\n昨日[{}]".format(str(config.yesterday)))
    print('销售额:{}元 订单总数:{} 取消订单:{}'.format(
        sale['销售额'], sale['订单总数'], sale['取消订单数']))


if __name__ == '__main__':
    run_dingdan_tj()
    run_kefu_tj()
