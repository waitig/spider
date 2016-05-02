# -*- coding: gbk -*-

import os, urllib, codecs, imghdr
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding("gbk")


class MakeChm:
    def __init__(self):
        self.blog = ''
        self.blog_pre = ''
        self.path_pre = ''
        self.post_list = []
        self.chm_hhk = 'CHM_HHK.hhk'
        self.chm_hhc = 'CHM_HHC.hhc'
        self.chm_hhp = 'CHM_HHP.hhp'
        self.work_home = 'other/'
        self.path = 'csdn'
        self.post_number = 1
        self.part_number = 1
        self.partly_number = 50
        self.cur_path = self.cur_file_dir() + '/'
        self.chm_path = self.cur_path
        self.save_img = 0
        self.clear_html = 1
        self.clear_img = 0
        self.hhk_head = ''.join(['<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">\r\n<HTML>',
                                 '\r\n<HEAD>\r\n<meta name="GENERATOR" content="www.waitig.com">\r\n<!-- Sitemap 1.0 -->',
                                 '</HEAD>\r\n<BODY><UL>'])
        self.hhk_tail = ''.join(['</UL>\r\n</BODY></HTML><br><hr><br>You can download software at :',
                                 '<a href="http://www.waitig.com/" target=_blank>http://www.waitig.com</a> <br><br>'])
        self.hhc_head = ''.join(['<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">',
                                 '<HTML>\r\n<HEAD>\r\n<meta name="GENERATOR" content="www.waitig.com">\r\n<!-- Sitemap 1.0 -->\r\n</HEAD><BODY>',
                                 '<OBJECT type="text/site properties">\r\n<param name="ExWindow Styles" value="0x200">',
                                 '<param name="Window Styles" value="0x800025">\r\n<param name="Font" value="MS Sans Serif,9,0">\r\n</OBJECT>\r\n<UL>'])

    def set_para(self, work_home, blog, path):
        self.work_home = work_home
        self.blog_pre = blog
        self.path_pre = self.work_home + '/' + path
        self.blog = blog
        self.path = self.work_home + '/' + path
        self.part_number = 1
        self.post_number = 1
        del self.post_list[:]

    def create_hhk(self):
        print 'Start to create hhk file!'
        obj_head = '\r\n<LI> <OBJECT type="text/sitemap">\r\n<param name="Name" value="'
        obj_mid = '">\r\n<param name="Local" value="'
        obj_tail = '">\r\n</OBJECT>\r\n'
        try:
            hhk = codecs.open(self.path + "/" + self.chm_hhk, 'w', 'gbk')
            hhk.write(self.hhk_head)
            hhk.flush()
            num = 1
            for n in self.post_list:
                filename = str(n['id']) + '.html'
                if (n['title'] != []):
                    title = '[' + str(num) + ']' + n['title'].replace('"', '\'')
                else:
                    title = ''
                obj_text = obj_head + title + obj_mid + filename + obj_tail
                try:
                    hhk.write(obj_text)
                except UnicodeEncodeError:
                    print 'Encode Error! Title has illagel word!'
                hhk.flush()
                num += 1
            hhk.write(self.hhk_tail)
            hhk.flush()
            hhk.close()
        except IOError:
            print "Failed to create hhk file!"

    def create_hhc(self):
        print 'Start to create hhc file!'
        obj_head = '\r\n<LI> <OBJECT type="text/sitemap">\r\n<param name="Name" value="'
        obj_mid = '">\r\n<param name="ImageNumber" value="0">\r\n<param name="Local" value="'
        obj_tail = '">\r\n</OBJECT>\r\n'
        try:
            hhc = codecs.open(self.path + "/" + self.chm_hhc, 'w', 'gbk')
            hhc.write(self.hhc_head)
            hhc.flush()
            num = 1
            for n in self.post_list:
                filename = str(n['id']) + '.html'
                if (n['title'] != []):
                    title = '[' + str(num) + ']' + n['title'].replace('"', '\'')
                else:
                    title = ''
                obj_text = obj_head + title + obj_mid + filename + obj_tail
                try:
                    hhc.write(obj_text)
                except UnicodeEncodeError:
                    print 'Encode Error! Title has illagel word!'
                hhc.flush()
                num += 1
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
        blogs = self.blog.split('/')
        self.blog = blogs[len(blogs) - 1]
        # print unicode(self.blog,'gbk')
        hhpText = ''.join(['[OPTIONS]\r\nCompatibility=1.1 or later\r\nCompiled file=', self.blog, '.chm'
                                                                                                   '\r\nContents file=',
                           self.chm_hhc,
                           '\r\nDisplay compile progress=Yes\r\nIndex file=', self.chm_hhk,
                           '\r\nLanguage=0x804\r\ntitle=', self.blog,
                           '\r\nDefault topic=index.html\r\nImageType=Folder'])
        try:
            hhp = codecs.open(self.path + "/" + self.chm_hhp, 'w', 'gbk')
            hhp.write(hhpText)
            hhp.flush()
            hhp.close()
        except IOError:
            print "Failed to create hhp file!"
        except UnicodeEncodeError:
            print 'Encode Error! Title has illagel word!'
            blogTitles = self.path.split('/')
            self.blog = blogTitles[len(blogTitles) - 1]
            hhpText = ''.join(['[OPTIONS]\r\nCompatibility=1.1 or later\r\nCompiled file=', self.blog, '.chm'
                                                                                                       '\r\nContents file=',
                               self.chm_hhc,
                               '\r\nDisplay compile progress=Yes\r\nIndex file=', self.chm_hhk,
                               '\r\nLanguage=0x804\r\ntitle=', self.blog,
                               '\r\nDefault topic=index.html\r\nImageType=Folder'])
            hhp.write(hhpText)
            hhp.flush()
            pass
        except UnicodeDecodeError:
            blogTitles = self.path.split('/')
            self.blog = blogTitles[len(blogTitles) - 1]
            hhpText = ''.join(['[OPTIONS]\r\nCompatibility=1.1 or later\r\nCompiled file=', self.blog, '.chm'
                                                                                                       '\r\nContents file=',
                               self.chm_hhc,
                               '\r\nDisplay compile progress=Yes\r\nIndex file=', self.chm_hhk,
                               '\r\nLanguage=0x804\r\ntitle=', self.blog,
                               '\r\nDefault topic=index.html\r\nImageType=Folder'])
            hhp.write(hhpText)
            hhp.flush()
            pass
        hhp.close()

    def save_post(self, post):
        postInfo = {}
        postInfo['title'] = post['title']
        postInfo['id'] = post['id']
        self.post_list.append(postInfo)
        if (os.path.exists(self.path) == False):
            os.makedirs(self.path)
        try:
            path = self.path + "/" + str(post['id']) + '.html'
            print '[' + str(self.post_number) + '] Creating ' + path
            if (os.path.exists(path) and self.clear_html == 0):
                print '[' + str(self.post_number) + '] HTML File: [' + path + '] existed ,continue !'
                self.post_number += 1
                return
            file = open(path, 'w')
            file.write(
                '<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head><body style="padding:20px;background-color:#C7EDCC;line-height:120%">\n')
            if (post['title'] != []):
                file.write('<h1>' + post['title'] + '</h1>\n')
            file.write(u'关键词: ')
            for keyword in post['keywords']:
                file.write(keyword + ',')
            file.write('</br>' + u'所属分类: ')
            for cate in post['categories']:
                file.write(cate + ',')
            if (post['url'] != []):
                file.write('</br>' + u'原文链接: ' + '<a href="' + post['url'] + '" target="_blank">')
            if (post['title'] != []):
                file.write(post['title'])
            file.write('</a>')
            if (self.save_img):
                post['content'] = self.deal_pic(post['content'], self.path + '/', post['id'])
            file.write('<div style="padding:10px">\n' + post['content'])
            file.write('</div></body></html>')
            file.flush()
            file.close()
        except IOError:
            print "Failed to create html file!"
        except UnicodeEncodeError:
            print 'Encode Error! Title has illagel word!'
            pass
        self.post_number += 1
        if (self.post_number > self.partly_number):
            self.save_it()

    def make_chm(self):
        print 'Start to create chm file !'
        self.create_hhk()
        self.create_hhc()
        self.create_hhp()
        cmd = '.\hhc.exe "' + self.path + '/' + self.chm_hhp + '"'
        os.system(cmd)
        chm_name = self.blog + '.chm'
        src_path = self.path + '/' + chm_name
        if (os.path.exists(self.chm_path + chm_name)):
            os.remove(self.chm_path + chm_name)
        os.rename(src_path, self.chm_path + chm_name)

    def deal_pic(self, content, htmlpath, id):
        img_path = htmlpath + '/img/'
        if (os.path.exists(img_path) == False):
            os.makedirs(img_path)
        soup = BeautifulSoup(content, "html.parser")
        # print soup
        imgs = soup.find_all('img')
        # print imgs
        num = 1
        for n in imgs:
            src = n.get('src')
            if (src):
                print 'Find img : ' + src
                urllib.urlretrieve(src, 'tmp', None)
                imgType = imghdr.what('tmp')
                if (imgType):
                    img_name = str(id) + '_' + str(num) + '.' + imgType
                else:
                    img_name = str(id) + '_' + str(num) + '.unknown'
                img_src = self.cur_path + '/' + img_path + img_name
                img_src = img_src.replace('//', '/')
                n['src'] = img_src
                if (os.path.exists(img_src) and self.clear_img == 0):
                    print 'Picture [' + n['src'] + '] exsited, continue!'
                    os.remove('tmp')
                else:
                    os.rename('tmp', img_src)
                    print 'Saved img as ' + n['src'] + '!'
                num += 1
        return str(soup)

    def set_chm_path(self, path):
        self.chm_path = path + '/'
        if (os.path.exists(self.chm_path) == False):
            os.makedirs(self.chm_path)

    def set_partlyNum(self, num):
        self.partly_number = num

    def set_save_img(self, save):
        self.save_img = save

    def set_clear_html(self, clear_html):
        self.clear_html = clear_html

    def set_clear_img(self, clear_img):
        self.clear_img = clear_img

    # 获取脚本文件的当前路径
    def cur_file_dir(self):
        # 获取脚本路径
        path = sys.path[0]
        # 判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
        if os.path.isdir(path):
            return path
        elif os.path.isfile(path):
            return os.path.dirname(path)

    # 强制存储
    def save_it(self):
        if self.post_number > 2:
            self.part_number += 1
            self.make_chm()
            self.blog = self.blog_pre + '_part_' + str(self.part_number)
            self.path = self.path_pre + '_part_' + str(self.part_number)
            self.post_number = 1
            del self.post_list[:]

    # 析构函数
    def __del__(self):
        self.save_it()
