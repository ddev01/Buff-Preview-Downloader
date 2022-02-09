from selenium import webdriver
import urllib.request
import time

browser = webdriver.Chrome()

downloadLocation = 'C:/Users/Admin/Desktop/gloves/'
linkURL = 'https://buff.163.com/goods/42360?from=market#tab=selling&page_num=1&sort_by=price.asc'
pageCount = 5

browser.get('https://buff.163.com/')
input('Log into buff.163.com and press enter: ')
ItemInspectURLList = []

for x in range(1, pageCount + 1):
    print('Crawling page', x)
    browser.get(linkURL + str(x)+'&sort_by=price.asc')
    time.sleep(2)
    itemInspectElements = browser.find_elements_by_xpath('//*[starts-with(@id,"sell_order_")]/td[2]/div/a')
    for itemInspectElement in itemInspectElements:
        ItemInspectURLList.append(itemInspectElement.get_attribute('data-inspecturl'))

print('Starting download: ')
print('Images to download: ', len(ItemInspectURLList))
counter = 0

for ItemInspectURL in ItemInspectURLList:
    urllib.request.urlretrieve(ItemInspectURL, downloadLocation + str(counter) + '.png')
    if counter % 20 == 0:
        print('Downloaded: ', counter, '/', len(ItemInspectURLList))
        time.sleep(5)
