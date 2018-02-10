# //*[@id="promos"]/article/div/div[4]/a
# //*[@id="promos"]/div[1]/article[2]/div/a
# //*[@id="promos"]/div[1]/article[1]/div/a
# //*[@id="promos"]/div[2]/article/div/a
import sys
reload(sys)
sys.setdefaultencoding('utf8')
#E:Flynavaintern.promotions_trigger import PromoRuleChangeTrigger
# #from E:Flynavaintern.promotions_trigger import PromoDateChangeTrigger
# from E:Flynavaintern.promotions_trigger import PromoFareChangeTrigger
# from E:Flynavaintern.promotions_trigger import PromoNewPromotionTrigger
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from requests.exceptions import ConnectionError
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException
from pymongo import UpdateOne
import time
import traceback
from dateutil.parser import parse
import datetime
import re
import csv
import array
import urllib2
import bs4
import string
from urllib2 import urlopen as uReq
from bs4 import BeautifulSoup 
import sys
import requests
reload(sys)
sys.setdefaultencoding('utf-8')

chrome_path = r"E:\FlynavaIntern\chromedriver"
driver = webdriver.Chrome(chrome_path)

driver.wait = WebDriverWait(driver, 5)
driver.set_window_size(1920, 1080)
driver.maximize_window()
# <a class="btn btn-large-arrow btn-color1 btn-offer btnIframeImagery" href="http://www.etihad.com/en-vn/deals/view-more/?promotion_id=11413" role="button" data-viewmoretext="View more" data-viewlesstext="View less">View more<span></span><span class="hiddenText">December Special Offers</span></a>
# <a class="btn btn-medium-arrow btn-color1 btn-offer fontSmall " href="http://www.etihad.com/en-tr/deals/view-more/?promotion_id=2983" role="button" data-viewmoretext="View more" data-viewlesstext="View less">View more<span></span><span class="hiddenText">Discover the best</span></a>
# driver.maximize_window() #promos > div:nth-child(2) #promos > div:nth-child(3)

url=("http://www.etihad.com/en-tr/deals/promotions-main/")

print url
driver.get(url)
time.sleep(10)

# driver.execute_script("window.scrollTo(0,600);") //*[@id="promos"]/article/div/div[4]/a   //*[@id="promos"]/div/article/div/a
driver.execute_script("window.scrollTo(0,500);")

time.sleep(5)

count=len(driver.find_elements_by_xpath('//*[@id="promos"]/div/article'))
print "count:",count
if count%2 ==0:
  no_of_rows=count/2
else:
  no_of_rows=(count+1)/2

print "no of rows",no_of_rows
no_of_cols=(no_of_rows*2)-count
print "no of cols :",no_of_cols
pixel = 700
for k in range(no_of_rows):
  try:

    driver.find_element_by_xpath('//*[@id="promos"]/article/div/div[4]/a').click()
    print "in try"
  except Exception:
    for i in range(no_of_rows):

      print "i",i
      pixel +=300
      time.sleep(5)
      for j in range(1,3):
        print "j",j
        url=("http://www.etihad.com/en-tr/deals/promotions-main/")
        print url
        time.sleep(5)
        driver.get(url)
        driver.execute_script("window.scrollTo(0,"+ str(pixel) +");")

        # time.sleep(5)
        try:
          view_more1=driver.find_element_by_xpath('//*[@id="promos"]/div['+ str(i+1) +']/article['+ str(j)+']/div/a')
          time.sleep(5)
          view_more1.click()
        except NoSuchElementException:
          pass

    print "in except"


  
  
  

# driver.refresh()


    # driver.execute_script("window.scrollTo(0,"+ str(pixel) +");")
    # # time.sleep(5)
    # if driver.find_element_by_xpath('//*[@id="promos"]/div['+ str(i) +']/article['+ str(j)+']/div/a').is_displayed():
    #   view_more1=driver.find_element_by_xpath('//*[@id="promos"]/div['+ str(i) +']/article['+ str(j)+']/div/a')

    #   time.sleep(5)
    #   view_more1.click()

    # else:
    #   print "no"
    #   pass