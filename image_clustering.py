from skimage.io import imread
from skimage import img_as_float64
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import compare_psnr
import warnings
import math


def get_MSE(I, K):
    sum = 0
    for i in range(len(I)):
        for j in range(len(I[0])):
            for k in range(len(I[0][0])):
                sum += (I[i][j][k] - K[i][j][k])**2
    MSE = 1/(3*len(I)*len(I[0])) * sum

    return MSE

def get_PSNR(I, K):
    MSE = get_MSE(I, K)
    PSNR = 20*math.log10(1) - 10*math.log10(MSE)
    return PSNR

def draw_image(data, title):
    fig, ax = plt.subplots()
    ax.imshow(data)
    ax.set_title(title, fontsize=20, fontfamily='Arial')
    fig.set_figwidth(6)
    fig.set_figheight(6)
    plt.axis('off')
    plt.show()

def reback_to_image(data):
    x_,y_ = data.shape
    im = np.reshape(data, (int(x_/y), int(x_/x), y_))
    return im

def get_middle_matrix(obj_feat_matr_middle, pixels_of_clusters):
    middles = []

    for i in range(len(pixels_of_clusters)):
        middles.append([np.mean(np.array(pixels_of_clusters[i])[:,1]), np.mean(np.array(pixels_of_clusters[i])[:,2]), np.mean(np.array(pixels_of_clusters[i])[:,3])])

    for i in range(len(pixels_of_clusters)):
        for j in range(len(pixels_of_clusters[i])):
            for k in range(3):
                obj_feat_matr_middle[pixels_of_clusters[i][j][0]][k] = middles[i][k]

    return obj_feat_matr_middle

def get_median_matrix(obj_feat_matr_median, pixels_of_clusters):
    medians = []

    for i in range(len(pixels_of_clusters)):
        medians.append([np.median(np.array(pixels_of_clusters[i])[:, 1]), np.median(np.array(pixels_of_clusters[i])[:, 2]),
                        np.median(np.array(pixels_of_clusters[i])[:, 3])])

    for i in range(len(pixels_of_clusters)):
        for j in range(len(pixels_of_clusters[i])):
            for k in range(3):
                obj_feat_matr_median[pixels_of_clusters[i][j][0]][k] = medians[i][k]

    return obj_feat_matr_median

def get_middle_median_matrixes(n_clusters):
    obj_feat_matr_middle = np.array(objects_features_matrix)
    obj_feat_matr_median = np.array(objects_features_matrix)
    pixels_for_clusters = []

    for i in range(n_clusters):
        pixels_for_clusters.append([])

    for i in range(len(objects_features_matrix)):
        element = [i]
        for j in range(len(objects_features_matrix[i])):
            element.append(objects_features_matrix[i][j])
        pixels_for_clusters[kmeans.labels_[i]].append(element)

    obj_feat_matr_middle = get_middle_matrix(obj_feat_matr_middle, pixels_for_clusters)
    obj_feat_matr_median = get_median_matrix(obj_feat_matr_median, pixels_for_clusters)

    return obj_feat_matr_middle, obj_feat_matr_median


warnings.filterwarnings("ignore")

image = imread('parrots.jpg')
image = img_as_float64(image)
draw_image(image, 'Inital image')

x, y, z = image.shape
objects_features_matrix = np.reshape(image, (x * y, z))

PSNR_middle = []
PSNR_median = []

print('Log:\n')
for n_clusters in range(8,21):
    print('Number of clusters: ' + str(n_clusters))
    kmeans = KMeans(init='k-means++', random_state=241, n_clusters=n_clusters)
    print('[MESSAGE]: Please, wait! Start get clusters...')
    kmeans.fit(objects_features_matrix)
    print('[MESSAGE]: Succesfull finish get clusters!!!')
    print('[MESSAGE]: Please, wait! Start get matrixes...')
    obj_feat_matr_middle, obj_feat_matr_median = get_middle_median_matrixes(n_clusters)
    print('[MESSAGE]: Succesfull finish get matrixes!!!')
    image_middle = reback_to_image(obj_feat_matr_middle)
    image_median = reback_to_image(obj_feat_matr_median)
    draw_image(image_middle, 'Middle-clusterization image\nNumber of clusters = ' + str(n_clusters))
    print('[MESSAGE]: Succesfull show middle-clusterization image!!!')
    draw_image(image_median, 'Median-clusterization image\nNumber of clusters = ' + str(n_clusters))
    print('[MESSAGE]: Succesfull show median-clusterization image!!!')
    print('[MESSAGE]: Please, wait! Start calculate PSRN for middle-matrix and median-matrix...')
    # PSNR_middle.append(compare_psnr(image, image_middle))
    # PSNR_median.append(compare_psnr(image, image_median))
    PSNR_middle.append(get_PSNR(image, image_middle))
    PSNR_median.append(get_PSNR(image, image_median))
    print('[MESSAGE]: Succesfull finish calculate PSRN for middle-matrix and median-matrix!!!')
    print('[MESSAGE]: For n_clusters=' + str(n_clusters) + ':')
    print('          1) PSNR_middle: ' + str(PSNR_middle[n_clusters - 8]))
    print('          2) PSNR_median: ' + str(PSNR_median[n_clusters - 8]))
    print('\n')

print('PSNR_middle: ' + str(PSNR_middle))
print('PSNR_median: ' + str(PSNR_median))

number_of_clusters = 8
while(PSNR_middle[number_of_clusters - 8] <= 20 and PSNR_median[number_of_clusters - 8] <= 20):
    number_of_clusters += 1
print('Minimum number of clusters, when PSNR > 20: ' + str(number_of_clusters))

f = open('task_1_answer.txt', 'w')
f.write(str(number_of_clusters))
print('\nMESSAGE: The required information has been successfully written to files: \'task_1_answer.txt\'')