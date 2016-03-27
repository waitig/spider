# -*- coding: utf-8 -*-

import time,re,os
from bs4 import BeautifulSoup
from make_chm import *
from spider_engine import *
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
		self.dely=0.3
		self.partlyNum=50
		self.work_home='csdn'
		self.maxPage=1
		self.pageNum=1
		self.index_url='http://blog.csdn.net/'
		headers = {
			'Host': 'blog.csdn.net',
			'User-Agent':' Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
			'Accept-Encoding': 'gzip, deflate',
			'Referer': 'http://blog.csdn.net/',
			'Connection': 'keep-alive'
			}
		self.se=Spider_Engine()
		self.se.set_headers(headers)
		
	#Get urls from the page
	#type:1--user index;2--other page
	def get_urls(self,url,type=1):
		if(type==2):
			self.get_page_urls(url)
			return
		reStr = {
		'urlList':'href=\"(?P<path_list>/[^/]*?/article/details/\d+)\"',
		'nextUrl':u'<a href=\"(?P<path_list>/[^\"]*?/article/list/\d+)\">下一页</a>',
		'title':'<title>(?P<path_list>.*?)</title>'
		}
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
			blogTitle=urlInfo['title']
			self.blog=self.work_home+'_'+blogTitle
			self.path=url.split('/')[3]
			return

	#获取其他页面的可爬取url列表
	def get_page_urls(self,url):
		print 'Loadding page [ '+str(self.pageNum)+' ] : '+url
		tm=time.strftime('%y_%m_%d',time.localtime(time.time()))
		reStr = {
		'urlList':'href=\"(?P<path_list>http://blog.csdn.net/[^/]*?/article/details/\d+)\"',
		'nextUrl':u'<a href=\"(?P<path_list>[^\"]*?\&page=\d+)\">下一页</a>',
		'title':'<title>(?P<path_list>.*?)</title>'
		}
		urlInfo=self.se.get_urls(url,reStr)
		trueUrl=url.replace(self.index_url,'')
		trueUrl=trueUrl.replace('//','/').replace('?','_').replace('&','_').replace('.','_')
		self.path=(trueUrl.replace('/','_')+'_'+tm).replace('__','_')
		try:
			title=urlInfo['title'].split(' - ')[0]
			self.blog=(title+'_'+tm).decode('utf-8')
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
	def get_index_data(self,mcm):
		self.pageNum=1
		#deal index posts
		self.get_urls(self.index_url,2)
		self.get_posts(mcm)
		#deal categroy posts
		reStr = {
		'urlList':'href=\"(?P<path_list>/[^/]*?/[^\"]*?\.html)\"',
		'nextUrl':'',
		'title':'<title>(?P<path_list>.*?)</title>'
		}
		urlInfo=self.se.get_urls(self.index_url,reStr)
		for url in urlInfo['urlList']:
			url=self.index_url+url
			print 'Find url: '+url
			self.get_urls(url,2)
			self.get_posts(mcm)

	#Get posts
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
		titles=post['title'].split('-')
		post['title']="".join(titles[0:(len(titles)-3)])
		post['content']=re.sub('<script[^>]*?>[\s\S]*?</script>','',post['content'])
		#print post
		self.post_list.append(post)


	def save_html_partly(self,mcm,part,partly):
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


if __name__ == '__main__':
	sc=Spider_Csdn()
	mcm=MakeChm()
	mcm.set_save_img(0)
	mcm.set_chm_path('E:\pycode\spider\chm\csdn_host')
	sc.set_partlyNum(3)
	sc.set_max_page(1)
	sc.get_index_data(mcm)

