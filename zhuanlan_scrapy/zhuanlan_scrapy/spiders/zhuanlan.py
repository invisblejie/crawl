# -*- coding: utf-8 -*-
import scrapy
import json


class ZhuanlanSpider(scrapy.Spider):
    name = 'zhuanlan'
    allowed_domains = ['zhihu.com']
    start_urls = ['wontfallinyourlap']

    def start_requests(self):
    	return [scrapy.Request('http://www.zhihu.com/',callback=self.login)]

    def login(self,response):
    	xsrf = response.xpath('//input[@name="_xsrf"]/@value').extract_first()
    	return [scrapy.FormRequest('https://www.zhihu.com/login/email',
                                   formdata={'remember_me':'true','email': 'rrygyidy@sharklasers.com', 'password': 'abc987', '_xsrf': xsrf},
                                   callback=self.logged_in)]

    def logged_in(self,response):
        if json.loads(response.text)['msg'] != 0:
            captcha_url = 'https://www.zhihu.com/' +'/captcha.gif?r='+str(int(time.time())*1000)+'&type=login'
            return [scrapy.Request('https://www.zhihu.com/' +'/captcha.gif?r='+str(int(time.time())*1000)+'&type=login',
                                   callback=self.verify_picture)]
            with open("checkcode.jpeg",'wb') as f:
                f.write(captcha_picture.content)
            login_data["captcha"] = input("验证码: ")
            return [scrapy.FormRequest('https://www.zhihu.com/login/email',formdata = login_data,callback = self.logged_in)]
    	print(json.loads(response.text)['msg'])
    	for i in range(1,9):
    		for zhuanlan_name in self.start_urls:
    			yield self.make_requests_from_url('https://zhuanlan.zhihu.com/api/columns/'+ zhuanlan_name + '/followers?limit=20&offset=' + str(20 * i))

    def verify_picture(self,response):
        with open("checkcode.jpeg",'wb') as f:
                f.write(response.content)
        login_data["captcha"] = input("验证码: ")
        return [scrapy.FormRequest('https://www.zhihu.com/login/email',formdata = login_data,callback = self.logged_in)]

    def parse(self,response):
    	resp = json.loads(response.body.decode('utf-8'))
    	for j in resp:
    		yield j
    	number = int(response.url[response.url.find('offset') + 7:])
    	new_url = response.url[:response.url.find('offset') + 7] + str(number + 160)
    	if len(resp) == 20:
    		yield scrapy.Request(new_url, callback=self.parse)
        if len(resp) == 0:
            pass





