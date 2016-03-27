# -*- coding: utf-8 -*-

import time,re,os
from bs4 import BeautifulSoup
from make_chm import *
from spider_crust import *
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

#----------- 爬取csdn用户所有文章 -----------
class Spider_Csdn:
	def __init__(self):
		self.url_list=[]
		self.post_list=[]
		self.blog=''
		self.url=''
		self.path=''
		headers = {
			'Host': 'blog.csdn.net',
			'User-Agent':' Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
			'Accept-Encoding': 'gzip, deflate',
			'Referer': 'http://blog.csdn.net/',
			'Connection': 'keep-alive'
			}
		self.se=Spider_Crust()
		self.se.set_headers(headers)
		self.se.set_index_url('http://blog.csdn.net/')
		
	def set_dely(self,dely):
		self.se.set_dely(dely)
	def set_work_home(self,work_home):
		self.se.set_work_home(work_home)
	def set_index_url(self,index_url):
		self.se.set_index_url(index_url)
	def set_max_page(self,max_page):
		self.se.set_max_page(max_page)
	def set_page_num(self,page_num):
		self.se.set_page_num(page_num)
		
	#Get urls from the page
	#type:1--user index;2--other page
	def get_user_index_urls(self,url):
		reStr = {
		'urlList':'href=\"(?P<path_list>/[^/]*?/article/details/\d+)\"',
		'nextUrl':u'<a href=\"(?P<path_list>/[^\"]*?/article/list/\d+)\">下一页</a>',
		'title':'<title>(?P<path_list>.*?)</title>'
		}
		self.se.get_user_index_urls(url,reStr)
		

	#获取其他页面的可爬取url列表
	def get_page_urls(self,url):
		reStr = {
		'urlList':'href=\"(?P<path_list>http://blog.csdn.net/[^/]*?/article/details/\d+)\"',
		'nextUrl':u'<a href=\"(?P<path_list>[^\"]*?\&page=\d+)\">下一页</a>',
		'title':'<title>(?P<path_list>.*?)</title>'
		}
		self.se.get_page_urls(url,reStr)

	#从主页开始获取所有频道首页文章
#	def get_index_data(self,mcm):
#		self.pageNum=1
#		#deal index posts
#		self.get_urls(self.index_url,2)
#		self.get_posts(mcm)
#		#deal categroy posts
#		reStr = {
#		'urlList':'href=\"(?P<path_list>/[^/]*?/[^\"]*?\.html)\"',
#		'nextUrl':'',
#		'title':'<title>(?P<path_list>.*?)</title>'
#		}
#		urlInfo=self.se.get_urls(self.index_url,reStr)
#		for url in urlInfo['urlList']:
#			url=self.index_url+url
#			print 'Find url: '+url
#			self.get_urls(url,2)
#			self.get_posts(mcm)

	#Get posts
	def get_posts(self,mcm):
		self.se.get_posts(mcm)

	#根据链接获取文章相关信息
#	def get_post(self,url):
#		reStar={
#		'id':'http://blog.csdn.net/[^/]*?/article/details/(?P<id>\d+)',
#		'keywords':'blog_articles_tag\']\);\">(?P<keywords>[^<]*?)</a>',
#		'categories':'blog_articles_fenlei\']\);\">(?P<cate>[\s\S]*?)</span>',
#		'content':'<div id=\"article_content\" class=\"article_content\">(?P<content>[\s\S]*?)</div>[^<]*?<!-- Baidu Button BEGIN -->'
#		}
#		post=self.se.get_post(url,reStar)
#		titles=post['title'].split('-')
#		post['title']="".join(titles[0:(len(titles)-3)])
#		post['content']=re.sub('<script[^>]*?>[\s\S]*?</script>','',post['content'])
#		#print post
#		self.post_list.append(post)
#
#
#	def save_html_partly(self,mcm,part,partly):
#		if(partly>0):
#			blog=self.blog+'_part_'+str(part)
#			path=self.path+'_part_'+str(part)
#		else:
#			blog=self.blog
#			path=self.path
#		mcm.set_para(self.work_home,blog,path,self.post_list)
#		mcm.save()
#		del self.post_list[:]



if __name__ == '__main__':
	sc=Spider_Csdn()
	mcm=MakeChm()
	mcm.set_save_img(0)
	mcm.set_chm_path('E:\pycode\spider\chm\csdn_host')
	sc.set_partlyNum(3)
	sc.set_max_page(1)
	sc.get_index_data(mcm)

