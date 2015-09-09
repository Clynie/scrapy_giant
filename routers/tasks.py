
from routers.loader import Loader
from datetime import datetime, timedelta


routers = {
    # key, search path, init node, middle node, end node
    'StockProfileUp0': ('routers/table/StockProfileUp0.yaml', {
        'twse': ([0,1,2], [3], [4]),
        'otc': ([5,6,7], [8], [9])
        }),
    'StockProfileDown0': ('routers/table/StockProfileDown0.yaml', {
        'twse': ([0,1,2], [3], [4]),
        'otc': ([5,6,7], [8], [9])
        }),
    'StockProfileUp1': ('routers/table/StockProfileUp1.yaml', {
        'twse': ([0], [1,2,3], [4]),
        'otc': ([5], [6,7,8], [9])
        }),
    'StockProfileDown1': ('routers/table/StockProfileDown1.yaml', {
        'twse': ([0], [1,2,3], [4]),
        'otc': ([5], [6,7,8], [9])
        }),
    'StockProfileUp2': ('routers/table/StockProfileUp2.yaml', {
        'twse': ([0], [1,2,3], [4]),
        'otc': ([5], [6,7,8], [9])
        }),
    'StockProfileDown2': ('routers/table/StockProfileDown2.yaml', {
        'twse': ([0], [1,2,3], [4]),
        'otc': ([5], [6,7,8], [9])
        }),
    'TraderProfileUp0': ('routers/table/TraderProfileUp0.yaml', {
        'twse': ([0], [], [1]),
        'otc': ([2], [], [3])
        }),
    'TraderProfileDown0': ('routers/table/TraderProfileDown0.yaml', {
        'twse': ([0], [], [1]),
        'otc': ([2], [], [3])
        }),
    'TraderGroup0': ('routers/table/TraderGroup0.yaml', {
        'twse': ([0], [], [1]),
        'otc': ([2], [], [3])
        }),
    'TraderGroup1': ('routers/table/TraderGroup1.yaml', {
        'twse': ([0], [], [1]),
        'otc': ([2], [], [3])
        }),
    'TraderGroup2': ('routers/table/TraderGroup2.yaml', {
        'twse': ([0], [], [1]),
        'otc': ([2], [], [3])
        }),
    'TraderGroup3': ('routers/table/TraderGroup3.yaml', {
        'twse': ([0], [], [1]),
        'otc': ([2], [], [3])
        }),
    'StockGroup0': ('routers/table/StockGroup0.yaml', {
        'twse': (),
        'otc': ()
        }),
    'StockGroup1': ('routers/table/StockGroup1.yaml', {
        'twse': (),
        'otc': ()
        })
}

def schedule_router_tasks(**collect):
    opt = collect.pop('opt', 'twse')
    algorithm = collect.pop('algorithm', 'StockProfileUp0')
    starttime = collect.pop('starttime', datetime.utcnow() - timedelta(days=15))
    endtime = collect.pop('endtime', datetime.utcnow())
    stockids = collect.pop('stockids', [])
    traderids = collect.pop('traderids', [])
    debug = collect.pop('debug', False)

    starts = routers[algorithm][1][opt][0]
    middles = routers[algorithm][1][opt][1]
    ends = routers[algorithm][1][opt][2]
    tmps = routers[algorithm][1]['otc'] if opt == 'twse' else routers[algorithm][1]['twse']
    cuts = []
    map(lambda x: cuts.extend(x), tmps)

    loader = Loader()
    graph = loader.create_graph(routers[algorithm][0], priority=1, debug=True)

    for n in starts:
        ptr = graph.node[n]['ptr']
        ptr.kwargs.update({
            'starttime': starttime if starttime else ptr.kwargs['starttime'],
            'endtime': endtime if endtime else ptr.kwargs['endtime'],
            'stockids': stockids if stockids else ptr.kwargs['stockids'],
            'traderids': traderids if traderids else ptr.kwargs['traderids'],
            'debug': debug
        })
    for n in middles:
        ptr = graph.node[n]['ptr']
        ptr.kwargs.update({
            'starttime': starttime,
            'endtime': endtime,
            'debug': debug
        })
    for n in ends:
        ptr = graph.node[n]['ptr']
        ptr.kwargs.update({
            'starttime': starttime,
            'endtime': endtime,
            'debug': debug
        })
    for n in cuts:
        graph.remove_node(n)

    loader.finalize(graph)
    graph.start()
    graph.join()

    nodes = filter(lambda x: x['node'] == ends[0], graph.record)
    return nodes[0]['retval']