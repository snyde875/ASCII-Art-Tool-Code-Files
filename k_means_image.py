import random
import numpy as np
from math import sqrt
from PIL import Image
from ascii_art import get_width_height

BLACK = (0, 0, 0)


def get_ascii_data(file_name):
    """Returns a 3 dimensional numpy array of an image with colors represented in RGB format"""
    img = Image.open(file_name).convert("RGB")
    img_data = np.array(img)

    return img_data


def random_color():
    """Returns a random color as a 3-tuple representing RGB values.
       Each color component will be between 0 and 255"""
    return random.randrange(256), random.randrange(256), random.randrange(256)


def create_k_means(k):
    """Creates a k-long list of random colors by using random_color()"""
    k_means = []

    for index in range(0, k):
        k_means.append(random_color())

    return k_means


def initialize(k, cluster, img):
    height, width = get_width_height(img)

    for row in range(0, height):
        for col in range(0, width):
            i = random.randrange(0, k)

            color = img[col][row]
            cluster[i].append(color)

    return update_k_means(cluster)


def create_empty_cluster(k):
    """
    Creates a k-long 2-dimensional list designed to hold color clusters
    for each k-mean color value

    :param k: The number of color clusters/k-means; Each k corresponds to an empty list
    :return: An empty 2-dimensional list that's k-long
    """
    clusters = []

    for index in range(0, k):
        clusters.append([])

    return clusters


def color_distance(color, k_means):
    """
    Determines the euclidean distance between two 3-tuple variables

    :param color: A tuple representing an RGB color value; color = (red, blue, green)
    :param k_means: A k-long list of color averages
    :return: Returns the index of the color average that most closely corresponds to variable color
    """
    col1 = color
    color_distances = [0] * len(k_means)

    for i in range(0, len(color_distances)):
        col2 = k_means[i]

        distance = sqrt((col1[0] - col2[0]) ** 2 + (col1[1] - col2[1]) ** 2 + (col1[2] - col2[2]) ** 2)
        color_distances[i] = distance

    closest_match = min(color_distances)
    index = color_distances.index(closest_match)

    return index


def average_color(color_cluster):
    """
    Determines the average color in a cluster of colors

    :param color_cluster: A list that stores 3-tuple values representing colors closest
    to a particular k-mean color
    :return: The average color as a 3-tuple RGB value out of all the colors in the list
    """
    num_colors = len(color_cluster)

    if num_colors == 0:
        return BLACK

    r_sum = 0
    g_sum = 0
    b_sum = 0

    for r, g, b in color_cluster:
        r_sum += r
        g_sum += g
        b_sum += b

    r = r_sum // num_colors
    g = g_sum // num_colors
    b = b_sum // num_colors

    avg_color = (r, g, b)
    return avg_color


def group_colors(image, k_means):
    """
    Compares every pixel in the image to each k-mean;
    Afterwards, determines which k-mean that pixel is closest to;
    Essentially clusters each color in the image to a specific average color listed in k-means

    :param image: A two dimensional list that represents every color in
     the image in the form of a 3-tuple
    :param k_means: The current color averages for the image
    :return: A k-long list of color clusters; all colors in a specific cluster are closest in color
    value to their corresponding average color

    For example, all colors in the cluster located at index 0 are closest in color value to the color
    average at index 0 in the list k-means
    """
    height, width = get_width_height(image)
    k = len(k_means)

    groupings = create_empty_cluster(k)

    for row in range(0, height):
        for col in range(0, width):
            color = image[col][row]
            closest_group_index = color_distance(color, k_means)

            groupings[closest_group_index].append(color)

    return groupings


def is_different(old_k_means, new_k_means):
    """
    Determines whether or not two k-means lists are different
    Primarily used to determine whether or not the while loop in run_k_means should
    continue to run

    :param old_k_means: The original k_means at the beginning of each iteration of the while loop in run_k_means
    :param new_k_means: The k-means created after every single color was compared to the old_k_means averages
    :return: True if averages are different, false is averages are the same
    """

    if old_k_means == new_k_means:
        return False
    else:
        return True


def update_k_means(clusters):
    """
    Creates a new, k-mean color average list from an existing color cluster

    :param clusters: A k-long two dimensional list; each index of the list corresponds to
    a single cluster of colors stored in another list
    :return: Returns a new set of color averages adapted from color clusters
    """
    new_k_means = []
    for color_cluster in clusters:
        avg_color = average_color(color_cluster)
        new_k_means.append(avg_color)

    return new_k_means


def create_image(cur_img, k_means):
    """
    Creates a PIL image object of the new image after the k_means algorithm has finished
    :param cur_img: the original 3-dimensional numpy array representing the original image uploaded
    :param k_means: a k-long list of cur_imgs average color clusters
    :return: a PIL image object of the new, modified image
    """
    height, width = get_width_height(cur_img)

    for row in range(0, height):
        for col in range(0, width):
            cur_color = cur_img[col][row]
            new_color_index = color_distance(cur_color, k_means)

            new_color = k_means[new_color_index]
            cur_img[col][row] = new_color

    return Image.fromarray(cur_img)


def k_means(label, img, k):
    """Takes an image and averages it to k number of colors"""
    img_data = get_ascii_data(img)  # Converts data into ASCII RGB format represented as a numpy array
    k_means = create_k_means(k)
    # cluster = create_empty_cluster(k)
    # k_means = initialize(k, cluster, img_data)
    different = True
    while different:
        cluster_list = group_colors(img_data, k_means)
        new_k_means = update_k_means(cluster_list)

        different = is_different(k_means, new_k_means)
        k_means = new_k_means

    return create_image(img_data, k_means), label


def execute_infile(img, new_file_name, k):
    """Same as the function k_means but meant for infile use"""
    img_data = get_ascii_data(img)

    k_means = create_k_means(k)
    # cluster = create_empty_cluster(k)

    # k_means = initialize(k, cluster, img_data)
    different = True
    while different:
        cluster_list = group_colors(img_data, k_means)
        new_k_means = update_k_means(cluster_list)

        different = is_different(k_means, new_k_means)
        k_means = new_k_means

    create_image(img_data, k_means)


if __name__ == "__main__":
    import time

    t0 = time.process_time()

    execute_infile("imgs/kimlip.png", "friends.png", 5)

    t1 = time.process_time()
    print("Time elapsed:", t1 - t0, "seconds")





































