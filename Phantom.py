# -*- encoding: utf-8 -*-
# Author: Shiyun Li(Swing Leo)
# Mail: lishiyun19@163.com
# Created on 2015-01-09 15:38:50

from pyspider.libs.base_handler import *

class Phantom(BaseHandler):
    def on_start(self):
        self.crawl('http://movie.douban.com/explore#more',
                   fetch_type='js', js_script="""
                   function() {
                     setTimeout("$('.more').click()", 1000);
                   }""", callback=self.phantomjs_parser)
    
    def phantomjs_parser(self, response):
        return [{
            "title": "".join(
                s for s in x('p').contents() if isinstance(s, basestring)
            ).strip(),
            "rate": x('p strong').text(),
            "url": x.attr.href,
        } for x in response.doc('a.item').items()]
