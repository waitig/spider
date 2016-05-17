# -*- coding: utf-8 -*-

import re, sys
from save_chm import *
from spider_model import *

reload(sys)
sys.setdefaultencoding("utf-8")


# ----------- 爬取csdn用户所有文章 -----------
class Spider_Csdn(SpiderModel):
    def __init__(self, Spider):
        headers = {
            'Host': 'blog.csdn.net',
            'User-Agent': ' Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://blog.csdn.net/',
            'Connection': 'keep-alive'
        }
        SpiderModel.__init__(self, headers, Spider)
        self.user_index_reStr = {
            'urlList': 'href=\"(?P<path_list>/[^/]*?/article/details/\d+)\"',
            'nextUrl': u'<a href=\"(?P<path_list>/[^\"]*?/article/list/\d+)\">下一页</a>',
            'title': '<title>(?P<path_list>[\s\S]*?)</title>'
        }
        self.page_url_reStr = {
            'urlList': 'href=\"(?P<path_list>http://blog.csdn.net/[^/]*?/article/details/\d+)\"',
            'nextUrl': u'<a href=\"(?P<path_list>[^\"]*?\&page=\d+)\">下一页</a>',
            'title': '<title>(?P<path_list>[\s\S]*?)</title>'
        }
        self.index_url_reStr = {
            'urlList': 'href=\"(?P<path_list>/[^/]*?/[^\"]*?\.html)\"',
            'nextUrl': '',
            'title': '<title>(?P<path_list>[\s\S]*?)</title>'
        }
        self.post_reStr = {
            'id': 'http://blog.csdn.net/[^/]*?/article/details/(?P<id>\d+)',
            'title': '<title>(?P<path_list>[\s\S]*?)</title>',
            'keywords': 'blog_articles_tag\']\);\">(?P<keywords>[^<]*?)</a>',
            'categories': 'blog_articles_fenlei\']\);\">(?P<cate>[\s\S]*?)</span>',
            'content': '<div id=\"article_content\" class=\"article_content\">(?P<content>[\s\S]*?)</div>[^<]*?<!-- Baidu Button BEGIN -->'
        }
        self.work_home = 'html/csdn'
        self.index_url = 'http://blog.csdn.net/'

    #        SpiderModel.__init__(self, headers,Spider)

    def deal_post_title(self, title):
        titles = title.split('-')
        return "".join(titles[0:(len(titles) - 3)])

    def deal_post_content(self, content):
        return re.sub('<script[^>]*?>[\s\S]*?</script>', '', content)

    def __del__(self):
        # SpiderModel.__del__(self)
        pass


if __name__ == '__main__':
    sc = Spider_Csdn()
    mcm = MakeChm()
    mcm.set_save_img(0)
    mcm.set_partlyNum(50)
    mcm.set_chm_path('E:\pycode\spider\chm\csdn_host')
    sc.set_max_page(1)
    sc.get_urls('http://blog.csdn.net/u010189918', 1, mcm)
    sc.get_posts(mcm)
# sc.get_index_data(mcm)
