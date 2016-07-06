# -*- coding: utf-8 -*-

import time, re, os
from save_chm import *
from spider_model import *
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


# ----------- 爬取csdn用户所有文章 -----------
class SpiderRunoob(SpiderModel):
    def __init__(self, Spider=''):
        headers = {
            'Host': 'www.runoob.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://www.runoob.com/linux/linux-tutorial.html',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0'
        }
        SpiderModel.__init__(self, headers, Spider)
        self.user_index_reStr = {'urlList': 'href=\"/(?P<path_list>.*?/[^\.]*?\.html)\"',
                                 'nextUrl': u'<a rel=\"next\" href=\"/(?P<path_list>[^>]*?page=\d+)\">'
                                 }
        self.page_url_reStr = {  # href="/linux/linux-comm-cat.html"
            'urlList': 'href=\"/(?P<path_list>.*?/[^\.]*?\.html)\"',
            'nextUrl': u'<a rel=\"next\" href=\"/(?P<path_list>[^>]*?page=\d+)\">'
        }
        self.index_url_reStr = {  # href="/t/node.js"
            'urlList': 'href=\"/(?P<path_list>t/[^\"]*?)\"',
            'nextUrl': ''
        }
        self.post_reStr = {
            'id': '/.*?(?P<path_list>[^/]*?)\.html',
            'title' : '<h2>(?P<title>[\s\S]*?)</h2>',
            'keywords': '<a class=\"tag\"[^>][\s\S]*?>(?P<keywords>[^<]*?)</a>',
            'categories': 'blog_articles_fenlei\']\);\">(?P<cate>[\s\S]*?)</span>',
            'content': '<div class=\"article-intro\" id=\"content\">(?P<content>[\s\S]*?)</div></div>'
        }
        self.work_home = 'html/runoob'
        self.index_url = 'http://www.runoob.com/'


if __name__ == '__main__':
    sc = SpiderRunoob()
    mcm = MakeChm()
    mcm.set_save_img(0)
    mcm.set_partlyNum(20)
    mcm.set_chm_path('E:\pycode\spider\chm\\runoob_host')
    sc.set_dely(1)
    sc.set_max_page(2)
    sc.get_urls('http://www.runoob.com/linux/linux-command-manual.html',2,mcm)
    #sc.get_index_data(mcm)
    sc.get_posts(mcm)
