# -*- coding: utf-8 -*-

import requests, re, sys
from save_chm import *
from spider_model import *

reload(sys)
sys.setdefaultencoding("utf-8")


# ----------- 爬取csdn用户所有文章 -----------
class Spider163(SpiderModel):
    def __init__(self):
        self.headers = {
            'Host': 'api.blog.163.com',
            'User-Agent': ' Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://api.blog.163.com/crossdomain.html?t=20100205',
            'Connection': 'keep-alive'
        }
        SpiderModel.__init__(self, self.headers)
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
        self.work_home = 'csdn'
        self.index_url = 'http://blog.csdn.net/'

    # HOCKS
    def deal_post_title(self, title):
        titles = title.split('-')
        return "".join(titles[0:(len(titles) - 3)])

    def deal_post_content(self, content):
        return re.sub('<script[^>]*?>[\s\S]*?</script>', '', content)

    def deal_user_index_urls(self, url):
        text = self.get_others(url, self.headers, useUrllib=1)
        userID = ''
        userIDs = re.findall('userId:(?P<ID>\d+)', text)
        if (userIDs != []):
            userID = userIDs[0]
        userNames = re.findall('userName:\'(?P<userName>.*?)\'', text)
        userName = ''
        if (userName != []):
            userName = userNames[0]

        result = self.get_others(url, self.headers, usePost=0, useUrllib=0)
        cook = result.cook.text
        headers = {
            'Host': 'api.blog.163.com',
            'User-Agent': ' Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://api.blog.163.com/crossdomain.html?t=20100205',
            'Connection': 'keep-alive',
            'cookies': cook
        }
        postData = {
            'callCount': '1',
            'scriptSessionId': '187',
            'c0-scriptName': 'BlogBeanNew',
            'c0-methodName': 'getBlogs',
            'c0-id': '0',
            'c0-param0': 'number:' + str(userID),
            'c0-param1': 'number:0',
            'c0-param2': 'number:20',
            'batchId': '236674'
        }
        url = 'http://api.blog.163.com/' + userName + '/dwr/call/plaincall/BlogBeanNew.getBlogs.dwr'
        print url
        text = self.get_others(url, headers, usePost=1, useUrllib=0, postData=postData)

        print text
        # self.set_usePost(1)
        # self.set_postData(postData)
        # print userIDs
        exit()

    def __del__(self):
        # SpiderModel.__del__(self)
        pass


if __name__ == '__main__':
    sc = Spider163()
    mcm = MakeChm()
    mcm.set_save_img(0)
    mcm.set_partlyNum(50)
    mcm.set_chm_path('E:\pycode\spider\chm\\blog163_host')
    sc.set_max_page(1)
    sc.get_urls('http://unei66.blog.163.com/blog/', 1, mcm)
# sc.get_posts(mcm)
# sc.get_index_data(mcm)
