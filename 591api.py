import pymongo

# 【 男生可承租 】 且 【 位於新北 】 的租屋物件
def maleNewtaipei():
    ret=[]
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["591"]
    mycol = mydb["rent"]

    myquery = {"$or":[{"sex":0},{"sex": 2 }],"city":"newtaipei"}

    mydoc = mycol.find(myquery,{"_id":0})
    for i in mydoc:
        ret.append(i)
    return ret


#以 【 聯絡電話 】 查詢租屋物件
def findphone(phone):
    ret=[]
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["591"]
    mycol = mydb["rent"]

    myquery = {"phone":phone}

    mydoc = mycol.find(myquery,{"_id":0})
    
    for i in mydoc:
        ret.append(i)
    return ret
    

#所有 【 非屋主自行刊登 】 的租屋物件
def nohouse():
    ret=[]
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["591"]
    mycol = mydb["rent"]

    myquery = {"identity":{"$ne":'屋主'}}

    mydoc = mycol.find(myquery,{"_id":0,"id":0})

    for x in mydoc:
        ret.append(x)
    return ret


#【 臺北 】【 屋主為女性 】【 姓氏 為吳 】 所刊登的所有租屋 物件
def wuWoTaipei():
    ret=[]
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["591"]
    mycol = mydb["rent"]

    myquery = {"renter":{"$regex":'吳小姐'},"city":"taipei"}

    mydoc = mycol.find(myquery,{"_id":0,"id":0})

    for x in mydoc:
        ret.append(x)
    
    return ret