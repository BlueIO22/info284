import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.mixture import GMM
from scipy.spatial.distance import cdist
from sklearn.decomposition import PCA
import pylab as pl

# getting the dataset, and reading it converting it into an array
data = pd.read_csv('dataset.txt', delim_whitespace=True)

# setting variables for location of data
x = 1
y = 0

# creating an array to store the findings from the elbow method
dis = []

# we take a random range from 1-10, to determine the best cluster number to use
K = range(1,10)

# by iterating and calculating the sum of each n_cluster, we can determine where the elbow begins
for k in K:
    kmeanModel = KMeans(n_clusters=k).fit(data)
    kmeanModel.fit(data)
    dis.append(sum(np.min(cdist(data, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / data.shape[0])

n_clusters = int(dis[0])

# using sklearn to get the kMeans clustering algorithm, populating it and scattering it to the plot.
kmeans = KMeans(n_clusters=n_clusters).fit(data)
hello = kmeans.predict(data)
kmeans_plot = plt.subplot(2, 1, 1)
kmeans_plot.scatter(data.iloc[:, x], data.iloc[:, y], c=hello, s=40, cmap='viridis', zorder=2)
plt.title('KMeans')

# using sklearn to get the Gaussian Mixture Clustering algorithm.
gmm = GMM(n_components=n_clusters).fit(data)
labels = gmm.predict(data)
gmm_plot = plt.subplot(2, 1, 2)
plt.title('Gaussian Mixture Clustering')
gmm_plot.scatter(data.iloc[:, x], data.iloc[:, y], c=labels, s=40, cmap='viridis', zorder=2)

# showing the graph
plt.show()





