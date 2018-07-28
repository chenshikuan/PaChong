from selenium import webdriver  #导入Selenium
from selenium.webdriver.common.keys import Keys  #导入Keys
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup  #导入BeautifulSoup 模块
import os  #导入os模块
import pymssql
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
# 开发一个日志系统， 既要把日志输出到控制台， 还要写入日志文件
import logging
import time
#用字典保存日志级别
format_dict = {
   1: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   2: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   3: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   4: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   5: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
}


class Logger():
    def __init__(self, logname, loglevel, logger):
        '''
           指定保存日志的文件路径，日志级别，以及调用文件
           将日志存入到指定的文件中
        '''

        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(logname)
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = format_dict[int(loglevel)]
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def getlog(self):
        return self.logger

def get_url(web_url):
    print('开始网页get请求')
    # 创建chrome参数对象
    opt = Options()
    # 把chrome设置成无界面模式
    opt.add_argument('--headless')
    driver = webdriver.Chrome(options=opt)
    driver.get(web_url)
    #print(driver.page_source)
    #self.scroll_down(driver=driver, times=3)  #执行网页下拉到底部操作，执行3次
    print('开始获取所有a标签')
    all_a = BeautifulSoup(driver.page_source, 'lxml').findAll('div', class_='co_content2')  #获取网页中的class为cV68d的所有div标签

    for a in all_a:
        herf = a("a")
        logger.info('herfNumber:'+str(len(herf)))
        i = 0
        for h in herf:
            if 'href' in h.attrs.keys():
                name = h.text
                threading.TIMEOUT_MAX = 30
                t = threading.Thread(target=get_magn, args=(web_url+h.attrs['href'], name))
                t.start()
                while threading.active_count() > 15:
                    #print('the numbers of current thread is ' + str(threading.active_count()))
                    time.sleep(1)

    while threading.active_count() > 1:
        time.sleep(1)


infoDic = {}
lock = threading.Lock()


def get_magn(url, name):

    print('the current thread\'name is '+threading.current_thread().name)
    logger.info(url)
    opt = Options()
    # 把chrome设置成无界面模式
    opt.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=opt)
    try:
        driver.get(url)
        SoupTbody = BeautifulSoup(driver.page_source, 'lxml').find('div', class_='co_content8')
        child = SoupTbody.find('a')
        magn_url = child.attrs['href']
        lock.acquire()
        infoDic[name] = magn_url
        lock.release()
        logger.info('movieName:'+name+'--movieMagn:'+magn_url)
        driver.quit()
    except Exception as err:
        print("A exception happened " + str(err))


def insertDB():
    result = []
    try:
        conn = pymssql.connect(host='127.0.0.1', user='sa', password='******', database='movie', charset='utf8')
    except Exception as err:
        print('数据库链接错误：' + str(err))
        return
    for key in infoDic:
            u=(key,infoDic[key])
            result.append(u)
    sql = 'insert into T_movie(movieName,movieURL) values(%s,%s)'
    try:
        cursor = conn.cursor()
        cursor.executemany(sql, result)
        conn.commit()
    except Exception as err:
        conn.rollback()
        print("A sql'exception happened " + str(err))
    finally:
        conn.close()





#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}  #给请求指定一个请求头来模拟chrome浏览器
web_url = 'http://www.dytt8.net'  #要访问的网页地址

logger = Logger('log.txt', 1, 'kk').getlog()
get_url(web_url)
insertDB()
