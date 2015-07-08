# -*- coding: utf-8 -*-
# ref: http://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_digits.html

import pytz
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from datetime import datetime, timedelta
from collections import deque

from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import *

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale

from bin.mongodb_driver import *
from bin.start import *
from handler.hisdb_handler import TwseHisDBHandler, OtcHisDBHandler
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler
from algorithm.report import Report


class KmeansAlgorithm(TradingAlgorithm):

    def __init__(self, dbhandler, **kwargs):
        self._debug = kwargs.pop('debug', False)
        self._buf_win = kwargs.pop('buf_win', 30)
        self._samples = kwargs.pop('samples', 10)
        self._trains =  kwargs('trains', 100)
        self._tests = kwargs.pop('tests', 10)
        super(KmeansAlgorithm, self).__init__(**kwargs)
        self.dbhandler = dbhandler
        self.sids = self.dbhandler.stock.ids

    def initialize(self):
        self.window = deque(maxlen=self._buf_win)
        self.X = deque(maxlen=self._samples)
        self.Y = deque(maxlen=self._samples)
        self.invested = False

    def _bench_k_means(self, estimator, name, data, labels):
        t0 = time.time()
        estimator.fit(data)
        print('% 9s   %.2fs    %i   %.3f   %.3f   %.3f   %.3f   %.3f    %.3f'
              % (name, (time.time() - t0), estimator.inertia_,
                 metrics.homogeneity_score(labels, estimator.labels_),
                 metrics.completeness_score(labels, estimator.labels_),
                 metrics.v_measure_score(labels, estimator.labels_),
                 metrics.adjusted_rand_score(labels, estimator.labels_),
                 metrics.adjusted_mutual_info_score(labels,  estimator.labels_),
                 metrics.silhouette_score(data, estimator.labels_,
                                          metric='euclidean',
                                          sample_size=self._samples)))

    def _classifier(self, data, labels):
        # cluster: 
        self._bench_k_means(KMeans(init='k-means++', n_clusters=5, n_init=10),
                          name="k-means++", data=data, labels=labels)

        self._bench_k_means(KMeans(init='random', n_clusters=5, n_init=10),
                          name="random", data=data, labels=labels)

        # in this case the seeding of the centers is deterministic, hence we run the
        # kmeans algorithm only once with n_init=1
        pca = PCA(n_components=5).fit(data)
        self._bench_k_means(KMeans(init=pca.components_, n_clusters=5, n_init=1),
                      name="PCA-based", data=data, labels=labels)
        print(79 * '_')

        ###############################################################################
        # Visualize the results on PCA-reduced data

        reduced_data = PCA(n_components=2).fit_transform(data)
        kmeans = KMeans(init='k-means++', n_clusters=5, n_init=10)
        kmeans.fit(reduced_data)

        # Step size of the mesh. Decrease to increase the quality of the VQ.
        h = .002     # point in the mesh [x_min, m_max]x[y_min, y_max].

        # Plot the decision boundary. For that, we will assign a color to each
        x_min, x_max = reduced_data[:, 0].min(), reduced_data[:, 0].max()
        y_min, y_max = reduced_data[:, 1].min(), reduced_data[:, 1].max()
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

        # Obtain labels for each point in mesh. Use last dataed model.
        Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

        # Put the result into a color plot
        Z = Z.reshape(xx.shape)
        plt.figure(1)
        plt.clf()
        plt.imshow(Z, interpolation='nearest',
                   extent=(xx.min(), xx.max(), yy.min(), yy.max()),
                   cmap=plt.cm.Paired,
                   aspect='auto', origin='lower')

        plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
        # Plot the centroids as a white X
        centroids = kmeans.cluster_centers_
        plt.scatter(centroids[:, 0], centroids[:, 1],
                    marker='x', s=169, linewidths=3,
                    color='w', zorder=10)
        plt.title('K-means clustering on the stock  dataset (PCA-reduced data)\n'
                  'Centroids are marked with white cross')
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        plt.xticks(())
        plt.yticks(())
        plt.savefig("kmeans_%s.png" %(self.sids[0]))
        #plt.show()

    def handle_data(self, data):

        self.window.append((
            data[self.sids[0]].close,
            data[self.sids[0]].volume
        ))

        if len(self.window) == self._buf_win:
            close, volume = [np.array(i) for i in zip(*self.window)]
            changes = np.diff(close) / close[1:]
            self.X.append(changes[:-1])
            self.Y.append(changes[-1] > 0)

        if len(self.X) == self._samples and len(self.Y) == self._samples:
            self._classifier(data=np.array(list(self.X)), labels=np.array(list(self.Y)))
            self.invested = True


def run(opt='twse', debug=False, limit=0):
    maxlen = 30
    starttime = datetime.utcnow() - timedelta(days=300)
    endtime = datetime.utcnow()
    report = Report(
        sort=[('buys', False), ('sells', False), ('portfolio_value', False)], limit=20)
    # set debug or normal mode
    kwargs = {
        'debug': debug,
        'limit': limit,
        'opt': opt
    }
    idhandler = TwseIdDBHandler(**kwargs) if kwargs['opt'] == 'twse' else OtcIdDBHandler(**kwargs)
    for stockid in idhandler.stock.get_ids():
        kwargs = {
            'debug': True,
            'opt': opt
        }
        dbhandler = TwseHisDBHandler(**kwargs) if kwargs['opt'] == 'twse' else OtcHisDBHandler(**kwargs)
        dbhandler.stock.ids = [stockid]
        args = (starttime, endtime, [stockid], 'stock', ['-totalvolume'], 10)
        cursor = dbhandler.stock.query_raw(*args)
        data = dbhandler.stock.to_pandas(cursor)
        if len(data[stockid].index) < maxlen:
            continue
        kmeans = KmeansAlgorithm(dbhandler=dbhandler, debug=True)
        results = kmeans.run(data).fillna(0)
        report.collect(stockid, results)
        #report.collect(stockid, results)
        print "%s pass" %(stockid)

#    if report.report.empty:
#        return
#
#    # report summary
#    stream = report.summary(dtype='html')
#    report.write(stream, 'superman.html')
#
#    for stockid in report.iter_stockid
#        stream = report.iter_report(stockid, dtype='html', has_other=True, has_sideband=True)
#        report.write(stream, "superman_%s.html" % (stockid))
#
#    for stockid in report.iter_stockid():
#        fig = plt.figure()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test kmeans algorithm')
    parser.add_argument('--debug', dest='debug', action='store_true', default=False, help='debug mode')
    parser.add_argument('--opt', dest='opt', action='store', type=str, default='twse', help='twse/otc')
    parser.add_argument('--limit', dest='limit', action='store', type=int, default=0, help='limit')
    args = parser.parse_args()
    #proc = start_main_service(args.debug)
    run(args.opt, args.debug, args.limit)
    #close_main_service(proc, args.debug)
