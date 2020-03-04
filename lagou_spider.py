#encoding:utf-8
from selenium import webdriver
import os
import time
from lxml import etree
import re

class lagou():
    def __init__(self, driver):
        self.driver = driver

    #点击页面按钮
    def run(self):
        for page in range(1, 31):
            page_button = self.driver.find_element_by_xpath("//div[@class='pager_container']/span[@page=%d]" % page)
            page_button.click()
            self.parse_position()
            break

    #获取每页的所有职位url
    def parse_position(self):
        source = self.driver.page_source
        html = etree.HTML(source)
        alist = html.xpath("//a[@class='position_link']/@href")
        for a in alist:
            self.driver.execute_script("window.open('%s')" % a)
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.parse_position_detail()
            time.sleep(3)
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

    #输出每个职位的相关信息：职位名、职位要求、职位诱惑、职位描述
    def parse_position_detail(self):
        source = self.driver.page_source
        html = etree.HTML(source)
        job_name = html.xpath("//div[@class='job-name']/h1[@class='name']/text()")[0]
        print(job_name)
        job_request = html.xpath("//dd[@class='job_request']")[0]
        new_job_request = re.sub(r'<.*?>| [\n+\s+]', '', etree.tostring(job_request, encoding='utf-8').decode('utf-8'))
        print(new_job_request)
        job_advantage = html.xpath("//dd[@class='job-advantage']")[0]
        new_job_advantage = re.sub(r'<.*?>| [\n+\s+]', '', etree.tostring(job_advantage, encoding='utf-8').decode('utf-8'))
        print(new_job_advantage)
        job_bt = html.xpath("//dd[@class='job_bt']")[0]
        new_job_bt = re.sub(r'<.*?>| [\n+\s+]', '',etree.tostring(job_bt, encoding='utf-8').decode('utf-8'))
        print(new_job_bt)
        print('='*30)

def main():
    #创建chromedriver驱动器
    driver_path = os.getcwd() + r'\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=driver_path)

    # 进入拉勾网搜索python关键字
    driver.get('https://www.lagou.com/')
    driver.switch_to.window(driver.window_handles[1])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    aEle = driver.find_element_by_xpath("//p[@class='checkTips']/a[@class='tab focus']")
    aEle.click()
    searchInput = driver.find_element_by_id('search_input')
    searchInput.send_keys('python')
    searchButton = driver.find_element_by_id('search_button')
    searchButton.click()
    gei_button = driver.find_element_by_class_name('body-btn')
    gei_button.click()

    p = lagou(driver)
    p.run()

if __name__ == '__main__':
    main()