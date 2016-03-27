# -*- coding: utf-8 -*-

import time,re,os
from spider_engine import *
from make_chm import *
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

#----------- 爬取csdn用户所有文章 -----------
class Spider_Cnblogs:

	def __init__(self):
		self.url_list=[]
		self.post_list=[]
		self.blog=''
		self.path=''
		self.dely=0.3
		self.partlyNum=50
		self.work_home='cnblogs'
		self.maxPage=1
		self.pageNum=1
		self.index_url='http://www.cnblogs.com/'
		headers = {
			'Host':'www.cnblogs.com',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
			'Accept-Encoding': 'gzip, deflate',
			'Referer': 'http://www.cnblogs.com/',
			'Connection': 'keep-alive',
			'Cache-Control': 'max-age=0'
			}
		self.se=Spider_Engine(headers)
	#Get urls from the page
	#type:1--user index;2--other page
	def get_urls(self,url,type,flag=0):
		if(type==1):
			self.get_user_index_urls(url,type)
			return
		else:
			self.get_page_urls(url,type)
			return
		
	#Get user index urls
	def get_user_index_urls(self,url,type,flag=0):
		reStr = {
		'urlList':'href=\"(?P<path_list>/[^/]*?/article/details/\d+)\"',
		'nextUrl':u'<a href=\"http://www.cnblogs.com/(?P<path_list>[^/]*?/default.html\?page=\d+)\">下一页</a>',
		'title':'<title>(?P<path_list>.*?)</title>'
		}
		urlInfo['urlList']=[]
		urlInfo['nextUrl']=''
		urlInfo['title']=''
		urlInfo=self.se.get_urls(url,reStr,self.index_url)
		self.url_list+=urlInfo['urlList']
		if(flag==0):
			self.blog=self.get_blog(1,urlInfo['title'])
			self.path=self.get_path(1,url)
		if urlInfo['nextUrl']:
			print 'Loading url:'+urlInfo['nextUrl']
			time.sleep(self.dely)
			self.get_user_index_urls(urlInfo['nextUrl'],1,1)
		else:
			return

	#获取任意页面可爬取的url列表
	def get_page_urls(self,url,type,flag=0):
		print 'Loadding page [ '+str(self.pageNum)+' ] : '+url
		reStr = {
		'urlList':'href=\"http://www.cnblogs.com/(?P<path_list>[^/]*?/p/[^\.]*?\.html)\"',
		'nextUrl':u'<a href=\"\/(?P<path_list>[^\"]*?\/\d+)\" onclick=\"[^\"]*?\">Next &gt;</a>',
		'title':'<title>(?P<path_list>.*?)</title>'
		}
		urlInfo=self.se.get_urls(url,reStr)
		if(flag==0):
			self.path=self.get_path(type,url)
			self.blog=self.get_blog(type,urlInfo['title'])
		self.url_list+=urlInfo['urlList']
		#Recursive
		self.pageNum+=1
		if(self.pageNum>self.maxPage and self.maxPage!=-1):
			self.pageNum=1
			return
		else:
			if urlInfo['nextUrl']:
				self.get_page_urls(urlInfo['nextUrl'],type,1)
			else:
				self.pageNum=1
				return
	#从主页开始获取所有频道首页文章
	def get_index_data(self,mcm):
		self.pageNum=1
		#deal index posts
		self.get_urls(self.index_url,3)
		self.get_posts(mcm)
		#deal categroy posts
		reStr = {
		'urlList':'href=\"(?P<path_list>/cate/\d+\/)\"',
		'nextUrl':'',
		'title':'<title>(?P<path_list>.*?)</title>'
		}
		urlInfo=self.se.get_urls(self.index_url,reStr)
		for url in urlInfo['urlList']:
			print 'Find url: '+url
			self.get_page_urls(url,2)
			self.get_posts(mcm)

	#获取文章
	def get_posts(self,mcm):
		self.url_list=list(set(self.url_list))
		print 'Total '+str(len(self.url_list))+' articles found , start loading.'
		num=1
		part=1
		partly=0
		for n in self.url_list:
			print 'NO ['+str(num)+'] Loading URL:'+n
			self.get_post(n)
			num+=1
			if(num>self.partlyNum):
				partly=1
				print 'Get '+str(self.partlyNum)+' articles,start to create html'
				self.save_html_partly(mcm,part,partly)
				part+=1
				num=1
			time.sleep(self.dely)
		self.save_html_partly(mcm,part,partly)
		del self.url_list[:]

	#根据链接获取文章相关信息
	def get_post(self,url):
		reStar={
		'id':'http://blog.csdn.net/[^/]*?/article/details/(?P<id>\d+)',
		'keywords':'blog_articles_tag\']\);\">(?P<keywords>[^<]*?)</a>',
		'categories':'blog_articles_fenlei\']\);\">(?P<cate>[\s\S]*?)</span>',
		'content':'<div id=\"article_content\" class=\"article_content\">(?P<content>[\s\S]*?)</div>[^<]*?<!-- Baidu Button BEGIN -->'
		}
		post=self.se.get_post(url,reStar)
		post['title']=self.get_post_title(post['title'])
		self.post_list.append(post)

	#Return the file name in client version
	def get_blog(self,type,title):
		titles=title.split('-')
		fileName="cnblogs_".join(titles[0:(len(titles)-2)])
		if(type!=1):
			tm=time.strftime('%y_%m_%d',time.localtime(time.time()))
			fileName=fileName+'_'+tm
		return fileName
	#Return the direction name in all version
	#type--1:user index --2:other page --3:blog index
	def get_path(self,type,url):
		if(type!=3):
			url=url.replace(self.index_url,'')
		url=(url.replace('//','/')).strip('/')
		url=url.replace('?','_').replace('&','_').replace('.','_')
		path=(url.replace('__','_')).strip('_')
		if(type!=1):
			tm=time.strftime('%y_%m_%d',time.localtime(time.time()))
			path=path+'_'+tm
		return path
	#Return the post titles 
	def get_post_title(self,title):
		titles=title.split('-')
		post['title']="".join(titles[0:(len(titles)-2)])
		
	def save_html_partly(self,mcm):
		if(partly>0):
			self.blog=self.blog+'_part_'+str(part)
			self.path=self.path+'_part_'+str(part)
		mcm.set_para(self.work_home,self.blog,self.path,self.post_list)
		mcm.save()
		del self.post_list[:]

	def set_dely(self,dely):
		self.dely=dely

	def set_partlyNum(self,partlyNum):
		self.partlyNum=partlyNum

	def set_max_page(self,maxPage):
		self.maxPage=maxPage

if __name__ == '__main__':
	sc=Spider_Cnblogs()
	mcm=MakeChm()
	mcm.set_save_img(0)
	mcm.set_chm_path('E:\pycode\spider\chm\cnblogs_host')
	sc.set_dely(1)
	sc.set_max_page(2)
	sc.get_index_data(mcm)
	#sc.get_posts(mcm)