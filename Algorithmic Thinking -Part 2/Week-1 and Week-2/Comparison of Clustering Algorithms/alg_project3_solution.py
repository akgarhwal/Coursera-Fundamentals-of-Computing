"""
slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""

import math
import alg_cluster


######################################################
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters

    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.
    """
    ans = (float("inf"), -1, -1)
    for ind_i, point_i in enumerate(cluster_list):
        for ind_j, point_j in enumerate(cluster_list):
            if ind_i != ind_j:
                distance = point_i.distance(point_j)
                if distance < ans[0]:
                    ans = (distance, ind_i, ind_j)
    return ans


def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.
    """
    num = len(cluster_list)
    if num <= 3:
        ans = slow_closest_pair(cluster_list)
    else:
        middle = num // 2
        p_left = cluster_list[:middle]
        p_right = cluster_list[middle:]
        d_left = fast_closest_pair(p_left)
        d_right = fast_closest_pair(p_right)
        ans = d_left
        if d_left[0] > d_right[0]:
            ans = (d_right[0], d_right[1] + middle, d_right[2] + middle)

        mid = (cluster_list[middle - 1].horiz_center() + cluster_list[middle].horiz_center()) / 2

        res = closest_pair_strip(cluster_list, mid, ans[0])
        if res[0] < ans[0]:
            ans = res

    return ans


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip

    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.
    """
    # cluster_list.sort(key = lambda cluster: cluster.vert_center())
    index_set = list()
    for ind, point in enumerate(cluster_list):
        if abs(point.horiz_center() - horiz_center) < half_width:
            index_set.append(ind)
    index_set = sorted(index_set, key=lambda x: cluster_list[x].vert_center(), reverse=True)

    k_items = len(index_set)
    ans = (float("inf"), -1, -1)
    for u_ind in range(0, k_items - 1):
        for v_ind in range(u_ind + 1, min(u_ind + 3, k_items - 1) + 1):
            distance = cluster_list[index_set[u_ind]].distance(cluster_list[index_set[v_ind]])
            if ans[0] > distance:
                ans = (distance, min(index_set[u_ind], index_set[v_ind]), max(index_set[u_ind], index_set[v_ind]))

    return ans


# res = closest_pair_strip([alg_cluster.Cluster(set([]), 0, 0, 1, 0), alg_cluster.Cluster(set([]), 0, 1, 1, 0), alg_cluster.Cluster(set([]), 1, 0, 1, 0), alg_cluster.Cluster(set([]), 1, 1, 1, 0)], 0.5, 1.0)
# print(res)

######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list

    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    while len(cluster_list) > num_clusters:
        # sort list very importtant
        cluster_list = sorted(cluster_list, key=lambda cluster: cluster.horiz_center())
        pair = fast_closest_pair((cluster_list))
        cluster_list[pair[1]].merge_clusters(cluster_list[pair[2]])
        cluster_list.pop(pair[2])

    return cluster_list


######################################################################
# Code for k-means clustering


def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list

    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """

    # position initial clusters at the location of clusters with largest populations
    cluster_list_sorted = sorted(cluster_list, key=lambda cluster: cluster.total_population(), reverse=True)
    k_cluster_center = []
    for idx in range(0, num_clusters):
        k_cluster_center.append((cluster_list_sorted[idx].horiz_center(), cluster_list_sorted[idx].vert_center()))

    for dummy_iter in range(1, num_iterations + 1):
        # Initialize k empty sets C1, . . . , Ck;
        new_cluster = [alg_cluster.Cluster(set([]), 0, 0, 1, 0) for dummy_idx in range(0, num_clusters)]
        for index in range(0, len(cluster_list)):
            distance_list = [math.sqrt((k_cluster_center[ind_f][0] - cluster_list[index].horiz_center()) ** 2 + (
            k_cluster_center[ind_f][1] - cluster_list[index].vert_center()) ** 2) for ind_f in range(0, num_clusters)]
            index_min = distance_list.index(min(distance_list))
            new_cluster[index_min].merge_clusters(cluster_list[index])

        for index in range(0, num_clusters):
            k_cluster_center[index] = (new_cluster[index].horiz_center(), new_cluster[index].vert_center())

    return new_cluster

