# -*- coding: utf-8 -*-
#in and vn table format is difft
#run rs and check
#tr has 4 view more buttons to click

def run():

  import sys
  reload(sys)
  sys.setdefaultencoding('utf8')
  from FlynavaIntern.airlines_promo_files.promotions_trigger import PromoRuleChangeTrigger
  from FlynavaIntern.airlines_promo_files.promotions_trigger import PromoDateChangeTrigger
  from FlynavaIntern.airlines_promo_files.promotions_trigger import PromoFareChangeTrigger
  from FlynavaIntern.airlines_promo_files.promotions_trigger import PromoNewPromotionTrigger
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
  from pymongo import UpdateOne
  import time
  import traceback
  from dateutil.parser import parse
  import datetime
  import re
  # Connecting to Mongodb
  import pymongo
  client = pymongo.MongoClient("mongodb://localhost:27017")
  db = client['fzDB_stg']
  cursor_OD = list(db.JUP_DB_OD_Master.aggregate([{'$project': {'_id': 0, 'OD': 1}}]))

  #Defining the Chrome path
  chrome_path = r"E:\Flynava intern\chromedriver"
  driver = webdriver.Chrome(chrome_path)

  driver.wait = WebDriverWait(driver, 5)
  driver.set_window_size(1920, 1080)

  def more_promos1():
    print "In more_promos1"
    country =  ["au","at","bd","be","br","bn","kh","ca","hr","dk","fr","de","gr","hk","in","id","ie","it","jp","la","my","mv","mm","np","nl","nz","no","cn","ph",
    "pl","pt","ru","sa","sg","za","kr","es","lk","se","ch","tw","th","tr","ae","gb","us","vn"]
    t=0
    bulk_update_doc = []

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
        more=driver.find_element_by_xpath('//*[@id="viewallbycity"]')
        print "It has View all promotions button"
        # time.sleep(5)
        time.sleep(5)
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

          for j in range(4):
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
                    driver.find_element_by_xpath('//*[@id="main-inner"]/div[4]/section/article['+ str(i)+']/div[1]/a[1]/div').click()
                    print "in try"
                  except Exception:
                    pixel1 += 300
                    driver.execute_script("window.scrollTo(0,"+ str(pixel1)+");")
                    print "in except"
                    time.sleep(10)
                    driver.find_element_by_xpath('//*[@id="main-inner"]/div[4]/section/article['+ str(i)+']/div[1]/a[1]/div').click()
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
                  
                  #Storing the parameters in a dictionary
                  data_doc = dict()
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

                  doc = {
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
                    "Url" : url ,
                    "Last Updated Date" : datetime.datetime.now().strftime ("%Y-%m-%d"),
                    "Last Updated Time" : datetime.datetime.now().strftime ("%H")
                    }
                  
                  print "data_doc:", data_doc
                  print "doc:", doc

                  print "1---yes"
                  a = 0
                  for i in cursor_OD:
                    if (data_doc['OD'] == i['OD']):
                    print "OD in list:", i['OD']
                    print "present OD:", data_doc['OD']
                    rule_trig = 0

                    def rule_change():
                      rule_trig = 0
                      a=0
                      print "rule_change_trigger_starts"
                      cursor = list(db.JUP_DB_Promotions.aggregate([
                        {'$match': {'OD': data_doc['OD'], 'Airline': data_doc['Airline'],
                                    'Fare': data_doc['Fare'],
                                    'dep_date_from': data_doc['dep_date_from'],
                                    'dep_date_to': data_doc['dep_date_to']}},
                        {"$sort": {"Last Updated Date": -1, "Last Updated Time": -1}}]))
                      # cursor = json.dump(cursor)
                      print cursor
                      # print "data_doc: ", data_doc
                      if len(cursor) > 0:
                        for i in range(len(cursor)):
                          if (cursor[i]['Valid from'] == data_doc['Valid from']) and (
                                    cursor[i]['Currency'] == data_doc['Currency']) \
                                  and (
                                            cursor[i]['Valid till'] == data_doc['Valid till']) \
                                  and (
                                            cursor[i]['compartment'] == data_doc['compartment']):
                            pass
                          else:
                            pass
                          if (cursor[i]['Valid from'] != data_doc['Valid from']) or (
                                    cursor[i]['Valid till'] != data_doc['Valid till']) \
                                  or (
                                            cursor[i]['Currency'] != data_doc['Currency']) \
                                  or (
                                            cursor[i]['compartment'] != data_doc['compartment']):
                            print "Raise Rule Change Trigger"  ### Call the trigger
                            promo_rule_change_trigger = PromoRuleChangeTrigger("promotions_ruleschange",
                                                                               old_doc_data=cursor[0],
                                                                               new_doc_data=doc,
                                                                               changed_field="Rules")
                            promo_rule_change_trigger.do_analysis()
                            rule_trig += 1
                          else:
                            pass
                          if rule_trig == 1:
                            a+=1
                            break

                        print "rule change checked"
                      else:
                        print "No matches in Rule Change Trigger Check"
                        pass

                      print "done with rule change"

                      date_trig = 0
                      def date_change():
                        date_trig = 0
                        print "date range trigger starts"
                        print data_doc
                        cursor = list(db.JUP_DB_Promotions.aggregate([
                          {'$match': {'OD': data_doc['OD'], 'Airline': data_doc['Airline'],
                                      'compartment': data_doc['compartment'], 'Currency': data_doc['Currency'],
                                      'Fare': data_doc['Fare'], 'Valid from': data_doc['Valid from'],
                                      'Valid till': data_doc['Valid till'],
                                      }},
                          {"$sort": {"Last Updated Date": -1, "Last Updated Time": -1}}]))
                        # cursor = json.dump(cursor)
                        print cursor
                        if len(cursor) > 0:
                          for i in range(len(cursor)):

                            if (cursor[i]['dep_date_from'] == data_doc['dep_date_from']) and (
                                      cursor[i]['dep_date_to'] == data_doc['dep_date_to']):
                              pass
                            else:
                              pass
                            if (cursor[i]['dep_date_from'] != data_doc['dep_date_from']) or (
                                      cursor[i]['dep_date_to'] != data_doc['dep_date_to']):
                              print "Raise Date Change Trigger (dep period is updated)"
                              promo_date_change_trigger = PromoDateChangeTrigger("promotions_dateschange",
                                                                                 old_doc_data=cursor[0],
                                                                                 new_doc_data=doc,
                                                                                 changed_field="dep_period")
                              promo_date_change_trigger.do_analysis()
                              date_trig += 1
                            else:
                              pass
                            if date_trig == 1:
                              a = 2
                              break
                            else:
                              pass

                          else:
                            print "No docs in Date Change trigger check"
                            pass
                      
                      print "coming in ----yes1"
                      fare_trig = 0

                      def fare_change():
                        fare_trig = 0
                        print "fare_range"
                        cursor = list(db.JUP_DB_Promotions.aggregate([
                          {'$match': {'OD': data_doc['OD'], 'Airline': data_doc['Airline'],
                                      'compartment': data_doc['compartment'], 'Currency': data_doc['Currency'],
                                      'Valid from': data_doc['Valid from'],
                                      'dep_date_from': data_doc['dep_date_from'],
                                      'dep_date_to': data_doc['dep_date_to'],
                                      'Valid till': data_doc['Valid till'],
                                      }},
                          {"$sort": {"Last Updated Date": -1, "Last Updated Time": -1}}]))
                        # cursor = json.dump(cursor)
                        print cursor
                        if len(cursor) > 0:
                          for i in range(len(cursor)):
                            if (cursor[i]['Fare'] == data_doc['Fare']):
                              pass
                            else:
                              pass
                            if (cursor[i]['Fare'] != data_doc['Fare']):
                              print "Raise Fare Change Trigger (Fare is updated)"  ### Call the trigger
                              promo_fare_change_trigger = PromoFareChangeTrigger("promotions_fareschange",
                                                                                 old_doc_data=cursor[i],
                                                                                 new_doc_data=doc,
                                                                                 changed_field="Fare")
                              promo_fare_change_trigger.do_analysis()
                              fare_trig += 1
                            else:
                              pass
                            if fare_trig == 1:
                              a = 3
                              break
                            else:
                              pass
                          else:
                            print "No docs in fares change check"
                            pass

                      new_trig = 0

                      def new_promotion():
                        new_trig = 0
                        print "new_promotion"
                        # cursor = list(db.JUP_DB_Promotions.find({}))
                        cursor = list(db.JUP_DB_Promotions.aggregate([
                          {'$match': {'Airline': data_doc['Airline']}}]))
                        print "cursor:", cursor
                        print "len of cursor:", len(cursor)
                        if len(cursor) > 0:

                          for i in range(len(cursor)):
                            change_flag_list = []
                            if (cursor[i]['Valid from'] == data_doc['Valid from']) and (
                                      cursor[i]['Valid till'] == data_doc['Valid till']) \
                                    and (
                                                        cursor[i]['compartment'] == data_doc['compartment']
                                                    and (cursor[i]['OD'] == data_doc['OD']) and (
                                                            cursor[i]['Fare'] == data_doc['Fare']) and (
                                                          cursor[i]['Currency'] == data_doc['Currency']) and (
                                                        cursor[i]['dep_date_from'] == data_doc['dep_date_from']) and (
                                                      cursor[i]['dep_date_to'] == data_doc['dep_date_to'])):
                              pass
                            else:
                              pass

                            if (cursor[i]['Valid from'] == data_doc['Valid from']) and (
                                      cursor[i]['Valid till'] == data_doc['Valid till']) \
                                    and (
                                                        cursor[i]['compartment'] == data_doc['compartment']
                                                    and (cursor[i]['OD'] != data_doc['OD']) and (
                                                            cursor[i]['Fare'] == data_doc['Fare']) and (
                                                          cursor[i]['Currency'] == data_doc['Currency']) and (
                                                        cursor[i]['dep_date_from'] == data_doc['dep_date_from']) and (
                                                      cursor[i]['dep_date_to'] == data_doc['dep_date_to'])):
                              print("Raise New Promotion Released Trigger")
                              promo_new_promotion_trigger = PromoNewPromotionTrigger(
                                "new_promotions",
                                old_doc_data=cursor[i],
                                new_doc_data=doc,
                                changed_field="OD")
                              promo_new_promotion_trigger.do_analysis()
                              new_trig += 1
                              if new_trig == 1:
                                break
                              else:
                                pass
                            else:
                              pass

                            if cursor[i]['Valid from'] != data_doc['Valid from']:
                              change_flag_list.append(1)
                            else:
                              pass
                            if cursor[i]['Valid till'] != data_doc['Valid till']:
                              change_flag_list.append(2)
                            else:
                              pass
                            if cursor[i]['compartment'] != data_doc['compartment']:
                              change_flag_list.append(5)
                            else:
                              pass
                            if cursor[i]['OD'] != data_doc['OD']:
                              change_flag_list.append(6)
                            else:
                              pass
                            if cursor[i]['Fare'] != data_doc['Fare']:
                              change_flag_list.append(7)
                            else:
                              pass
                            if cursor[i]['Currency'] != data_doc['Currency']:
                              change_flag_list.append(8)
                            else:
                              pass
                            if cursor[i]['dep_date_from'] != data_doc['dep_date_from']:
                              change_flag_list.append(9)
                            else:
                              pass
                            if cursor[i]['dep_date_to'] != data_doc['dep_date_to']:
                              change_flag_list.append(10)
                            else:
                              pass
                            print "change_flag_list:", change_flag_list
                            if len(change_flag_list) > 2:
                              print("Raise New Promotion Released Trigger, new promotions are released")
                              promo_new_promotion_trigger = PromoNewPromotionTrigger("new_promotions",
                                                                                     old_doc_data=cursor[i],
                                                                                     new_doc_data=doc,
                                                                                     changed_field="new")
                              promo_new_promotion_trigger.do_analysis()
                              new_trig += 1
                            else:
                              pass
                            if new_trig == 1:
                              a = 4
                              break
                            else:
                              pass

                        else:
                          print "No docs in New Promo check"
                          pass


                      for i in range(1, 2):
                        rule_change()
                        if rule_trig == 1:
                          break
                        else:
                          pass
                        date_change()
                        if date_trig == 1:
                          break
                        else:
                          pass
                        fare_change()
                        if fare_trig == 1:
                          break
                        else:
                          pass
                        new_promotion()
                        if new_trig == 1:
                          break
                        else:
                          pass
                      else:
                        pass

                  if t == 2:
                    st = time.time()
                    print "updating: ", count

                    # print bulk_update_doc
                    db['JUP_DB_Promotions'].bulk_write(bulk_update_doc)
                    print "updated!", time.time() - st
                    bulk_list = []
                    count += 1
                    t = 0
                    # driver.execute_script("window.scrollTo(0,600);")
                    print "yes---------------------->"
                  else:
                    bulk_update_doc.append(UpdateOne(data_doc, {"$set": doc}, upsert=True))
                    # print bulk_update_doc
                    t += 1
                    print "t= :", t

                  continue
            try:
              more_promos1()
            except:
              print traceback.print_exc()
              pass

            except:
              pass

      except:
        print "There are no promotions."

if __name__ == "__main__":
    run()    





# filename= "singapore_airlines"
# f=open(filename, "w")
# f.write(str(k)+ ","+ origin+ ","+ destination+ ","+ valid_till+","+Price+","+classes+","+Currency+","+start_date+","+end_date+ "\n")



