# -*- coding: utf-8 -*-

import urllib2,time,re,os,string
from bs4 import BeautifulSoup
from make_chm import *
import simplejson as json
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

#----------- 爬取csdn用户所有文章 -----------
class Spider_Sina:

	def __init__(self):
		self.url_list=[]
		self.post_list=[]
		self.blog=''
		self.url=''
		self.path=''
		self.dely=1
		self.partlyNum=1
		self.work_home='sina'
		self.headers = {
			'Host':'blog.sina.com.cn',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
			'Referer': 'http://blog.sina.com.cn',
			'Connection': 'keep-alive',
			'Cache-Control': 'max-age=0'
			}

	#获取作者主页中的可爬取文章url列表
	def get_urls(self,url,type):
		if(type==2):
			self.get_page_urls(url)
			return

		self.url=url
		response = urllib2.urlopen(url)
		text=response.read().replace('<![endif]','<')
		soup = BeautifulSoup(text,"html.parser")
		postUrls=soup.find_all("span",{"class":"atc_title"})
		for n in postUrls:
			url=n.a.get("href")
			self.url_list.append(url)
		nexturls=soup.find_all("li",{"class":"SG_pgnext"})
		if(nexturls):
			for n in nexturls:
				urls=n.a.get("href")
			print 'Find url:'+urls
			time.sleep(self.dely)
			self.get_urls(urls)
		else:
			blog=soup.title.get_text().split(' - ')
			pos=len(blog)-2
			self.blog="".join(blog[pos])
			urls=self.url.split('/')
			self.path=urls[4].split('_')[1]
			return

	#获取其他页面的可爬取url列表
	def get_page_urls(self,url):
		#del self.url_list[:]
		tm=time.strftime('%y_%m_%d',time.localtime(time.time()))
		response = urllib2.urlopen(url)
		text=response.read()
		trueUrl=url.replace('http://','')
		self.path=trueUrl.replace('/','_').replace('.','_')+tm
		title=re.findall('<title>(?P<path_list>.*?)</title>',text)
		try:
			self.blog=(title[0]+'_'+tm).decode('utf-8')
		except UnicodeDecodeError:
			self.blog=self.path
		urllist=re.findall('href=\"(?P<path_list>http://blog.sina.com.cn/s/blog_[^\"]*?.html)[^\"]*?\"',text)
		urllist=list(set(urllist))
		for n in urllist:
			self.url_list.append(n)

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
		ids=url.split('/')
		id=ids[len(ids)-1]
		response = urllib2.urlopen(url)
		text=response.read().replace('<![endif]','<')
		soup = BeautifulSoup(text,"html.parser")
		post={}
		post['id']=id.split('.')[0]
		post['url']=url
		post['title']=''
		post['keywords']=[]
		post['categories']=[]
		post['content']=''
		title=soup.title
		try:
			post['title']=title.get_text().split('_')[0]
		except AttributeError:
			post['title']=u'404啦'
		keywords=soup.find_all("td",{"class":"blog_tag"})
		for n in keywords:
			if(n.h3):
				post['keywords'].append(n.h3.a.get_text())
		categories=soup.find_all("div",{"id":"BlogPostCategory"})
		for n in categories:
			if(n.a):
				post['categories'].append(n.a.get_text())
		content=soup.find_all("div",{"id":"sina_keyword_ad_area2"})
		for n in content:
			try:
				if (n.script):
					n.script.extract()
				post['content']=str(n).replace('src','r_src')
				post['content']=post['content'].replace('real_r_src','src')
			except RuntimeError:
				print 'Error ! Cant solve the content!'
		self.post_list.append(post)

	def save_html_partly(self,mcm,part,partly):
		if(partly>0):
			blog=self.blog+'_part_'+str(part)
			path=self.path+'_part_'+str(part)
		else:
			blog=self.blog
			path=self.path
		mcm.set_para(self.work_home,blog,path,self.post_list)
		mcm.make_chm()
		del self.post_list[:]

	def set_dely(self,dely):
		self.dely=dely

	def set_partlyNum(self,partlyNum):
		self.partlyNum=partlyNum
	#从主页开始获取所有频道首页文章
	def get_index_data(self,mcm):
		#self.get_urls('http://blog.sina.com.cn/',2)
		#self.get_posts(mcm)
		response = urllib2.urlopen('http://blog.sina.com.cn/')
		text=response.read()
		urls=re.findall('href=\"(?P<path_list>http://blog.sina.com.cn/lm/[^/]*?/)\"',text)
		urls=list(set(urls))
		for url in urls:
			print 'Find url: '+url
			self.get_urls(url,2)
			self.get_posts(mcm)

if __name__ == '__main__':
	sc=Spider_Sina()
	mcm=MakeChm()
	mcm.set_save_img(0)
	mcm.set_clear_html(1)
	mcm.set_chm_path('E:\pycode\spider\chm\sina_host')
	sc.set_partlyNum(50)
	sc.get_urls('http://blog.sina.com.cn/',2)
	sc.get_posts(mcm)
	#sc.get_index_data(mcm)