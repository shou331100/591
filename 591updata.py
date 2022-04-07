import pymongo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json, os, pprint ,re
from urllib import parse
from time import sleep
import random

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--incognito')
options.add_argument('--disable-popup-blocking')


#取得資料庫裡的舊的id
def getid(city):
    ret=[]
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["591"]
    mycol = mydb["rent"]


    mydoc = mycol.find({"city":city},{"_id":0,"id":1})
    for i in mydoc:
        ret.append(i["id"])
    return ret


#取得新的id
def getnewid(city):
    houseid=[]
    driver = webdriver.Chrome(options = options)
    url = f"https://rent.591.com.tw/?kind=0&region={city}"
    driver.get(url)
    sleep(8)

    while(True):
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located( 
                (By.CSS_SELECTOR, 'a.pageNext') 
            )
        )

        a_elms = driver.find_elements(By.CSS_SELECTOR, '.vue-list-rent-item')
        nextpage = driver.find_element(By.CSS_SELECTOR,'a.pageNext')
        for i in a_elms:
            aLink = i.get_attribute('data-bind')
            houseid.append(aLink)
            
        if nextpage.get_attribute('href') != None:
            driver.find_element(By.CSS_SELECTOR,'a.pageNext').click()
            sleep(8)
        else:
            print("結束")
            break

    driver.quit()
    return houseid


#判斷性別需求
def sex(str1):
    if "限男生" in str1:
        return 0
    elif "限女生" in str1:
        return 1
    else:
        return 2

#把新的資料加入資料庫
def newid(ni,oi,city):
    listData=[]
    for i in ni :
        if i not in oi:
            listData.append(i)
    
    driver = webdriver.Chrome(options = options)
    for ids in listData:
        url = f"https://rent.591.com.tw/home/{id}"
        driver.get(url)
        try:
            WebDriverWait(driver, 8).until(
                EC.presence_of_element_located( 
                    (By.CSS_SELECTOR, 'div.reference .tel-txt') 
                )
            )
            a_elms=driver.find_elements(By.CSS_SELECTOR, 'section.clearfix.horizontalLayout div.base-info.clearfix div.info p.name')
            phone_elms=driver.find_elements(By.CSS_SELECTOR, 'div.reference .tel-txt')
            housetype_elms=driver.find_elements(By.CSS_SELECTOR, '.house-pattern span')
            try:
                sex_elms=sex(driver.find_element(By.CSS_SELECTOR, '.service-rule div span').text)

            except:
                sex_elms=2
            print(a_elms[1].text.split(":")[1],a_elms[1].text.split(":")[0],phone_elms[2].text,housetype_elms[6].text,housetype_elms[0].text,sex_elms)
            listData.append({
                "id":ids,
                "city":city,
                "renter": a_elms[1].text.split(":")[1],
                "identity" : a_elms[1].text.split(":")[0],
                "phone" : phone_elms[2].text,
                "housetype" :housetype_elms[6].text,
                "situation" :housetype_elms[0].text,
                "sex":sex_elms

            })    
        
        except:
           pass
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["591"]
    mycol = mydb["rent"]
    mycol.insert_many(listData)
    

#刪除以出租的資料
def delOldId(ni,oi):
    listData=[]
    myclient = pymongo.MongoClient("mongodb://localhostlistData7/")
    mydb = myclielistData91"]
    mycol = mydb["rent"]
    for i in oi:
        if i not in ni:
            listData.append(i)
    for i in listData:
  mycol mycol.delete_one({"id":str(i)})



if __name__ == "__main__":
    cityid={"newtaipei":"3","taipei":"1"}
    for i in cityid:
        old=getid(i)
        ni=getnewid(cityid[i])
        newid(ni,old,i)
        delOldId(ni,old)
     
