#This is a use of python and vnstat to control, vps, daily traffic limits
## Implement
	iptables -A OUTPUT -p tcp --dport 80  -j REJECT and iptables -A OUTPUT -p tcp --dport 443  -j REJECT 
	recover iptables -F
	default python 2.7 test ok, python3 not test
	edit NetLimit.py DAY_LIMIT_OF_MB = 450 define Number
	
## Usage
### centOS 7.5 
	yum -y install iptables
	yum -y install iptables-services
	systemctl stop firewalld
	systemctl disable firewalld
	systemctl enable iptables.service
	systemctl start iptables.service
	wget http://humdi.net/vnstat/vnstat-1.13.tar.gz
	tar -xvf vnstat-1.13.tar.gz
	cd vnstat-1.13/
	make
	make install
	mkdir /var/lib/vnstat
	mkdir /var/log/vnstat
	vnstat --create -i ens33
	vi /etc/vnstat.conf
	Interface "ens33"
	chmod +x *
	vnstatd -d
	./run.sh &
	or write /etc/rc.local

## Update
	add centOS 7.5 setup method
	compatibility vnStat sort date
	add match GB out
	add run.sh
	add mini vnstat.php 
	
## 中文介绍
	本软件采用 vnstat 做流量统计使用 python 配和 iptables 进行流量限制。
	可以通过编辑NetLimit.py 中的 DAY_LIMIT_OF_MB 来设置每天的流量限制。
	仅在 centOS 7.5 python 2.x 下测试 其它未做测试，如果有问题可以反馈给我。
	
## 修改更新
	添加 centOS 7.5 下配置方法
	兼容 vnStat 1.15 返回的短日期的问题
	增加 run.sh 解决非 en.US 语言下不能使用的问题

