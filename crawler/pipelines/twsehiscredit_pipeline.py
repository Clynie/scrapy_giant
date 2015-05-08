# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import pytz
from datetime import datetime

from scrapy import log
from crawler.pipelines.base_pipeline import BasePipeline
from handler.hisdb_handler import *

__all__ = ['TwseHisCreditPipeline']

class TwseHisCreditPipeline(BasePipeline):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        super(TwseHisCreditPipeline, self).__init__()
        self._name = 'twsehiscredit'
        kwargs = {
            'debug': crawler.settings.getbool('GIANT_DEBUG'),
            'opt': 'twse'
        }
        self._db = TwseHisDBHandler(**kwargs)

    def process_item(self, item, spider):
        if spider.name not in [self._name]:
            return item
        item = self._clear_item(item)
        item = self._update_item(item)
        self._write_item(item)

    def _clear_item(self, item):
        jstream = self._encode_item(item)
        return self._decode_item(jstream)

    def _update_item(self, item):
        item = item['data']
        def _encode_datetime(it):
            yy, mm, dd = it.split('-')
            return datetime(int(yy), int(mm), int(dd), 0, 0, 0, 0, pytz.utc)
        for it in item:
            it['date'] = _encode_datetime(it['date'])
        # use pd frame as sorted item and trans unicode to each item type
        log.msg("item: %s" % (item), level=log.DEBUG)
        return item

    def _write_item(self, item):
        self._db.credit.insert_raw(item)