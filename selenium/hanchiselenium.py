from selenium import webdriver
from selenium.webdriver.common.keys import Keys


## GETTING STUFF FROM HANCHI SINICA CORPUS
## ---------------------------------------

## SET VARIABLES
##target word
target = '濛濛'

## periodizations
xianqin = 'DY.0.2.0.3.S' # 先秦 name='DY.0.2.0.3.S'
qinhan = 'DY.0.2.3.3.S' # 秦漢 name='DY.0.2.3.3.S'
weijin = 'DY.0.2.6.3.S' # 魏晉南北朝 name='DY.0.2.6.3.S'
suitang = 'DY.0.2.9.3.S' # 隋唐五代 name='DY.0.2.9.3.S'
songjin = 'DY.0.2.12.3.S' # 宋遼金 name='DY.0.2.12.3.S'
yuan = 'DY.0.2.15.3.S' # 元 name='DY.0.2.15.3.S'
ming = 'DY.0.2.18.3.S' # 明 name='DY.0.2.18.3.S'
qing = 'DY.0.2.21.3.S' # 清 name='DY.0.2.21.3.S'
minguo = 'DY.0.2.24.3.S' # 民國 name='DY.0.2.24.3.S'

# ------------

browser = webdriver.Chrome("/Users/Thomas/Dropbox/Doctoraat/pythonforhumanities/selenium/chromedriver")

#getting website
browser.get("http://hanchi.ihp.sinica.edu.tw/ihp/hanji.htm")
enter = browser.find_element_by_xpath("//a[2]")
enter.send_keys(Keys.ENTER)

#parameter settings
## checked: 書名、內文、異體字
## unchecked: 注釋、同義詞
browser.find_element_by_xpath("//*[@name='BN.0.1.0.3.S']").click()
browser.find_element_by_xpath("//*[@name='RM.0.1.6.3.S']").click()

#search term
query = browser.find_element_by_xpath("//input[@name='XX.0.0.0.0.T']")
#<input type="text" name="XX.0.0.0.0.T" value="" size="28" class="">
query.send_keys(target)


## here begins FOR LOOP for periodization
# set period
periodxpath = "//*[@name='" + xianqin + "']"
browser.find_element_by_xpath(periodxpath).click()
#browser.find_element_by_xpath("//*[@name='DY.0.2.9.3.S']").click()

# now we click
query.send_keys(Keys.ENTER)

# all occurrences 命中 in this corpus on one page
browser.find_element_by_xpath("//*[@name='_IMG_檢索報表']").click()

hits = browser.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "ab02", " " ))] | //h3 | //div')
#hits = browser.find_element_by_css_selector("div:nth-child(2)")
#print(hits[0].text)

for i in hits:
    element_contents = i.text
    print(element_contents)





## END PROGRAM
browser.close()
