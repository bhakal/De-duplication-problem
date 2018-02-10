from selenium import webdriver
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import requests
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys

df=pd.read_csv('E:/FlynavaIntern/matrix.csv')
od=df['Origin']
des=df['Destination']
driver = webdriver.Firefox()
# driver=webdriver.PhantomJS('E:/FlynavaIntern/phantomjs.exe')
def selection(od,destination):
  url=('https://matrix.itasoftware.com')
  driver.get(url)
  one_way=driver.find_element_by_xpath('//*[@id="searchPanel-0"]/div/table/tbody/tr[1]/td/table/tbody/tr/td[3]/div/div')
  one_way.click()
  OD=driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div/table/tbody/tr/td[1]/div/div/table/tbody/tr[2]/td/div/div[2]/div/div/div[2]/div/div/div/input')
  time.sleep(2)
  OD.click()
  OD.send_keys(od)
  time.sleep(3)
  OD.send_keys(Keys.RETURN)
  Des=driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div/table/tbody/tr/td[1]/div/div/table/tbody/tr[2]/td/div/div[2]/div/div/div[4]/div/div/div/input')
  time.sleep(2)
  Des.click()
  Des.send_keys(destination)
  time.sleep(3)
  Des.send_keys(Keys.RETURN)
  date=driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div/table/tbody/tr/td[1]/div/div/table/tbody/tr[2]/td/div/div[2]/div/div/div[9]/div[1]/div[1]/div[2]/input')
  date.click()
  date_select=driver.find_element_by_xpath('/html/body/div[4]/div/table/tbody/tr[2]/td/div/table[1]/tbody/tr[2]/td[5]/div')
  time.sleep(3)
  date_select.click()
  time.sleep(2)
  Search=driver.find_element_by_xpath('//button[@type="button"]')
  Search.click()
  time.sleep(10)
    
list1=[]
list2=[]
for i in range(len(df)):
  selection(od[i],des[i])
  driver.execute_script("window.scrollTo(0,-1);")
  time.sleep(5)                           
  all_button=driver.find_element_by_xpath('//*[@id="contentwrapper"]/div[1]/div/div[6]/div[4]/div[3]/a[5]')
  time.sleep(2)
  all_button.click()
  driver.execute_script("window.scrollTo(0,0);")
  time.sleep(10)
  No_airlines = driver.find_elements_by_xpath("//*[@class='IR6M2QD-u-j']")
  tot3=len(No_airlines)
  print tot3
  pixel=0
  for k in range(tot3+1):
    print "k",k
    pixel +=50
    driver.execute_script("window.scrollTo(0,"+str(pixel)+");")
    time.sleep(2)
    try:
            
      if driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[2]/button').is_displayed():
        print "in if"
        driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[2]/button').click()
        time.sleep(2)
        Search=driver.find_element_by_xpath('//button[@type="button"]')
        Search.click()
        time.sleep(10)
        driver.execute_script("window.scrollTo(0,-1);")
        time.sleep(3)
        all_button=driver.find_element_by_xpath('//*[@id="contentwrapper"]/div[1]/div/div[6]/div[4]/div[3]/a[5]')
        time.sleep(3)
        all_button.click()
        driver.execute_script("window.scrollTo(0,0);")
        time.sleep(15)
        driver.execute_script("window.scrollTo(0,"+str(pixel)+");")
                
    except:
      "in except"
      pass
    try:
            
      offer1=driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div/div[6]/div[4]/div[2]/div/div['+str(k+1)+']/div[1]/table/tbody/tr/td[1]/div/button')
      time.sleep(3)#2
      airline_name=driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div/div[6]/div[4]/div[2]/div/div['+str(k+1)+']/div[1]/table/tbody/tr/td[2]/table/tbody/tr/td[1]')
      total_text=offer1.text + airline_name.text
      print total_text
      if total_text not in list1:
        list1.append(total_text)
        offer1=driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div/div[6]/div[4]/div[2]/div/div['+str(k+1)+']/div[1]/table/tbody/tr/td[1]/div/button')
        time.sleep(2)
        offer1.click()
        time.sleep(5)
        driver.execute_script("window.scrollTo(0,1000);")
        time.sleep(1)
        text1=driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div/table/tbody/tr[3]/td/div/div/div[3]/table[1]/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody')
        text1=text1.text
        print text1
        list2.append(text1)
        driver.execute_script("window.scrollTo(0,0)")
        driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div/div[1]/div[1]/table/tbody/tr/td[4]/div/a').click() 
        time.sleep(1)
        driver.execute_script("window.scrollTo(0,-1);")
        time.sleep(3)
        all_button=driver.find_element_by_xpath('//*[@id="contentwrapper"]/div[1]/div/div[6]/div[4]/div[3]/a[5]')
        time.sleep(3)
        all_button.click()
        driver.execute_script("window.scrollTo(0,0);")
        time.sleep(14)
    
    except:
      print "k---------missing",k
      pass
