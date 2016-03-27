# -*- coding: utf-8 -*-

import requests,time,re,os
from bs4 import BeautifulSoup
from make_chm import *
import simplejson as json
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

#----------- 爬取csdn用户所有文章 -----------
class Spider_Cnblogs:

	def __init__(self):
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
		self.headers = {
			'Host':'www.cnblogs.com',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
			'Accept-Encoding': 'gzip, deflate',
			'Referer': 'http://www.cnblogs.com/',
			'Connection': 'keep-alive',
			'Cache-Control': 'max-age=0'
			}
		self.se = requests.Session()

	#获取作者主页中的可爬取文章url列表
	def get_urls(self,url,type):
		if(type==2):
			self.get_page_urls(url)
			return

		self.url=url
		Reslut=self.se.get(url,headers=self.headers)
		soup = BeautifulSoup(Reslut.text,"html.parser")
		postUrls=soup.find_all("div",{"class":"postTitle"})
		if(postUrls==[]):
			postUrls=soup.find_all("div",{"class":"post"})
			for n in postUrls:
				url=n.h2.a.get("href")
				self.url_list.append(url)
		else:
			for n in postUrls:
				url=n.a.get("href")
				self.url_list.append(url)
		list=re.findall(u'<a href=\"(?P<path_list>http://www.cnblogs.com/[^/]*?/default.html\?page=\d+)\">下一页</a>',Reslut.text)
		if list:
			urls=list[0]
			print 'Loading url:'+urls
			time.sleep(self.dely)
			self.get_urls(urls)
		else:
			blog=soup.title.get_text().split(' - ')
			pos=len(blog)-2
			self.blog=self.work_home+'_'+blog[pos]
			self.path=url.split('/')[3]
			return

	#获取任意页面可爬取的url列表
	def get_page_urls(self,url):
		print 'Loadding page [ '+str(self.pageNum)+' ] : '+url
		tm=time.strftime('%y_%m_%d',time.localtime(time.time()))
		Reslut=self.se.get(url,headers=self.headers)
		text=Reslut.text
		trueUrl=url.replace('http://www.cnblogs.com/','')
		trueUrl=trueUrl.replace('//','/').replace('?','_').replace('&','_').replace('.','_')
		self.path=(trueUrl.replace('/','_')+'_'+tm).replace('__','_')
		titles=re.findall('<title>(?P<path_list>.*?)</title>',text)
		try:
			title=titles[0].split(' - ')
			self.blog=(title[1]+'_'+title[0]+'_'+tm).decode('utf-8')
		except UnicodeDecodeError:
			self.blog=self.path
		#http://www.cnblogs.com/liqun-12345/p/5287428.html
		urllist=re.findall('href=\"(?P<path_list>http://www.cnblogs.com/[^/]*?/p/[^\.]*?\.html)\"',text)
		urllist=list(set(urllist))
		for n in urllist:
			self.url_list.append(n)
		#Recursive
		self.pageNum+=1
		if(self.pageNum>self.maxPage and self.maxPage!=-1):
			self.pageNum=1
			return
		else:
			nextUrl=re.findall(u'<a href=\"\/(?P<path_list>[^\"]*?\/\d+)\" onclick=\"[^\"]*?\">Next &gt;</a>',text)
			if nextUrl:
				self.get_page_urls(self.index_url+nextUrl[0])
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
		Reslut=self.se.get(self.index_url,headers=self.headers)
		text=Reslut.text
		urllist=re.findall('href=\"(?P<path_list>/cate/\d+\/)\"',text)
		urllist=list(set(urllist))
		for url in urllist:
			url=self.index_url+url
			print 'Find url: '+url
			self.get_urls(url,2)
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
		ids=url.split('/')
		id=ids[len(ids)-1]
		try:
			Reslut=self.se.get(url,headers=self.headers)
		except requests.exceptions.TooManyRedirects:
			print 'Need to login,skipped!'
			return
		soup = BeautifulSoup(Reslut.text,"html.parser")
		post={}
		post['id']=id.split('.')[0]
		post['url']=url
		post['title']=[]
		post['keywords']=[]
		post['categories']=[]
		post['content']=''
		title="".join(soup.title.get_text().split())
		post['title']="".join(title.split('-')[0])
		keywords=soup.find_all("div",{"id":"EntryTag"})
		for n in keywords:
			if(n.a):
				post['keywords'].append(n.a.get_text())
		categories=soup.find_all("div",{"id":"BlogPostCategory"})
		for n in categories:
			if(n.a):
				post['categories'].append(n.a.get_text())
		content=soup.find_all("div",{"id":"cnblogs_post_body"})
		for n in content:
			try:
				if (n.script):
					n.script.extract()
				post['content']=str(n)
			except RuntimeError:
				print 'Error ! Cant solve the content!'
		self.post_list.append(post)

	def get_blog(self):
		return "cnblogs_".join(self.blog)

	def get_path(self):
		urls=self.url.split('/')
		print urls[3]
		return urls[3]

	def save_html_partly(self,mcm,part,partly):
		#mcm=MakeChm()
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
