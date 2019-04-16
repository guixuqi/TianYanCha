import json
import re
import time
from collections import OrderedDict
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class TianYanCha:
	
	def __init__(self, driver):
		self.url = 'https://m.tianyancha.com'
		self.driver = driver
		self.UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'

	#发送请求
	def send_request(self, company):
		#设置请求头
		options = webdriver.ChromeOptions()
		# 设置中文
		options.add_argument('lang=zh_CN.UTF-8')
		# 更换头部
		options.add_argument(self.UA)
		try:
			self.driver.get(self.url)
			time.sleep(1)
			input = self.driver.find_element_by_id('live-search')
			input.send_keys(company)
			# dev = self.driver.find_element_by_class_name('input-group-addon')
			dev = self.driver.find_element_by_xpath('//*[@class="input-submit"]/i')
			dev.click()
			element = WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_elements_by_xpath('//div[@class="col-10 search-name"]/a')[0])
			element.click()
		except Exception as e:
			raise '请求天眼查失败:'.format(e)
		
	#提取数据
	def get_content(self, company):
		dict = OrderedDict()
		browser = self.driver
		#公司名称
		# name = browser.find_element_by_xpath('//div[@class="f18 new-c3 float-left"]').text
		try:
			name = browser.find_element_by_xpath('//div[@class="title-name"]').text
		except:
			return dict
		if not re.search(company, name):
			return dict
		dict['公司名称']=name
		#基本信息[基本信息,企业关系图,股权结构图,主要人员,股东信息,对外投资,变更信息,企业年报,分支机构,核心团队,企业业务,竞品信息]
		#基本信息
		self.info1(browser,dict)
		#企业关系图
		self.info2(browser,dict)
		#股权结构图
		self.info3(browser,dict)
		#主要人员
		self.info4(browser,dict)
		#股东信息
		self.info5(browser,dict)
		#对外投资
		self.info6(browser,dict)
		#变更信息
		self.info7(browser,dict)
		#企业年报
		self.info8(browser,dict)
		#分支机构
		self.info20(browser,dict)
		#核心团队
		self.info9(browser, dict)
		#企业业务
		self.info10(browser,dict)
		#竞品信息
		self.info11(browser,dict)
		#司法信息[法律诉讼,法院公告,被执行人,行政处罚,股权出质]
		# self.info12(browser,dict)
		# self.info13(browser,dict)
		# self.info14(browser,dict)
		# self.info15(browser,dict)
		# self.info16(browser,dict)
		#经营状况[招聘信息,税务评级,产品信息,抽查检查,招投标,债券信息,购地信息]
		# 招聘信息
		self.info17(browser,dict)
		# 税务评级
		self.info18(browser,dict)
		# 产品信息
		self.info19(browser,dict)
		# 抽查检查
		self.info21(browser,dict)
		# 招投标
		self.info22(browser,dict)
		# 债券信息
		self.info23(browser,dict)
		# 购地信息
		self.info24(browser,dict)
		# js = json.dumps(dict, indent=4, separators=(',', ':'),ensure_ascii=False)
		# print(js)
		return dict

	#基本信息
	def info1(self,browser,dict):
		dict1 = OrderedDict()
		try:
			title = browser.find_element_by_id('nav-main-baseInfo').text
			contents = browser.find_elements_by_xpath('//div[@class="content-container pb10"]/div')
			for con in contents:
				span = con.find_elements_by_xpath('./span')
				key = span[0].text.split('：')[0]
				dict1[key]=span[1].text
			dict[title]=dict1
		except:
			dict['基本信息']={}
	#企业关系
	def info2(self,browser,dict):
		try:
			div = browser.find_element_by_xpath('//div[@id="nav-main-graphInfo"]')
			title = div.find_element_by_xpath('./div').text
			src = div.find_element_by_xpath('../a/img').get_attribute('src')
			dict[title] = src
		except:
			dict['企业关系']={}
	#股权结构
	def info3(self,browser,dict):
		try:
			div = browser.find_element_by_xpath('//div[@id="nav-main-equityStructure"]')
			title = div.find_element_by_xpath('./div').text
			src = div.find_element_by_xpath('../a/img').get_attribute('src')
			dict[title] = src
		except:
			dict['股权结构'] = {}
	#主要人员
	def info4(self,browser,dict):
		dict1 = OrderedDict()
		try:
			div = browser.find_element_by_xpath('//div[@id="nav-main-staffCount"]')
			title = div.find_element_by_xpath('./div').text
			contents = div.find_elements_by_xpath('..//div[@class="content-container"]/div')
			for con in contents:
				name = con.find_elements_by_xpath('./a')[0].text
				span = con.find_element_by_xpath('.//span[@class="float-right"]/span').text
				dict1[name]=span
			dict[title]=dict1
		except:
			dict['主要人员'] = {}
	# 股东信息
	def info5(self,browser,dict):
		list = []
		try:
			div = browser.find_element_by_xpath('//div[@id="nav-main-holderCount"]')
			title = div.find_element_by_xpath('./div').text
			cons = div.find_elements_by_xpath('..//div[@class="content-container"]/div')
			for con in cons:
				dict1 = OrderedDict()
				contents = con.find_elements_by_xpath('./div')
				name = contents[0].find_elements_by_xpath('./a')[0].text
				dict1['名称']=name
				#认缴出资
				span1 = contents[1].find_elements_by_xpath('./span')
				s1 = span1[0].text
				s2 = span1[1].find_element_by_xpath('./span').text
				dict1[s1]=s2
				#出资比例
				span2 = contents[2].find_elements_by_xpath('./span')
				s3 = span2[0].text
				s4 = span2[1].find_element_by_xpath('.//img').get_attribute('src')
				dict1[s3] = s4
				list.append(dict1)
			dict[title]=list
		except:
			dict['股东信息'] = []
	# 对外投资
	def info6(self,browser,dict):
		list = []
		try:
			div = browser.find_element_by_xpath('//div[@id="nav-main-inverstCount"]')
			title = div.find_element_by_xpath('./div').text
			cons = div.find_elements_by_xpath('..//div[@class="content-container"]/div')
			for con in cons:
				dict1 = OrderedDict()
				name = con.find_element_by_xpath('./a/span').text
				dict1['名称'] = name
				contents = con.find_elements_by_xpath('./div')
				for content in contents:
					span = content.find_elements_by_xpath('./span')
					key = span[0].text.split('：')[0]
					try:
						val = span[1].text
					except:
						val = content.find_element_by_xpath('./a').get_attribute('href')
					dict1[key]=val
				list.append(dict1)
			dict[title]=list
		except:
			dict['对外投资'] = []
	# 变更信息
	def info7(self,browser,dict):
		list = []
		try:
			div = browser.find_element_by_xpath('//div[@id="nav-main-changeCount"]')
			title = div.text
			cons = div.find_elements_by_xpath('../..//div[@class="content-container"]/div')
			num = 0
			for con in cons:
				num +=1
				dict1 = OrderedDict()
				dict1['num'] = num
				contents = WebDriverWait(con, 50).until(lambda con: con.find_elements_by_xpath('.//div[@class="in-block vertical-top"]/div'))
				for content in contents:
					span = content.find_elements_by_xpath('./span')
					key = span[0].text.split('：')[0]
					val = span[1].text
					dict1[key]=val
				#变更前
				change = con.find_element_by_xpath('.//div[@class="left-content float-left new-border"]')
				change1 = change.find_element_by_xpath('.//div[@class="changeSubTitle"]')
				change_key = change1.text
				change2 = change.find_element_by_xpath('.//div[@class="changeSubText"]')
				#点击详细
				try:
					detail = change2.find_element_by_link_text('详细')
					detail.click()
					ems = change2.find_elements_by_xpath('.//span[@class="js-full-container"]//em')
					change_val = ''
					if ems:
						for em in ems[::2]:
							font = em.find_element_by_xpath('.//font')
							change_val += font.text
					else:
						change_val = change2.find_element_by_xpath('./span/span[1]/div').text
					dict1[change_key] = change_val
				except:
					pass

				# 变更后
				change = con.find_element_by_xpath('.//div[@class="right-content float-right new-border"]')
				change1 = change.find_element_by_xpath('.//div[@class="changeSubTitle"]')
				change_key = change1.text
				change2 = change.find_element_by_xpath('.//div[@class="changeSubText"]')
				# 点击详细
				try:
					detail = change2.find_element_by_link_text('详细')
					detail.click()
					ems = change2.find_elements_by_xpath('.//span[@class="js-full-container"]//em')
					change_val = ''
					for em in ems:
						font = em.find_element_by_xpath('.//font')
						change_val += font.text
					dict1[change_key] = change_val
					list.append(dict1)
				except:
					pass

			dict[title]=list
		except:
			dict['变更信息'] = []
	# 企业年报
	def info8(self,browser,dict):
		list = []
		try:
			div = browser.find_element_by_xpath('//div[@id="nav-main-reportCount"]')
			title = div.find_element_by_xpath('./div').text
			cons = div.find_elements_by_xpath('..//div[@class="content-container"]/div/a')
			for con in cons:
				dict1 = OrderedDict()
				href=con.get_attribute('href')
				span = con.find_element_by_xpath('./span').text
				dict1[span]=href
				list.append(dict1)
			dict[title]=list
		except:
			dict['企业年报'] = []
	# 核心团队
	def info9(self,browser,dict):
		list = []
		try:
			div = browser.find_element_by_xpath('//div[@id="nav-main-companyTeammember"]')
			title = div.find_element_by_xpath('./div').text
			cons = div.find_elements_by_xpath('..//div[@class="content-container"]/div')
			for con in cons:
				dict1 = OrderedDict()
				left_text = con.find_element_by_xpath('.//div[@class="left-text"]')
				val = left_text.text
				key = left_text.find_element_by_xpath('../div[1]').text
				dict1[key]=val
				list.append(dict1)
			dict[title]=list
		except:
			dict['核心团队'] = []
	# 企业业务
	def info10(self, browser, dict):
		list = []
		try:
			div = browser.find_element_by_xpath('//div[@id="nav-main-companyProduct"]')
			title = div.find_element_by_xpath('./div').text
			cons = div.find_elements_by_xpath('..//div[@class="content-container"]/div')
			for con in cons:
				dict1 = OrderedDict()
				contents = con.find_elements_by_xpath('.//div[@class="new-c2 mobile-img-detail"]/div')
				num = 0
				for content in contents:
					spans = content.find_elements_by_xpath('./span')
					num += 1
					if num == 1:
						dict1['名称'] = spans[0].text
					else:
						key = spans[0].text.split('：')[0]
						if len(spans) == 1:
							val = content.find_elements_by_xpath('./a')[0].text
						else:
							val = spans[1].text
						dict1[key]=val
				list.append(dict1)
			dict[title]=list
		except:
			dict['企业业务'] = []
	# 竞品信息
	def info11(self, browser, dict):
		list = []
		try:
			div = browser.find_element_by_xpath('//div[@id="nav-main-companyJingpin"]')
			title = div.find_element_by_xpath('./div').text
			cons = div.find_elements_by_xpath('..//div[@class="content-container"]/div')
			for con in cons:
				dict1 = OrderedDict()
				contents = con.find_elements_by_xpath('.//div[@class="new-c2 mobile-img-detail"]/div')
				num = 0
				for content in contents:
					spans = content.find_elements_by_xpath('./span')
					num += 1
					if num == 1:
						dict1['名称']=spans[0].text
					else:
						key = spans[0].text.split('：')[0]
						if len(spans) == 1:
							val = content.find_elements_by_xpath('./a')[0].text
						else:
							val = spans[1].text
						dict1[key]=val
				list.append(dict1)
			dict[title]=list
		except:
			dict['竞品信息'] = []
	# 法律诉讼
	def info12(self, browser, dict):
		list = []
		try:
			div = browser.find_element_by_xpath('//div[@id="nav-main-lawsuitCount"]')
			title = div.find_element_by_xpath('./div').text
			cons = div.find_elements_by_xpath('..//div[@class="content-container"]/div')
			for con in cons:
				dict1 = OrderedDict()
				contents = con.find_elements_by_xpath('./div')
				num = 0
				for content in contents:
					spans = content.find_elements_by_xpath('./span')
					num += 1
					if num == 1:
						a = content.find_elements_by_xpath('./a')
						if a[0].text=="":
							break
						dict1['名称']=a[0].text
						dict1['链接']=a[0].get_attribute('href')

					else:
						key = spans[0].text.split('：')[0]
						if len(spans) == 1:
							val = content.find_elements_by_xpath('./a')[0].text
						else:
							val = spans[1].text
						dict1[key]=val
				if dict1:
					list.append(dict1)
			dict[title]=list
		except:
			dict['法律诉讼'] = []
	# 法院公告
	def info13(self, browser, dict):
		list = []
		try:
			div = browser.find_element_by_xpath('//div[@id="nav-main-courtCount"]')
			title = div.find_element_by_xpath('./div').text
			cons = div.find_elements_by_xpath('..//div[@class="content-container"]/div')
			for con in cons:
				dict1 = OrderedDict()
				a = con.find_elements_by_xpath('./a')
				if a[0].text == "":
					break
				dict1['链接'] = a[0].get_attribute('href')
				contents = con.find_elements_by_xpath('.//div')
				for content in contents:
					spans = content.find_elements_by_xpath('./span')
					if len(spans)>0:
						key = spans[0].text.split('：')[0]
						val = spans[1].text
						dict1[key]=val
				if dict1:
					list.append(dict1)
			dict[title]=list
		except:
			dict['法院公告'] = []
	# 被执行人
	def info14(self, browser, dict):
		list = []
		try:
			div = browser.find_element_by_xpath('//div[@id="nav-main-zhixing"]')
			title = div.find_element_by_xpath('./div').text
			cons = div.find_elements_by_xpath('..//div[@class="content-container"]/div')
			for con in cons:
				dict1 = OrderedDict()
				contents = con.find_elements_by_xpath('./div')
				num = 0
				for content in contents:
					spans = content.find_elements_by_xpath('./span')
					num += 1
					if num == 1:
						if content.text == "":
							break
						dict1['执行文件'] = content.text
					else:
						key = spans[0].text.split('：')[0]
						if len(spans) == 1:
							val = content.find_elements_by_xpath('./a')[0].text
						else:
							val = spans[1].text
						dict1[key] = val
				if dict1:
					list.append(dict1)
			dict[title] = list
		except:
			dict['被执行人'] = []
	# 行政处罚
	def info15(self, browser, dict):
		list = []
		try:
			div = browser.find_element_by_xpath('//div[@id="nav-main-punishment"]')
			title = div.find_element_by_xpath('./div').text
			cons = div.find_elements_by_xpath('..//div[@class="content-container"]/div')
			for con in cons:
				dict1 = OrderedDict()
				#点击弹窗
				con.find_element_by_xpath('./div').click()
				# 内容
				contents = browser.find_elements_by_xpath('//div[@class="modal-content"]//div[@class="modal-body new-c2"]/div')
				for content in contents:
					key = content.text.split('：')[0]
					spans = content.find_elements_by_xpath('./span')
					if len(spans)>0:
						val = spans[0].text
						dict1[key]=val
				# 关闭弹窗
				browser.find_element_by_xpath('//div[@class="modal-content"]//i[@class="tic tic-close"]').click()
				if dict1:
					list.append(dict1)
			dict[title]=list
		except:
			dict['行政处罚'] = []
	# 股权出质
	def info16(self, browser, dict):
		list = []
		try:
			div = browser.find_element_by_xpath('//div[@id="nav-main-equityCount"]')
			title = div.find_element_by_xpath('./div').text
			cons = div.find_elements_by_xpath('..//div[@class="content-container"]/div')
			for con in cons:
				dict1 = OrderedDict()
				#点击弹窗
				con.find_element_by_xpath('./div').click()
				# 内容
				contents = browser.find_elements_by_xpath('//div[@class="modal-content"]//div[@class="new-c2"]/div')
				for content in contents:
					key = content.text.split('：')[0]
					spans = content.find_elements_by_xpath('./span')
					if len(spans)>0:
						val = spans[0].text
						dict1[key]=val
				# 关闭弹窗
				browser.find_element_by_xpath('//div[@class="modal-content"]//i[@class="tic tic-close"]').click()
				if dict1:
					list.append(dict1)
			dict[title]=list
		except:
			dict['股权出质'] = []
	# 招聘信息
	def info17(self, browser, dict):
		list = []
		try:
			div = browser.find_element_by_xpath('//div[@id="nav-main-baipin"]')
			title = div.find_element_by_xpath('./div[@class="itemTitle"]').text.split('\n')[0]
			cons = div.find_elements_by_xpath('..//div[@class="baipin-list"]/div')
			for con in cons:
				dict1 = OrderedDict()
				span = con.find_elements_by_xpath('.//div[@class="row zp-title"]/span')
				dict1['职位']=span[0].text
				dict1['工资']=span[1].text
				data = con.find_element_by_xpath('.//div[@class="row zp-diqu"]')
				dict1['要求']=data.text
				date = con.find_element_by_xpath('.//div[@class="zp-time"]')
				dict1['日期']=date.text
				if dict1:
					list.append(dict1)
			dict[title]=list
		except:
			dict['招聘信息'] = []
	# 税务评级
	def info18(self, browser, dict):
		list = []
		try:
			div = browser.find_element_by_xpath('//div[@id="nav-main-taxCreditCount"]')
			title = div.find_element_by_xpath('./div').text
			cons = div.find_elements_by_xpath('..//div[@class="content-container"]/div')
			for con in cons:
				contents = con.find_elements_by_xpath('./div')
				for content in contents:
					list.append(content.text)
			dict[title] = list
		except:
			dict['税务评级'] = []
	# 产品信息
	def info19(self, browser, dict):
		list = []
		try:
			div = browser.find_element_by_xpath('//div[@id="nav-main-productinfo"]')
			title = div.find_element_by_xpath('./div').text
			cons = div.find_elements_by_xpath('..//div[@class="content-container"]/div')
			for con in cons:
				dict1 = OrderedDict()
				contents = con.find_elements_by_xpath('.//div[@class="new-c2 mobile-img-middle"]/div')
				num = 0
				for content in contents:
					spans = content.find_elements_by_xpath('./span')
					num += 1
					if num == 1:
						dict1['名称'] = spans[0].text
					else:
						key = spans[0].text.split('：')[0]
						if len(spans) == 1:
							val = content.find_elements_by_xpath('./a')[0].text
						else:
							val = spans[1].text
						dict1[key]=val
				list.append(dict1)
			dict[title]=list
		except:
			dict['产品信息'] = []
	# 分支机构
	def info20(self, browser, dict):
		list = []
		try:
			div = browser.find_element_by_xpath('//div[@id="nav-main-branchCount"]')
			title = div.find_element_by_xpath('./div').text
			cons = div.find_elements_by_xpath('..//div[@class="content-container"]/div')
			for con in cons:
				dict1 = OrderedDict()
				span = con.find_element_by_xpath('./a/span').text
				dict1['机构名称']=span
				if span:
					list.append(dict1)
			dict[title]=list
		except:
			dict['分支机构'] = []
	# 抽查检查
	def info21(self, browser, dict):
		list = []
		try:
			div = browser.find_element_by_xpath('//div[@id="nav-main-checkCount"]')
			title = div.find_element_by_xpath('./div').text
			cons = div.find_elements_by_xpath('..//div[@class="content-container"]/div')
			for con in cons:
				contents = con.find_elements_by_xpath('./div')
				for content in contents:
					list.append(content.text)
			dict[title] = list
		except:
			dict['抽查检查'] = []
	# 招投标
	def info22(self, browser, dict):
		list = []
		try:
			div = browser.find_element_by_xpath('//div[@id="nav-main-bidCount"]')
			title = div.find_element_by_xpath('./div').text
			cons = div.find_elements_by_xpath('..//div[@class="content-container"]/div')
			for con in cons:
				contents = con.find_elements_by_xpath('./div')
				for content in contents:
					list.append(content.text)
			dict[title] = list
		except:
			dict['招投标信息'] = []
	# 债券信息
	def info23(self, browser, dict):
		try:
			browser.find_element_by_xpath('//div[@id="nav-main-bondCount"]')
		except:
			dict['债券信息'] = []
	# 购地信息
	def info24(self, browser, dict):
		try:
			browser.find_element_by_xpath('//div[@id="nav-main-goudiCount"]')
		except:
			dict['购地信息'] = []

	def run(self, company):
		self.send_request(company)
		js = self.get_content(company)
		return js

def run(driver, company):
	tyc = TianYanCha(driver)
	js = tyc.run(company)
	return js

# if __name__ == '__main__':
# 	driver = webdriver.Chrome()
# 	company = '腾讯'
# 	run(driver, company)
# 	driver.quit()
