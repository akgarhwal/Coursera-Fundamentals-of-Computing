
# coding: utf-8

# # Comparison of Clustering Algorithms

# Comparison of two clustering Algorithms
# 
# 1. Hierarchical Clustering
# 2. K-Means Clustering
# 
# we will compare these two clustering methods in three areas:<br>
# 
# <b>Efficiency</b> - Which method computes clusterings more efficiently?<br>
# <b>Automation</b> - Which method requires less human supervision to generate reasonable clusterings?<br>
# <b>Quality</b> - Which method generates clusterings with less error?<br>
# 
# <br>
# We will apply our clustering methods to several sets of 2D data that include information about lifetime cancer risk from air toxics. The raw version of this data is available from <a href="https://www.epa.gov/national-air-toxics-assessment/2005-national-air-toxics-assessment">this</a> website.<br> 
# Each entry in the data set corresponds to a county in the USA (identified by a unique 5 digit string called a FIPS county code) and includes information on the total population of the county and its per-capita lifetime cancer risk due to air toxics.
# 
# <br>
# To visualizing this data, we have processed this county-level data to include the (x,y) position of each county when overlaid on <a href="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/USA_Counties_with_FIPS_and_names.svg/1000px-USA_Counties_with_FIPS_and_names.svg.png">this</a> map of the USA.
# 
# <a href="https://github.com/akgarhwal/Coursera-Fundamentals-of-Computing/tree/master/Algorithmic%20Thinking%20-Part%202/Week-1%20and%20Week-2/CSV_files"><b>Data for comparison</b></a>

# # The Cluster class

# In[9]:


"""
Cluster class for Module 3
"""

import math


class Cluster:
    """
    Class for creating and merging clusters of counties
    """
    
    def __init__(self, fips_codes, horiz_pos, vert_pos, population, risk):
        """
        Create a cluster based the models a set of counties' data
        """
        self._fips_codes = fips_codes
        self._horiz_center = horiz_pos
        self._vert_center = vert_pos
        self._total_population = population
        self._averaged_risk = risk
        
        
    def __repr__(self):
        """
        String representation assuming the module is "alg_cluster".
        """
        rep = "alg_cluster.Cluster("
        rep += str(self._fips_codes) + ", "
        rep += str(self._horiz_center) + ", "
        rep += str(self._vert_center) + ", "
        rep += str(self._total_population) + ", "
        rep += str(self._averaged_risk) + ")"
        return rep


    def fips_codes(self):
        """
        Get the cluster's set of FIPS codes
        """
        return self._fips_codes
    
    def horiz_center(self):
        """
        Get the averged horizontal center of cluster
        """
        return self._horiz_center
    
    def vert_center(self):
        """
        Get the averaged vertical center of the cluster
        """
        return self._vert_center
    
    def total_population(self):
        """
        Get the total population for the cluster
        """
        return self._total_population
    
    def averaged_risk(self):
        """
        Get the averaged risk for the cluster
        """
        return self._averaged_risk
   
        
    def copy(self):
        """
        Return a copy of a cluster
        """
        copy_cluster = Cluster(set(self._fips_codes), self._horiz_center, self._vert_center,
                               self._total_population, self._averaged_risk)
        return copy_cluster


    def distance(self, other_cluster):
        """
        Compute the Euclidean distance between two clusters
        """
        vert_dist = self._vert_center - other_cluster.vert_center()
        horiz_dist = self._horiz_center - other_cluster.horiz_center()
        return math.sqrt(vert_dist ** 2 + horiz_dist ** 2)
        
    def merge_clusters(self, other_cluster):
        """
        Merge one cluster into another
        The merge uses the relatively populations of each
        cluster in computing a new center and risk
        
        Note that this method mutates self
        """
        if len(other_cluster.fips_codes()) == 0:
            return self
        else:
            self._fips_codes.update(set(other_cluster.fips_codes()))
 
            # compute weights for averaging
            self_weight = float(self._total_population)                        
            other_weight = float(other_cluster.total_population())
            self._total_population = self._total_population + other_cluster.total_population()
            self_weight /= self._total_population
            other_weight /= self._total_population
                    
            # update center and risk using weights
            self._vert_center = self_weight * self._vert_center + other_weight * other_cluster.vert_center()
            self._horiz_center = self_weight * self._horiz_center + other_weight * other_cluster.horiz_center()
            self._averaged_risk = self_weight * self._averaged_risk + other_weight * other_cluster.averaged_risk()
            return self

    def cluster_error(self, data_table):
        """
        Input: data_table is the original table of cancer data used in creating the cluster.
        
        Output: The error as the sum of the square of the distance from each county
        in the cluster to the cluster center (weighted by its population)
        """
        # Build hash table to accelerate error computation
        fips_to_line = {}
        for line_idx in range(len(data_table)):
            line = data_table[line_idx]
            fips_to_line[line[0]] = line_idx
        
        # compute error as weighted squared distance from counties to cluster center
        total_error = 0
        counties = self.fips_codes()
        for county in counties:
            line = data_table[fips_to_line[county]]
            singleton_cluster = Cluster(set([line[0]]), line[1], line[2], line[3], line[4])
            singleton_distance = self.distance(singleton_cluster)
            total_error += (singleton_distance ** 2) * singleton_cluster.total_population()
        return total_error


# # Helper Methods for clustering methods

# In[10]:


"""
slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)

where cluster_list is a 2D list of clusters in the plane
"""

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
    ans = (float("inf"),-1,-1)
    for ind_i,point_i in enumerate(cluster_list):
        for ind_j,point_j in enumerate(cluster_list):
            if ind_i != ind_j :
                distance = point_i.distance(point_j)
                if distance < ans[0]:
                    ans = (distance,ind_i,ind_j)
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
            ans = (d_right[0],d_right[1]+middle,d_right[2]+middle)
        
        mid = (cluster_list[middle-1].horiz_center() + cluster_list[middle].horiz_center()) / 2
        
        ans_2 = closest_pair_strip(cluster_list,mid,ans[0])
        if ans_2[0] < ans[0]:
            ans = ans_2

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
    #cluster_list.sort(key = lambda cluster: cluster.vert_center())
    index_set = list()
    for ind, point in enumerate(cluster_list):
        if abs(point.horiz_center()-horiz_center) < half_width :
            index_set.append(ind)
    index_set = sorted(index_set, key = lambda x: cluster_list[x].vert_center(), reverse = True)
    
    k_items = len(index_set)
    ans = (float("inf"),-1,-1)
    for u_ind in range(0,k_items-1):
        for v_ind in range(u_ind+1,min(u_ind+3,k_items-1)+1):
            distance = cluster_list[index_set[u_ind]].distance(cluster_list[index_set[v_ind]])
            if ans[0] > distance :
                ans = (distance,min(index_set[u_ind],index_set[v_ind]),max(index_set[u_ind],index_set[v_ind]))
    
    return ans
            


# # Clustering Methods 

# In[11]:


"""
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)
"""

######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    while len(cluster_list) > num_clusters :
        # sort list very importtant
        cluster_list = sorted(cluster_list, key = lambda cluster:cluster.horiz_center())
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
    cluster_list_sorted = sorted(cluster_list, key = lambda cluster:cluster.total_population(), reverse = True)
    k_cluster_center = []
    for idx in range(0,num_clusters):
        k_cluster_center.append((cluster_list_sorted[idx].horiz_center(),cluster_list_sorted[idx].vert_center()))
    
    for dummy_iter in range(1,num_iterations+1):
        #Initialize k empty sets C1, . . . , Ck;
        new_cluster = [alg_cluster.Cluster(set([]),0,0,1,0) for dummy_idx in range(0,num_clusters)]
        for index in range(0,len(cluster_list)):
            distance_list = [math.sqrt((k_cluster_center[ind_f][0] - cluster_list[index].horiz_center()) ** 2 + (k_cluster_center[ind_f][1] - cluster_list[index].vert_center()) **2 ) for ind_f in range(0,num_clusters)]
            index_min = distance_list.index(min(distance_list))	
            new_cluster[index_min].merge_clusters(cluster_list[index])
            
        for index in range(0, num_clusters):
            k_cluster_center[index] = (new_cluster[index].horiz_center(),new_cluster[index].vert_center())
    
    return new_cluster


# In[12]:


## Load data to program 
def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib2.urlopen(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print("Loaded", len(data_lines), "data points")
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]


# # Efficiency Comparison 

# Q1. Comparision between running time of slow_closest_pair and fast_closest_pair.<br>
# 
#   Complexity of fast_closest_pair : O(n log<sup>2</sup> n)  <br> 
#   Complexity of slow_closest_pair : O(n<sup>2</sup>) <br> 
# 
# <img src="https://raw.githubusercontent.com/akgarhwal/Coursera-Fundamentals-of-Computing/master/Algorithmic%20Thinking%20-Part%202/Week-1%20and%20Week-2/Comparison%20of%20Clustering%20Algorithms/Running_time_slow_and_fast_closest_pair.png"/>

# Q2. An image of the 15 clusters generated by applying hierarchical clustering to the 3108 county cancer risk data set.
# 
# <img src="https://raw.githubusercontent.com/akgarhwal/Coursera-Fundamentals-of-Computing/master/Algorithmic%20Thinking%20-Part%202/Week-1%20and%20Week-2/Comparison%20of%20Clustering%20Algorithms/Hierachical_clustering_15_cluster_3108.png"/>

# Q3.An image of the 15 clusters generated by applying 5 iterations of k-means clustering to the 3108 county cancer risk data set.
# 
# <img src="https://raw.githubusercontent.com/akgarhwal/Coursera-Fundamentals-of-Computing/master/Algorithmic%20Thinking%20-Part%202/Week-1%20and%20Week-2/Comparison%20of%20Clustering%20Algorithms/K-means_clustering_15_cluster_3108.png.png" />

# Q4. Which clustering method is faster when the number of output clusters is either a small fixed number or a small fraction of the number of input clusters?<br>
# Ans : If there are n input clusters and k output clusters, hierarchical clustering makes (n−k) calls to fast_closest_pair. If k is fixed or a small fraction of n, each call to fast_closest_pair is O(nlog<sup>2</sup>⁡n) and, therefore, the running time for hierarchical clustering using fast_closest_pair is O(n<sup>2</sup>log<sup>2</sup>⁡n). <br>
# 
# For k-means, the running time is either O(n) or O(n<sup>2</sup>) depending on whether the size of output cluster is fixed or varies as a function n. 
# Even in the this second case, k being a small fraction of n will reduce the running time in practice.

# # Automation Comparison 

# Q5. An image of the 9 clusters generated by applying hierarchical clustering to the 111 county cancer risk data set. 
# 
# <img src="https://raw.githubusercontent.com/akgarhwal/Coursera-Fundamentals-of-Computing/master/Algorithmic%20Thinking%20-Part%202/Week-1%20and%20Week-2/Comparison%20of%20Clustering%20Algorithms/Hierachical_clustering_9_cluster_111.png.png"/>

# Q5. An image of the 9 clusters generated by applying k-means clustering to the 111 county cancer risk data set. 
# 
# <img src="https://raw.githubusercontent.com/akgarhwal/Coursera-Fundamentals-of-Computing/master/Algorithmic%20Thinking%20-Part%202/Week-1%20and%20Week-2/Comparison%20of%20Clustering%20Algorithms/K-means_clustering_9_cluster_111.png.png"/>

# Q7. Write a function compute_distortion(cluster_list) that takes a list of clusters and uses cluster_error to compute its distortion. 

# In[13]:


#data_table = load_data_table(DATA_XXXXX_URL)

def error_count(cluster_list):
    error_sum = 0.0
    for cluster in cluster_list:
        error_sum += cluster.cluster_error(data_table)   ## Cluster class error function
    return error_sum


# 1. The distortion(or error) for 9 clusters by hierarchical clustering on 111 county data set is = 1.7516 * 10^11 OR 175163886916.0 <br>
# 2. The distortion for 9 clusters by K-means clustering on 111 county data set is = 2.712 * 10^11 OR 271254226925.0

# Q8. Describe the difference between the shapes of the clusters produced by these two methods on the <a href="https://en.wikipedia.org/wiki/West_Coast_of_the_United_States">west coast of the USA</a>. What caused one method to produce a clustering with a much higher distortion? To help you answer this question, you should consider how k-means clustering generates its initial clustering in this case.
# 
# Ans : Each method generates 3 clusters on the west coast of the USA. Hierarchical clustering generates one cluster in Washington state, one in northern California and one in southern California. K-means clustering generates one cluster that includes Washington state and parts of northern California, one cluster that includes the Los Angeles area, and one cluster that includes San Diego. The k-means clustering has substantially higher distortion due in part to the fact that southern California is split into two clusters while northern California is clustered with Washington state.<br>
# <br>
# This difference in cluster shape is due to the fact that the initial clustering used in k-means clustering includes the 3 counties in southern California with high population and no counties in northern California or Washington state. Due to a poor choice of the initial clustering based on large population counties, k-means clustering produces a clustering with relatively high distortion.

# Q9. Which method (hierarchical clustering or k-means clustering) requires less human supervision to produce clustering with relatively low distortion?<br><br>
# Ans : Hierarchical clustering requires less human supervision than k-means clustering to produce clustering of relatively low distortion as it requires no human interaction beyond the choice of the number of output clusters. On the other hand, k-means clustering requires a good strategy for choosing the initial cluster centers.

# # Quality Comparison

# Q10. Comparison between Distortion of hierarchical and k-means methods for 111 data set.
# 
# <img src="https://raw.githubusercontent.com/akgarhwal/Coursera-Fundamentals-of-Computing/master/Algorithmic%20Thinking%20-Part%202/Week-1%20and%20Week-2/Comparison%20of%20Clustering%20Algorithms/Distortion_of_hierarchical_and_k-means_for_111.png" />

# Q11. Comparison between Distortion of hierarchical and k-means methods for 290 data set.
# 
# <img src="https://raw.githubusercontent.com/akgarhwal/Coursera-Fundamentals-of-Computing/master/Algorithmic%20Thinking%20-Part%202/Week-1%20and%20Week-2/Comparison%20of%20Clustering%20Algorithms/Distortion_of_hierarchical_and_k-means_for_290.png" />

# Q12. Comparison between Distortion of hierarchical and k-means methods for 896 data set.
# 
# <img src="https://raw.githubusercontent.com/akgarhwal/Coursera-Fundamentals-of-Computing/master/Algorithmic%20Thinking%20-Part%202/Week-1%20and%20Week-2/Comparison%20of%20Clustering%20Algorithms/Distortion_of_hierarchical_and_k-means_for_896.png" />

# Q13. Analysis of Distortion by Hierarchical and k-means for above 3 set.
# 
# Ans : For the 111 county data set, hierarchical clustering consistently produces clusterings with less distortion. <br>
# For the other two data sets, neither clustering method consistently dominates. 
# 
# For our knowledge : <br>
# Interestingly, k-means clustering produces lower distortion clusterings for the 3108 county data set. <br>
# <a href="http://storage.googleapis.com/codeskulptor-alg/matplotlib_distortion_3018.png">Link</a> to a plot of distortion for the clusterings produced by both methods.

# Q14. Which clustering method would you prefer when analyzing these data sets?
# 
# On these data sets, neither method dominates in all three areas: efficiency, automation, and quality. In terms of efficiency, k-means clustering is preferable to hierarchical clustering as long as the desired number of output clusters is known beforehand. However, in terms of automation, k-means clustering suffers from the drawback that a reliable method for determining the initial cluster centers needs to be available. Finally, in terms of quality, neither method produces clusterings with consistently lower distortion on larger data sets.

# 
# 
# For More details please visit to <a href="https://github.com/akgarhwal/Coursera-Fundamentals-of-Caomputing">Abhinesh Garhwal @Github </a>
# 
# <a href="https://github.com/akgarhwal/Coursera-Fundamentals-of-Computing.git">GitHub Repository</a>
