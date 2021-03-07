
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.cluster import DBSCAN
from src.example import make_matrix, print_clusters


# Try out DBScan
colors, distance_matrix = make_matrix()

# Compute DBSCAN
# The results are pretty bad
db = DBSCAN(eps=17, metric="precomputed", min_samples=1).fit(distance_matrix)
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print("Estimated number of clusters: %d" % n_clusters_)
print("Estimated number of noise points: %d" % n_noise_)

if -1 in labels:
    print('There were no clusters found')
else:
    print_clusters(colors, labels, distance_matrix)