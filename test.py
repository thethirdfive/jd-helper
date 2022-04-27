import pandas as pd
import config
import pyperclip


kf_name = {
    'hesong-sansan': '丁沪婉',
    'hesong-leixuan': '雷轩',
    '鹤松医药011': '季雅囡',
    '鹤松医药008': '兜底组008',
    '鹤松009': '兜底组009',
    '闻毓': '闻毓',
    'tsurumatsu': 'tsurumatsu'
}
kf_sum_jd ={
    'hesong-sansan': 0,
    'hesong-leixuan': 15,
    '鹤松医药011': 0,
    '鹤松医药008': 3,
    '鹤松009': 0,
    '闻毓': 3,
    'tsurumatsu': 0
}
kf_sum_cc ={
    'hesong-sansan': 0,
    'hesong-leixuan': 2,
    '鹤松医药011': 0,
    '鹤松医药008': 1,
    '鹤松009': 0,
    '闻毓': 0,
    'tsurumatsu': 0
}
kfs = ['hesong-leixuan','鹤松医药008','闻毓']
sum_jd = 0# 接待总数
sum_cc= 0# 促成总数
prt_str_jd = ''# 接待
prt_str_cc = ''# 促成
for kf in kfs:
    prt_str_jd = prt_str_jd + ', {}接待{}位'.format(kf_name[kf], kf_sum_jd[kf])
    if(kf_sum_cc[kf] != 0):
        prt_str_cc = prt_str_cc + ', {}接待{}位'.format(kf_name[kf], kf_sum_cc[kf])
    sum_jd = sum_jd + kf_sum_jd[kf]
    sum_cc = sum_cc + kf_sum_cc[kf]
sum_dd = 23
text = "[{}]共接待{}位{}; 共下单{}位{},{}位未咨询".format(str(config.yesterday), sum_jd, prt_str_jd, sum_dd, prt_str_cc, (sum_dd - sum_cc))
pyperclip.copy(text)
print("\n\n\n{}\n\n\n".format(text))