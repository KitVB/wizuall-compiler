import numpy as np
import matplotlib.pyplot as plt

x = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
y = np.array([5.0, 7.0, 9.0, 11.0, 13.0, 15.0, 17.0, 19.0, 21.0, 23.0])
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
def vector_average(x, window=None):
    if window and window != 'None':
        # Moving average
        window = int(window)
        padded_data = np.pad(x, (window-1, 0), 'edge')
        windows = sliding_window_view(padded_data, window)
        return np.mean(windows, axis=1)
    else:
        # Total average
        return np.mean(x)
result = vector_average(x, window=None)
print(result)
sum_x = None
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
def vector_max(y, window=None):
    if window and window != 'None':
        # Moving maximum
        window = int(window)
        padded_data = np.pad(y, (window-1, 0), 'edge')
        windows = sliding_window_view(padded_data, window)
        return np.max(windows, axis=1)
    else:
        # Total maximum
        return np.max(y)
result = vector_max(y, window=None)
print(result)
max_y = None
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
def vector_min(x, window=None):
    if window and window != 'None':
        # Moving minimum
        window = int(window)
        padded_data = np.pad(x, (window-1, 0), 'edge')
        windows = sliding_window_view(padded_data, window)
        return np.min(windows, axis=1)
    else:
        # Total minimum
        return np.min(x)
result = vector_min(x, window=None)
print(result)
min_x = None
z = (x + y)
w = (x * 2.0)
v = (y / 2.0)
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
def vector_average(y, window=3.0):
    if window and window != 'None':
        # Moving average
        window = int(window)
        padded_data = np.pad(y, (window-1, 0), 'edge')
        windows = sliding_window_view(padded_data, window)
        return np.mean(windows, axis=1)
    else:
        # Total average
        return np.mean(y)
result = vector_average(y, window=3.0)
print(result)
moving_avg = None
import matplotlib.pyplot as plt
import numpy as np
def plot_data(x, y):
    plt.figure(figsize=(10, 6))
    plt.plot(x, y)
    plt.grid(True)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('WizuAll Plot')
    plt.savefig('wizuall_plot.png')
    plt.show()
plot_data(x, y)
import matplotlib.pyplot as plt
import numpy as np
def scatter_plot(x, z):
    plt.figure(figsize=(10, 6))
    plt.scatter(x, z, alpha=0.7, s=50)
    plt.grid(True, alpha=0.3)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('WizuAll Scatter Plot')
    plt.savefig('wizuall_scatter.png')
    plt.show()
scatter_plot(x, z)
import matplotlib.pyplot as plt
import numpy as np
def histogram(y, bins=5.0):
    plt.figure(figsize=(10, 6))
    plt.hist(y, bins=int(5.0), alpha=0.7, color='steelblue', edgecolor='black')
    plt.grid(True, alpha=0.3)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('WizuAll Histogram')
    plt.savefig('wizuall_histogram.png')
    plt.show()
histogram(y, bins=5.0)
combined = np.array([x, y])
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
def clustering(combined, n_clusters=2.0):
    # Reshape data if needed
    if len(np.array(combined).shape) == 1:
        data_reshaped = np.array(combined).reshape(-1, 1)
    else:
        data_reshaped = np.array(combined)
    # Perform KMeans clustering
    kmeans = KMeans(n_clusters=int(2.0))
    labels = kmeans.fit_predict(data_reshaped)
    centers = kmeans.cluster_centers_
    # Visualization if 2D data
    if data_reshaped.shape[1] == 2:
        plt.figure(figsize=(10, 6))
        plt.scatter(data_reshaped[:, 0], data_reshaped[:, 1], c=labels, cmap='viridis', s=50, alpha=0.8)
        plt.scatter(centers[:, 0], centers[:, 1], c='red', marker='X', s=100)
        plt.title('WizuAll Clustering')
        plt.grid(True, alpha=0.3)
        plt.savefig('wizuall_clustering.png')
        plt.show()
    return labels, centers
labels, centers = clustering(combined, n_clusters=2.0)
print("Cluster Labels:", labels)
print("Cluster Centers:", centers)
clusters = None