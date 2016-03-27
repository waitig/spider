# -*- coding: utf-8 -*-
#This is the heart of this spider

import requests,time,re,os

class Spider_Engine:
	def __init__(self,headers):
		self.debug=1
		self.headers = headers
		self.se = requests.Session()
	def set_debug(self,debug):
		self.debug=debug
	def set_headers(self,headers):
		self.headers=headers
	def get_title(self):
		return self.title
	def dpt(self,str):
		if(self.debug):
			print str
		else:
			pass
	
	#Get urls in the page
	def get_urls(self,url,reStr,pre_url=''):
		urlInfo = {'title':'','urlList':[],'nextUrl':''}
		Reslut=self.se.get(url,headers=self.headers)
		urlList=re.findall(reStr['urlList'],Reslut.text)
		urlList=list(set(urlList))
		for n in urlList:
			urlInfo['urlList'].append(pre_url+n)
		#urlInfo['urlList']=urlList
		title=re.findall(reStr['title'],Reslut.text)
		if(title!=[]):
			urlInfo['title']=title[0]
		nextUrl=re.findall(reStr['nextUrl'],Reslut.text)
		if(nextUrl!=[]):
			urlInfo['nextUrl']=pre_url+nextUrl[0]
		return urlInfo
	
	#Get post from the url
	def get_post(self,url,reStr):
		post={}
		post['id']=''
		post['url']=url
		post['title']=''
		post['keywords']=[]
		post['categories']=[]
		post['content']=''
		try:
			Reslut=self.se.get(url,headers=self.headers)
		except requests.exceptions.ConnectionError:
			print 'This article not found [404]!'
			post['title']='404 NOT FOUND!'
			post['content']='404 NOT FOUND!'
			return post
		text=Reslut.text
		title=re.findall('<title>(?P<path_list>.*?)</title>',text,re.S)
		try:
			post['title']="".join(title[0].split())
		except UnicodeDecodeError:
			print 'Get title unicode decode error!'
		id=re.findall(reStr['id'],url)
		try:
			post['id']=id[0]
		except UnicodeDecodeError:
			print 'Get ID unicode decode error!'
		keywords=re.findall(reStr['keywords'],text)
		for n in keywords:
			post['keywords'].append(n)
		categories=re.findall(reStr['categories'],text)
		for n in categories:
			post['categories'].append(n)
		content=re.findall(reStr['content'],text,re.S)
		#self.dpt(reStr['content'])
		#self.dpt(post)
		try:
			#post['content']=re.sub('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>','',content[0])
			post['content']=content[0]
		except UnicodeDecodeError:
			print 'Get content unicode decode error!'
		return post
		
		
		
if __name__ == '__main__':
	se=Spider_Engine()
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
	se.set_headers(headers)
	reStar={
	'id':'http://www.cnblogs.com/[^/]*?/p/(?P<id>\d+)\.html',
	'keywords':'<div id=\"EntryTag\">(?P<keywords>[^<]*?)</div>',
	'categories':'<div id=\"BlogPostCategory\">(?P<cate>[^<]*?)</div>',
	'content':'<div id=\"cnblogs_post_body\">(?P<content>.*?)</div><div id=\"MySignature\">'
	}
	post=se.get_post('http://www.cnblogs.com/AndyJee/p/4695813.html',reStar)
	print post
	
		