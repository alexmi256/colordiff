# TODO: Look into https://baoilleach.blogspot.com/2014/01/convert-distance-matrix-to-2d.html
# https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html#sklearn.cluster.AgglomerativeClustering
# https://www.datatechnotes.com/2019/10/agglomerative-clustering-example-in.html

import matplotlib.pyplot as plt
import numpy as np

from sklearn.metrics.pairwise import pairwise_distances
from sklearn.cluster import AgglomerativeClustering
from src.example import make_matrix, print_clusters


# Try out DBScan
colors, distance_matrix = make_matrix()
distances = pairwise_distances(distance_matrix, metric="precomputed")


aggloclust = AgglomerativeClustering(n_clusters=None, affinity='precomputed', linkage='average', distance_threshold=28).fit(distance_matrix)

labels = aggloclust.labels_
print_clusters(colors, labels, distance_matrix)
