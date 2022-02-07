# 您需要爬取的网站地址，双引号内，每两个网站之间要有逗号
website = [
    "http://www.baidu.com",
    "https://www.homeforsmes.com.cn/train/type.do?pageNo=1&actType=0&trainTypeId=0",

]

# 与上方网址一一对应的xpath
websiteXpath = [
    "/html/body/div[1]/div[1]/div[5]/div/div/div[3]/ul/li[1]/a/span[2]",
    "/html/body/div[1]/div/div[2]/div/div/div/div[2]/ul/li[1]/a/div",
]

#server酱的sendkey，需要去官网获取
sendkey = "SCT118145TsuYhm9aGlvSSJ0dGxLFQQFOr"
#server酱的推送地址，默认不改
pushURL = "https://sctapi.ftqq.com/"
