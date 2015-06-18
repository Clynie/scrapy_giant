# -*- coding: utf-8 -*-

import networkx as nx
import timeit 

class Worker(nx.DiGraph):
    
    def __init__(self):
        super(Worker, self).__init__()
        self._run_queue = []
        self._wait_queue = []
        self._finish_queue = []
        self._record = []

    @property
    def record(self):
        return self._record

    def set_start_node(self, node):
        self.node[node]['ptr'].status = 'run'
        self._add_wait_queue(node)

    def _is_ready_to_run(self, node):
        if self.node[node]['ptr'].status == 'idle':
            for pre, cur in self.in_edges(node):
                if self.edge[pre][cur]['weight'] <= 0:
                    return (node, False)
            return (node, True)
        elif self.node[node]['ptr'].status == 'run':
            return (node, True)
        else:
            return (node, False)

    def _dec_weight(self, node):
        for pre, cur in self.in_edges(node):
            if self.node[pre]['ptr'].status == 'finish' and self.node[cur]['ptr'].status == 'finish':
                self.edge[pre][cur]['weight'] = self.edge[pre][cur]['weight'] -1

    def _find_ready_to_run(self):
        results = map(lambda x: self._is_ready_to_run(x), self._wait_queue)
        for it in set(filter(lambda x: x[1] == True, results)):
            yield it[0]

    def _is_ready_to_wait(self, node):
        pool = []
        if self.node[node]['ptr'].status != 'run':
            for cur, nxt in self.out_edges(node):
                if self.edge[cur][nxt]['weight'] <= 0:
                    pool.append((nxt, False))
                else:
                    pool.append((nxt, True))
        return pool

    def _find_ready_to_wait(self):
        results = []
        [results.extend(self._is_ready_to_wait(it)) for it in self._finish_queue]
        for it in set(filter(lambda x: x[1] == True, results)):
            yield it[0]

    def _is_ready_to_join(self, node):
        return (node, self.node[node]['ptr'].is_ready())

    def _find_ready_to_join(self):
        results = map(lambda x: self._is_ready_to_join(x), self._run_queue)
        for it in set(filter(lambda x: x[1] == True, results)):
            yield it[0]

    def _is_ready_to_idle(self, node):
        for cur, nxt in self.out_edges(node):
            if self.node[cur]['ptr'].status == 'finish' and self.node[nxt]['ptr'].status != 'finish':  
                return (node, False)
        return (node, True)

    def _find_ready_to_idle(self):
        results = map(lambda x: self._is_ready_to_idle(x), self._finish_queue)
        for it in set(filter(lambda x: x[1] == True, results)):
            yield it[0]

    def _start_to_run(self, node):
        self.node[node]['ptr'].run()
        self.node[node]['ptr'].status = 'run'
        self.node[node]['ptr'].visited += 1
        self.node[node]['ptr'].runtime = timeit.Timer()

    def _join_to_run(self, node):
        self.node[node]['ptr'].status = 'finish'
        self.node[node]['ptr'].finish()
        rec = {
            'node': node,
            'retval': self.node[node]['ptr'].retval,
            'visited': self.node[node]['ptr'].visited,
            'runtime': "%.2f" %(self.node[node]['ptr'].runtime.timeit())
        }
        self._record.append(rec)

    def _switch_to_idle(self, node):
        self.node[node]['ptr'].status = 'idle'

    def _add_run_queue(self, node):
        if node not in self._run_queue:
            self._run_queue.append(node)

    def _del_run_queue(self, node):
        if node in self._run_queue:
            self._run_queue.remove(node)

    def _add_wait_queue(self, node):
        if node not in self._wait_queue:
            self._wait_queue.append(node)

    def _del_wait_queue(self, node):
        if node in self._wait_queue:
            self._wait_queue.remove(node)

    def _add_finish_queue(self, node):
        if node not in self._finish_queue:
            self._finish_queue.append(node)

    def _del_finish_queue(self, node):
        if node in self._finish_queue:
            self._finish_queue.remove(node)

    def _is_ready_to_finish(self, node):
        if self.node[node]['ptr'].status == 'idle':
            for pre, cur in self.in_edges(node):
                if self.edge[pre][cur]['weight'] >= 0:
                    return (node, False)
            return (node, True)
        elif self.node[node]['ptr'].status == 'run':
            return (node, False)
        else:
            return (node, True)

    def _find_ready_to_finish(self):
        return sum([len(self._wait_queue), len(self._run_queue), len(self._finish_queue)]) == 0

    def _dump_run_queue(self):
        return map(lambda x: (x, self.node[x]['ptr'].status), self._run_queue)

    def _dump_wait_queue(self):
        return map(lambda x: (x, self.node[x]['ptr'].status), self._wait_queue)

    def _dump_finish_queue(self):
        return map(lambda x: (x, self.node[x]['ptr'].status), self._finish_queue)

    def pre_check(self):
        # check the graph is no violation
        pass

    def post_check(self):
        pass

    def coverage(self):
        # find how many nodes/edges has visited
        pass

    def uncoverage_nodes(self):
        # unvisited nodes 
        pass

    def uncoverage_edges(self):
    	# unvisited edges
        pass

    def run(self):
        # need gevent ?
        while not self._find_ready_to_finish():
            for node in self._find_ready_to_join():
                self._join_to_run(node)
                self._dec_weight(node)
                self._add_finish_queue(node)
                self._del_run_queue(node)
            for node in self._find_ready_to_wait():
                self._add_wait_queue(node)
            for node in self._find_ready_to_idle():
                self._switch_to_idle(node)
                self._del_finish_queue(node)
            for node in self._find_ready_to_run():
                self._start_to_run(node)
                self._add_run_queue(node)
                self._del_wait_queue(node)