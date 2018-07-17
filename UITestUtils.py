# -*- coding:utf-8 -*-
# Author: Shiyun Li
# Mail: lishiyun19@163.com
# Created Time: Tue Oct 19 14:20:55 2017

from dispatcher import Dispatcher
from log import logger
from network import Network
from uitools import UITools


class UITestUtils:
    driver = None
    proxy = None
    bandwidth = None

    def __init__(self):
        self.size = (1920, 1080)  # default screen size
        self.uitools = UITools()
        self.dispatcher = Dispatcher()

    def init_uitest_env(self, proxy_path, test_network):
        """
        init ui test environment, including Linux server browser display status, webdriver, proxy.

        :param proxy_path: browsermob-proxy dir location.
        :param test_network: network status.
        :return: browsermob-proxy, selenium webdriver
        """
        logger.info("Init UI Test Environment: ")

        self.uitools.start_display(self.size)

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
        return self.proxy, self.driver

    def start_recording(self, har_name):
        logger.info("Start Recording: ")
        self.proxy.new_har(har_name)

    def end_recording(self, test_network, test_case, page_name, test_round):
        logger.info("End Recording: ")

        # wait until page get fully loaded
        self.proxy.wait_for_traffic_to_stop(1, 60)

        # get browsermob-proxy result
        results = self.proxy.har
        logger.info(results)

        # record ui test fields
        fields = {'test_network': test_network, 'test_case': test_case, 'page_name': page_name,
                  'test_round': test_round}
        logger.info("UI Test Fields: " + str(fields))

        self.dispatcher.update_results(results, fields)  # upload results to UCP server

    def destroy_uitest_env(self):
        logger.info("Destroy UI Test Environment: ")

        self.uitools.stop_driver()
        self.uitools.stop_proxy()
        self.uitools.stop_display()