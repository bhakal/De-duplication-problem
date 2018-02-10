# -*- coding: utf-8 -*-
#in and vn table format is difft
#run rs and check
#tr has 4 view more buttons to click


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
import pymongo
from pymongo import UpdateOne
import time
import csv
import traceback
from dateutil.parser import parse
import datetime
import re
import pandas as pd

# Connecting to Mongodb
# import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["singapore"]
# collection=db["Singapore_airlines"]
#cursor_OD = list(db.JUP_DB_OD_Master.aggregate([{'$project': {'_id': 0, 'OD': 1}}]))

#Defining the Chrome path
chrome_path = r"E:\FlynavaIntern\chromedriver"
driver = webdriver.Chrome(chrome_path)

driver.wait = WebDriverWait(driver, 5)
driver.set_window_size(1920, 1080)

#
print "In more_promos1"
country =  ["au","at","bd","be","br","bn","kh","ca","hr","dk","fr","de","gr","hk","in","id","ie","it","jp","la","my","mv","mm","np","nl","nz","no","cn","ph",
"pl","pt","ru","sa","sg","za","kr","es","lk","se","ch","tw","th","tr","ae","gb","us","vn"]
# t=0
# bulk_update_doc = []
# origin1=[]
# destination1=[]
# valid_till_date=[]
# compartment1=[]
# start_date_1=[]
# end_date_1=[]
# Price1=[]
# Currency1=[]
# Country1=[]
for each_country in country:


  count = 0
  url = ("http://www.singaporeair.com/en_UK/" + each_country +"/home")
  print url
  # driver.maximize_window()
  driver.get(url)
  time.sleep(15)
  print "finding error"
  time.sleep(5)
  #to dismiss when pop up appears....
  try:

    driver.find_element_by_css_selector("body > div.insider-opt-in-notification > div > div:nth-child(3) > div.insider-opt-in-notification-button-container > div.insider-opt-in-notification-button.insider-opt-in-disallow-button")
    time.sleep(5)             
    error=driver.find_element_by_css_selector("body > div.insider-opt-in-notification > div > div:nth-child(3) > div.insider-opt-in-notification-button-container > div.insider-opt-in-notification-button.insider-opt-in-disallow-button").click()
    print "No pop ups now."
    time.sleep(5)

  except:
    pass  


  driver.execute_script("window.scrollTo(0,500);")
  time.sleep(10)
  try:

    #//*[@id="viewallbycity"]/h1
    more=driver.find_element_by_xpath('//*[@id="viewallbycity"]')
    print "It has View all promotions button"
    # time.sleep(5)
    time.sleep(10)
    more.click()
    time.sleep(5)
    # more.click()
    # time.sleep(5)
    driver.execute_script("window.scrollTo(0,500);")

    dropdown_button=driver.find_element_by_xpath('//*[@id="fare-deal-city-1"]')
    time.sleep(5)
    dropdown_button.click()
    
    time.sleep(5)
    table = driver.find_element_by_xpath('//*[@id="ui-id-1"]')
    rows = table.find_elements_by_tag_name("li")
    count1 = 0 # no of items in the dropdownlist
    for count in rows:
      count1 +=1
    print "count1:", count1


    for alpha in range(1,count1+1):
      driver.find_element_by_xpath('//*[@id="fare-deal-city-1"]').click()
      time.sleep(10)
      element = driver.find_element_by_xpath('//*[@id="ui-id-1"]/div/div/li['+ str(alpha) +']')
      time.sleep(10)
      actions = ActionChains(driver)
      actions.move_to_element(element).perform()
      time.sleep(5)
      element.click()
  # driver.refresh()

      for j in range(3):
        print "j============",j 
        driver.find_element_by_xpath('//*[@id="customSelect-0-combobox"]').click()
        time.sleep(10)
        classes=[]
        if j==0 or j==1:
          Class=classes.append("Y")
        else:
          Class=classes.append("J")
        Class=classes[0]
        print "Classes :",Class 
        time.sleep(6)
        try:
          driver.find_element_by_xpath('//*[@id="customSelect-0-option-'+ str(j) +'"]')
          print "Yes displayed......."
          select_class=driver.find_element_by_xpath('//*[@id="customSelect-0-option-'+ str(j) +'"]')
          time.sleep(5)
          select_class.click()
          time.sleep(5)
          driver.execute_script("window.scrollTo(0,500);")
          time.sleep(10)
          pixel=500
    # loop , if there are more than 1 see more button. //*[@id="main-inner"]/div[6]/a[1]
          elem = driver.find_element_by_xpath('//*[@id="main-inner"]/div[6]/a[1]')
          while elem.is_displayed():
            pixel += 400
            driver.execute_script("window.scrollTo(0,"+ str(pixel) +");") 
            pixel+=800  
            driver.find_element_by_xpath('//*[@id="main-inner"]/div[6]/a[1]').click()
     
          time.sleep(5)
          driver.execute_script("scroll(0,400);")
    # To find the number of offers of that particular city.....
          table1 = driver.find_element_by_xpath('//*[@id="main-inner"]/div[4]/section') 
          offers = table1.find_elements_by_tag_name("article")
          count2=0
          for each in offers:
            count2 += 1
          print "Number of offers :",count2
          pixel1=400
          
          for i in range(1,count2+1):
            print "offer :",i
            if i != 0: 
              print "scrolling down..."
              driver.execute_script("window.scrollTo(0,400);")
              try: #//*[@id="main-inner"]/div[4]/section/article[3]/div[1]/a[1]/div
                element_no=driver.find_element_by_xpath('//*[@id="main-inner"]/div[4]/section/article['+ str(i)+']/div[1]/a[1]/div')
                time.sleep(5)
                element_no.click()
                print "in try"
              except Exception:
                pixel1 += 300
                driver.execute_script("window.scrollTo(0,"+ str(pixel1)+");")
                print "in except"
                time.sleep(10)
                element_no=driver.find_element_by_xpath('//*[@id="main-inner"]/div[4]/section/article['+ str(i)+']/div[1]/a[1]/div')
                time.sleep(5)
                element_no.click()
            else:
              pass
            time.sleep(10)
            content = driver.find_element_by_xpath('//*[@id="main-inner"]/div[4]/section/article['+ str(i)+']/div[2]').text.splitlines()
            time.sleep(5)
            print len(content),content
            origin = (content[0].split(" ")[0]).lower()
            destination = (content[0].split(" ")[2]).lower()
            print origin,destination
            count3 = len(driver.find_elements_by_xpath('//*[@id="main-inner"]/div[4]/section/article['+ str(i)+']/div[2]/div/table/tbody/tr'))
            print "count3 :",count3
            time.sleep(5)

            list1=[]
            print "in the for loop"
     
            for k in range(1,count3+1):
              print "reached for loop"
              
              content2=driver.find_element_by_xpath('//*[@id="main-inner"]/div[4]/section/article['+ str(i)+']/div[2]/div/table/tbody/tr['+ str(k)+']/td[3]').text.splitlines()
              time.sleep(2)
              content1=driver.find_element_by_xpath('//*[@id="main-inner"]/div[4]/section/article['+ str(i)+']/div[2]/div/table/tbody/tr['+ str(k)+']/td[1]').text.split(" ")
              time.sleep(2)
              content3=driver.find_element_by_xpath('//*[@id="main-inner"]/div[4]/section/article['+ str(i)+']/div[2]/div/table/tbody/tr['+ str(k)+']/td[4]').text.splitlines()
              time.sleep(2)

              Price1=(content1[2]).strip('*')
              Currency1=content1[0]

              dt=parse(content2[0])
              valid_till1=dt.strftime('%Y-%m-%d')
              start_date1=(parse((content3[0]).split("-")[0])).strftime('%Y-%m-%d')
              end_date1=(parse((content3[0]).split("-")[1])).strftime('%Y-%m-%d')
              print Price1,Currency1,start_date1,end_date1,valid_till1
              list1.append([Price1,Currency1,start_date1,end_date1,valid_till1])
            # list1
            time.sleep(5)
            print "list1 is about to print"
            list1.extend((classes,origin,destination))
            # list1
            print "list1:",list1
            for i in range(0,count3):
              valid_till=list1[i][4]
              start_date=list1[i][2]
              end_date=list1[i][3]
              Price=list1[i][0]
              Currency=list1[i][1]
              compartment=list1[-3][0]

              print "Origin : ",origin,'\n',"destination : ",destination,"\n","Valid_till : ",valid_till ,'\n',"Price:", Price ,"\n","compartment:",compartment ,"\n", "Currency :",Currency,'\n', "Start-date :",start_date, '\n' , "End-date : ",end_date
              data_doc = {
                "Airline" : "SQ",
                "OD" : origin+destination,
                "Valid from" : "",
                "Valid till" : valid_till,
                "compartment" : compartment,
                "Fare" : Price,
                "Currency" : Currency,
                "Minimum Stay" : "",
                "Maximum Stay" : "",
                "dep_date_from" : start_date,
                "dep_date_to" : end_date,
                "Url" : url
                }
              db.Singapore_Airlines.insert(data_doc)
              



        except:
          pass

  except:
    print "There are no promotions."


# Singapore_Airlines=pd.DataFrame({'Origin':origin1,'Desination':destination1,'Currency':Currency1,'Price':Price1,'Start_Date':start_date_1,'End_Date':end_date_1,'Valid_Date':valid_till_date,'Compartment':compartment1})

# bulk_update_doc.append()  
# print "listsssssssssssss :",origin1,'\n',destination1,'\n',Price1,'\n',compartment1,'\n',start_date_1,'\n',end_date_1,'\n',valid_till_date.'\n',Currency1




# filename= "singapore_airlines"
# f=open(filename, "w")
# f.write(str(k)+ ","+ origin+ ","+ destination+ ","+ valid_till+","+Price+","+classes+","+Currency+","+start_date+","+end_date+ "\n")



