from MyClass import Logger
from MyClass import MySql
from selenium import webdriver  #导入Selenium
import re
import urllib3
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup  #导入BeautifulSoup 模块
import requests #导入requests 模块
import threading

logger = Logger('log.txt', 1, 'kk').getlog()
def getpage(url):
    print('开始网页请求....')
    opt = Options()
    # 把chrome设置成无界面模式
    opt.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=opt)
    try:
        driver.get(url)
    except Exception as err:
        logger.info('链接:'+str(url)+'失败！'+err)
        return 'error'
    return driver.page_source
    #print(driver.page_source)
def get_type_url():
    mysql = MySql('127.0.0.1', 'sa', '873196023', 'movie')
    response = urllib3.urlopen("http://www.dytt8.net/")
    page_source=response.read()
    if page_source=='error':
        return
    all_div = BeautifulSoup(page_source, 'lxml').findAll('div', class_='contain')  # 获取网页中的class为cV68d的所有div标签
    div=all_div[1]
    all_a=div.findAll('a')
    for h in all_a:
        h.attrs['href']
        re=mysql.selectData("select IsFW from T_Url where Url = '"+h.attrs['href']+"'")
        #re = mysql.selectData("select IsFW from T_Url where Url = 'qwe'")
        if len(re)==0:

            mysql.insertdata("insert into T_Url(Url) values('"+h.attrs['href']+"'")
            #mysql.insertdata("insert into T_Url(Url) values('qwe'")
        else:
            print(re[0][0])
            pass



def get_xinxi_url1(type_url):
    page_source=getpage(type_url)
    pass


get_type_url()