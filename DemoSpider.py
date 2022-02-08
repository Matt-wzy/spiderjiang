import sqlite3
import schedule

from spider import webCrawler

if __name__ == '__main__':
    sql_name = "Test4.db"            # 数据库名称
    run_T = 1                        # 运行周期,以小时为单位
    con = sqlite3.connect(sql_name)  # 打开或创建数据库

    schedule.every(run_T).hour.do(webCrawler,con)

    while True:
        schedule.run_pending()