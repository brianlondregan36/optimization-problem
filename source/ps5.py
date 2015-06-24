# 6.00.2x Problem Set 5
# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
from graph import * 




#
# Problem 2: Building up the Campus Map
#
'''
MIT campus will be modeled as a digraph. Read in the input file and... 
1. Create a node for every building found in the file (first two columns)
2. Create a weighted edge for each row in the file (weights are in last two columns)
3. Choose an algorithm (probably shortest DFS) to go through the graph and
find the shortest route from one building to another (first weight) with a 
constraint on the amount of time you will spend walking outside (second weight)
'''

def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph...
    Parameters: mapFilename, the name of the map file
    Assumes: Each entry in the map file consists of the following four positive 
    integers separated by a blank space - From To TotalDistance DistanceOutdoors
    Returns: a directed graph representing the map
    """
    g = WeightedDigraph()    
    inFile = open(mapFilename, 'r', 0)
    edgeList = []
    for edge in inFile:
        edgeList.append(edge)
        items = edge.split(' ')
        n1 = Node(items[0])
        n2 = Node(items[1])
        if g.hasNode(n1) != True:
            g.addNode(n1)
        if g.hasNode(n2) != True:
            g.addNode(n2)
        e = WeightedEdge(n1, n2, float(items[2]), float(items[3]))
        g.addEdge(e)
    return g
          



'''
#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and what the constraints are
#

def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors, \
    currDist1=0, currPath=[], allPaths=[]):    
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    
    start = Node(start)
    currPath = currPath + [start]
    edges = digraph.edges[start]
    end = Node(end)  
    
    print 'Current DFS path: ', printPath(currPath)
    
    if start == end:
        allPaths.append(currPath)
        return currPath
        
    for node in digraph.childrenOf(start):
        print "start", start, "and the node", node
        if node not in currPath: 
            for e in edges:
                if e[0] == node:
                    print "found the edge", e
                    if (currDist1 + e[1][0]) <= maxTotalDist:
                        currDist1 = currDist1 + e[1][0]
                        print "it fits, the current distance is", currDist1
                        newPath = bruteForceSearch(digraph, node, end, maxTotalDist, \
                        maxDistOutdoors, currDist1, currPath, allPaths)
                        if newPath != None:
                            currDist1 = 0 
    return allPaths
'''




#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors, path=[], currD1=0, currD2=0, shortest=None):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """   
    path = path + [start]
    edges = digraph.edges[Node(start)]
    
    #print 'Current DFS path: ', printPath(path)

    if start == end:
        return path
        
    for node in digraph.childrenOf(Node(start)):
        if str(node) not in path: 
            if shortest == None or len(path) < len(shortest):
                for e in edges:
                    if e[0] == node and currD1 + int(e[1][0]) <= maxTotalDist and currD2 + int(e[1][1]) <= maxDistOutdoors:
                            currD1 = currD1 + int(e[1][0])
                            currD2 = currD2 + int(e[1][1])
                            newPath = directedDFS(digraph, str(node), end, maxTotalDist, maxDistOutdoors, path, currD1, currD2, shortest)
                            if newPath != None:
                                currD1 = currD1 - int(e[1][0])
                                currD2 = currD2 - int(e[1][1])
                                shortest = newPath
    if shortest == None and len(path) == 1:
        raise ValueError('No such path!')
    return shortest





if __name__ == '__main__':
    mitMap = load_map('C:\Users\brianl\Documents\GitHub\optimization-problem\source\mit_map.txt')
    print isinstance(mitMap, Digraph)
    print isinstance(mitMap, WeightedDigraph)
    print 'nodes', mitMap.nodes
    print 'edges', mitMap.edges

    LARGE_DIST = 1000000

    print "---------------"
    print "Test case 1:"
    print "Find the shortest-path from Building 32 to 56"
    expectedPath1 = ['32', '56']
    dfsPath1 = directedDFS(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath1
    print "DFS: ", dfsPath1

    print "---------------"
    print "Test case 2:"
    print "Find the shortest-path from Building 32 to 56 without going outdoors"
    expectedPath2 = ['32', '36', '26', '16', '56']
    dfsPath2 = directedDFS(mitMap, '32', '56', LARGE_DIST, 0)
    print "Expected: ", expectedPath2
    print "DFS: ", dfsPath2

    print "---------------"
    print "Test case 3:"
    print "Find the shortest-path from Building 2 to 9"
    expectedPath3 = ['2', '3', '7', '9']
    dfsPath3 = directedDFS(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath3
    print "DFS: ", dfsPath3

    print "---------------"
    print "Test case 4:"
    print "Find the shortest-path from Building 2 to 9 without going outdoors"
    expectedPath4 = ['2', '4', '10', '13', '9']
    dfsPath4 = directedDFS(mitMap, '2', '9', LARGE_DIST, 0)
    print "Expected: ", expectedPath4
    print "DFS: ", dfsPath4

    print "---------------"
    print "Test case 5:"
    print "Find the shortest-path from Building 1 to 32"
    expectedPath5 = ['1', '4', '12', '32']
    dfsPath5 = directedDFS(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath5
    print "DFS: ", dfsPath5

    print "---------------"
    print "Test case 6:"
    print "Find the shortest-path from Building 1 to 32 without going outdoors"
    expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
    dfsPath6 = directedDFS(mitMap, '1', '32', LARGE_DIST, 0)
    print "Expected: ", expectedPath6
    print "DFS: ", dfsPath6

    print "---------------"
    print "Test case 7:"
    print "Find the shortest-path from Building 8 to 50 without going outdoors"
    dfsRaisedErr = 'No'
    try:
        directedDFS(mitMap, '8', '50', LARGE_DIST, 0)
    except ValueError:
        dfsRaisedErr = 'Yes'
    
    print "Expected: No such path! Should throw a value error."
    print "Did DFS search raise an error?", dfsRaisedErr

    print "---------------"
    print "Test case 8:"
    print "Find the shortest-path from Building 10 to 32 without walking"
    print "more than 100 meters in total"
    dfsRaisedErr = 'No'
    try:
        directedDFS(mitMap, '10', '32', 100, LARGE_DIST)
    except ValueError:
        dfsRaisedErr = 'Yes'
    
    print "Expected: No such path! Should throw a value error."
    print "Did DFS search raise an error?", dfsRaisedErr


