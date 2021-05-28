from bs4 import BeautifulSoup
import requests
import os
import concurrent.futures
import time
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

# 改成自己的firefox.exe位置
firefox_path = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'

# 改成自己的網頁driver位置
webdriver_path = 'D:\\geckodriver.exe'
binary = FirefoxBinary(firefox_path)

data = []
all_data = []

def reptile_title(search):
    # 開啟firefox
    Firefox_options =  webdriver.FirefoxOptions()

    # 視窗最大 抓取數量多 根據螢幕size調整
    Firefox_options.add_argument("--width=512")
    Firefox_options.add_argument("--height=1000")

    # 隱藏視窗
    Firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(executable_path=webdriver_path,firefox_binary=binary,options=Firefox_options) 
    driver.implicitly_wait(3)

    url = "https://www.dcard.tw" + "/topics/" + search

    # 前往 google
    driver.get(url)

    # 往下捲
    for i in range(10):

        soup = BeautifulSoup(driver.page_source, "html.parser")

        a_tag = soup.find_all("h2",class_="tgn9uw-2 jWUdzO")

        for i in range(len(a_tag)) :
            index = a_tag[i].find("a").get('href')
            data.append("https://www.dcard.tw" + index)
            print(index)

        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
        time.sleep(1)
    driver.close()
    print("over")


def reptile_title2(url) :
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    a_tag = soup.find_all("div",class_="sc-2xcoxb-0 iJlszd")

    for j in range(len(a_tag)) :
        all_data.append(a_tag[j].find("img").get('src'))
        print(all_data[j])

def write_txt():
    f = open("Dacard_Photo.txt","w+")
    string = ""
    for i in range(len(all_data)):
        string = string + all_data[i] + "\n"
    f.write(string)
    f.close()

def download_photo(url,i):
    img = requests.get(url)                                   # 下載圖片
    with open("images\\" + str(i+1) + ".jpg", "wb") as file:  # 開啟資料夾及命名圖片檔
         file.write(img.content)                              # 寫入圖片的二進位碼

if __name__ == "__main__":
    print("請輸入關鍵字:")
    search = input()
    start_time = time.time()  # 
    print("正在解析網址...")
    reptile_title(search)

    if len(data) > 0 :
        print("正在尋找圖片..." + "總計: " + str(len(data)) + " 個網址")
        # 同時建立及啟用30個執行緒
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=30)

        for i in range(len(data)) :
            executor.submit(reptile_title2,data[i])
        executor.shutdown()
    write_txt()

    if not os.path.exists("images"):
       os.mkdir("images")                               # 建立資料夾

    print("正在下載圖片..."+"總計: " + str(len(all_data)) + " 個圖片")

    # 同時建立及啟用100個執行緒
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=100)

    for i in range(len(all_data)):
        executor.submit(download_photo,all_data[i],i)
    executor.shutdown()

    end_time = time.time()
    print("...完成...")
    print("約 " + round(end_time-start_time,2) + "sec")
    
