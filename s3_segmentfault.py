# -*- coding: utf-8 -*-

import time, re, os
from save_chm import *
from spider_model import *
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


# ----------- 爬取csdn用户所有文章 -----------
class SpiderSegement(SpiderModel):
    def __init__(self, Spider):
        headers = {
            'Host': 'segmentfault.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://segmentfault.com/',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0'
        }
        SpiderModel.__init__(self, headers, Spider)
        self.user_index_reStr = {'urlList': 'href=\"/(?P<path_list>a/\d+)\"',
                                 'nextUrl': u'<a rel=\"next\" href=\"/(?P<path_list>[^>]*?page=\d+)\">'
                                 }
        self.page_url_reStr = {  # /a/1190000004736240#<a rel="next" href="/blogs?page=2">
            'urlList': 'href=\"/(?P<path_list>a/\d+)\"',
            'nextUrl': u'<a rel=\"next\" href=\"/(?P<path_list>[^>]*?page=\d+)\">'
        }
        self.index_url_reStr = {  # href="/t/node.js"
            'urlList': 'href=\"/(?P<path_list>t/[^\"]*?)\"',
            'nextUrl': ''
        }
        self.post_reStr = {
            'id': '/a/(?P<path_list>\d+)',
            'keywords': '<a class=\"tag\"[^>][\s\S]*?>(?P<keywords>[^<]*?)</a>',
            'categories': 'blog_articles_fenlei\']\);\">(?P<cate>[\s\S]*?)</span>',
            'content': '<div class=\"article fmt article__content\"[^>]*?>(?P<content>[\s\S]*?)</div>[^<]*?<div class=\"clearfix'
        }
        self.work_home = 'segmentfault'
        self.index_url = 'https://segmentfault.com/'

    # 重写相关代码
    def deal_post_title(self, title):
        titles = title.split('-')
        return "".join(titles[0:(len(titles) - 2)])

    def deal_post_content(self, content):
        content = content.replace('data-src', 'src')
        content = content.replace('src=\"/img/', 'src=\"' + self.index_url + 'img/')
        return re.sub('<script[^>]*?>[\s\S]*?</script>', '', content)

    def deal_index_data(self):
        return 'https://segmentfault.com/blogs'

    def deal_page_urls(self, url):
        if re.match('https://segmentfault.com/t/.*?[^page=\d+]$', url):
            url = url + '/blogs'
        return url


if __name__ == '__main__':
    sc = SpiderSegement()
    mcm = MakeChm()
    mcm.set_save_img(0)
    mcm.set_partlyNum(50)
    mcm.set_chm_path('E:\pycode\spider\chm\segment_host')
    print type(mcm)
    sc.set_dely(1)
    sc.set_max_page(2)
    # sc.get_urls('https://segmentfault.com/t/javascript',2,mcm)
    sc.get_index_data(mcm)
    # sc.get_posts(mcm)
