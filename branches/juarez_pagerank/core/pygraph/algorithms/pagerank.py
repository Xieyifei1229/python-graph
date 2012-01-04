# Copyright (c) 2010 Pedro Matiello <pmatiello@gmail.com>
#                    Juarez Bochi <jbochi@gmail.com>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.


"""
PageRank algoritm

@sort: PageRank
"""

DAMPING_FACTOR = 0.85 #PageRank dumping factor
MAX_ITERACTIONS = 100 #max number of iteractions 
TOLERANCE = 0.00001 #tolerance against last iteraction

def pagerank(graph):
    """
    Compute and return the PageRank in an directed graph.    
    
    @type graph: digraph 
    @param graph: Digraph
    
    @rtype: Dict
    @return: Dict containing all the nodes PageRank 
    """
    
    nodes = graph.nodes()
    graph_size = len(nodes)
    if graph_size == 0:
        return {}
    min_value = (1.0-DAMPING_FACTOR)/graph_size #value for nodes without inbound links
    
    # itialize the page rank dict with 1/N for all nodes
    pagerank = dict.fromkeys(nodes, 1.0/graph_size)
        
    for i in range(MAX_ITERACTIONS):
        diff = 0 #total difference compared to last iteraction
        # computes each node PageRank based on inbound links
        for node in nodes:
            rank = min_value
            for referring_page in graph.incidents(node):
                rank += DAMPING_FACTOR * pagerank[referring_page] / len(graph.neighbors(referring_page))
                
            diff += abs(pagerank[node] - rank)
            pagerank[node] = rank
        
        #stop if PageRank has converged
        if diff < TOLERANCE:
            break
    
    return pagerank