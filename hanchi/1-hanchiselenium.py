from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time

#"./chromedriver"

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")
browser = webdriver.Chrome(executable_path = DRIVER_BIN)


## GETTING STUFF FROM HANCHI SINICA CORPUS
## ---------------------------------------

## periodization dictionaries
xianqin = {
    'name' : 'xianqin', # 先秦
    'webelem' : 'DY.0.2.0.3.S'
}

qinhan = {
    'name' : 'qinhan', # 秦漢 
    'webelem' : 'DY.0.2.3.3.S'
}

weijin = {
    'name' : 'weijin', # 魏晉南北朝
    'webelem' : 'DY.0.2.6.3.S'
}

suitang = {
    'name' : 'suitang', # 隋唐五代 
    'webelem' : 'DY.0.2.9.3.S' 
}

songjin = {
    'name' : 'songjin', # 宋遼金
    'webelem' : 'DY.0.2.12.3.S'
}

yuan = {
    'name' : 'yuan', # 元
    'webelem' : 'DY.0.2.15.3.S'
}

ming = {
    'name' : 'ming', # 明
    'webelem' : 'DY.0.2.18.3.S' 
}

qing = {
    'name' : 'qing', # 清
    'webelem' : 'DY.0.2.21.3.S'
}

minguo = {
    'name' : 'minguo', # 民國
    'webelem' : 'DY.0.2.24.3.S'
}

allperiods = [xianqin, qinhan, weijin, suitang, songjin, yuan, ming, qing, minguo]


# ------------
# FUNCTION DEFINITION

def scriptasinica (target):

    # needs to be called before function
    browser = webdriver.Chrome(DRIVER_BIN) 

    #getting website
    browser.get("http://hanchi.ihp.sinica.edu.tw/ihp/hanji.htm")
    enter = browser.find_element_by_xpath("//a[2]")
    enter.send_keys(Keys.ENTER)

    #parameter settings
    ## checked: 書名、內文、異體字
    ## unchecked: 注釋、同義詞
    browser.find_element_by_xpath("//*[@name='BN.0.1.0.3.S']").click()
    browser.find_element_by_xpath("//*[@name='RM.0.1.6.3.S']").click()

    # enter search term
    query = browser.find_element_by_xpath("//input[@name='XX.0.0.0.0.T']")
    query.send_keys(target)

    ## here begins FOR LOOP for periodization
    # set period
    for p in periods:
        time.sleep(5) # wait 5 seconds
        periodxpath = f"//*[@name='{p['webelem']}']"
        browser.find_element_by_xpath(periodxpath).click()
        #browser.find_element_by_xpath("//*[@name='DY.0.2.9.3.S']").click()

        # now we enter search term
        #query.send_keys(Keys.ENTER)

        #now we click
        browser.find_element_by_xpath("//*[@name='_IMG_執行檢索']").click()

        # all occurrences 命中 in this corpus on one page
        #if #assert browser.page_source.find("抱歉，找不到您所查詢的資料")
        try:# browser.find_element_by_xpath("//*[@name='_IMG_檢索報表']"):
            browser.find_element_by_xpath("//*[@name='_IMG_檢索報表']").click()

            hits = browser.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "ab02", " " ))] | //h3 | //div')
            #hits = browser.find_element_by_css_selector("div:nth-child(2)")
            #print(hits[0].text)

            for i in hits:
                element_contents = i.text
                if not os.path.exists('./results/'):
                    os.makedirs('./results')
                with open(f"./results/{target}_{p['name']}.txt", mode='a', encoding='utf8') as fp:
                    print(element_contents, file=fp)
            #wait another 5 seconds
            time.sleep(5) 
            
            # go back to previous page
            browser.find_element_by_xpath("//*[@name='_IMG_回前頁']").click()
        except:
            pass
        # unclick period
        browser.find_element_by_xpath(periodxpath).click()
        time.sleep(5)


## END PROGRAM
browser.close()


# ----------
# RUN FUNCTION

## SET VARIABLES
##target words
targets = ['熠熠',
    '煜煜',
    '燿燿',
    '耀耀',
    '爚爚',
    '灼灼',
    '爍爍',
    '鑠鑠',
    '犖犖',
    '燁燁',
    '爗爗',
    '曄曄',
    '煒煒',
    '韡韡',
    '煇煇',
    '輝輝',
    '暉暉']



## periods
periods = allperiods
## or periods is a specific period, e.g. periods = qinhan

for target in targets:
    scriptasinica(target)