from operator import itemgetter
import sys
#ID: 28900057
#name: Chong Kah Ying
# In this question your program will read a simple, weighted, undirected, and connected graph,
# G(V, E, W), and compute:
# 1. a smallest-weight spanning tree of G, and
# 2. a second-smallest-weight spanning tree of G, whose weight is greater than or equal to
# the smallest.
# To address this task, you must implement Kruskal’s algorithm by employing union-by-rank
# data structure with path compression.
class DisjointSet():
    def __init__(self, n_elements):
        self.parent_array = []
        self.initialize_parentArr(n_elements)

    def initialize_parentArr(self,n):
        for _ in range(n):
            self.parent_array.append(-1)

    def find(self, element):
        if self.parent_array[element] < 0:
            return element
        else:
            self.parent_array[element] = self.find(self.parent_array[element])
            return self.parent_array[element]

    def union(self, element_a, element_b):
        root_a = self.find(element_a)
        root_b = self.find(element_b)

        if root_a == root_b:
            return False
        
        height_a = -self.parent_array[root_a]
        height_b = -self.parent_array[root_b]

        if height_a > height_b:
            self.parent_array[root_b] = root_a
        elif height_b > height_a:
            self.parent_array[root_a] = root_b
        else:
            self.parent_array[root_b] = root_a
            self.parent_array[root_a] = -(height_a+1) 
        return True

def make_mst(disjoint_set,size,sequence):
    sum  = 0
    mst_edges = []
    unused_edges = []
    skip = 0
    for edge in sequence:
        made_it = disjoint_set.union(edge[0],edge[1])
        if made_it:
            skip += 1
            sum += edge[2]
            mst_edges.append(edge)
        else:
            unused_edges.append(edge)
        if skip == size - 1:
            break
    return mst_edges, unused_edges, sum 

def create_normal_spanning_tree(size,sequence):
    disjoint_set =DisjointSet(size)
    sequence = sorted(sequence,key=itemgetter(2))
    return make_mst(disjoint_set,size,sequence)
    
def create_second_minimum_spanning_tree(size,sequence,unused_edges,sum):
    #brute force solution
    second_smallest = None
    for i in range(len(sequence)-1,-1,-1):
        # remove a different edge from the smallest mst created earlier 
        temp  = sequence.copy()
        temp.pop(i)
        for j in range(len(unused_edges)):
            # add an unused edge into the smallest mst with an edge removed 
            partial_disjoint_set = DisjointSet(size)
            temp1 = temp.copy()
            temp1.append(unused_edges[j])
            used_edges, not_used, second_sum = make_mst(partial_disjoint_set,size,temp1)
            # if there are edges that are not used, this means that the edges do not form a minimum spanning tree 
            if len(not_used) == 0:
                # second smallest sum must be bigger than the smallest mst sum weight 
                if second_smallest == None and second_sum > sum:
                    second_smallest = [used_edges,second_sum]
                else:
                    if second_smallest != None:
                        if second_sum < second_smallest[1] and second_sum > sum:
                            second_smallest = [used_edges, second_sum]
                
    return second_smallest

def readInput(filename):
    txtFile = open(filename,'r')
    txt = txtFile.read()
    txtFile.close()
    txt = txt.split('\n')
    nodesn_edgesn = txt[0].split(" ")
    nodes_n = int(nodesn_edgesn[0])
    edges_n = int(nodesn_edgesn[1])
    v1_v2_w_list = []
    for i in range(1,edges_n+1):
        v1_v2_w = txt[i].split()
        v1_v2_w[0] = int(v1_v2_w[0])
        v1_v2_w[1] = int(v1_v2_w[1])
        v1_v2_w[2] = int(v1_v2_w[2])
        v1_v2_w_list.append(v1_v2_w)
    return nodes_n, v1_v2_w_list

def writeOutput(smallest_mst,second_smallest_mst):
    smallest_mst_edges = smallest_mst[0]
    smallest_sum = smallest_mst[1]

    second_smallest_mst_edges = second_smallest_mst[0]
    second_smallest_sum = second_smallest_mst[1]

    output_string = "Smallest Spanning Tree Weight = " + str(smallest_sum)
    output_string += "\n#List of edges in the smallest spanning tree:"
    
    for v1_v2_w in smallest_mst_edges:
        output_string += "\n" + str(v1_v2_w[0]) + " " + str(v1_v2_w[1]) + " " + str(v1_v2_w[2])
    
    output_string += "\nSecond-smallest Spanning Tree Weight = " + str(second_smallest_sum)
    output_string += "\n#List of edges in the second smallest spanning tree:"
    for v1_v2_w in second_smallest_mst_edges:
        output_string += "\n" + str(v1_v2_w[0]) + " " + str(v1_v2_w[1]) + " " + str(v1_v2_w[2])
    
    outputFile = open('output_spanning.txt','w')
    outputFile.write(output_string)
    outputFile.close()


if __name__ == "__main__":
    file = sys.argv[1]
    nodes_n, v1_v2_weight_list =readInput(file)
    smallest_mst, unused_edges, smallest_sum = create_normal_spanning_tree(nodes_n+1,v1_v2_weight_list)
    second_smallest = create_second_minimum_spanning_tree(nodes_n+1,smallest_mst,unused_edges,smallest_sum)
    smallest_mst = [smallest_mst,smallest_sum]
    writeOutput(smallest_mst,second_smallest)
    