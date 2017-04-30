This is a use of python and vnstat to control, vps, daily traffic limits

通过 iptables -A OUTPUT -p tcp --dport 80  -j REJECT 和 iptables -A OUTPUT -p tcp --dport 443  -j REJECT 来禁止出站

通过 iptables -F 来恢复

bash shell 不太熟悉，使用 python 2.7 来实现 （python3 未测试也许可以）

通过 os.system("iptables -A OUTPUT -p tcp --dport 80  -j REJECT") 来添加 iptables rule

读取 vnstat 的显示结果通过 commands.getstatusoutput("vnstat -i eth0 -d")  或 subprocess.check_output(["vnstat", "-i", "eth0", "-d"])

但经过测试发现 commands.getstatusoutput("vnstat -i eth0 -d") 结果，只可以 print 输入，不可以在使用 正则 来拆分出想要的结果。

所以本文使用 subprocess.check_output(["vnstat", "-i", "eth0", "-d"])

可以修改NetLimit.py 中的 DAY_LIMIT_OF_MB = 450 来定义你的流量使用限制

使用方法，sudo python2.7 NetLimit.py &


