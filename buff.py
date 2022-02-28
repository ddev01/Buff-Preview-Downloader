from selenium import webdriver
import urllib.request
import time
import os

browser = webdriver.Edge()

#Location where the inspect images will be saved.
downloadLocation = 'C:/Users/Admin/Desktop/Wildfire/'

#Item URL's to download images from. E.G.: 
# https://buff.163.com/goods/871750?from=market#tab=selling or
# https://buff.163.com/goods/871750?from=market#tab=selling&max_price=52&sort_by=paintwear.asc
linkURL = [
    'https://buff.163.com/goods/773698?from=market#tab=selling&max_price=52&sort_by=paintwear.asc&extra_tag_ids=non_empty&min_paintwear=0.15&max_paintwear=0.18',
    ]
if not os.path.exists(downloadLocation):
    os.makedirs(downloadLocation)
#Open set url using selenium driver.
browser.get('https://buff.163.com/')
#Give user time to log into buff since you can't view the site without being logged in.
input('Log into buff.163.com and press enter: ')

def getInspectURLS():
    for link in linkURL:
        global ItemInspectURLList 
        ItemInspectURLList = []
        pageLoop = 1
        #Create infinite loop which will be broken later since we don't know how many pages there are to scrape.
        while True:
            print('Crawling page', pageLoop)
            browser.get(link + '&page_num=' + str(pageLoop)) #Possibly add +'&sort_by=price.asc&max_price=250'
            #Sleep since loading first page might take some time.
            time.sleep(2)
            #Will return only xpaths pointing to inspect URLS.
            itemInspectElements = browser.find_elements_by_xpath('//*[starts-with(@id,"sell_order_")]/td[2]/div/a')
            #Check if any xpaths were found.
            if itemInspectElements:
                pageLoop += 1
                #Appends attribute 'data-inspecturl' as string to ItemInspectURLList
                for itemInspectElement in itemInspectElements:
                    ItemInspectURLList.append(itemInspectElement.get_attribute('data-inspecturl'))
            #if no new xpaths were found print pageLoop - 1 since we didn't crawl empty page.
            else:
                print('Finished crawling all ', pageLoop - 1, ' pages.')
                break

def downloadImages():
    #counter will be used to name files and keep track of download progress.
    counter = 0
    #Set var with count of URLS inside ItemInspectURLList
    urlCount = len(ItemInspectURLList)
    print('Starting download: ')
    print('Images to download: ', urlCount)
    for ItemInspectURL in ItemInspectURLList:
        #some fresh items have a different 'inspect' button, are gray and can't be scraped.
        if not isinstance(ItemInspectURL, str):
            print('Skipped one item that does not have inspect button.')
            continue
        #Download inspect image and name it 0.png etc.
        urllib.request.urlretrieve(ItemInspectURL, downloadLocation + str(counter) + '.png')
        counter += 1
        #Print download progress every for 10 images downloaded.
        if counter % 10 == 0 or counter == urlCount:
            print('Downloaded: ', counter, '/', urlCount)
    print('Finished downloading all images.')

def main():
    getInspectURLS()
    downloadImages()
    print('Closing selenium web driver...')
    browser.quit()

main()