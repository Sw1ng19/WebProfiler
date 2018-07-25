FROM debian:stretch
MAINTAINER lishiyun19@163.com

# 安装依赖包
RUN apt-get install openjdk-8-jdk xvfb libgtk-3-dev python-dateutil bzip2
RUN pip install -U pyvirtualdisplay selenium browsermob-proxy

# 安装 Firefox
ADD https://ftp.mozilla.org/pub/firefox/releases/52.3.0esr/linux-x86_64/en-US/firefox-52.3.0esr.tar.bz2 /root/firefox-52.3.0esr.tar.bz2
RUN cd root && tar -jxvf firefox-52.3.0esr.tar.bz2 -C /opt
RUN rm /root/firefox-52.3.0esr.tar.bz2
RUN ln -s /opt/firefox/firefox /usr/bin/firefox

# 安装 geckdriver
ADD https://github.com/mozilla/geckodriver/releases/download/v0.16.0/geckodriver-v0.16.0-linux64.tar.gz /root/geckodriver-v0.16.0-linux64.tar.gz
RUN cd root && tar -zxvf geckodriver-v0.16.0-linux64.tar.gz -C /usr/bin
Run rm /root/geckodriver-v0.16.0-linux64.tar.gz
