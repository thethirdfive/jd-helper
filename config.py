import time
import datetime

cookie = ''
duration = 3  # 执行间隔时间秒
run_type = 1  # 类型
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

today_date = time.strftime("%Y-%m-%d", time.localtime())
today_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
today_time_title = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
AcceptEncoding = 'gzip, deflate, br'
AcceptLanguage = 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en;q=0.7,en-US;q=0.6'
Referer = 'https://xi.jd.com/customerassistant/filterCustomer.html?menu=ddQuery&content=waiterSession'
sec_ch_ua = '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"'
sec_ch_ua_mobile = '?0'
sec_ch_ua_platform = '"Windows"'
Sec_Fetch_Dest = 'empty'
Sec_Fetch_Mode = 'cors'
Sec_Fetch_Site = 'same-site'
Host = 'kf.jd.com'
Accept = '*/*'
Connection = 'keep-alive'

Host_export = 'export.shop.jd.com'
Accept_export = 'application/json, text/plain, */*'
ContentType_export = 'application/x-www-form-urlencoded;charset=UTF-8'
Sec_Fetch_Site_export = 'same-origin'
