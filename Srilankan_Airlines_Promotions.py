
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from requests.exceptions import ConnectionError


from pymongo import UpdateOne
import time
import traceback
from dateutil.parser import parse
import datetime
import re
import pymongo
client = pymongo.MongoClient("mongodb://analytics:KNjSZmiaNUGLmS0Bv2@13.92.251.7:42525/")
# db = client['fzDB_stg']
# cursor_OD = list(db.JUP_DB_OD_Master.aggregate([{'$project': {'_id': 0, 'OD': 1}}]))

# import pymongo
# client = pymongo.MongoClient("mongodb://analytics:KNjSZmiaNUGLmS0Bv2@13.92.251.7:42525/")
# db = client['fzDB_stg']
# cursor_OD = list(db.JUP_DB_OD_Master.aggregate([{'$project': {'_id': 0, 'OD': 1}}]))

#Defining the Chrome path
chrome_path =  r"E:\FlynavaIntern\chromedriver"
driver = webdriver.Chrome(chrome_path)
# driver = webdriver.PhantomJS()
driver.wait = WebDriverWait(driver, 5)
driver.set_window_size(1920, 1080)

driver.maximize_window()



url=("https://www.srilankan.com/en_uk/special-offers/free-baggage-allowance-for-Students")
print url
driver.get(url)
time.sleep(5)

driver.execute_script("window.scrollTo(0,500);")
text1=driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div[1]/p[3]/b').text.splitlines()
print "text1 :",text1

txt1 = text1[0].encode('ascii', 'ignore')
txt1 = txt1.strip('Book between')

txt2 = text1[1].encode('ascii', 'ignore')
txt2 = txt2.strip('Fly between')
txt3 = txt2.split('till')



print "txt1;",txt1,'\n',"txt2",txt2

txt1a = ' '.join(txt1.split(' ')[:3]).replace("th", '').replace("st",'').replace("rd",'')
txt1b = ' '.join(txt1.split(' ')[3:]).replace("th", '').replace("st",'').replace("rd",'')
txt2a =   txt3[0].replace("th", '').replace("st",'').replace("rd",'')
txt2b = txt3[1].replace("th", '').replace("st",'').replace("rd",'')


print "txt1a:",txt1a, "txt1b:",txt1b , "txt2a:",txt2a, "txt2b:",txt2b
try:
    dt1=parse(txt1a)
    dt2=parse(txt1b)
    dt3=parse(txt2a)
    dt4=parse(txt2b)
    valid=dt1.strftime('%Y-%m-%d')
    valid_till=dt2.strftime('%Y-%m-%d')
    start_date=dt3.strftime('%Y-%m-%d')
    end_date=dt4.strftime('%Y-%m-%d')

except:
    pass
origin="All"
destination="All"
Promotions_for="Students"
abc=driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div[1]/p[1]').text
value_discount=re.findall('\d+', abc)
Fare='-'+value_discount[0]+'%'
dis_2='-'+value_discount[1]+'%'
dis_3='-'+value_discount[2]+'%'
eligible=driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div[1]/ul[1]').text.splitlines()
offer_valid_for=driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div[1]/ol/li[3]').text
if "economy" in offer_valid_for:
    compartment="Y"
elif "business" in offer_valid_for:
    compartment="J"
else:
    print "there is other class"

print "origin",origin,'\n',"destination",destination,'\n',"valid",valid,'\n',"valid till",valid_till,'\n',"start date",start_date,'\n',"end date",end_date,'\n',"Fare",Fare,'\n',"Offer Eligibility :",'\n',eligible[0],'\n',eligible[1],'\n',eligible[2],'\n',eligible[3],'\n',"Fare restrictions:",'\n',"discount on air tickets purchased thereafter :",dis_2,'\n',"discount on airfare for your parents or spouse:",dis_3,'\n',"compartment ",compartment,'\n',"Promotions for :",Promotions_for

data_doc = dict()
data_doc = {
  "Airline" : "UL",
  "OD" : origin+destination,
  "Valid from" : valid,
  "Valid till" : valid_till,
  "compartment" : compartment,
  "Fare" : Fare,
  "Currency" : "All",
  "Minimum Stay" : "",
  "Maximum Stay" : "",
  "dep_date_from" : start_date,
  "dep_date_to" : end_date,
  "Url" : url
    }

doc = {
  "Airline" : "UL",
  "OD" : origin+destination,
  "Valid from" : valid,
  "Valid till" : valid_till,
  "compartment" : compartment,
  "Fare" : Fare,
  "Currency" : "All",
  "Minimum Stay" : "",
  "Maximum Stay" : "",
  "dep_date_from" : start_date,
  "dep_date_to" : end_date,
  "Url" : url ,
  "Last Updated Date" : datetime.datetime.now().strftime ("%Y-%m-%d"),
  "Last Updated Time" : datetime.datetime.now().strftime ("%H")
    }




