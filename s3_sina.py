# -*- coding: utf-8 -*-

import time, re, os
from save_chm import *
from spider_model import *
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


# ----------- 爬取csdn用户所有文章 -----------
class SpiderSina(SpiderModel):
    def __init__(self):
        self.work_home = 'sina'
        self.index_url = 'http://blog.sina.com.cn/'
        self.splitChar = '_'
        headers = {
            'Host': 'blog.sina.com.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://blog.sina.com.cn/s/blog_8765683c0102wf57.html',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0'
        }  # http://blog.sina.com.cn/s/blog_4eb5b1410102wm6f.html
        self.user_index_reStr = {'urlList': 'href=\"http://blog.sina.com.cn/(?P<path_list>s/blog_[^\.]*?\.html)\"',
                                 # <li class="SG_pgnext"><a href="http://blog.sina.com.cn/s/articlelist_2271569980_0_2.html"
                                 'nextUrl': u'<li class=\"SG_pgnext\"><a href=\"http://blog.sina.com.cn/(?P<path_list>s/articlelist_[^\.]*?\.html)\"',
                                 }
        self.page_url_reStr = {
            'urlList': 'href=\"http://blog.sina.com.cn/(?P<path_list>s/blog_[^\.]*?\.html)',
            'nextUrl': u'<a href=\"\/(?P<path_list>[^\"]*?\/\d+)\" onclick=\"[^\"]*?\">Next &gt;</a>',
        }
        self.index_url_reStr = {  # http://blog.sina.com.cn/lm/
            'urlList': 'href=\"http://blog.sina.com.cn/(?P<path_list>/lm/[^/]*?/)\"',
            'nextUrl': '',
        }
        self.post_reStr = {
            'id': 'http://blog.sina.com.cn/s/(?P<id>[^\.]*?)\.html',
            # <a href="http://search.sina.com.cn/?c=blog&q=%D3%E9%C0%D6&by=tag" target="_blank">娱乐</a>
            'keywords': 'by=tag\" target=\"_blank\">(?P<keywords>[^<]*?)</a>',
            'categories': 'blog_articles_fenlei\']\);\">(?P<cate>[\s\S]*?)</span>',
            'content': u'<div id=\"sina_keyword_ad_area2\"[^>]*?>(?P<content>[\s\S]*?)</div>[^<]*?<!--',
            'content1': u'<!-- 正文开始 -->(?P<content>[\s\S]*?)<!-- 正文结束 -->'
        }
        SpiderModel.__init__(self, headers)
        self.set_useUrllib2(1)
        self.set_splitChar('_')

    # 重写相关代码
    def deal_post_title(self, title):
        title = title.decode('utf-8').replace('&nbsp;', ' ')
        titles = title.split('_')
        return "".join(titles[0:(len(titles) - 2)])

    def deal_post_content(self, content):
        content = content.decode('utf-8').replace('src', 'r_src')
        content = content.replace('real_r_src', 'src')
        # print content
        return re.sub('<script[^>]*?>[\s\S]*?</script>', '', content)

    def deal_title(self, title):
        title = title.decode('utf-8')
        return title


if __name__ == '__main__':
    sc = SpiderSina()
    mcm = MakeChm()
    mcm.set_save_img(0)
    mcm.set_partlyNum(20)
    mcm.set_chm_path('E:\pycode\spider\chm\sina_host')
    sc.set_dely(1)
    sc.set_max_page(2)
    # sc.get_urls('http://blog.sina.com.cn/s/articlelist_2271569980_0_1.html',1,mcm)
    # sc.get_posts(mcm)
    sc.get_index_data(mcm)
