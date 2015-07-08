# -*- coding: utf-8 -*-
from __future__ import absolute_import

import pandas as pd
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler
from handler.hisdb_handler import TwseHisDBHandler, OtcHisDBHandler

from giant.celery import app
from celery import shared_task

from celery.utils.log import get_task_logger
logger = get_task_logger('handler')

hisdb_tasks = {
    'twse': TwseHisDBHandler,
    'otc': OtcHisDBHandler
}

iddb_tasks = {
    'twse': TwseIdDBHandler,
    'otc': OtcIdDBHandler
}

hisitems = ['stock', 'credit', 'future', 'trader']

@shared_task
def collect_hisitem(opt, targets, starttime, endtime, base='stock', order=[], stockids=[], traderids=[], limit=10, callback=None, debug=False):
    """ as middleware collect raw his stock/toptrader/credit/future to item
    """

    #asssert ...
    item = {}
    dbhandler = hisdb_tasks[opt](debug=debug)
    for target in targets:
        if target in hisitems:
            ptr = getattr(dbhandler, target)
            if target in ['trader']:
                args = (starttime, endtime, stockids, traderids, base, order, limit)
            else:
                args = (starttime, endtime, stockids, base, order, limit)

            dt = ptr.query_raw(*args)
            if dt:
                item.update({target+'item': dt})
    return item


def collect_hisframe(opt, targets, starttime, endtime, base='stock', order=[], stockids=[], traderids=[], limit=10, callback=None, debug=False):
    """  as middleware collect raw his stock/toptrader/credit/future to df
    <stockid>                                | <stockid> ...
                open| high| financeused| top0|           open | ...
    20140928    100 | 101 | 0,2        | 100 |20140928 | 110  | ...
    20140929    100 | 102 | 0.3        | 200 |20140929 | 110  | ...
    """

    #assert ...
    group = []
    dbhandler = hisdb_tasks[opt](debug=debug)
    for target in targets:
        if target in hisitems:
            ptr = getattr(dbhandler, target)
            cb = ptr.to_pandas
            if target in ['trader']:
                ptr.ids = stockids if base == 'stock' else traderids
                args = (starttime, endtime, stockids, traderids, base, order, limit, cb)
            else:
                ptr.ids = stockids
                args = (starttime, endtime, stockids, base, order, limit, cb)

            df = ptr.query_raw(*args)
            if not df.empty:
                group.append(df)
                
    if group:
        panel = pd.concat(group, axis=2).fillna(0)
        return panel, dbhandler
    return pd.Panel(), dbhandler