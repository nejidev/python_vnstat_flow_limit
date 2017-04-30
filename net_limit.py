#!/usr/bin/python
#coding:utf-8
'''
author:ningci dev
date:2017-04-30 05:54
此python 脚本检测网卡流量使用情况，当达到设定值时，就会使用 iptables 关闭 80 443 
'''
import time
import os
import re
import string
import commands
import subprocess

#每天限制流量使用450M
DAY_LIMIT_OF_MB = 450
#流量未超时每5分钟检查一次
INTVAL_NORMAL   = 300
#流量超出后每1小时检查一次
INTVAL_SLEEP    = 3600

class NetLimit:

	def __net_up(self):
		os.system("iptables -F")
		self.inteval = INTVAL_NORMAL

	def __net_down(self):
		os.system("iptables -A OUTPUT -p tcp --dport 80  -j REJECT")
		os.system("iptables -A OUTPUT -p tcp --dport 443 -j REJECT")
		self.inteval = INTVAL_SLEEP

	def __check_flow(self):
		#经过测试 commands.getstatusoutput 返回结果不能使用 正则拆分
		#vnstat_days = commands.getstatusoutput("vnstat -i eth0 -d")
		vnstat_days = subprocess.check_output(["vnstat", "-i", "eth0", "-d"])
		'''
		数据格式 这里是随便手写的不是真实的
		eth0  /  daily

	         day         rx      |     tx      |    total    |   avg. rate
	     ------------------------+-------------+-------------+---------------
	     01/01/2018    10.00 MiB |   10.00 MiB |   20.00 MiB |    6.58 kbit/s
	     01/02/2018    10.00 MiB |   20.00 MiB |   30.00 MiB |   10.36 kbit/s
	     ------------------------+-------------+-------------+---------------
	     estimated        --     |      --     |      --     |

		'''
		#使用正则匹配每行匹配当前日期
		vnstat_rows = re.findall(r"([\d|/]{10})\s+([\w\.\s]+)[^\d]+([\w\.\s]+)[^\d]+([\w\.\s]+)", vnstat_days)
		#输出格式 [('01/01/2018', '10.00 MiB ', '10.00 MiB ', '20.00 MiB '), ('01/02/2018', '10.00 MiB ', '20.00 MiB ', '30.00 MiB ')]
		for vnstat_row in vnstat_rows:
			#比较当前日期
			if time.strftime("%m/%d/%Y", time.localtime(time.time())) == vnstat_row[0]:
				total_day = vnstat_row[3]
				#查询 流量单位 MiB , KiB 忽略不计
				if 0 < total_day.find("MiB"):
					#果然是不如 PHP 方便，PHP 可以直接转为 int 
					#使用 空格拆分取数字
					total_day = string.atof(total_day.split(" ")[0])
					if total_day > DAY_LIMIT_OF_MB:
						return True
		return False
	
	def __init__(self):
		self.__net_up()
		#设定每5分钟执行一次
		self.inteval = INTVAL_NORMAL

	def run(self):
		while True:
			self.__net_down() if self.__check_flow() else self.__net_up()
			print("run ..")
			time.sleep(self.intval)

NetLimit().run()

