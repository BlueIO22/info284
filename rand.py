import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

x = 0
y = 1
wheat_data = wheat_type = 0

def load_data():
    global wheat_data, wheat_type
    # 0. area A,
    # 1. perimeter P,
    # 2. compactness C = 4*pi*A/P^2,
    # 3. length of kernel,
    # 4. width of kernel,
    # 5. asymmetry coefficient
    # 6. length of kernel groove.
    wheat_data = np.loadtxt("dataset.txt")
    wheat_type = wheat_data.astype(np.int32)[:, 7]
    # Set wheat class to 0, 1 or 2
    wheat_type = [x - 1 for x in wheat_type]
    # Delete actual wheat type data
    wheat_data = np.delete(wheat_data, 7, 1)

    # Unable to use this method because the dimentions 'disappear'
    # n = ('area', 'perimeter', 'compactness', 'kernel_length', 'kernel_width', 'asym_coef', 'groove_length', 'type')
    # wheat_data = np.genfromtxt("seedsdata.txt", names=n)

def run():
    global wheat_data
    load_data()
    wheat_data = StandardScaler().fit_transform(wheat_data)
    pca = PCA(n_components=5)
    wheat_data = pca.fit_transform(wheat_data)
    #Print eigen values - importance of each feature
    #print(pca.explained_variance_ratio_)
    #print(pca.components_[0])
    kmean()
    gauss_mixture()

def kmean():
    #Instanciate Kmeans with 3 clusters
    kmeans = KMeans(n_clusters=3, random_state=9)
    #Save predicted classes to list
    pred_type = kmeans.fit_predict(wheat_data)
    #Save cluster center points
    centroids = kmeans.cluster_centers_
    # Fill a plot with predicted types. Add a title
    predplot = fill_plot(pred_type, 'Predicted using kmean')
    #Add cluster center points
    predplot.scatter(centroids[:, x], centroids[:, y], marker="x", s=100, zorder=10)
    plt.show()

def gauss_mixture():
    #Instanciate Gaussian Mixture with 3 components and fit data
    gmm = GaussianMixture(n_components=3, random_state=18).fit(wheat_data)
    #Save predicted classes to list
    pred_type = gmm.predict(wheat_data)
    #Fill a plot with predicted types. Add a title
    fill_plot(pred_type, 'Predicted using gauss')
    plt.show()

def fill_plot(pred_type, title):
    acc = round(metrics.accuracy_score(wheat_type, pred_type), 5)
    ari = round(metrics.adjusted_rand_score(wheat_type, pred_type), 5)

    # Create a subplot spanning two columns and one row, at index 1
    predplot = plt.subplot(2, 1, 1)
    # Fill subplot with predicted values
    predplot.scatter(wheat_data[:, x], wheat_data[:, y], c=pred_type, cmap='rainbow')
    plt.title('{}. Accuracy = {}'.format(title, acc),loc='left')
    plt.title('{}. ARI = {})'.format("", ari), loc='right')

    # Create a subplot spanning two columns and one row, at index 2
    actualplot = plt.subplot(2, 1, 2)
    # Fill subplot with actual values
    actualplot.scatter(wheat_data[:, x], wheat_data[:, y], c=wheat_type, cmap='rainbow')
    plt.title('Actual')

    #Show the plot without titles overlapping
    plt.tight_layout()

    #Return plot of predictions for further editing
    return predplot

run()