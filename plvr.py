# 匯入套件
import pandas as pd


# 匯入csv
df_a = pd.read_csv('a_lvr_land_a.csv')
df_b = pd.read_csv('b_lvr_land_a.csv')
df_e = pd.read_csv('e_lvr_land_a.csv')
df_f = pd.read_csv('f_lvr_land_a.csv')
df_h = pd.read_csv('h_lvr_land_a.csv')

# 刪除第一行
df_a=df_a.drop([0])
df_b=df_b.drop([0])
df_e=df_e.drop([0])
df_f=df_f.drop([0])
df_h=df_h.drop([0])

# 合併成一個dataframe
df_all=pd.concat([df_a,df_b,df_e,df_f,df_h],axis=0)
df_all.reset_index(inplace=True, drop=True)

# 選出要篩選的'主要用途',"建物型態","總樓層數"
filter_a=df_all.loc[:,['主要用途',"建物型態","總樓層數"]]

# 刪除建物型態後面的字
def map1(str1):
    return str1.split("(")[0]

# 把總樓成數換成數字
def map2(str1):
    ret=0
    num=["","一","二","三","四","五","六","七","八","九"]
    if type(str1)==float:
        return 0
    str1=str1.split("層")[0]
    list1=str1.split("十")
    if (len(list1)==2)&(list1[0]!=""):
        ret = num.index(list1[0])*10+num.index(list1[1])
    if (len(list1)==2)&(list1[0]==""):
        ret = 10+num.index(list1[1])
    if len(list1)==1:
        ret = num.index(list1[0])
    return ret

# 取出有多少車位
def map3(str1):
    ret=str1.split("車位")[1]
    return ret

# 更改filter_a裡面的數值
filter_a["總樓層數"]=filter_a["總樓層數"].map(map2)
filter_a["建物型態"]=filter_a["建物型態"].map(map1)

# 篩選出我們要的條件
a=(filter_a["主要用途"]=="住家用")&(filter_a["建物型態"]=="住宅大樓")&(filter_a["總樓層數"]>=13)
df_all=df_all.loc[a]


# 算有多少車位
car=df_all.loc[:,["交易筆棟數"]]
car["交易筆棟數"]=car["交易筆棟數"].map(map3)
totalcar=pd.to_numeric(car["交易筆棟數"],errors='coerce').sum()

# 算平均房價
price=df_all.loc[:,["總價元"]]
totalprice=pd.to_numeric(price["總價元"],errors='coerce').sum()
avetotalprice=totalprice/2563

# 算平均車位價格
carprice=df_all.loc[:,["車位總價元"]]
totalcarprice=pd.to_numeric(carprice["車位總價元"],errors='coerce').sum()
avetotalcarprice=totalcarprice/totalcar

# 存成csv
df2=pd.DataFrame({"總件數":[2563],"總車位數":[2375],"平均總價元":avetotalprice,"平均車位總價元":avetotalcarprice})
df_all.to_csv("filter_a.csv",index=False,encoding='utf_8_sig')
df2.to_csv("filter_b.csv",index=False,encoding='utf_8_sig')







