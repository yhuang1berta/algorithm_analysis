class Max_heap:
    # a binary max-heap data structure implemented using python list
    def __init__(self, A=None):
        self._heap = []
        if A:
            for item in A:
                self.insert(item)

    def max(self):
        # return node with maximum probability
        return self._heap[0]

    def is_empty(self):
        # return if heap is empty
        return len(self._heap) == 0

    def insert(self, x):
        # insert node x at index to heap
        self._heap.append(x)
        parent_index = (len(self._heap) - 2) // 2
        if parent_index < 0:
            return
        parent = self._heap[parent_index]
        if parent.name != x.name:
            x.parent = parent
            if parent.left_child:
                parent.right_child = x
            else:
                parent.left_child = x
        self.bubble_up(x, parent_index)

    def bubble_up(self, x, parent_index):
        # move larger node to upper levels, helper function of insert
        while parent_index >= 0 and self._heap[parent_index].prob < x.prob and self._heap[parent_index].name != x.name:
            temp = self._heap[parent_index]
            x.name, temp.name = temp.name, x.name
            x.prob, temp.prob = temp.prob, x.prob
            x.path_from, temp.path_from = temp.path_from, x.path_from
            parent_index = (parent_index - 1) // 2
            x = temp

    def bubble_down(self, x):
        # move smaller node to lower level, helper function of extract_max
        # note: index is not necessary since we can use the left/right_child property
        # of Vertex_node to move down the heap
        while (x.left_child and x.left_child.prob > x.prob) or (x.right_child and x.right_child.prob > x.prob):
            if x.left_child.prob > x.prob:
                x.left_child.name, x.name = x.name, x.left_child.name
                x.left_child.prob, x.prob = x.prob, x.left_child.prob
                x.left_child.path_from, x.path_from = x.path_from, x.left_child.path_from
                x = x.left_child
            else:
                x.left_child.name, x.name = x.name, x.left_child.name
                x.left_child.prob, x.prob = x.prob, x.left_child.prob
                x.left_child.path_from, x.path_from = x.path_from, x.left_child.path_from
                x = x.right_child

    def extract_max(self):
        # return the node with maximum probability while mainteining max-heap property
        if not self._heap[0].left_child and not self._heap[0].right_child:
            return self._heap.pop()
        max_node, min_node = self._heap[0], self._heap[-1]
        max_node.prob, min_node.prob = min_node.prob, max_node.prob
        max_node.name, min_node.name = min_node.name, max_node.name
        max_node.path_from, min_node.path_from = min_node.path_from, max_node.path_from
        max_node = self._heap.pop()
        if max_node.parent.left_child is max_node:
            max_node.parent.left_child = None
        else:
            max_node.parent.right_child = None
        max_node.parent = None
        self.bubble_down(self._heap[0])
        return max_node

    def delete(self, x):
        # delete the node with name x while mainteining the max-heap property
        min_node = self._heap[-1]
        if x == min_node.name:
            if not min_node.parent:
                return self._heap.pop()
            if min_node is min_node.parent.left_child:
                min_node.parent.left_child = None
            else:
                min_node.parent.right_child = None
            min_node.parent = None
            return self._heap.pop()
        for v in self._heap:
            if v.name == x:
                v.name, min_node.name = min_node.name, v.name
                v.prob, min_node.prob = min_node.prob, v.prob
                v.path_from, min_node.path_from = min_node.path_from, v.path_from
                return_node = self._heap.pop()
                if return_node.parent.left_child is return_node:
                    return_node.parent.left_child = None
                else:
                    return_node.parent.right_child = None
                return_node.parent = None
                self.bubble_down(v)
                return return_node

class Vertex_node:
  def __init__(self, name):
    # name of vertex
    self.name = name
    # heap structure
    self.parent = None
    # heap structure
    self.left_child = None
    # heap structure
    self.right_child = None
    # the maximum probability to get to this node from a node in X
    self.prob = 0
    # the connecting vertex that has the maximum probability path to this node
    self.path_from = None


def maximum_likelihood(num_vertices, edges, s, t):
    '''
    Pre: num_vertices, edges, start vertex s, target vertex t
    Post: return the path that maximizes the probabilityof a successful traversal and its weight  '''
    # # Uncommenting the following lines will result in Case 1 passing
    # path = [1,3,4]
    # prob = 0.15
    # return path, prob  pass
    # TODO: implement this function

    # initialize
    Vertices = [Vertex_node(i) for i in range(1,num_vertices+1)]
    Vertices[s - 1].prob = 1
    path = [t]
    H = Max_heap(Vertices)
    X = []

    # run Dijkstra algorithm till H is empty
    while not H.is_empty():
        v = H.extract_max()
        X.append(v.name)
        i = 0
        # remove any edges that have already been taken, saves some iterations
        while i < len(edges):
            e = edges[i]
            if e[0] == v.name:
                if not e[1] in X:
                    y = H.delete(e[1])
                    if y.prob < v.prob * e[2]:
                        y.prob = v.prob * e[2]
                        y.path_from = v
                    H.insert(y)
                edges.pop(i)
            else:
                i += 1

    # trying to find target in list of vertex_nodes
    target = None
    for node in Vertices:
        if node.name == t:
            curr = node
            target = node
            break

    # trace path by calling path_from attribute of vertex_node
    while curr.path_from:
        path.append(curr.path_from.name)
        curr = curr.path_from
    path.reverse()

    # if t is not in list of nodes, then it can't be reached
    if not target or target.prob == 0:
        return [], 0

    return path, target.prob

# testing code below
# a=[0,1,2,3,4,5]
# v = [Vertex_node(i) for i in a]
# v[4].prob = 100
# heap = Max_heap(v)
# print(maximum_likelihood(    4,    [[1,2,0.2], [1,3,0.5], [1,4,0.1], [2,4,0.5], [3,4,0.3]],    1,    4    ))
# print(maximum_likelihood(5, [[1,2,0.3],[1,3,0.8],[1,5,0.4],[2,4,0.1],[2,5,0.7],[3,2,0.4],[4,1,0.2],[4,3,0.5],[5,4,0.6]],1,4))
# print(maximum_likelihood(2, [[1,2,0]], 1, 2)) #[] 0
# print(maximum_likelihood(1, [], 1, 1)) # [1], 1
# print(maximum_likelihood(1, [[1,1,0.2], [1,1,0.5]], 1,1)) # [1], 1
# print(maximum_likelihood(2, [[1,2,0.2], [1,2,0.5]], 1, 2)) #[1,2], 0.5
# print(maximum_likelihood(2, [[1,2,0.2], [1,2,0.5]], 2, 1)) # [], 0
# print(maximum_likelihood(6, [[1,2,0.9], [2,3,0.9], [3,5,0.9], [2,5,0.5]], 2, 5)) # [2,3,5], 0.81
# print(maximum_likelihood(6, [[3,1,0.9], [1,3,0.9], [3,5,0.9]], 3, 5)) # [3,5], 0.9)
# print(maximum_likelihood(5, [[1,4,0.36], [1,3,0.8], [2,1,0.1], [2,3,0.1], [3,2,0.5], [2,4,0.9], [5,1,1], [4,1,0.2], [1,4,0.04]], 5, 4)) # [5,1,3,2,4], 0.36000000000000004)
# print(maximum_likelihood(5, [[1,4,0.37], [1,3,0.8], [2,1,0.1], [2,3,0.1], [3,2,0.5], [2,4,0.9], [5,1,1], [4,1,0.2], [1,4,0.04]], 5, 4)) # [5,1,4], 0.37)
