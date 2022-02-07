import sqlite3
import time
import threading

from spider import webCrawler


def timeClawler(sql_name, hour_time):

    con = sqlite3.connect(sql_name)  # 打开或创建数据库
    global timer
    timer = threading.Timer(600000, webCrawler(con))
    timer.start()

if __name__ == '__main__':
    sql_name = "Test1.db"
    while True:
        timeClawler(sql_name, 1)

    # cur = con.cursor()  # 获取游标
    # cursor = cur.execute("select id, content, website from messsage")  # 查询当前的所有数据
    # print("\n查询数据库")
    # for row in cursor:
    #     print("id = ", row[0])
    #     print("titl = ", row[1])
    #     print("web = ", row[2],"\n")
    #
    # print("查询完毕")
    # con.close()

