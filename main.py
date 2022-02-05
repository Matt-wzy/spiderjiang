import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import http.client
import mimetypes
from codecs import encode
import myconfig


# markdown换行，不知道有无更优雅的实现
huanhang = '''

--- 


'''


# 通过webdriver获取内容，包装为函数
def mywebdriverget(driver,website,xpath):
    isOK = True
    driver.get(website)
    driver.implicitly_wait(10)
    try:
        getvalue = driver.find_element_by_xpath(xpath)
        returnval = getvalue.text
    except:
        returnval = isOK
        isOK = False
    return returnval,isOK

# 推送消息方法，内部参数全为字符串类型
def myPush(website,tittle,contentnew,contentold = ''):

    conn = http.client.HTTPSConnection("sctapi.ftqq.com")
    dataList = []
    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=title;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("网站内容变更"+website[8:23]))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=desp;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode(
        "您监听的网站："+website+huanhang+"由原来的内容："+contentold+"变更为："+contentnew
        ))
    dataList.append(encode('--'+boundary+'--'))
    dataList.append(encode(''))
    body = b'\r\n'.join(dataList)
    payload = body
    headers = {
    'Content-type': 'multipart/form-data; boundary={}'.format(boundary) 
    }
    conn.request("POST", "/SCT117948TUYjOU1lngouS7OsRSg1otScG.send", payload, headers)
    res = conn.getresponse()
    # data = res.read()
    # print(data.decode("utf-8"))


# 自动注册安装webdriver
driver = webdriver.Edge(EdgeChromiumDriverManager(log_level=20).install())
# 进行爬取，获取配置文件内全部网站的内容
for i in range(len(myconfig.website)):
    returnval,isOK = mywebdriverget(driver,myconfig.website[i],myconfig.websiteXpath[i])
    print(returnval," and ",isOK)
    myPush(myconfig.website[i],"网站内容变更",returnval)
    # myPush(driver,myconfig.website[i],"网站内容变更","您监听的网站 "+myconfig.website[i]+" 内容变更为： "+returnval)
    # [8:23]
    print(i)
    
    pass
driver.quit()

