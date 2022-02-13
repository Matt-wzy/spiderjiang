import time
import myconfig
import http.client
import sqlite3
import mimetypes

from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from codecs import encode

# markdown换行，不知道有无更优雅的实现
huanhang = '''

    --- 

'''

def getWebDriver(driver, website, xpath):
    """
    通过webdriver获取内容，包装为函数
    :param driver:      浏览器驱动
    :param website:     目标网址
    :param xpath:       目标区域路径
    :return:            返回目标值以及状态（returnval, isOK）
    """

    isOK = True
    driver.get(website)
    driver.implicitly_wait(10)
    try:
        getvalue = driver.find_element_by_xpath(xpath)
        returnval = getvalue.text
    except:
        returnval = isOK
        isOK = False
    return returnval, isOK

def myPush(website, tittle, content_new, content_old=''):
    """
    推送消息方法，内部参数全为字符串类型
    :param website:      网址
    :param tittle:       标题
    :param content_new:  新内容
    :param content_old:  旧内容
    :return:             NULL
    """

    conn = http.client.HTTPSConnection("sctapi.ftqq.com")
    dataList = []
    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=title;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("网站内容变更" + website[8:23]))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=desp;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode(
        "您监听的网站：" + website + huanhang + "由原来的内容：" + content_old + "变更为：" + content_new
    ))
    dataList.append(encode('--' + boundary + '--'))
    dataList.append(encode(''))
    body = b'\r\n'.join(dataList)
    payload = body
    headers = {
        'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
    }
    URL1 = "/"+myconfig.sendkey+".send"
    conn.request("POST", URL1, payload, headers)
    res = conn.getresponse()


# 自动注册安装webdriver
driver = webdriver.Edge(EdgeChromiumDriverManager(log_level=20).install())
list_insert = []  # 多行数据列表
id_insert = 1  # 插入序号
# 进行爬取，获取配置文件内全部网站的内容
for i in range(len(myconfig.website)):
    returnval, isOK = getWebDriver(driver, myconfig.website[i], myconfig.websiteXpath[i])
    print(returnval, " and ", isOK)
    if isOK:
        list_insert.append((id_insert, str(returnval)))
        id_insert = id_insert + 1
    # myPush(myconfig.website[i],"网站内容变更",returnval)

driver.quit()

sqlName = 'example12345.db'
con = sqlite3.connect(sqlName)  # 打开或创建数据库
cur = con.cursor()  # 获取游标

cur.execute("create table messsage (id, context)")  # 创建表
cur.executemany("insert into messsage values (?, ?)", list_insert)  # 多行数据同时插入
cursor = cur.execute("select id, context from messsage")  # 查询当前的所有数据

print("\n查询数据库")
for row in cursor:
    print("id = ", row[0])
    print("titl = ", row[1], "\n")

print("查询完毕")
con.close()