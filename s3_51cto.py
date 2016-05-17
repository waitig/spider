# -*- coding: utf-8 -*-

import re, sys
from save_chm import *
from spider_model import *

reload(sys)
sys.setdefaultencoding("utf-8")


# ----------- 爬取51cto博客用户所有文章 -----------
class Spider_51CTO(SpiderModel):
    def __init__(self, Spider):
        headers = {
            'Host': 'blog.51cto.com',
            'User-Agent': ' Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://www.51cto.com/',
            'Connection': 'keep-alive'
        }
        SpiderModel.__init__(self, headers, Spider)
        self.user_index_reStr = {
            # href="http://506554897.blog.51cto.com/2823970/1764842"http://os.51cto.com/art/201604/510421.htm
            'urlList': 'href=\"(?P<path_list>http://[^/]*?.51cto.com/[\"]*?)\"',
            'nextUrl': '',
            'title': '<title>(?P<path_list>[\s\S]*?)</title>'
        }
        self.page_url_reStr = {
            'urlList': 'href=\"(?P<path_list>http://[^/]*?.51cto.com/[\"]*?)\"',
            'nextUrl': '',
            'title': '<title>(?P<path_list>[\s\S]*?)</title>'
        }
        self.index_url_reStr = {
            'urlList': 'href=\"(?P<path_list>http://[^/]*?.51cto.com/[\"]*?)\"',
            'nextUrl': '',
            'title': '<title>(?P<path_list>[\s\S]*?)</title>'
        }
        self.post_reStr = {
            'id': 'http://[^/]*?.51cto.com/\d+/(?P<id>\d+)',
            'title': '<title>(?P<path_list>[\s\S]*?)</title>',
            'keywords': 'class=\"operlink\">(?P<keywords>.*?)</a>',  # <div class="zwnr">
            'categories': '',
            'content': u'<div class=\"zwnr\">(?P<content>[\s\S]*?)</div>[^<]*?<div class=\"share5\">',
            'content1': u'<!--正文 begin-->(?P<content>[\s\S]*?)<!--正文 end-->'
        }
        self.work_home = 'html/cto51'
        self.index_url = 'http://www.51cto.com/'

    #        SpiderModel.__init__(self, headers)

    def deal_post_title(self, title):
        titles = title.split('-')
        return "".join(titles[0:(len(titles) - 3)])

    def deal_post_content(self, content):
        return re.sub('<script[^>]*?>[\s\S]*?</script>', '', content)

    def deal_pre_url(self):
        return ''

    def __del__(self):
        # SpiderModel.__del__(self)
        pass


if __name__ == '__main__':
    sc = Spider_51CTO()
    mcm = MakeChm()
    mcm.set_save_img(0)
    mcm.set_partlyNum(50)
    mcm.set_chm_path('E:\pycode\spider\chm\cto51_host')
    sc.set_max_page(1)
    # sc.get_urls('http://blog.csdn.net/u010189918', 1, mcm)
    # sc.get_posts(mcm)
    sc.get_index_data(mcm)
