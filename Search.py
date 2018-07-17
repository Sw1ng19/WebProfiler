﻿# -*- coding:utf-8 -*-
# Author: Shiyun Li(Swing Leo)
# Mail: lishiyun19@163.com
# Created Time: Tue Oct 19 14:20:55 2017

import time

from selenium.webdriver.common.keys import Keys
from splunk_environment import SplunkEnvironment
from log import logger


class Search():
    def __init__(self, uiutil):
        self.uiutil = uiutil
        self.splunk_env = SplunkEnvironment(c)
        self.host = self.splunk_env.roles['search_head'].agent()  # current host
        self._test_round = 0  # 测试回合

    @property
    def test_round(self):
        return self._test_round

    @test_round.setter
    def test_round(self, value=1):
        self._test_round += value

    def login(self):
        logger.info("Login Test: ")

        self.uiutil.start_recording("Login Test")

        self.uiutil.driver.get("http://%s:%d" % (self.host.hostname, self.splunk_env.port))
        username_ele = self.uiutil.driver.find_element_by_id("username")
        username_ele.send_keys(self.splunk_env.username)
        password_ele = self.uiutil.driver.find_element_by_id("password")
        password_ele.send_keys(self.splunk_env.password)
        login_btn_xpath = "//form[@class='loginForm']//input[@type='submit']"
        login_btn = self.uiutil.driver.find_element_by_xpath(login_btn_xpath)
        login_btn.send_keys(Keys.ENTER)

        self.uiutil.end_recording(self.splunk_env.network, self.splunk_env.search, self.splunk_env.LOGIN_PAGE, self.test_round)
        time.sleep(5)

    def search_element(self):
        logger.info("Search Element: ")
        logger.debug("Current Page: " + self.uiutil.driver.current_url)

        try:
            logger.info("Skip help Splunk: ")
            skip_btn_xpath = "//div[@class='modal-footer']/a[contains(@class,'modal-btn-cancel')]"
            skip_btn = self.uiutil.driver.find_element_by_xpath(skip_btn_xpath)
            skip_btn.send_keys(Keys.ENTER)  # keyboard events
            time.sleep(5)
        except:
            pass

        self.uiutil.start_recording("Search Element")
        search_ele_xpath = "//div/a[contains(@href, 'app/search')]"
        search_ele_btn = self.uiutil.driver.find_element_by_xpath(search_ele_xpath)
        search_ele_btn.send_keys(Keys.ENTER)
        self.uiutil.end_recording(self.splunk_env.network, self.splunk_env.search, self.splunk_env.SEARCH_PAGE, self.test_round)
        time.sleep(5)

    def spl_search(self):
        logger.info("SPL Search Test: ")
        logger.debug("Current Page: " + self.uiutil.driver.current_url)

        splunk_version = self.splunk_env.splunk_version()
        if splunk_version == 'Minty':
            search_xpath = "//textarea"
            button_xpath = "//table[@class='search-bar']//a[@class='btn']"
        elif splunk_version == 'Kimono':
            search_xpath = "//textarea"
            button_xpath = "//table[@class='search-bar']//a[@class='btn']"
        elif splunk_version == 'Ivory':
            search_xpath = "//div/pre/textarea"
            button_xpath = "//td[@class='search-button']//a[@class='btn']"
        elif splunk_version == 'Galaxy':
            search_xpath = "//div/textarea"
            button_xpath = "//td[@class='search-button']//a[@class='btn']"
        else:
            search_xpath = "//textarea"
            button_xpath = "//table[@class='search-bar']//a[@class='btn']"

        self.uiutil.start_recording("SPL Search Test")
        keywords_ele = self.uiutil.driver.find_element_by_xpath(search_xpath)
        keywords_ele.send_keys(self.splunk_env.spl)
        search_btn = self.uiutil.driver.find_element_by_xpath(button_xpath)
        self.uiutil.driver.execute_script("$(arguments[0]).click()", search_btn)

        self.uiutil.end_recording(self.splunk_env.network, self.splunk_env.search, self.splunk_env.SEARCH_PAGE, self.test_round)
        time.sleep(5)

    def logout(self):
        logger.info("Logout Test: ")

        self.uiutil.start_recording("Logout Test")
        self.uiutil.driver.get("http://%s:%d/en-US/account/logout" % (self.host.hostname, self.splunk_env.port))
        self.uiutil.end_recording(self.splunk_env.network, self.splunk_env.search, self.splunk_env.LOGOUT_PAGE, self.test_round)
        time.sleep(5)