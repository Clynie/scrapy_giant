# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from StringIO import StringIO
import string
from datetime import datetime
from dateutil.relativedelta import relativedelta

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import Request, FormRequest
from scrapy import log
from crawler.items import OtcHisStockItem

from handler.iddb_handler import OtcIdDBHandler

__all__ = ['OtcHisStockSpider']

class OtcHisStockSpider(CrawlSpider):
    name = 'otchisstock'
    allowed_domains = ['http://www.gretai.org.tw']
    download_delay = 2
    _headers = [
        (u'日期', u'date'),
        (u'成交仟股', u'volume'),
        (u'成交仟元', u'exhprice'),
        (u'開盤', u'open'),
        (u'最高', u'high'),
        (u'最低', u'low'),
        (u'收盤', u'close'),
        (u'漲跌', u'offset'),
        (u'筆數', u'exhvolume')]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        super(OtcHisStockSpider, self).__init__()
        kwargs = {
            'debug': crawler.settings.getbool('GIANT_DEBUG'),
            'limit': crawler.settings.getint('GIANT_LIMIT'),
            'opt': 'otc'
        }
        self._id = OtcIdDBHandler(**kwargs)

    def start_requests(self):
        for i,stockid in enumerate(self._id.stock.get_ids()):
            if self._id.stock.is_warrant(stockid):
                continue
            for mon in range(2, -1, -1):
                timestamp = datetime.utcnow() - relativedelta(months=mon)
                if mon == 0:
                    if timestamp.day == 1 and timestamp.hour <= 14:
                        continue
                URL = (
                    'http://www.gretai.org.tw/web/stock/aftertrading/' +
                    'daily_trading_info/st43_download.php?l=zh-tw&d=%(year)3d/%(mon)02d&' +
                    'stkno=%(stock)s&s=0,asc,0') % {
                        'year': timestamp.year - 1911,
                        'mon': timestamp.month,
                        'stock': stockid
                }
                item = OtcHisStockItem()
                item.update({
                    'stockid': stockid,
                    'count': 0
                })
                request = Request(
                    URL,
                    meta={
                        'item': item,
                        'cookiejar': i
                    },
                    callback=self.parse,
                    dont_filter=True)
                yield request

    def parse(self, response):
        """
        data struct
        [
            {
                'date':
                'stockid':
                'oepn':
                'high':
                'low':
                'close':
                'volume':
            }, ...
        ]
        """
        log.msg("URL: %s" % (response.url), level=log.DEBUG)
        item = response.meta['item']
        item['url'] = response.url
        item['data'] = []
        # use as pandas frame to dict
        try:
            frame = pd.read_csv(
                StringIO(response.body), delimiter=',',
                na_values=['--'], header=None, skiprows=[0, 1, 2, 3, 4, -1], dtype=np.object).dropna()
            if frame.empty:
                log.msg("fetch %s empty" % (item['stockid']), log.INFO)
                return
        except:
            log.msg("fetch %s fail" % (item['stockid']), log.INFO)
            return
        for elems in frame.T.to_dict().values():
            nwelem = [str(it).strip(string.whitespace).replace(',', '') for it in elems.values()]
            sub = {}
            for indx, elem in enumerate(nwelem):
                if indx == 0:
                    # pass empty data
                    try:
                        yy, mm, dd = map(int, elem.split('/'))
                    except Exception:
                        continue
                    sub[self._headers[indx][1]] = u"%s-%s-%s" % (1911+yy, mm, dd)
                    sub['stockid'] = item['stockid']
                elif indx == 1:
                    sub[self._headers[indx][1]] = u"%d" % (int(elem) * 1000)
                else:
                    sub[self._headers[indx][1]] = elem
            item['data'].append(sub)
        log.msg("fetch %s pass at %d times" % (item['stockid'], item['count']), log.INFO)
        log.msg("item[0] %s ..." % (item['data'][0]), level=log.DEBUG)
        yield item
