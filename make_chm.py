# -*- coding: gbk -*-

import os,urllib,codecs,imghdr
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding( "gbk" )

class MakeChm:
	def __init__(self):
		self.blog=''
		self.post_list=[]
		self.chm_hhk='CHM_HHK.hhk'
		self.chm_hhc='CHM_HHC.hhc'
		self.chm_hhp='CHM_HHP.hhp'
		self.work_home='other/'
		self.path='csdn'
		self.cur_path=self.cur_file_dir()+'/'
		self.chm_path=self.cur_path
		self.save_img=0
		self.clear_html=1
		self.clear_img=0
		self.hhk_head=''.join(['<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">\r\n<HTML>',
		'\r\n<HEAD>\r\n<meta name="GENERATOR" content="www.waitig.com">\r\n<!-- Sitemap 1.0 -->',
		'</HEAD>\r\n<BODY><UL>'])
		self.hhk_tail=''.join(['</UL>\r\n</BODY></HTML><br><hr><br>You can download software at :',
		'<a href="http://www.waitig.com/" target=_blank>http://www.waitig.com</a> <br><br>'])
		self.hhc_head=''.join(['<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">',
		'<HTML>\r\n<HEAD>\r\n<meta name="GENERATOR" content="www.waitig.com">\r\n<!-- Sitemap 1.0 -->\r\n</HEAD><BODY>',
		'<OBJECT type="text/site properties">\r\n<param name="ExWindow Styles" value="0x200">',
		'<param name="Window Styles" value="0x800025">\r\n<param name="Font" value="MS Sans Serif,9,0">\r\n</OBJECT>\r\n<UL>'])

	def set_para(self,work_home,blog,path,post_list):
		self.work_home=work_home
		self.blog=blog
		self.post_list=post_list
		self.path=self.work_home+'/'+path

	def create_hhk(self):
		print 'Start to create hhk file!'
		obj_head='\r\n<LI> <OBJECT type="text/sitemap">\r\n<param name="Name" value="'
		obj_mid='">\r\n<param name="Local" value="'
		obj_tail='">\r\n</OBJECT>\r\n'
		try:
			hhk=codecs.open(self.path+"/"+self.chm_hhk,'w','gbk')
			hhk.write(self.hhk_head)
			hhk.flush()
			num=1
			for n in self.post_list:
				filename=str(n['id'])+'.html'
				if(n['title']!=[]):
					title='['+str(num)+']'+n['title'].replace('"','\'')
				else:
					title=''
				obj_text=obj_head+title+obj_mid+filename+obj_tail
				try:
					hhk.write(obj_text)
				except UnicodeEncodeError:
					print 'Encode Error! Title has illagel word!'
				hhk.flush()
				num+=1
			hhk.write(self.hhk_tail)
			hhk.flush()
			hhk.close()
		except IOError:
			print "Failed to create hhk file!"

	def create_hhc(self):
		print 'Start to create hhc file!'
		obj_head='\r\n<LI> <OBJECT type="text/sitemap">\r\n<param name="Name" value="'
		obj_mid='">\r\n<param name="ImageNumber" value="0">\r\n<param name="Local" value="'
		obj_tail='">\r\n</OBJECT>\r\n'
		try:
			hhc=codecs.open(self.path+"/"+self.chm_hhc,'w','gbk')
			hhc.write(self.hhc_head)
			hhc.flush()
			num=1
			for n in self.post_list:
				filename=str(n['id'])+'.html'
				if(n['title']!=[]):
					title='['+str(num)+']'+n['title'].replace('"','\'')
				else:
					title=''
				obj_text=obj_head+title+obj_mid+filename+obj_tail
				try:
					hhc.write(obj_text)
				except UnicodeEncodeError:
					print 'Encode Error! Title has illagel word!'
				hhc.flush()
				num+=1
			hhc.write(self.hhk_tail)
			hhc.flush()
			hhc.close()
		except IOError:
			print "Failed to create hhc file!"
		except UnicodeEncodeError:
			print 'Encode Error! Title has illagel word!'
			pass

	def create_hhp(self):
		print 'Start to create hhp file !'
		#print unicode(self.blog,'gbk')
		hhpText=''.join(['[OPTIONS]\r\nCompatibility=1.1 or later\r\nCompiled file=',self.blog,'.chm'
		'\r\nContents file=',self.chm_hhc,
		'\r\nDisplay compile progress=Yes\r\nIndex file=',self.chm_hhk,
		'\r\nLanguage=0x804\r\ntitle=',self.blog,
		'\r\nDefault topic=index.html\r\nImageType=Folder'])
		try:
			hhp=codecs.open(self.path+"/"+self.chm_hhp,'w','gbk')
			hhp.write(hhpText)
			hhp.flush()
			hhp.close()
		except IOError:
			print "Failed to create hhp file!"
		except UnicodeEncodeError:
			print 'Encode Error! Title has illagel word!'
			blogTitles=self.path.split('/')
			self.blog=blogTitles[len(blogTitles)-1]
			hhpText=''.join(['[OPTIONS]\r\nCompatibility=1.1 or later\r\nCompiled file=',self.blog,'.chm'
					'\r\nContents file=',self.chm_hhc,
					'\r\nDisplay compile progress=Yes\r\nIndex file=',self.chm_hhk,
					'\r\nLanguage=0x804\r\ntitle=',self.blog,
					'\r\nDefault topic=index.html\r\nImageType=Folder'])
			hhp.write(hhpText)
			hhp.flush()
			pass
		except UnicodeDecodeError:
			blogTitles=self.path.split('/')
			self.blog=blogTitles[len(blogTitles)-1]
			hhpText=''.join(['[OPTIONS]\r\nCompatibility=1.1 or later\r\nCompiled file=',self.blog,'.chm'
					'\r\nContents file=',self.chm_hhc,
					'\r\nDisplay compile progress=Yes\r\nIndex file=',self.chm_hhk,
					'\r\nLanguage=0x804\r\ntitle=',self.blog,
					'\r\nDefault topic=index.html\r\nImageType=Folder'])
			hhp.write(hhpText)
			hhp.flush()
			pass
		hhp.close()

	def create_html(self):
		print 'Start to create html file '
		if(os.path.exists(self.path)==False):
			os.makedirs(self.path)
		num=1;
		for n in self.post_list:
			try:
				path=self.path+"/"+str(n['id'])+'.html'
				print '['+str(num)+'] Creating '+path
				if(os.path.exists(path) and self.clear_html==0):
					print '['+str(num)+'] HTML File: ['+path+'] existed ,continue !'
					num+=1
					continue
				file=open(path,'w')
				file.write('<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head><body style="padding:20px;background-color:#C7EDCC;line-height:120%">\n')
				if(n['title']!=[]):
					file.write('<h1>'+n['title']+'</h1>\n')
				file.write(u'关键词: ')
				for keyword in n['keywords']:
					file.write(keyword+',')
				file.write('</br>'+u'所属分类: ')
				for cate in n['categories']:
					file.write(cate+',')
				if(n['url']!=[]):
					file.write('</br>'+u'原文链接: '+'<a href="'+n['url']+'" target="_blank">')
				if(n['title']!=[]):
					file.write(n['title'])
				file.write('</a>')
				if(self.save_img):
					n['content']=self.deal_pic(n['content'],self.path+'/',n['id'])
				file.write('<div style="padding:10px">\n'+n['content'])
				file.write('</div></body></html>')
				file.flush()
				file.close()
			except IOError:
				print "Failed to create html file!"
			except UnicodeEncodeError:
				print 'Encode Error! Title has illagel word!'
				pass
			num+=1

	def save(self):
		print 'Start to create chm file !'
		self.create_html()
		self.create_hhk()
		self.create_hhc()
		self.create_hhp()
		cmd='.\hhc.exe "'+self.path+'/'+self.chm_hhp+'"'
		os.system(cmd)
		chm_name=self.blog+'.chm'
		src_path=self.path+'/'+chm_name
		if(os.path.exists(self.chm_path+chm_name)):
			os.remove(self.chm_path+chm_name)
		print src_path
		print self.chm_path+chm_name
		os.rename(src_path,self.chm_path+chm_name)

	def deal_pic(self,content,htmlpath,id):
		img_path=htmlpath+'/img/'
		if(os.path.exists(img_path)==False):
			os.makedirs(img_path)
		soup = BeautifulSoup(content,"html.parser")
		#print soup
		imgs=soup.find_all('img')
		#print imgs
		num=1
		for n in imgs:
			src=n.get('src')
			if(src):
				print 'Find img : '+src
				urllib.urlretrieve(src,'tmp',None)
				imgType = imghdr.what('tmp')
				if(imgType):
					img_name=str(id)+'_'+str(num)+'.'+imgType
				else:
					img_name=str(id)+'_'+str(num)+'.unknown'
				img_src=self.cur_path+'/'+img_path+img_name
				img_src=img_src.replace('//','/')
				n['src']=img_src
				if(os.path.exists(img_src) and self.clear_img==0):
					print 'Picture ['+n['src']+'] exsited, continue!'
					os.remove('tmp')
				else:
					os.rename('tmp',img_src)
					print 'Saved img as '+n['src']+'!'
				num+=1
		return str(soup)

	def set_chm_path(self,path):
		self.chm_path=path+'/'
		if(os.path.exists(self.chm_path)==False):
			os.makedirs(self.chm_path)

	def set_save_img(self,save):
		self.save_img=save

	def set_clear_html(self,clear_html):
		self.clear_html=clear_html
	def set_clear_img(self,clear_img):
		self.clear_img=clear_img

	#获取脚本文件的当前路径
	def cur_file_dir(self):
		#获取脚本路径
		path = sys.path[0]
		#判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
		if os.path.isdir(path):
			return path
		elif os.path.isfile(path):
			return os.path.dirname(path)
