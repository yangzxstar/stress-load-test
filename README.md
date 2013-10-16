stress-load-test
================

这是用python写的一个简单web压力测试工具！


使用方法

一个有三个参数：要压测的url地址，每个线程的目标qps，开启的压测线程数量

比如压测google主页：
进入src目录执行 python stress.py http://www.google.com 50 3

日志在src/log下：查看日志，执行 tail -f log/app.log
