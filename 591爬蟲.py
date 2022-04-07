from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json, os, pprint
from urllib import parse
from time import sleep

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--incognito')
options.add_argument('--disable-popup-blocking')

houseid=[]

def visit():
    url = "https://rent.591.com.tw/?kind=0&region=1"
    driver.get(url)
    sleep(8)


#取得租屋資料的網址
def getid():
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
            sleep(5)
        else:
            print("結束")
            break


# 關閉瀏覽器
def close():
    driver.quit()



if __name__ == "__main__":
    driver = webdriver.Chrome(options = options)
    visit()
    getid()
    close()



def visit(hid):
    url = f"https://rent.591.com.tw/home/{hid}"
    driver.get(url)
    sleep(1)

#判斷性別需求
def sex(str1):
    if "限男生" in str1:
        return 0
    elif "限女生" in str1:
        return 1
    else:
        return 2

#取得租屋資料
def getinfo(id):
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
            "id":id,
            "city":"taipei",
            "renter": a_elms[1].text.split(":")[1],
            "identity" : a_elms[1].text.split(":")[0],
            "phone" : phone_elms[2].text,
            "housetype" :housetype_elms[6].text,
            "situation" :housetype_elms[0].text,
            "sex":sex_elms

        })    
        
    except:
       pass


# 關閉瀏覽器
def close():
    driver.quit()



if __name__ == "__main__":
    houseidok=[]
    driver = webdriver.Chrome(options = options)
    count=1
    for i in houseid:
        print(count,":",i)
        visit(i)
        getinfo(i)
        count=count+1
        houseidok.append(i)
    close()
    print("end")
    






