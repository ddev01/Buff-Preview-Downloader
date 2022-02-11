from selenium import webdriver
import urllib.request
import time

browser = webdriver.Chrome()

downloadLocation = 'C:/Users/Admin/Desktop/knives/'
linkURL = [
    'https://buff.163.com/goods/759682#tab=selling&page_num=',
    'https://buff.163.com/goods/759640#tab=selling&page_num='
    ]
counter = 100
browser.get('https://buff.163.com/')
input('Log into buff.163.com and press enter: ')
for link in linkURL:
    ItemInspectURLList = []
    pageLoop = 1
    while True:
        print('Crawling page', pageLoop)
        browser.get(link + '&page_num=' + str(pageLoop)+'&sort_by=price.asc&max_price=250')
        time.sleep(2)
        itemInspectElements = browser.find_elements_by_xpath('//*[starts-with(@id,"sell_order_")]/td[2]/div/a')
        if itemInspectElements:
            pageLoop += 1
            for itemInspectElement in itemInspectElements:
                ItemInspectURLList.append(itemInspectElement.get_attribute('data-inspecturl'))
        else:
            print('Finished crawling all ', pageLoop, ' pages.')
            break

    print('Starting download: ')
    print('Images to download: ', len(ItemInspectURLList))
    for ItemInspectURL in ItemInspectURLList:
        if not isinstance(ItemInspectURL, str): #some fresh items have a different 'inspect' button, are gray and return no string url.
            print('found black sheep')
            continue
        urllib.request.urlretrieve(ItemInspectURL, downloadLocation + str(counter) + '.png')
        time.sleep(0.2)
        if counter % 10 == 0:
            print('Downloaded: ', counter, '/', len(ItemInspectURLList))
            time.sleep(5)
        counter += 1