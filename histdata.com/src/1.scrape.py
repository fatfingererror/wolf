import glob
import time
import os
import zipfile

from selenium import webdriver

pairs = ['eurusd', 'gbpusd'] #'usdjpy', 'usdchf', 'usdcad', 'audusd', 'nzdusd']
months = ['8']
years = ['2016']
destination_path = os.path.join(os.path.expanduser('~'), 'git/working/projects/wolf/histdata.com/data/csv')
downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')

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
                print("scraping " + u)

                driver.get(u)
                time.sleep(5)
                element = driver.find_element_by_id("a_file")
                element.click()
                time.sleep(20)

driver.quit()

os.chdir(downloads_path)
filenames = glob.glob('HISTDATA_COM_ASCII_*')
for f in filenames:
    ticks_file = os.path.join(downloads_path, f)
    with zipfile.ZipFile(ticks_file, "r") as z:
        for name in z.namelist():
            if name.endswith('.csv'):
                z.extract(name, destination_path)
    os.remove(ticks_file)
