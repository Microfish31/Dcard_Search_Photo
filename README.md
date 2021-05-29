# Dcard_Search_Photo

## 說明
輸入關鍵字。  
即可自動從Dcard爬蟲圖片，並且下載下來。

## 設計
主要模組: BeautifulSoup Selenium  
1.先爬取各標題內的網址，再爬取各圖片的網址。  
2.標題會因為網頁的滾動而產生變化，因此必須將網頁下滑再進行爬蟲。  
3.下載圖片並非一個個下載，必須使用平行處理，開Thread Pool，這樣才能節省時間。   
  (但是python 的 實際上沒有真的平行處理，可搜尋GLI)  

## 輸入  
拉麵  

## 爬取結果  
![image](https://github.com/Microfish31/Dcard_Search_Photo/blob/main/photo1.PNG)  
