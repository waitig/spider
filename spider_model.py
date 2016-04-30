# -*- coding: utf-8 -*-

import time,re,os
from spider_engine import *
from save_chm import *
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

#----------- 爬取csdn用户所有文章 -----------
class SpiderModel:

	def __init__(self,headers):
		self.url_list=[]
		self.dely=0.3
		self.maxPage=1
		self.pageNum=1
		self.splitChar='-'
		self.se=Spider_Engine(headers)
		
	#Set and get
	def set_useUrllib2(self,used):
		self.se.set_useUrllib2(used)
	def set_usePost(self,used):
		self.se.set_usePost(used)
	def set_postData(self,postData):
		self.se.set_postData(postData)
	def set_dely(self,dely):
		self.dely=dely
	def set_max_page(self,maxPage):
		self.maxPage=maxPage
	def set_splitChar(self,splitChar):
		self.splitChar=splitChar
	#Get urls from the page
	#type:1--user index;2--other page
	def get_urls(self,url,type,mcm,flag=0):
		if(type==1):
			self.get_user_index_urls(url,type,mcm)
			return
		else:
			self.get_page_urls(url,type,mcm)
			return
		
	#Get user index urls
	def get_user_index_urls(self,url,type,mcm,flag=0):
		url=self.deal_user_index_urls(url)
		urlInfo={}
		urlInfo['urlList']=[]
		urlInfo['nextUrl']=''
		urlInfo['title']=''
		urlInfo=self.se.get_urls(url,self.user_index_reStr,self.index_url)
		self.url_list+=urlInfo['urlList']
		if(flag==0):
			blog=self.get_blog(1,urlInfo['title'])
			path=self.get_path(1,url)
			mcm.set_para(self.work_home,blog,path)
		#Recursive
		self.pageNum+=1
		if(self.pageNum>self.maxPage and self.maxPage!=-1):
			self.pageNum=1
			return
		else:
			if urlInfo['nextUrl']:
				print 'Loading url:'+urlInfo['nextUrl']
				time.sleep(self.dely)
				self.get_user_index_urls(urlInfo['nextUrl'],1,mcm,1)
			else:
				self.pageNum=1
				return

	#获取任意页面可爬取的url列表
	def get_page_urls(self,url,type,mcm,flag=0):
		url=self.deal_page_urls(url)
		print 'Loadding page [ '+str(self.pageNum)+' ] : '+url
		urlInfo=self.se.get_urls(url,self.page_url_reStr,self.index_url)
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
				self.get_page_urls(urlInfo['nextUrl'],type,mcm,1)
			else:
				self.pageNum=1
				return
			
	#从主页开始获取所有频道首页文章
	def get_index_data(self,mcm):
		index_url=self.deal_index_data()
		self.pageNum=1
		#deal index posts
		self.get_urls(index_url,3,mcm)
		self.get_posts(mcm)
		#deal categroy posts
		urlInfo=self.se.get_urls(self.index_url,self.index_url_reStr,self.index_url)
		for url in urlInfo['urlList']:
			print 'Find url: '+url
			self.get_page_urls(url,2,mcm)
			self.get_posts(mcm)

	#获取文章
	def get_posts(self,mcm):
		self.deal_get_posts()
		self.url_list=list(set(self.url_list))
		print 'Total '+str(len(self.url_list))+' articles found , start loading.'
		num=1
		for n in self.url_list:
			print 'NO ['+str(num)+'] Loading URL:'+n
			post=self.se.get_post(n,self.post_reStr)
			post['title']=self.deal_post_title(post['title'])
			post['content']=self.deal_post_content(post['content'])
			mcm.save_post(post)
			time.sleep(self.dely)
			num+=1
		mcm.save_it()
		del self.url_list[:]
		
	#Return the file name in client version
	def get_blog(self,type,title):
		title=self.deal_title(title)
		titles=title.split(self.splitChar)
		fileName=self.work_home+'_'+"".join(titles[0:(len(titles)-1)])
		if(type!=1):
			tm=time.strftime('%y_%m_%d',time.localtime(time.time()))
			fileName=fileName+'_'+tm
		return fileName.strip('_')
	#Return the direction name in all version
	#type--1:user index --2:other page --3:blog index
	def get_path(self,type,url):
		if(type!=3):
			url=url.replace(self.index_url,'')
		else:
			url=url.replace('http://','')
			url=url.replace('https://','')
		url=((url.replace('//','/')).strip('/')).replace('/','_')
		url=url.replace('?','_').replace('&','_').replace('.','_')
		path=(url.replace('__','_')).strip('_')
		if(type!=1):
			tm=time.strftime('%y_%m_%d',time.localtime(time.time()))
			path=path+'_'+tm
		return path
	
	def get_others(self,url,headers,useUrllib=0,usePost=0,postData={}):
		return self.se.get_others(url=url,headers=headers,useUrllib=useUrllib,usePost=usePost,postData=postData)
	#Return the post titles 
	#HOCKS
	def deal_post_title(self,title):
		titles=title.split(self.splitChar)
		return "".join(titles[0:(len(titles)-1)])
	def deal_post_content(self,content):
		return content
	def deal_title(self,title):
		return title
	def deal_user_index_urls(self,url):
		return url
	def deal_page_urls(self,url):
		return url
	def deal_get_posts(self):
		return
	def deal_index_url(self):
		return self.index_url

	

if __name__ == '__main__':
	pass
#	sc=Spider_Cnblogs()
#	mcm=MakeChm()
#	mcm.set_save_img(0)
#	mcm.set_partlyNum(20)
#	mcm.set_chm_path('E:\pycode\spider\chm\cnblogs_host')
#	sc.set_dely(1)
#	sc.set_max_page(2)
#	sc.get_index_data(mcm)
#	#sc.get_posts(mcm)