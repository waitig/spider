# -*- coding: utf-8 -*-

import time, re, os
from save_chm import *
from spider_model import *
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


# ----------- 爬取csdn用户所有文章 -----------
class SpiderCnblogs(SpiderModel):
    def __init__(self, Spider):
        headers = {
            'Host': 'www.cnblogs.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://www.cnblogs.com/',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0'
        }
        SpiderModel.__init__(self, headers, Spider)
        self.user_index_reStr = {'urlList': 'href=\"http://www.cnblogs.com/(?P<path_list>[^/]*?/p/[^\.]*?\.html)\"',
                                 'nextUrl': u'<a href=\"\/(?P<path_list>[^\"]*?\/\d+)\" onclick=\"[^\"]*?\">Next &gt;</a>',
                                 'title': '<title>(?P<title>[\s\S]*?)</title>'
                                 }
        self.page_url_reStr = {
            'urlList': 'href=\"http://www.cnblogs.com/(?P<path_list>[^/]*?/p/[^\.]*?\.html)\"',
            'nextUrl': u'<a href=\"\/(?P<path_list>[^\"]*?\/\d+)\" onclick=\"[^\"]*?\">Next &gt;</a>',
            'title': '<title>(?P<title>[\s\S]*?)</title>'
        }
        self.index_url_reStr = {
            'urlList': 'href=\"(?P<path_list>/cate/\d+\/)\"',
            'nextUrl': '',
            'title': '<title>(?P<title>[\s\S]*?)</title>'
        }
        self.post_reStr = {
            'title': '<title>(?P<title>[\s\S]*?)</title>',
            'id': 'http://www.cnblogs.com/[^/]*?/p/(?P<id>[^\.]*?)\.html',
            'keywords': 'blog_articles_tag\']\);\">(?P<keywords>[^<]*?)</a>',
            'categories': 'blog_articles_fenlei\']\);\">(?P<cate>[\s\S]*?)</span>',
            'content': '<div id=\"cnblogs_post_body\"[^>]*?>(?P<content>[\s\S]*?)</div><div id=\"MySignature\">',
            'content1': '<div id=\"cnblogs_post_body\">(?P<content>[\s\S]*?)</div><div id=\"MySignature\">'
        }
        self.work_home = 'html/cnblogs'
        self.index_url = 'http://www.cnblogs.com/'

    # 重写相关代码
    def deal_post_title(self, title):
        titles = title.split('-')
        return "".join(titles[0:(len(titles) - 2)])

    def deal_post_content(self, content):
        return re.sub('<script[^>]*?>[\s\S]*?</script>', '', content)


if __name__ == '__main__':
    sc = SpiderCnblogs()
    mcm = MakeChm()
    mcm.set_save_img(0)
    mcm.set_partlyNum(50)
    mcm.set_chm_path('E:\pycode\spider\chm\cnblogs_host')
    print type(mcm)
    sc.set_dely(1)
    sc.set_max_page(2)
    sc.get_urls('http://www.cnblogs.com/qjkobe/', 1, mcm)
    # sc.get_index_data(mcm)
    sc.get_posts(mcm)
