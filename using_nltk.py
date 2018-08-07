import nltk
import re
import string
from geotext import geotext
import pymongo
from pymongo import MongoClient
from nltk.corpus import stopwords
from selenium import webdriver
#parser to scarp the website of ajio
driver = webdriver.Chrome(r'C:\Users\jatoth.kumar\Downloads\chromedriver_win32 (1)\chromedriver.exe')
driver1 = webdriver.Chrome(r'C:\Users\jatoth.kumar\Downloads\chromedriver_win32 (1)\chromedriver.exe')
driver.get('https://www.ajio.com/s/fresh-men-aeropostale')
list_product = driver.find_elements_by_xpath('//a[@class="rilrtl-products-list__link"]')
description_1 = list_product[0].text
list2 = []
list4 = []
client = MongoClient('localhost',27017)
db = pymongo.MongoClient().webdata
for i in range(len(list_product)):
    print(list_product[i].get_attribute('href'))
    x = list_product[i].get_attribute('href')
    driver1.get(x)
    list3 = []
    list1 = driver1.find_elements_by_xpath('//ul[@class="prod-list"]/li')
    for j in range(len(list1)):
        print(list1[j].text)
        list3.append(list1[j].text)
        list4.append((list1[j].text))
    list2.append(list3)
    db.data1.insert({'data':list2[i]})
    print(list2[i])
    print('####')
db1 = client.webdata
data1 = []
[data1.append(i['data']) for i in db1.data1.find()]
print(data1[1])
lexicon = stopwords.words('english')
grammar = "NP:{<N.*>}"
res = []
res1 = {'clothing type':'','styling':'','zip':'','wash':'','raise':''}
for i in range(len(data1[1])):
    string1 = str(data1[1][i])
    string1 = re.sub(r'\d+','',string1)
    exclude = string.punctuation
    string1 = ''.join(x for x in string1 if x not in exclude)
    print(string1)
    print(nltk.word_tokenize(string1))
    words1 = []
    [print(i) for i in nltk.word_tokenize(string1) if i in lexicon]
    [words1.append(i) for i in nltk.word_tokenize(string1) if i not in lexicon]
    print(nltk.pos_tag(words1))
    words1 = nltk.pos_tag(words1)
    print(words1)
    [print(nltk.ne_chunk(x2)) for x2 in words1]
    x1 = (nltk.RegexpParser(grammar))
    print(x1.parse(words1))
    x7 = x1.parse(words1)
    print("%%%%%")
    x5 = ''
    for i in range(len(x7)):
        print(x7[i])
        if len(x7[i]) == 1:
            x5 = x5 + x7[i][0][0] + ' '
    res.append(x5)
print(res)
res1['clothing type'] = res[0]
res1['styling'] = res[1]
res1['zip'] = res[2]
res1['wash'] = res[3]
res1['raise'] = res[4]
print(res1)
