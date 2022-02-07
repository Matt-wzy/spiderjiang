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
    :return:            返回目标值以及状态（return_val, is_OK）
    """

    is_OK = True
    driver.get(website)
    driver.implicitly_wait(10)
    try:
        get_value = driver.find_element_by_xpath(xpath)
        return_val = get_value.text
    except:
        return_val = is_OK
        isOK = False
    return return_val, is_OK

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

    # dataList.append(encode("网站内容变更" + website[8:23]))
    dataList.append(encode(tittle + website[8:23]))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=desp;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode(
        "您监听的网站：" + website + huanhang + "由原来的内容：“" + content_old + "”，变更为：“" + content_new + "“。"
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

def cmpHistory(con, website, content):
    cur = con.cursor()  # 获取游标
    cursor = cur.execute("select id, content, website from messsage")  # 查询当前的所有数据
    new_website = False     # 当为新网址时，值为TRUE
    for data in cursor:
        if website == data[2]:
            new_website = False
            if content != data[1]:  # 此时为新内容，删除原有的数据，并插入新的数据
                del_id = (data[0],)
                del_contt = data[1]
                myPush(website, "网站内容变更", content, del_contt)               # 推送消息
                cur.execute('delete from messsage where id=?', del_id)          # 删除原有数据

                insert_msg = (data[0], content, website)
                cur.execute('insert into messsage values (?, ?, ?)', insert_msg)# 插入新的内容

                break
    if new_website: # 此时为新网址
        cursor = cur.execute("select id from messsage")  # 查询当前的所有数据
        new_id = len(list(cursor))
        insert_msg = (new_id, content, website)
        cur.execute('insert into messsage values (?, ?, ?)', insert_msg)
        con.commit()


def webCrawler(con):
    init_flag = False
    cur = con.cursor()  # 获取游标

    # 防重复建表检查
    try:
        data = cur.execute("SELECT id FROM messsage")
        if len(list(data)) == 0:
            init_flag = True
    except Exception as e:
        print("创建新表：message")
        cur.execute("create table messsage (id, content, website)")  # 创建表
        init_flag = True

    # 自动注册安装webdriver
    driver = webdriver.Edge(EdgeChromiumDriverManager(log_level=20).install())
    insert_id = 1  # 插入序号
    # 进行爬取，获取配置文件内全部网站的内容
    for i in range(len(myconfig.website)):
        return_val, is_OK = getWebDriver(driver, myconfig.website[i], myconfig.websiteXpath[i])
        print(return_val, " and ", is_OK)
        if is_OK:
            if init_flag:       # 如果需要初始化则全部数据都存入数据库内
                insert_msg = (insert_id, str(return_val), str(myconfig.website[i]))  # 如果数据库中为空则要将当前的数据存入到数据库中。
                cur.execute('insert into messsage values (?, ?, ?)', insert_msg)
                con.commit()
                insert_id = insert_id + 1
            else:               # 此时数据库已存在数据，需要进行存入检查、更新、消息推送
                cmpHistory(con, myconfig.website[1], return_val)

    driver.quit()

    # cursor = cur.execute("select id, content, website from messsage")  # 查询当前的所有数据
    # print("\n查询数据库")
    # for row in cursor:
    #     print("id = ", row[0])
    #     print("titl = ", row[1])
    #     print("web = ", row[2],"\n")
    #
    # print("查询完毕")
    # con.close()

# # if __name__ == '__main__':
#
#     # 参数初始化
#     sqlName = "Test1.db"
#     con = sqlite3.connect(sqlName)  # 打开或创建数据库

