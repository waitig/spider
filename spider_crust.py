# -*- coding: utf-8 -*-

import time,re,os
from spider_engine import *
from save_chm import *
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

#----------- 爬取csdn用户所有文章 -----------
class SpiderModel:

	def __init__(self,headers,index_url,work_home):
		self.url_list=[]
		self.dely=0.3
		self.work_home=work_home
		self.maxPage=1
		self.pageNum=1
		self.index_url=index_url
		self.se=Spider_Engine(headers)
		self.user_index_reStr={}
		self.page_url_reStr={}
		self.index_url_reStr={}
		self.post_reStr={}
		
	#Set and get
	def set_user_index_reStr(self,reStr):
		self.user_index_reStr=reStr
	def set_page_url_reStr(self,reStr):
		self.page_url_reStr=reStr
	def set_index_url_reStr(self,reStr):
		self.index_url_reStr=reStr
	def set_post_reStr(self,reStr):
		self.post_reStr=reStr
		
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
	def get_user_index_urls(self,url,type,mcm,flag=0):
		urlInfo['urlList']=[]
		urlInfo['nextUrl']=''
		urlInfo['title']=''
		urlInfo=self.se.get_urls(url,self.user_index_reStr,self.index_url)
		self.url_list+=urlInfo['urlList']
		if(flag==0):
			blog=self.get_blog(1,urlInfo['title'])
			path=self.get_path(1,url)
			mcm.set_para(self.work_home,blog,path)
		if urlInfo['nextUrl']:
			print 'Loading url:'+urlInfo['nextUrl']
			time.sleep(self.dely)
			self.get_user_index_urls(urlInfo['nextUrl'],1,1)
		else:
			return

	#获取任意页面可爬取的url列表
	def get_page_urls(self,url,type,mcm,flag=0):
		print 'Loadding page [ '+str(self.pageNum)+' ] : '+url
		urlInfo=self.se.get_urls(url,self.page_url_reStr)
		if(flag==0):
			path=self.get_path(type,url)
			blog=self.get_blog(type,urlInfo['title'])
			mcm.set_para(self.work_home,blog,path)
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
		self.get_urls(self.index_url,3,mcm)
		self.get_posts(mcm)
		#deal categroy posts
		urlInfo=self.se.get_urls(self.index_url,self.index_url_reStr)
		for url in urlInfo['urlList']:
			print 'Find url: '+url
			self.get_page_urls(url,2)
			self.get_posts(mcm)

	#获取文章
	def get_posts(self,mcm):
		self.url_list=list(set(self.url_list))
		print 'Total '+str(len(self.url_list))+' articles found , start loading.'
		num=1
		for n in self.url_list:
			print 'NO ['+str(num)+'] Loading URL:'+n
			post=self.se.get_post(url,self.post_reStr)
			post['title']=self.deal_post_title(post['title'])
			post['content']=self.deal_post_content(post['content'])
			mcm.save_post(post)
			time.sleep(self.dely)
		del self.url_list[:]
		
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
	def deal_post_title(self,title):
		titles=title.split('-')
		return "".join(titles[0:(len(titles)-2)])
	def deal_post_content(self,content):
		return content

	def set_dely(self,dely):
		self.dely=dely

	def set_max_page(self,maxPage):
		self.maxPage=maxPage

if __name__ == '__main__':
	sc=Spider_Cnblogs()
	mcm=MakeChm()
	mcm.set_save_img(0)
	mcm.set_partlyNum(20)
	mcm.set_chm_path('E:\pycode\spider\chm\cnblogs_host')
	sc.set_dely(1)
	sc.set_max_page(2)
	sc.get_index_data(mcm)
	#sc.get_posts(mcm)