# 6.00.2x Problem Set 5
# Graph optimization
#
# A set of data structures to represent graphs
#

class Node(object):
    def __init__(self, name):
        self.name = str(name)
    def getName(self):
        return self.name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def __eq__(self, other):
        return self.name == other.name
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        # Override the default hash method
        # Think: Why would we want to do this?
        return self.name.__hash__()

class Edge(object):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def __str__(self):
        return '{0}->{1}'.format(self.src, self.dest)

class WeightedEdge(Edge):
    def __init__(self, src, dest, weight1, weight2):
        self.src = src
        self.dest = dest
        self.weight1 = weight1
        self.weight2 = weight2
    def getTotalDistance(self):
        return self.weight1
    def getOutdoorDistance(self):
        return self.weight2
    def __str__(self):
        return str(self.src) + '->' + str(self.dest) + ' ' \
        + '(' + str(self.weight1) + ', ' + str(self.weight2) + ')'

class Digraph(object):
    """
    A directed graph...
    """
    def __init__(self):
        self.nodes = set([])
        self.edges = {}
        
    def addNode(self, node):
        if node in self.nodes:
            raise ValueError('Duplicate node')
        else:
            self.nodes.add(node)
            self.edges[node] = []
            
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)
        
    def childrenOf(self, node):
        return self.edges[node]
        
    def hasNode(self, node):
        return node in self.nodes
        
    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[k]:
                res = '{0}{1}->{2}\n'.format(res, k, d)
        return res[:-1]

class WeightedDigraph(Digraph):
    '''
    A weighted, directed graph...
    '''
    def __init__(self):
        self.nodes = set([])
        self.edges = {}
        
    def addEdge(self, edge):
        src = edge.getSource()
        dest = []
        dest.append(edge.getDestination())
        t = (edge.getTotalDistance(), edge.getOutdoorDistance())
        dest.append(t)      
        if not(src in self.nodes and dest[0] in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)       
        
    def childrenOf(self, node):
        childrenNodes = []
        destinations = self.edges[node]
        for k in destinations:
            childrenNodes.append(k[0])
        return childrenNodes
        
    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[k]:
                e1 = d[0]
                e2 = float(d[1][0])
                e3 = float(d[1][1])
                res = '{0}{1}->{2} ({3}, {4})\n'.format(res, k, e1, e2, e3)
        return res[:-1]


    
def printPath(path):
    # a path is a list of nodes
    result = ''
    for i in range(len(path)):
        if i == len(path) - 1:
            result = result + str(path[i])
        else:
            result = result + str(path[i]) + '->'
    return result