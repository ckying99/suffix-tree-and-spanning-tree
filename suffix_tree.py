#ID: 28900057
#name: Chong Kah Ying
# In the real-world, it is a routine task to search a collection (corpora) of texts and identify all
# occurrences of patterns (often, by ignoring characters’ upper/lower case).
# To render the search of any pattern efficient, an approach is to preprocess the collection of
# texts beforehand, and then use that processed data structure to support efficient identification
# of the locations of user-specified pattern(s).
# For this question, you are required to construct a single suffix tree containing information of
# suffixes of multiple (and not just one) input (text) strings: {txt1,txt2, . . . ,txtN }. In principle,
# N (number of texts in the collection) can grow arbitrarily large.
# Once the suffix tree for the set {txt1,txt2, . . . ,txtN } is constructed, you will have to use it
# to search and identify all the locations (positions) of exact occurrences of each pattern from a
# given set of pattern strings: {pat1
# , pat2
# , . . . , patM}.
# In this task, all strings (i.e., text strings and pattern strings) are read from their respective
# standard ASCII files (with 7-bit fixed-width ASCII code per character, where each character
# takes 1 Byte of storage). Also, it is perfectly safe to assume that none of the (text and pattern)
# strings being read from the ASCII files contain a ‘$’ (ASCII value 36) as one of its characters.
# Finally, in this exercise, although we are doing exact matching of patterns, you should handle any pattern matching case-insensitively. That is, if you were seaching for ‘FIT3155’ in some
# collection of texts, you should also report matches for ‘fit3155’ or ‘Fit3155’ or ‘fIt3155’ etc.
# along with the ‘FIT3155’


import sys
ASCII_N = 128   
NONE_128 = []
for _ in range(ASCII_N):
    NONE_128.append(None)

class Pointer:
    def __init__(self,value):
        self.value = value
    def increment(self):
        if type(self.value) == list:
            self.value[1] += 1
    def still_same_edge(self):
        if type(self.value) == list:
            end = self.value[0].end
            if type(end) == GlobalEnd:
                end = end.value
            if self.value[1] > end:
               return False
            else:
                return True
class GlobalEnd:
    def __init__(self):
        self.value = -1
    def increment(self):
        self.value += 1

class Node:
    def __init__(self,isLeaf,suffix_id,text_id):
        self.name = ""
        self.isLeaf = isLeaf
        self.text_id = text_id
        self.suffix_id = suffix_id
        self.children = NONE_128.copy()
        self.suffix_link = None
        self.suffix_ids_and_text_ids = []
        self.add_suffix_which_shares_same_pattern(text_id,suffix_id)

    def add_suffix_which_shares_same_pattern(self,text_id,suffix_id):
        if self.isLeaf:
            self.suffix_ids_and_text_ids.append((text_id,suffix_id))

class Edge:
    def __init__(self,start,end,exitNode,text_id):
        self.start = start
        self.end = end
        self.exitNode = exitNode
        self.text_id = text_id

class Tree:
    def __init__(self):
        self.root = Node(False,-1,-1)
        self.new_internal_node = None

    def addChild(self,node,text_i,edge,text):
        node.children[ord(text[text_i])] = edge

    def branch(self,edge,split_index, branch_index, end, text, active_node,text_id):
        #get original edge information 
        edge_end_index = edge.end
        edge_exit_node = edge.exitNode
        #split into two parts - make the second half first 
        split_second_half = Edge(split_index,edge_end_index,edge_exit_node,text_id)
        #change the ending index for the first half of the split 
        edge.end = split_index-1 

        new_internal_node = Node(False,-1,-1)
        new_internal_node.suffix_link = active_node
        self.new_internal_node =  new_internal_node

        #change exit node of the first half of the split
        edge.exitNode = new_internal_node

        #new leaf edge
        #branch edge becomes the suffix id  
        leaf_node = Node(True,branch_index,text_id)
        branch_edge =  Edge(branch_index,end,leaf_node,text_id)
        
        self.addChild(new_internal_node,split_index,split_second_half,text)
        self.addChild(new_internal_node,branch_index,branch_edge,text)
        

def gst(texts):  
    suffix_tree = Tree()
    suffix_tree.root.name = "r"
    #contruct tree by looping all texts provided in input file
    for id_and_text in texts:
        text_id = id_and_text[0]
        word = id_and_text[1] 
        n = len(word)
        i = 0
        pointer = Pointer(suffix_tree.root)
        global_end = GlobalEnd()
        last_j = -1
        active_node = None
        active_edge = None
        active_length = 0
        showstopper = False
        while i < n:
            #rule 1
            global_end.increment()
            j = last_j + 1
            prev_node = None

            while j <= i: 
                pointer.value = suffix_tree.root
                skipped = 0 
                length_of_edge = 0
                k = j
                traverse_before_active_point = False
                traverse_after_active_point = False
                #skip-count = 113-164
                if active_node != None:     
                    if active_edge != None:
                        if active_node == suffix_tree.root and not showstopper:
                            if active_length > 0:
                                active_length -= 1
                            k = active_edge.start + 1
                        else :
                            k = active_edge.start
                            end = active_edge.end
                            if type(end) == GlobalEnd:
                                end = end.value
                    if active_node.suffix_link == None:
                        active_node.suffix_link = active_node
                    if not showstopper:        
                        active_node = active_node.suffix_link
                    pointer.value = active_node
                    skipped = 0
                    if active_length > 0:
                        traverse_after_active_point = True
                        edge = pointer.value.children[ord(word[k])]   
                        end = edge.end
                        if type(end) == GlobalEnd:
                            end = end.value
                        length_of_edge = end - edge.start + 1
                        node = pointer.value
                        active_edge = edge
                        active_node = node
                        while skipped + length_of_edge < active_length:
                            k += length_of_edge
                            skipped += length_of_edge
                            node = edge.exitNode
                            pointer.value = node
                            edge = node.children[ord(word[k])]
                            active_edge = edge
                            end = edge.end
                            active_node = node
                            if type(end) == GlobalEnd:
                                end = end.value
                            length_of_edge = end - edge.start + 1
                        pointer.value = [active_edge,active_edge.start + active_length - skipped - 1]
                        active_length = active_length - skipped 
                        end = pointer.value[0].end
                        if type(end) == GlobalEnd:
                            end = end.value
                        skipped += active_length
                        if traverse_after_active_point or traverse_before_active_point:
                            pointer.increment()
                            if type(pointer.value) == list:
                                if not pointer.still_same_edge():
                                    pointer.value = pointer.value[0].exitNode
                                    active_node = pointer.value

                if type(pointer.value) == Node:
                    node = pointer.value
                    edge_that_starts_with_text_k = node.children[ord(word[i])]
                    #rule 2
                    if edge_that_starts_with_text_k == None:
                        #leaf_node for the new edge 
                        leaf_node = Node(True,i,text_id)
                        leaf_edge = Edge(i,global_end,leaf_node,text_id)
                        suffix_tree.addChild(node,i,leaf_edge,word)                        
                        active_node = node
                        active_edge = None
                        active_length = 0
                        showstopper = False
                        last_j += 1
                        j += 1
                        pointer.value = node
                    #rule 3
                    else:
                        active_node = node
                        active_edge = edge_that_starts_with_text_k
                        if word[i] == "$" and type(active_edge) == GlobalEnd:
                            leaf_node = active_edge.exitNode
                            leaf_node.add_suffix_which_shares_same_pattern(text_id,j)
                        active_length = 1
                        pointer.value = [active_edge,active_edge.start]
                        showstopper = True
                        if prev_node != None:
                            prev_node.suffix_link = node
                        break
                        
                else:
                    edge = pointer.value[0]
                    #rule 3
                    if word[i] == word[pointer.value[1]]:
                        if word[i] == "$" and type(active_edge) == GlobalEnd:
                            leaf_node = active_edge.exitNode
                            leaf_node.add_suffix_which_shares_same_pattern(text_id,j)
                        active_length += 1
                        showstopper = True
                        break
                    #rule 2
                    else:
                        split_index = pointer.value[1]
                        suffix_tree.branch(edge,split_index,i,global_end,word,active_node,text_id)
                        if prev_node != None:
                            prev_node.suffix_link = suffix_tree.new_internal_node
                        prev_node = suffix_tree.new_internal_node
                        last_j += 1
                        j += 1
                        showstopper = False
            i += 1
    return suffix_tree

def find_pattern_in_tree(suffix_tree,patterns,texts):
    # texts is indexing 0 but first index in the txt file is 1 

    pointer = Pointer(suffix_tree.root)
    patterns_texts_pos = []
    for patternID_pattern in patterns:
        pattern_id = patternID_pattern[0]
        pattern = patternID_pattern[1]
        found = True
        i = 0
        while i < len(pattern):
            char = pattern[i]
            if type(pointer.value) == Node:
                node = pointer.value
                edge = node.children[ord(char)]
                if edge == None:
                    found = False
                    break
                pointer.value = [edge,edge.start]
                i += 1
            else:
                text_id = edge.text_id 
                text = texts[text_id - 1][1]
                edge = pointer.value[0]
                pointer.increment()
                if pointer.still_same_edge():
                    edge_index = pointer.value[1]
                    if text[edge_index] == char:
                        i += 1
                else:
                    pointer.value = edge.exitNode
        if found:
            edge = pointer.value[0]
            node = edge.exitNode
            suffix_ids_and_text_ids = traverse_internal_nodes(node)
            for item in suffix_ids_and_text_ids:
                text_number = item[0]
                pos_in_text = item[1]
                patterns_texts_pos.append([pattern_id,text_number,pos_in_text])
    return patterns_texts_pos

def traverse_internal_nodes(node,text):
    if node.isLeaf:
        return node.suffix_ids_and_text_ids

    else:
        for edge in node.children:
            if edge != None:
                if type(edge.end) == GlobalEnd:
                    end = edge.end.value
                else:
                    end = edge.end
                traverse_internal_nodes(edge.exitNode,text)

def readInput(specification_filename):
    txtFile = open(specification_filename,'r')
    txt = txtFile.read()
    txtFile.close()
    texts = []
    patterns = []
    txt = txt.split("\n")
    i = 0
    item = txt[i]
    if item.isdigit():
        n = int(item)
        i += 1
        for _ in range(n):
            item = txt[i]
            item = item.split(" ")
            n_word = int(item[0])
            file_name = item[1]
            txtFile = open(file_name,'r')
            word = txtFile.read()
            txtFile.close()
            texts.append((n_word,word))
            i += 1
    item = txt[i+1]
    if item.isdigit():
        m = int(item)
        i += 1
        for _ in range(m):
            item = txt[i]
            item = item.split(" ")
            n_word = int(item[0])
            file_name = item[1]
            txtFile = open(file_name,'r')
            word = txtFile.read()
            txtFile.close()
            patterns.append((n_word,word))
            i += 1
    return texts, patterns
        

def writeOutput(pattern_text_pos):
    outputFile = open('output_gst.txt','w')
    output_string = ""
    for item in pattern_text_pos:
        output_string += str(item[0]) + " " + str(item[1]) + " " + str(item[2]) +"\n"
    outputFile.write(output_string)
    outputFile.close()

if __name__ == "__main__":
    file = sys.argv[1]
    texts,patterns = readInput(file)
    original_texts =texts.copy()
    texts.sort(key= lambda t:len(t[1]),reverse=True)
    suffix_tree = gst(texts)
    pattern_text_pos = find_pattern_in_tree(suffix_tree,patterns,original_texts)
    writeOutput(pattern_text_pos)
    
