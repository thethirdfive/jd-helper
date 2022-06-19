from ast import IsNot
from operator import is_not
from queue import Empty
import pandas as pd


def HS_goods_code():
    '''产品编码整理
    '''
    df1 = pd.read_excel(io="./data/pop店售卖商品简码ALL.xlsx")
    df2 = pd.read_excel(
        io="./data/已备案信息查询_20220619152156.xls", sheet_name=[0, 1])

    # print(df2[1].loc[1])
    df_for_check = df1[['商品名称(简称)', '套装规格', '事业部商品编码', '商家商品编码（SKU）']]
    df2_0 = df2[0][['SKU', 'UPC', '商品名称（中文）', '商品货号']]
    df2_1 = df2[1][['SKU', 'UPC', '商品名称（中文）', '商品货号']]
    df_all = pd.concat([df2_0, df2_1])
    # print(df_all)
    new_df = []
    for index, row in df_for_check.iterrows():
        dt_temp = []
        for r in row:
            dt_temp.append(r)
        temp = df_all.loc[df_all['SKU'] == str(row[3])]  # 可能存在找不到的值！！！
        if len(temp) != 0:
            for t in temp.iloc[0, :]:
                dt_temp.append(t)
        new_df.append(dt_temp)

    df_reult = pd.DataFrame(new_df, columns=[
                            '商品名称(简称)', '套装规格', '事业部商品编码', '商家商品编码（SKU）', 'SKU', 'UPC', '商品名称（中文）', '商品货号'])
    # 保存到本地excel
    df_reult.to_excel("./data/鹤松商品编码.xlsx", index=False)
    print("\n\t*Processing completed to excel*\n")


def format_kucun():
    '''库存数据格式化
    '''
    df1 = pd.read_excel(io="./data/pop店售卖商品简码ALL.xlsx")
    df2 = pd.read_csv(
        "./data/stock-report-shopStock-reporttsu_liyushu_1655621588234.csv", encoding='gbk')

    # print(df2[1].loc[1])
    df_for_check = df1[['商品名称(简称)', '套装规格', '事业部商品编码', '商家商品编码（SKU）']]
    # print(df_for_check)
    df_all = df2[['商家商品编码', '库存数量']]
    # print(df_all)
    new_df = []
    for index, row in df_for_check.iterrows():
        dt_temp = []
        for r in row:
            dt_temp.append(r)
        temp = df_all.loc[df_all['商家商品编码'] == row[3]]  # 可能存在找不到的值！！！注意数据类型

        if len(temp) != 0:
            for t in temp.iloc[0, :]:
                dt_temp.append(t)
        new_df.append(dt_temp)

    df_reult = pd.DataFrame(new_df, columns=[
                            '商品名称(简称)', '套装规格', '事业部商品编码', '商家商品编码（SKU）', '商家商品编码', '库存数量'])
    df_reult = df_reult[['商品名称(简称)', '套装规格', '库存数量',
                         '事业部商品编码', '商家商品编码（SKU）', '商家商品编码']]
    
    df_reult = df_reult.sort_values(by=['库存数量'], ascending=True)
    
    # 保存到本地excel
    df_reult.to_excel("./data/商品库存查询.xlsx", index=False)
    print("\n\t*Processing completed to excel*\n")


if __name__ == '__main__':
    format_kucun()
