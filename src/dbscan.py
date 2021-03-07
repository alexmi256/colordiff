import matplotlib.pyplot as plt
import numpy as np

from sklearn.metrics.pairwise import pairwise_distances
from sklearn.cluster import DBSCAN
from src.example import make_matrix


# Try out DBScan
colors, distance_matrix = make_matrix()
distances = pairwise_distances(distance_matrix, metric="precomputed")

# Compute DBSCAN
# The results are pretty bad
db = DBSCAN(eps=17, metric="precomputed", min_samples=1).fit(distances)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print("Estimated number of clusters: %d" % n_clusters_)
print("Estimated number of noise points: %d" % n_noise_)

# #############################################################################
# Plot result

# Black removed and is used for noise instead.
unique_labels = set(labels)
colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = labels == k

    xy = distances[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], "o", markerfacecolor=tuple(col), markeredgecolor="k", markersize=14)

    xy = distances[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], "o", markerfacecolor=tuple(col), markeredgecolor="k", markersize=6)

plt.title("Estimated number of clusters: %d" % n_clusters_)
plt.show()
