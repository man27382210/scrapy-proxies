# Copyright (C) 2013 by Aivars Kalvans <aivars.kalvans@gmail.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import re
import random
import base64
from scrapy import log

class RandomProxy(object):
    def __init__(self, settings):
        self.proxy_list = settings.get('PROXY_LIST')
        f = open(self.proxy_list)

        self.proxies = {}
        for l in f.readlines():
            # parts = re.match('(\w+://)(\w+:\w+@)?(.+)', l)

            # # Cut trailing @
            # if parts[1]:
            #     parts[1] = parts[1][:-1]

            # self.proxies[parts[0] + parts[2]] = parts[1]
            if parts.group(2) is None:
                self.proxies[parts.group(0)] = parts.group(1)
            else:
                self.proxies[parts.group(0)+parts.group(2)] = parts.group(1)

        f.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        proxy_address = random.choice(self.proxies.keys())
        proxy_user_pass = self.proxies[proxy_address]

        request.meta['proxy'] = proxy_address
        if proxy_user_pass:
            request.headers['Proxy-Authorization'] = 'Basic ' + base64.encodestring(proxy_user_pass)

    def process_exception(self, request, exception, spider):
        proxy = request.meta['proxy']
        log.msg('Removing failed proxy <%s>, %d proxies left' % (proxy, len(self.proxies)))
        try: del self.proxies[proxy]
        except ValueError: pass
