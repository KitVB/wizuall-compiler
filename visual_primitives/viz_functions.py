# visual_primitives/viz_functions.py
class VisualizationPrimitives:
    def __init__(self, target_language='python'):
        self.target_language = target_language
        # Dictionary mapping viz functions to their implementation templates
        self.viz_templates = {
            'python': {
                'plot': self._python_plot_template,
                'histogram': self._python_histogram_template,
                'heatmap': self._python_heatmap_template,
                'scatter': self._python_scatter_template,
                'bar': self._python_bar_template,
                'line': self._python_line_template,
                'vec_average': self._python_vector_average_template,
                'vec_max': self._python_vector_max_template,
                'vec_min': self._python_vector_min_template,
                'vec_reverse': self._python_vector_reverse_template,
                'vec_product': self._python_vector_product_template,
                'vec_compare': self._python_vector_compare_template,
                'clustering': self._python_clustering_template,
                'classification': self._python_classification_template
            },
            'c': {
                # Templates for C target language
                'plot': self._c_plot_template,
                # Add other C templates here
            },
            'r': {
                # Templates for R target language
                'plot': self._r_plot_template,
                # Add other R templates here
            }
        }
    
    def generate_code(self, function_name, args):
        """Generate target language code for visualization function"""
        if self.target_language not in self.viz_templates:
            raise ValueError(f"Unsupported target language: {self.target_language}")
        
        templates = self.viz_templates[self.target_language]
        if function_name not in templates:
            raise ValueError(f"Unsupported visualization function: {function_name}")
        
        # Call the appropriate template function
        return templates[function_name](args)
    
    # Python template functions
    def _python_plot_template(self, args):
        """Generate Python code for basic plotting"""
        args_str = ", ".join(args)
        return f"""
import matplotlib.pyplot as plt
import numpy as np

def plot_data({args_str}):
    plt.figure(figsize=(10, 6))
    plt.plot({args_str})
    plt.grid(True)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('WizuAll Plot')
    plt.savefig('wizuall_plot.png')
    plt.show()

plot_data({args_str})
"""
    
    def _python_histogram_template(self, args):
        """Generate Python code for histogram"""
        data_arg = args[0] if args else "data"
        bins_arg = args[1] if len(args) > 1 else "10"
        return f"""
import matplotlib.pyplot as plt
import numpy as np

def histogram({data_arg}, bins={bins_arg}):
    plt.figure(figsize=(10, 6))
    plt.hist({data_arg}, bins=int({bins_arg}), alpha=0.7, color='steelblue', edgecolor='black')
    plt.grid(True, alpha=0.3)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('WizuAll Histogram')
    plt.savefig('wizuall_histogram.png')
    plt.show()

histogram({data_arg}, bins={bins_arg})
"""

    def _python_heatmap_template(self, args):
        """Generate Python code for heatmap"""
        data_arg = args[0] if args else "data"
        return f"""
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def heatmap({data_arg}):
    plt.figure(figsize=(10, 8))
    sns.heatmap({data_arg}, annot=True, cmap='viridis')
    plt.title('WizuAll Heatmap')
    plt.savefig('wizuall_heatmap.png')
    plt.show()

heatmap({data_arg})
"""

    def _python_scatter_template(self, args):
        """Generate Python code for scatter plot"""
        x_arg = args[0] if len(args) > 0 else "x_data"
        y_arg = args[1] if len(args) > 1 else "y_data"
        return f"""
import matplotlib.pyplot as plt
import numpy as np

def scatter_plot({x_arg}, {y_arg}):
    plt.figure(figsize=(10, 6))
    plt.scatter({x_arg}, {y_arg}, alpha=0.7, s=50)
    plt.grid(True, alpha=0.3)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('WizuAll Scatter Plot')
    plt.savefig('wizuall_scatter.png')
    plt.show()

scatter_plot({x_arg}, {y_arg})
"""

    def _python_bar_template(self, args):
        """Generate Python code for bar chart"""
        x_arg = args[0] if len(args) > 0 else "categories"
        y_arg = args[1] if len(args) > 1 else "values"
        return f"""
import matplotlib.pyplot as plt
import numpy as np

def bar_chart({x_arg}, {y_arg}):
    plt.figure(figsize=(12, 6))
    plt.bar({x_arg}, {y_arg}, alpha=0.8, color='steelblue', edgecolor='black')
    plt.grid(True, axis='y', alpha=0.3)
    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title('WizuAll Bar Chart')
    plt.savefig('wizuall_bar.png')
    plt.show()

bar_chart({x_arg}, {y_arg})
"""

    def _python_line_template(self, args):
        """Generate Python code for line chart"""
        x_arg = args[0] if len(args) > 0 else "x_data"
        y_arg = args[1] if len(args) > 1 else "y_data"
        return f"""
import matplotlib.pyplot as plt
import numpy as np

def line_chart({x_arg}, {y_arg}):
    plt.figure(figsize=(10, 6))
    plt.plot({x_arg}, {y_arg}, marker='o', linestyle='-', linewidth=2, markersize=6)
    plt.grid(True, alpha=0.3)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('WizuAll Line Chart')
    plt.savefig('wizuall_line.png')
    plt.show()

line_chart({x_arg}, {y_arg})
"""

    def _python_vector_average_template(self, args):
        """Generate Python code for vector average"""
        data_arg = args[0] if args else "data"
        window_arg = args[1] if len(args) > 1 else "None"
        return f"""
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

def vector_average({data_arg}, window={window_arg}):
    if window and window != 'None':
        # Moving average
        window = int(window)
        padded_data = np.pad({data_arg}, (window-1, 0), 'edge')
        windows = sliding_window_view(padded_data, window)
        return np.mean(windows, axis=1)
    else:
        # Total average
        return np.mean({data_arg})

result = vector_average({data_arg}, window={window_arg})
print(result)
"""

    def _python_vector_max_template(self, args):
        """Generate Python code for vector maximum"""
        data_arg = args[0] if args else "data"
        window_arg = args[1] if len(args) > 1 else "None"
        return f"""
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

def vector_max({data_arg}, window={window_arg}):
    if window and window != 'None':
        # Moving maximum
        window = int(window)
        padded_data = np.pad({data_arg}, (window-1, 0), 'edge')
        windows = sliding_window_view(padded_data, window)
        return np.max(windows, axis=1)
    else:
        # Total maximum
        return np.max({data_arg})

result = vector_max({data_arg}, window={window_arg})
print(result)
"""

    def _python_vector_min_template(self, args):
        """Generate Python code for vector minimum"""
        data_arg = args[0] if args else "data"
        window_arg = args[1] if len(args) > 1 else "None"
        return f"""
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

def vector_min({data_arg}, window={window_arg}):
    if window and window != 'None':
        # Moving minimum
        window = int(window)
        padded_data = np.pad({data_arg}, (window-1, 0), 'edge')
        windows = sliding_window_view(padded_data, window)
        return np.min(windows, axis=1)
    else:
        # Total minimum
        return np.min({data_arg})

result = vector_min({data_arg}, window={window_arg})
print(result)
"""

    def _python_vector_reverse_template(self, args):
        """Generate Python code for vector reversal"""
        data_arg = args[0] if args else "data"
        return f"""
import numpy as np

def vector_reverse({data_arg}):
    return np.flip({data_arg})

result = vector_reverse({data_arg})
print(result)
"""

    def _python_vector_product_template(self, args):
        """Generate Python code for vector product"""
        x_arg = args[0] if len(args) > 0 else "x_data"
        y_arg = args[1] if len(args) > 1 else "y_data"
        product_type = args[2] if len(args) > 2 else "dot"
        return f"""
import numpy as np

def vector_product({x_arg}, {y_arg}, product_type='{product_type}'):
    if product_type == 'dot':
        return np.dot({x_arg}, {y_arg})
    elif product_type == 'cross':
        return np.cross({x_arg}, {y_arg})
    elif product_type == 'element':
        return {x_arg} * {y_arg}
    else:
        raise ValueError(f"Unsupported product type: {{product_type}}")

result = vector_product({x_arg}, {y_arg}, product_type='{product_type}')
print(result)
"""

    def _python_vector_compare_template(self, args):
        """Generate Python code for vector comparison"""
        x_arg = args[0] if len(args) > 0 else "x_data"
        y_arg = args[1] if len(args) > 1 else "y_data"
        comp_type = args[2] if len(args) > 2 else "greater"
        return f"""
import numpy as np

def vector_compare({x_arg}, {y_arg}, comp_type='{comp_type}'):
    if comp_type == 'greater':
        return {x_arg} > {y_arg}
    elif comp_type == 'less':
        return {x_arg} < {y_arg}
    elif comp_type == 'equal':
        return {x_arg} == {y_arg}
    elif comp_type == 'pareto':
        # Pareto dominance check
        dominates = np.all({x_arg} >= {y_arg}) and np.any({x_arg} > {y_arg})
        dominated_by = np.all({y_arg} >= {x_arg}) and np.any({y_arg} > {x_arg})
        return dominates, dominated_by
    else:
        raise ValueError(f"Unsupported comparison type: {{comp_type}}")

result = vector_compare({x_arg}, {y_arg}, comp_type='{comp_type}')
print(result)
"""

    def _python_clustering_template(self, args):
        """Generate Python code for clustering"""
        data_arg = args[0] if args else "data"
        n_clusters = args[1] if len(args) > 1 else "3"
        return f"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def clustering({data_arg}, n_clusters={n_clusters}):
    # Reshape data if needed
    if len(np.array({data_arg}).shape) == 1:
        data_reshaped = np.array({data_arg}).reshape(-1, 1)
    else:
        data_reshaped = np.array({data_arg})
    
    # Perform KMeans clustering
    kmeans = KMeans(n_clusters=int({n_clusters}))
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

labels, centers = clustering({data_arg}, n_clusters={n_clusters})
print("Cluster Labels:", labels)
print("Cluster Centers:", centers)
"""

    def _python_classification_template(self, args):
        """Generate Python code for classification"""
        x_train = args[0] if len(args) > 0 else "x_train"
        y_train = args[1] if len(args) > 1 else "y_train"
        x_test = args[2] if len(args) > 2 else "x_test"
        cls_type = args[3] if len(args) > 3 else "random_forest"
        return f"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report

def classification({x_train}, {y_train}, {x_test}, cls_type='{cls_type}'):
    # Choose classifier
    if cls_type == 'random_forest':
        clf = RandomForestClassifier(n_estimators=100, random_state=42)
    elif cls_type == 'svm':
        clf = SVC(kernel='rbf', probability=True, random_state=42)
    elif cls_type == 'knn':
        clf = KNeighborsClassifier(n_neighbors=5)
    else:
        raise ValueError(f"Unsupported classifier type: {{cls_type}}")
    
    # Train the classifier
    clf.fit({x_train}, {y_train})
    
    # Predict
    y_pred = clf.predict({x_test})
    
    return y_pred, clf

y_pred, clf = classification({x_train}, {y_train}, {x_test}, cls_type='{cls_type}')
print("Predictions:", y_pred)
"""

    # C template functions
    def _c_plot_template(self, args):
        """Generate C code for basic plotting using GNUPlot"""
        data_arg = args[0] if args else "data"
        return f"""
#include <stdio.h>
#include <stdlib.h>

void save_data_to_file(double *{data_arg}, int size) {{
    FILE *fp = fopen("data.txt", "w");
    if (fp == NULL) {{
        fprintf(stderr, "Error opening file\\n");
        return;
    }}
    
    for (int i = 0; i < size; i++) {{
        fprintf(fp, "%d %f\\n", i, {data_arg}[i]);
    }}
    
    fclose(fp);
}}

void plot_data(double *{data_arg}, int size) {{
    save_data_to_file({data_arg}, size);
    
    FILE *gnuplot = popen("gnuplot -persistent", "w");
    if (gnuplot == NULL) {{
        fprintf(stderr, "Error opening GNUPlot\\n");
        return;
    }}
    
    fprintf(gnuplot, "set title 'WizuAll Plot'\\n");
    fprintf(gnuplot, "set xlabel 'X'\\n");
    fprintf(gnuplot, "set ylabel 'Y'\\n");
    fprintf(gnuplot, "set grid\\n");
    fprintf(gnuplot, "plot 'data.txt' with lines title 'Data'\\n");
    
    pclose(gnuplot);
}}
"""
    
    # R template functions
    def _r_plot_template(self, args):
        """Generate R code for basic plotting"""
        data_arg = args[0] if args else "data"
        return f"""
# Basic plotting function
plot_data <- function({data_arg}) {{
  plot({data_arg}, type="l", main="WizuAll Plot", xlab="X", ylab="Y", col="blue")
  grid()
  # Save to file
  png("wizuall_plot.png")
  plot({data_arg}, type="l", main="WizuAll Plot", xlab="X", ylab="Y", col="blue")
  grid()
  dev.off()
}}

plot_data({data_arg})
"""