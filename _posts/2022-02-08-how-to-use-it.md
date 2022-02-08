---
layout: post
title: 开源代码使用教程
tags:
  - 使用说明
comments: true
---


Hi, there

首先，欢迎使用本开源代码，使用代码前，您需要一定的环境配置才能正常使本源代码发挥其应有作用。

步骤1：安装Python [py官方3.10.2下载地址,windows](https://www.python.org/ftp/python/3.10.2/python-3.10.2-amd64.exe) 

步骤2： 安装第三方库，在源代码位置打开cmd并执行

```bash
pip install -r requirements.txt 
```

步骤3： 正确配置server酱并获取key。

server酱[官网](https://sct.ftqq.com/sendkey) 

步骤4： 正确编辑myconfig.py，填入您需要爬取的网站以及需要爬取的位置的xpath路径，填入您的server酱key

步骤5： 在源代码位置打开cmd并运行：

```bash
python DemoSpider.py
```

