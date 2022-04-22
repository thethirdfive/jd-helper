import requests
import sys
import config
import json
import os,zipfile,io


def waiterSession(pageSize,startTime,endTime):
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
        with open("downloads/waiterSession.json", 'w',encoding='utf-8') as json_obj:
            json.dump(res, json_obj, ensure_ascii=False)
            json_obj.close()
        return

def orderDetail(pageSize,startTime,endTime):
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
        with open("downloads/orderDetail.json", 'w',encoding='utf-8') as json_obj:
            json.dump(res, json_obj, ensure_ascii=False)
            json_obj.close()
        return

def workload(startTime,endTime,servicePin):
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
        'servicePin':servicePin,
        'type': 1,
        'transferType': 1
    }
    r = requests.get(url, params=payload, headers=headers)
    if r.status_code == 200:
        r.encoding = 'utf-8'
        res = r.json()
        with open("downloads/workload.json", 'w',encoding='utf-8') as json_obj:
            json.dump(res, json_obj, ensure_ascii=False)
            json_obj.close()
        return

def doSave(startDate,endDate):
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
    taskDataParam = '{{"startDate":"{}","endDate":"{}","exportTaskType":0}}'.format(startDate,endDate)
    #print(taskDataParam)
    payload = {
        "exportType": 0,
        "taskDataParam": taskDataParam
        #'taskDataParam': '{"startDate":"2022-04-21 00:00:00","endDate":"2022-04-21 23:59:00","exportTaskType":0}'
    }

    r = requests.post(url=url, data=payload, headers=headers)
    
    if r.status_code == 200:
        r.encoding = 'utf-8'
        res = r.json()
        with open("downloads/doSave.json", 'w',encoding='utf-8') as json_obj:
            json.dump(res, json_obj, ensure_ascii=False)
            json_obj.close()
        return

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
        with open("downloads/list_{}.json".format(config.today_time_title), 'w',encoding='utf-8') as json_obj:
            json.dump(res, json_obj, ensure_ascii=False)
            json_obj.close()
        print(res['pageModel']['itemList'][0]['id'])
        return res['pageModel']['itemList'][0]['id']

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
        #'Upgrade-Insecure-Requests': 1,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    payload = {
        "taskId": id
    }
    r = requests.get(url=url, params=payload ,headers=headers)
    print(r)
    if r.status_code == 200:
        with open('downloads/{}.zip'.format(id),'wb') as filedownload:
            filedownload.write(r.content)
            filedownload.close()
        zfile = zipfile.ZipFile('downloads/{}.zip'.format(id),'r')
        zfile.extractall('downloads/{}/'.format(id),pwd='3xMqPE'.encode('utf-8'))

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
        with open("downloads/sendPassword.json", 'w',encoding='utf-8') as json_obj:
            json.dump(res, json_obj, ensure_ascii=False)
            json_obj.close()
        print(res)

if __name__ == '__main__':
    # 给在服务器后台执行使用
    if len(sys.argv) > 1:
        run_type = int(sys.argv[1])
        if run_type in [1, 2, 3]:
            config.run_type = run_type
    
    if not os.path.exists("downloads/waiterSession.json"):
        waiterSession(15,'2022-04-21','2022-04-21')
    if not os.path.exists("downloads/orderDetail.json"):
        orderDetail(15,'2022-04-21','2022-04-21')
    if not os.path.exists("downloads/workload.json"):
        workload('2022-04-21','2022-04-21','hesong-sansan')

    if not os.path.exists("downloads/doSave.json"):
        doSave("2022-04-21 00:00:00","2022-04-21 23:59:59")

    id = list()
    print(id)
    #export(str(id))
    #sendPassword("40828666")

