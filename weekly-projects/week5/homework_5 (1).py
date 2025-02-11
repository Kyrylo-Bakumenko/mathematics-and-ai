# -*- coding: utf-8 -*-
"""Homework 5.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fqLPDr3DkJRB_187hY_JSKePvxlpAKv2
"""

# Homework 5 (due 07/30/2024)

"""# SVM and Kernels

### Objective
Through this project, you will learn to use nonlinear kernels to improve a support vector classifier. The toy examples within this project aim to guide you as you build your intuition for the decision boundaries that can be generated via different kernels.

This project is structured as follows:
#### Part 1: Binary classification of synthetic data
1.1. Generate and explore synthetic data

1.2. SVM with nonlinear kernels
#### Part 2: US Flags
2.1. Load and explore flags data

2.2. SVMs for flag pixel data

2.3. Comparison to decision trees

"""

!unzip flags.zip

# standard imports
import os, random
import numpy as np
import matplotlib.pyplot as plt

# sklearn imports
from sklearn.datasets import *
from sklearn.svm import SVC
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.tree import DecisionTreeClassifier
import pandas as pd

# you may need to install the PIL in your environment
# for installation in mamba environment type "mamba install pillow -c conda-forge" in your miniforge prompt
# for installation in conda environment type "conda install pillow -c conda-forge" in your conda prompt or anaconda prompt
# for installation via pip type "pip install pillow" in your terminal
from PIL import Image

"""## Part 1: Binary classification of synthetic data

### Part 1.1: Generate and explore synthetic data
The next cell defines the function `generate_dataset`, which you can use to generate synthetic (i.e., computer generated) data sets for binary classification. It includes eight different methods for data-set generation.
1. Try out each method and visualize the resulting data set. For the 'swiss' and 'scurve' data sets, try out two different values of the keyword argument `splits`.
2. Comment on WHETHER and WHY you anticipate this data set to be relatively easy or relatively hard to classify with a linear classifier.
3. Comment on WHETHER and WHY you anticipate this data set to be relatively easy or relatively hard to classify with a nonlinear classifier.
"""

# Function to convert an array of real numbers into an array of 0s and 1s
def binarize(arr, split=10):
    # Calculate the decile thresholds
    percentiles = int(np.ceil(100/split))
    split_points = np.arange(0, 100+percentiles, percentiles)
    split_points[split_points>100] = 100
    deciles = np.percentile(arr, split_points)

    # Create a new array to hold the modified values
    modified_arr = np.zeros_like(arr)

    # Iterate through each decile range and set values accordingly
    for i in range(split):
        print(i)
        if i == split-1:
            if i % 2 == 0:
                # Set values in even deciles to 0
                modified_arr[(arr >= deciles[i])] = 0
            else:
                # Set values in odd deciles to 1
                modified_arr[(arr >= deciles[i])] = 1
        else:
            if i % 2 == 0:
                # Set values in even deciles to 0
                modified_arr[(arr >= deciles[i]) & (arr < deciles[i + 1])] = 0
            else:
                # Set values in odd deciles to 1
                modified_arr[(arr >= deciles[i]) & (arr < deciles[i + 1])] = 1

    return modified_arr

# Function to generate datasets
def generate_dataset(dataset_type, n_samples=300, noise=0.1, split=10, random_state=0):
    if dataset_type == 'linearly_separable':
        X, y = make_classification(n_samples=n_samples, n_features=2, n_redundant=0, n_informative=2,
                                   random_state=random_state, n_clusters_per_class=1)
    elif dataset_type == 'blobs':
        X, y = make_blobs(n_samples=[n_samples//2, n_samples//2], random_state=random_state, cluster_std=noise)
    elif dataset_type == 'quantiles':
        X, y = make_gaussian_quantiles(n_samples=n_samples, n_classes=2, cov=noise, random_state=random_state)
    elif dataset_type == 'moons':
        X, y = make_moons(n_samples=n_samples, noise=noise, random_state=random_state)
    elif dataset_type == 'circles':
        X, y = make_circles(n_samples=n_samples, noise=noise, factor=0.5, random_state=random_state)
    elif dataset_type == 'unstructured':
        X, y = np.random.random(size=(n_samples, 2)), np.random.randint(0,2, size=(n_samples))
    elif dataset_type == 'swiss':
        X, y = make_swiss_roll(n_samples=n_samples, noise=noise, random_state=random_state)
        X=np.array([X[:,0],X[:,2]]).T
        y = binarize(y, split=split)
    elif dataset_type == 'scurve':
        X, y = make_s_curve(n_samples=n_samples, noise=noise, random_state=random_state)
        X=np.array([X[:,0],X[:,2]]).T
        y = binarize(y, split=split)
    else:
        raise ValueError("Invalid dataset type")

    X = StandardScaler().fit_transform(X)
    return X, y

# Generate and visualize data blobs
'''ADD SOME CODE HERE'''

"""I anticipate that this data set [ADD SOME TEXT HERE]"""

# Generate and visualize unstructured data
'''ADD SOME CODE HERE'''

"""I anticipate that this data set [ADD SOME TEXT HERE]"""

# Generate and visualize circles data set
'''ADD SOME CODE HERE'''

"""I anticipate that this data set [ADD SOME TEXT HERE]"""

# Generate and visualize Gaussian quantiles
'''ADD SOME CODE HERE'''

"""I anticipate that this data set [ADD SOME TEXT HERE]"""

# Generate and visualize linearly separable data
'''ADD SOME CODE HERE'''

"""I anticipate that this data set [ADD SOME TEXT HERE]"""

# Generate and visualize moons data set
'''ADD SOME CODE HERE'''

"""I anticipate that this data set [ADD SOME TEXT HERE]"""

# Generate and visualize swiss role with 2 split sets
'''ADD SOME CODE HERE'''

"""I anticipate that this data set [ADD SOME TEXT HERE]"""

# Generate and visualize S curve with 2 split sets
'''ADD SOME CODE HERE'''

"""I anticipate that this data set [ADD SOME TEXT HERE]"""

# Generate and visualize swiss role with 10 split sets
'''ADD SOME CODE HERE'''

"""I anticipate that this data set [ADD SOME TEXT HERE]"""

# Generate and visualize S curve with 10 split sets
'''ADD SOME CODE HERE'''

"""I anticipate that this data set [ADD SOME TEXT HERE].

### Part 1.2: SVM with nonlinear kernels

The next cell defines the function `kernel_comparison`, which you can use to visually compare the decision boundaries generated by SVMs with different kernels.

1. The kernel comparison currently produces only visual results. Add code to the function so that it also outputs train and test accuracy of the different SVMs. (Note: Think carefully about where the right place in the code is to do a train-test split.)
2. Run the kernel comparison for the data sets from Part 1.1. Do the results confirm or contradict your expectations that you formulated in Part 1.1.? Did any of the results surprise you?
3. Consult sklearn's documentation to learn how the keyword arguments `degree` and `gamma` affect your classifier. Try out a few different values of these parameters. How and what can one infer from the shape of the decision boundary about the classifier's `degree` or `gamma`?
"""

def kernel_comparison(X, y, support_vectors=True, tight_box=False, if_flag=False):

    fig = plt.figure(figsize=(10,3))

    for ikernel, kernel in enumerate(['linear', 'poly', 'rbf', 'sigmoid']):
        # Train the SVC
        clf = svm.SVC(kernel=kernel, degree=3, gamma=3).fit(X, y)

        # Settings for plotting
        ax = plt.subplot(1,4,1+ikernel)
        #x_min, x_max, y_min, y_max = -3, 3, -3, 3
        #ax.set(xlim=(x_min, x_max), ylim=(y_min, y_max))

        # Plot decision boundary and margins
        common_params = {"estimator": clf, "X": X, "ax": ax}
        DecisionBoundaryDisplay.from_estimator(
            **common_params,
            response_method="predict",
            plot_method="pcolormesh",
            alpha=0.3,
        )
        DecisionBoundaryDisplay.from_estimator(
            **common_params,
            response_method="decision_function",
            plot_method="contour",
            levels=[-1, 0, 1],
            colors=["k", "k", "k"],
            linestyles=["--", "-", "--"],
        )

        if support_vectors:
            # Plot bigger circles around samples that serve as support vectors
            ax.scatter(
                clf.support_vectors_[:, 0],
                clf.support_vectors_[:, 1],
                s=150,
                facecolors="none",
                edgecolors="k",
            )

        # Plot samples by color and add legend
        ax.scatter(X[:, 0], X[:, 1], c=y, s=30, edgecolors="k")
        ax.set_title(kernel)
        ax.axis('off')
        if tight_box:
            ax.set_xlim([X[:, 0].min(), X[:, 0].max()])
            ax.set_ylim([X[:, 1].min(), X[:, 1].max()])

    fig.show()

    return dict, fig

# Show results of kernel comparison for data sets from part 1
'''ADD SOME CODE HERE'''

"""To summarize the results of the kernel comparison, [ADD SOME TEXT HERE]."""

# Examine effect of degree and gamma keyword
'''ADD SOME CODE HERE'''

"""The `degree` argument affects [ADD NAME OF DATA GENERATION METHOD]. It changes the model by [ADD SOME TEXT HERE]. This affects the model's bias-variance tradeoff by [ADD SOME TEXT HERE].

As one increases the `degree`, the decision boundary [ADD SOME TEXT HERE].

The `gamma` argument affects [ADD NAME OF DATA GENERATION METHOD]. It changes the model by [ADD SOME TEXT HERE]. This affects the model's bias-variance tradeoff by [ADD SOME TEXT HERE].

As one increases `gamma`, the decision boundary of [ADD SOME TEXT HERE].

## Part 2: US Flags

### Part 2.1: Load and explore flags data
The function `load_images` loads the image data from the flags folder and turns each image into a binary (i.e., black and white) array.

1. Load the flags data.
2. Display four flags of your choice in a figure. Use the `matplotlib` commands `subplot` and `imshow` to create a figure with 2x2 flags. Consult the `matplotlib` documentation to find a way set the aspect ratio of your displayed flags to match their original aspect ratio. Update your code accordingly.
"""

def load_images(folder):
    images = []
    labels = []
    for filename in os.listdir(folder):
        if filename.endswith(".png"):
            img_path = os.path.join(folder, filename)
            img = Image.open(img_path).convert('L')  # Convert image to black and white
            img = np.array(img)//(256/2) # Convert to BW
            images.append(img)
            labels.append(filename.split('.')[0])  # Extract the state code as label
    return images, labels

# Display four black-and-white flags in a 2x2 grid
# load
images, labels = load_images('flags')

# display
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
for i, ax in enumerate(axes.flat):
    ax.imshow(images[i], cmap='gray')
    ax.set_title(labels[i])
    ax.axis('off')
    ax.set_aspect('equal') # aspect ratio to match original
plt.tight_layout()
plt.show()

"""### Part 2.2: SVMs for flag pixel data
The function `sample_pixels` samples a pixel from a given image uniformly at random.

1. Use the `sample_pixels`  function to generate synthetic data sets of pixels from for a flag image.
2. Update the `kernel_comparison` function so that if `if_flag` is `True` the decision boundaries are plotted in a 2x2 grid of subplots with plot ranges matching the height and width of the flags.
3. Show the results of the kernel comparison for the four flags that your previously selected. Use the highest values of `degree` and `gamma` that still run *reasonably fast* on your laptop.
4. Adjust your code so that you can run the quantitative part (i.e., the calculation of train and test accuracy) without plotting the decision boundaries. Run the adjusted code on all flags to indentify for each kernel the flags that yield to best easiest-to-classify and hardest-to-classify data sets. Test how the number of of pixels sampled affects your results.
"""

def sample_pixels(image, num_samples=100):
    pixel_data = []
    pixel_labels = []
    height, width = image.shape
    for _ in range(num_samples):
        x1 = random.randint(0, width - 1)
        x2 = random.randint(0, height - 1)
        pixel_data.append([x1/width-0.5, x2/width-0.5])
        pixel_labels.append(image[x2,x1])
    return np.array(pixel_data), np.array(pixel_labels, dtype=int)

# Visual kernel comparison for selected flags

# selected flag: 0 (first one)
flag = 0
selected_flag = images[0]

# sample pixels
pixel_data, pixel_labels = sample_pixels(selected_flag)

# show flag
plt.imshow(selected_flag, cmap='gray')
plt.title(labels[0])
plt.show()

# print the sampled pixel data and labels
print(pixel_data)
print(pixel_labels)

# Visual kernel comparison for selected flags
selected_images = images[:4]
selected_labels = labels[:4]

for i in range(2):
  for j in range(2):
    index = i * 2 + j
    #
    flags_X, flags_y = sample_pixels(selected_images[index], num_samples=500)
    flag_dict, flag_fig = kernel_comparison(flags_X, flags_y, if_flag=True)
    flag_fig.suptitle(selected_labels[index])
    print(f'{selected_labels[index]}: {flag_dict}')

# Non-visual kernel comparison for all flags
def execute_kernel_comparison(X, y, degree=3, gamma=3):
    # Train test split should be at BEGINING of the function
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # dictionary to keep track of accuracy
    dict = {}

    for kernel in ['linear', 'poly', 'rbf', 'sigmoid']:
        # Train the SVC
        clf = svm.SVC(kernel=kernel, degree=degree, gamma=gamma).fit(X_train, y_train)

        # Compute train and test accuracy
        train_accuracy = clf.score(X_train, y_train)
        test_accuracy = clf.score(X_test, y_test)
        dict[kernel] = [train_accuracy, test_accuracy]

    return dict

def compare_all_flags(images, labels):
    res = {'flag': labels, 'lin_train': [], 'lin_test': [], 'poly_train': [], 'poly_test': [], 'rbf_train': [], 'rbf_test': [], 'sig_train': [], 'sig_test': []}

    for img, lbl in zip(images, labels):
        pixels_X, pixels_y = sample_pixels(img, num_samples=500)
        flag_result = execute_kernel_comparison(pixels_X, pixels_y)

        res['lin_train'].append(flag_result['linear'][0])
        res['lin_test'].append(flag_result['linear'][1])
        res['poly_train'].append(flag_result['poly'][0])
        res['poly_test'].append(flag_result['poly'][1])
        res['rbf_train'].append(flag_result['rbf'][0])
        res['rbf_test'].append(flag_result['rbf'][1])
        res['sig_train'].append(flag_result['sigmoid'][0])
        res['sig_test'].append(flag_result['sigmoid'][1])

    df_res = pd.DataFrame(res)
    return df_res

def compare_flags(images, labels, samples=400, deg=3, gm=3):
    res = {'flag': labels,
           'lin_train': [], 'lin_test': [],
           'poly_train': [], 'poly_test': [],
           'rbf_train': [], 'rbf_test': [],
           'sig_train': [], 'sig_test': []}

    for img, lbl in zip(images, labels):
        pix_X, pix_y = sample_pixels(img, num_samples=samples)
        flag_result = execute_kernel_comparison(pix_X, pix_y, degree=deg, gamma=gm)

        for kernel in ['linear', 'poly', 'rbf', 'sigmoid']:
            res[kernel[:3] + '_train'].append(flag_result[kernel][0])
            res[kernel[:3] + '_test'].append(flag_result[kernel][1])

    df_res = pd.DataFrame(res)
    return df_res

def analyze_flag_results(df_res, sort_col):
    df_sorted = df_res.sort_values(by=sort_col, ascending=False)

    # Get the top 3 and bottom 3 labels and values
    top_3 = df_sorted.head(3)
    bottom_3 = df_sorted.tail(3)

    print(f'Top 3 flags by {sort_col} accuracy:')
    print(top_3[['flag', sort_col]])

    print(f'\nBottom 3 flags by {sort_col} accuracy:')
    print(bottom_3[['flag', sort_col]])

df_results = compare_all_flags(images, labels)
df_results

"""For these experiments, I set `num_samples` to 400 because the results of the experiments seem to be the most stable for this number of sampled pixels.

The linear kernel performed best (i.e., highest test accuracy) on the flags of the following three states:

[Alaska, Rhode Island, South Caronlina]

It performed worst on the flags of the following three states:

[Florida, Iowa, Maryland]
"""

analyze_flag_results(df_results, 'lin_test')

"""The polynomial kernel performed best on the flags of the following three states:

[Alaska, Rhode Island, Nevada]

It performed worst on the flags of the following three states:

[West Virginia, Florida, Maryland]
"""

analyze_flag_results(df_results, 'poly_test')

"""The radial-basis function kernel performed best on the flags of the following three states:

[ADD TOP THREE STATE NAMES HERE]

It performed worst on the flags of the following three states:

[ADD TOP THREE STATE NAMES HERE]
"""

analyze_flag_results(df_results, 'rbf_test')

"""The sigmoid kernel performed best on the flags of the following three states:

[ADD TOP THREE STATE NAMES HERE]

It performed worst on the flags of the following three states:

[ADD TOP THREE STATE NAMES HERE]
"""

analyze_flag_results(df_results, 'sig_test')

"""### Part 2.3: Comparison to decision trees
Decision trees and SVMs yield substantially different decision boundaries.

1. An arbitrarily complex decision tree would be able to achieve perfect training accuracy on any data set. Explain why.
  
  (i.) An arbitrarily complex decision tree would be able to achieve perfect training accuracy on any dataset because it can create as many splits as necessary to ensure each leaf node contains only one or very few data points, thus perfectly classifying every instance in the training set.

2. For a very large data set of flag pixels, an arbitrarily complex decision tree is likely to achieve (almost) perfect test accuracy as well. Explain why.

  (i.) For a very large dataset of flag pixels, an arbitrarily complex decision tree is likely to achieve almost perfect test accuracy because the size and diversity of the dataset allow the model to learn general patterns and relationships, making it more robust and capable of generalizing well to new, unseen data.


3. Select four flags for which you anticipate a *simple* decision tree to outperform all your SVMs. Write code that fits a decision tree to a flag pixel data set. Use your code to check your hypothesis.

A simple decision tree is likely to perform well on the sampled pixel data of the flags of [ADD NAMES OF AT LEAST FOUR US STATES HERE].
"""

# Comparison of SVM and decision tree performance on sampled pixel data for four flags

def evaluate_tree(X, y):
    outcome = {}

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    tree_model = DecisionTreeClassifier(max_depth=5)
    tree_model.fit(X_train, y_train)
    train_accuracy = accuracy_score(y_train, tree_model.predict(X_train))
    test_accuracy = accuracy_score(y_test, tree_model.predict(X_test))

    outcome["tree"] = [train_accuracy, test_accuracy]

    return outcome

# Create dataframe of all test results and decision tree results constructed from same random sampling
results = {'flag': labels, 'lin_train': [], 'lin_test': [], 'poly_train': [], 'poly_test': [], 'rbf_train': [], 'rbf_test': [], 'sig_train': [], 'sig_test': [], 'tree_train': [], 'tree_test': []}

for img, lbl in zip(images, labels):
    pix_X, pix_y = sample_pixels(img, num_samples=500)
    kernel_result = execute_kernel_comparison(pix_X, pix_y)
    tree_result = evaluate_tree(pix_X, pix_y)

    results['lin_train'].append(kernel_result['linear'][0])
    results['lin_test'].append(kernel_result['linear'][1])
    results['poly_train'].append(kernel_result['poly'][0])
    results['poly_test'].append(kernel_result['poly'][1])
    results['rbf_train'].append(kernel_result['rbf'][0])
    results['rbf_test'].append(kernel_result['rbf'][1])
    results['sig_train'].append(kernel_result['sigmoid'][0])
    results['sig_test'].append(kernel_result['sigmoid'][1])
    results['tree_train'].append(tree_result['tree'][0])
    results['tree_test'].append(tree_result['tree'][1])

df_res = pd.DataFrame(results)
df_res

# Filter dataframe for only flags for which the decision tree outperformed all kernels.
filtered_res = df_res[(df_res['tree_test'] > df_res['lin_test']) &
                     (df_res['tree_test'] > df_res['poly_test']) &
                     (df_res['tree_test'] > df_res['rbf_test']) &
                     (df_res['tree_test'] > df_res['sig_test'])]

filtered_res.head()

# Sort filtered dataframe by highest decision tree test accuracy
top_tree_df = filtered_res.sort_values(by='tree_test', ascending=False)
top_tree_df.head(10)

