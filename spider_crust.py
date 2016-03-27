# -*- coding: utf-8 -*-

import time,re,os
from spider_engine import *
from make_chm import *
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

#----------- 爬取csdn用户所有文章 -----------
class Spider_Crust:

	def __init__(self,headers):
		self.url_list=[]
		self.post_list=[]
		self.blog=''
		self.url=''
		self.path=''
		self.dely=0.3
		self.partlyNum=50
		self.work_home='cnblogs'
		self.maxPage=1
		self.pageNum=1
		self.index_url='http://www.cnblogs.com/'
		self.se=Spider_Engine()
		self.se.set_headers(headers)
		
	def get_url_list(self):
		return self.url_list
	def get_post_list(self):
		return self.post_list
	def get_blog(self):
		return self.blog
	def get_path(self):
		return self.path
	def set_dely(self,dely):
		self.dely=dely
	def set_work_home(self,work_home):
		self.work_home=work_home
	def set_index_url(self,index_url):
		self.index_url=index_url
	def set_max_page(self,max_page):
		self.maxPage=max_page
	def set_page_num(self,page_num):
		self.pageNum=page_num
	def clear_url_list(self):
		del self.url_list[:]
	def clear_post_list(self):
		del self.post_list[:]
		

	#Get urls from the user index
	def get_user_index_urls(self,url,restr):
		urlInfo['urlList']=[]
		urlInfo['nextUrl']=''
		urlInfo['title']=''
		urlInfo=self.se.get_urls(url,reStr)
		for n in urlInfo['urlList']:
			url=self.index_url+n
			self.url_list.append(url)
		
		if urlInfo['nextUrl']:
			urls=self.index_url+urlInfo['nextUrl']
			print 'Loading url:'+urls
			time.sleep(self.dely)
			self.get_urls(urls,1)
		else:
			blog=urlInfo['title'].split('-')
			pos=len(blog)-2
			self.blog=self.work_home+'_'+blog[pos]
			self.path=url.split('/')[3]
			return True

	#获取任意页面可爬取的url列表
	def get_page_urls(self,url,reStr):
		print 'Loadding page [ '+str(self.pageNum)+' ] : '+url
		tm=time.strftime('%y_%m_%d',time.localtime(time.time()))
		urlInfo=self.se.get_urls(url,reStr)
		trueUrl=url.replace(self.index_url,'')
		trueUrl=trueUrl.replace('//','/').replace('?','_').replace('&','_').replace('.','_')
		self.path=(trueUrl.replace('/','_')+'_'+tm).replace('__','_')
		try:
			title=urlInfo['title'].split(' - ')
			self.blog=(title[1]+'_'+title[0]+'_'+tm).decode('utf-8')
		except UnicodeDecodeError:
			self.blog=self.path

		for n in urlInfo['urlList']:
			self.url_list.append(n)
		#Recursive
		self.pageNum+=1
		if(self.pageNum>self.maxPage and self.maxPage!=-1):
			self.pageNum=1
			return
		else:
			if urlInfo['nextUrl']:
				self.get_page_urls(self.index_url+urlInfo['nextUrl'])
			else:
				self.pageNum=1
				return

	#从主页开始获取所有频道首页文章
#	def get_index_data(self,mcm):
#		self.pageNum=1
#		#deal index posts
#		self.get_urls(self.index_url,2)
#		self.get_posts(mcm)
#		#deal categroy posts
#		reStr = {
#		'urlList':'href=\"(?P<path_list>/cate/\d+\/)\"',
#		'nextUrl':'',
#		'title':'<title>(?P<path_list>.*?)</title>'
#		}
#		urlInfo=self.se.get_urls(self.index_url,reStr)
#		for url in urlInfo['urlList']:
#			url=self.index_url+url
#			print 'Find url: '+url
#			self.get_urls(url,2)
#			self.get_posts(mcm)


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
	def get_post(self,url,restr):
		post=self.se.get_post(url,reStr)
		self.post_list.append(post)


	def save_html_partly(self,mcm,part,partly):
		#mcm=MakeChm()
		if(partly>0):
			blog=self.blog+'_part_'+str(part)
			path=self.path+'_part_'+str(part)
		else:
			blog=self.blog
			path=self.path
		mcm.set_para(self.work_home,blog,path,self.post_list)
		mcm.save()
		del self.post_list[:]

	def set_dely(self,dely):
		self.dely=dely

	def set_partlyNum(self,partlyNum):
		self.partlyNum=partlyNum

	def set_max_page(self,maxPage):
		self.maxPage=maxPage

	def set_index_url(self,index_url):
		self.index_url=index_url

if __name__ == '__main__':
	sc=Spider_Cnblogs()
	mcm=MakeChm()
	mcm.set_save_img(0)
	mcm.set_chm_path('E:\pycode\spider\chm\cnblogs_host')
	sc.set_dely(1)
	sc.set_max_page(2)
	sc.get_index_data(mcm)
	#sc.get_posts(mcm)

