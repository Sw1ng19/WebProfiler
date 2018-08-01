# WebAutomation
本项目是基于 Selenium 的 Web 自动化测试实践，通过模拟用户点击行为功能，对 Splunk 客户端进行全方位覆盖测试和性能分析。注：本 Repo 只是整个 Web 自动化测试实践的极小一部分用例，冰山一角，请大家谅解，重要的是学习和掌握方法。建议完整项目结构如下：  
```
web_profiler  
    |--config（配置文件）  
    |--data（数据文件）  
    |--drivers（驱动）  
    |--log（日志）  
    |--report（报告）  
    |--test（测试用例）  
    |--utils（公共方法）  
    |--ReadMe.md  
```

### Selenium 
Selenium 是一个专门用于 Web 应用程序测试的工具了，它能直接运行在浏览器中，就像真正的用户在操作一样，支持常用的浏览器包括 Firefox 和 Chrome 等。
#### Python 依赖包安装
```
pip install -U selenium
```

### Geckodriver
Geckodriver 是 Firefox 官方推出的浏览器驱动程序，Chrome 对应的是 Chrome Driver。由于操作系统历史原因，Linux 服务器上浏览器大多是 Firefox，因此，如果你希望能在 Jenkins 上持续集成测试，那么建议还是使用 Geckodriver 更方便。
#### 下载安装
```
wget -c https://github.com/mozilla/geckodriver/releases/download/v0.16.0/geckodriver-v0.16.0-linux64.tar.gz
```
建议将 Geckodriver 拷贝到系统环境变量执行目录中：
```
tar -zxvf geckodriver-v0.16.0-linux64.tar.gz -C /usr/bin
```
否则，运行时再指定 Geckodriver 路径有时候容易报错：
```
No such file or directory: 'geckodriver'
# 或者
The 'geckodriver' needs to be in PATH
```
注意：UI 自动化测试对软件版本信息特别敏感，如果 Geckodriver 和 Selenium 版本号对不上，就会报无法执行的错误：
```
OSError: [Errno 8] Exec format error
```

### BrowserMobProxy
BrowserMob-Proxy 在 HTTP 浏览器中设置代理，能够抓取并返回客户端和服务器之间所有的请求通信细节，最后将数据保存成为 HAR 文件。BMP 运行有两种模式，一是嵌入式模式是通过 Java Netty 服务器来启动代理运行；二是独立运行模式则可以通过 cURL 命令行来运行，然后通过 RESTful API 返回结果。
#### 下载安装
```
wget -c https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy-2.1.4/browsermob-proxy-2.1.4-bin.zip
```
将 BMP 解压后拷贝到指定执行目录中即可。

### 虚拟 Display
在 Linux 系统下运行浏览器需要启动系统显示服务，不然就会报错：
```
Error: GDK_BACKEND does not match available displays
```
本项目通过设置 Xvfb 和 Gtk 来虚拟这个显示服务：
```
apt-get install xvfb libgtk-3-dev
pip install pyvirtualdisplay
```
注：上述方法是在我的 Debian Docker 机上运行的，如果使用其他 Linux 发行版，可能实现的方法不一致，请大家自行验证。

### 精髓
本 Repo 虽然只截取了很少一部分用例，但麻雀虽小五脏俱全，基本上覆盖了常见的性能测试重难点：
#### id/xpath 元素定位
```Python
self.uiutil.driver.get("http://%s:%d" % (self.host.hostname, self.splunk_env.port))
# by id
username_ele = self.uiutil.driver.find_element_by_id("username")
username_ele.send_keys(self.splunk_env.username)
password_ele = self.uiutil.driver.find_element_by_id("password")
password_ele.send_keys(self.splunk_env.password)
# by xpath
login_btn_xpath = "//form[@class='loginForm']//input[@type='submit']"
login_btn = self.uiutil.driver.find_element_by_xpath(login_btn_xpath)
login_btn.send_keys(Keys.ENTER)
```

#### 动态加载问题
如果能直接准确的定位到动态元素 XPath：
```Python
keywords_ele = self.uiutil.driver.find_element_by_xpath(search_xpath)
keywords_ele.send_keys(self.splunk_env.spl)
search_btn = self.uiutil.driver.find_element_by_xpath(button_xpath)
# 调用 js 执行 Click 事件
self.uiutil.driver.execute_script("$(arguments[0]).click()", search_btn)
```
否则，可以尝试先加载页面，然后再在页面中寻找动态元素：
```Python
from tornado_fetcher import Fetcher

fetcher=Fetcher (
    user_agent='phantomjs', 
    phantomjs_proxy='http://localhost:12306', 
    poolsize=10, 
    async=False
)
fetcher.phantomjs_fetch(url)
fetcher.phantomjs_fetch(url, js_script='function(){setTimeout("window.scrollTo(0,100000)}", 1000)')
```

#### 弱网测试
```Python
# analog network
if test_network == 'cable':
    self.bandwidth = Network.cable.value
elif test_network == 'dsl':
    self.bandwidth = Network.dsl.value
elif test_network == 'mobile_4g':
    self.bandwidth = Network.mobile_4g.value
elif test_network == 'mobile_3g':
    self.bandwidth = Network.mobile_3g.value
else:
    self.bandwidth = Network.cable.value
self.proxy = self.uitools.start_proxy(proxy_path, self.bandwidth)
self.driver = self.uitools.start_driver()
```
#### 性能监控
Linux 系统中 /proc 文件虚拟系统允许用户进程与内核内部数据交互的伪文件系统，使得用户进程可以在系统运行时动态更改内核信息，而不需要重新引导内核系统。该目录中主要包含如下参数：  

|文件名|描述|  
| ------ | ------ |  
|APM|高级电源管理|  
|CPUINFO|CPU 信息|  
|IOPORTS|进程占用 IO 端口|  
|LOADAVG|系统平均负载均衡|  
|MEMINFO|内存信息|  
|NET|网络协议信息|  
|PCI|PCI 设备信息|  
|STAT|这个选项包含信息比较多，包括 CPU 利用率，磁盘，内存页，内存对换，全部中断，接触开关以及自举时间等|  
|SWAPS|交换分区信息|  

#### CPU
```Python
with open('/proc/CPUinfo') as f:
    for line in f:
        if not line.strip():
            # end of one processor
            CPUinfo['proc%s' % nprocs] = procinfo
            nprocs=nprocs+1
            # Reset
            procinfo=OrderedDict()
        else:
            if len(line.split(':')) == 2:
                procinfo[line.split(':')[0].strip()] = line.split(':')[1].strip()
            else:
                procinfo[line.split(':')[0].strip()] = ''
```

#### Mem
```Python
with open('/proc/meminfo') as f:
    for line in f:
        meminfo[line.split(':')[0]] = line.split(':')[1].strip()
```

#### I/O
```Python
# RX
ifstat = open('/proc/net/dev').readlines()
	for interface in ifstat:
		if INTERFACE in interface:
			stat = float(interface.split()[1])
			STATS[0:] = [stat]
            
# TX
ifstat = open('/proc/net/dev').readlines()
	for interface in ifstat:
		if INTERFACE in interface:
			stat = float(interface.split()[9])
			STATS[1:] = [stat]
```
