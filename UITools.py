# -*- coding:utf-8 -*-
# Author: Shiyun Li
# Mail: lishiyun@163.com
# Created Time: Tue Oct 19 14:20:55 2017

from selenium import webdriver
from browsermobproxy import Server
from pyvirtualdisplay import Display
from log import logger
from network import Network


class UITools:
    def __init__(self):
        self.display = None
        self.server = None
        self.proxy = None
        self.driver = None

    def start_display(self, display_size=(1920, 1080)):
        """
        display must be set false before start proxy on linux,
        you may ignore this method on Win or Mac.
        """
        logger.info("Start display: ")
        self.display = Display(visible=0, size=display_size)
        self.display.start()

    def start_proxy(self, proxy_path, bandwith=Network.cable.value):
        """
        init browsermob-proxy, limit network status.

        :param proxy_path: proxy dir location
        :param bandwith: analog network bandwith
        :return: browsermob-proxy
        """
        logger.info("Init browsermob-proxy: ")

        self.server = Server(proxy_path)
        self.server.start()  # init server
        self.proxy = self.server.create_proxy()
        self.proxy.limits(bandwith)  # limit bandwidth
        self.proxy.blacklist("http://.+:8000/en-US/splunkd/__raw/services/messages.+", 200)  # limit url requests
        return self.proxy

    def start_driver(self):
        """
        init firefox driver, using with browsermob-proxy.

        :return: selenium webdriver
        """
        logger.info("Init web driver: ")

        profile = webdriver.FirefoxProfile()
        """
            set_proxy() method has been deprecated by selenium3, however, 
            currently there is no better way to work with browsermob-proxy.
        """
        profile.set_proxy(self.proxy.selenium_proxy())
        self.driver = webdriver.Firefox(firefox_profile=profile)
        return self.driver

    def stop_proxy(self):
        logger.info("Stop proxy: ")
        self.server.stop()

    def stop_driver(self):
        logger.info("Stop driver: ")
        self.driver.quit()

    def stop_display(self):
        logger.info("Stop display: ")
        self.display.stop()