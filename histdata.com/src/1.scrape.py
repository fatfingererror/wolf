from selenium import webdriver
import time

pairs = ['eurusd', 'gbpusd', 'usdjpy', 'usdchf', 'usdcad', 'audusd', 'nzdusd']

months = ['5']
years = ['2016']
u = ''

fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.download.dir", "/home/git/working/projects/wolf/histdata.com/data")
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")

driver = webdriver.Firefox(firefox_profile=fp)

for p in pairs:
    for m in months:
            for y in years:
                u = "http://www.histdata.com/download-free-forex-historical-data/?/ascii/tick-data-quotes/" + p + "/" + y + "/" + m
                print "scraping " + u

                driver.get(u)
                time.sleep(5)
                driver.find_element_by_id("a_file").click()
                time.sleep(20)
                #drive.quit()
