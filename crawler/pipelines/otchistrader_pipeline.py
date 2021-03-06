
# -*- coding: utf-8 -*-

from crawler.pipelines.twsehistrader_pipeline import TwseHisTraderPipeline
from handler.hisdb_handler import *
from handler.iddb_handler import *

__all__ = ['OtcHisTraderPipeline']

class OtcHisTraderPipeline(TwseHisTraderPipeline):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        super(OtcHisTraderPipeline, self).__init__(crawler)
        self._name = 'otchistrader'
        kwargs = []
        for i in range(2):
            kwargs.append({
                'debug': crawler.settings.getbool('GIANT_DEBUG'),
                'opt': 'otc'
        })
        self._db = OtcHisDBHandler(**kwargs[0])
        self._id = OtcIdDBHandler(**kwargs[1])
