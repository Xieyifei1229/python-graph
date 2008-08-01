# Copyright (c) 2007-2008 Pedro Matiello <pmatiello@gmail.com>
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
python-graph

A library for working with graphs in Python.
"""


# Module metadata
__authors__ = "Pedro Matiello"
__license__ = "MIT"


# Imports
import accessibility
import generators
import minmax
import searching
import sorting
import readwrite


# Graph class

class graph:
	"""
	Graph class.

	@sort: __init__, __len__, __str__, generate, read, write, add_arrow, add_edge, add_graph, add_nodes, add_spanning_tree, del_arrow, del_edge, get_arrow_weight, get_edge_weight, get_edges, get_nodes, has_arrow, has_edge, has_node, accessibility, breadth_first_search, connected_components, cut_edges, cut_nodes, depth_first_search, minimal_spanning_tree, mutual_accessibility, shortest_path, topological_sorting
	"""


	def __init__(self):
		"""
		Initialize a graph.
		"""
		self.nodes = {}		# Arrow/Edge lists	(like an adjacency list)
		self.weights = {}	# Arrow/Edge weight list


	def __str__(self):
		"""
		Return a string representing the graph when requested by str() (or print).

		@rtype:  string
		@return: String representing the graph.
		"""
		return "<graph object " + str(self.get_nodes()) + " " + str(self.weights) + ">"


	def __len__(self):
		"""
		Return the size of the graph when requested by len().

		@rtype:  number
		@return: Size of the graph.
		"""
		return len(self.nodes)
	

	def read(self, string, fmt=None):
		"""
		Read a graph from a string. Nodes and arrows specified in the input will be added to the current graph.
		
		@type  string: string
		@param string: Input string specifying a graph.

		@type  fmt: string
		@param fmt: Input format. Possible formats are:
			1. 'xml' - XML (default)
		"""
		readwrite.read(self, string, fmt)	


	def write(self, fmt=None):
		"""
		Write the graph to a string. Depending of the output format, this string can be used by read() to rebuild the graph.
		
		@type  fmt: string
		@param fmt: Output format. Possible formats are:
			1. 'xml' - XML (default)
			2. 'dot' - DOT Language (for GraphViz)
			3. 'dotwt' - DOT Language with weight information

		@rtype:  string
		@return: String specifying the graph.
		"""
		return readwrite.write(self, fmt)
	
	
	def generate(self, num_nodes, num_edges, directed=False):
		"""
		Add nodes and random edges to the graph.
		
		@type  num_nodes: number
		@param num_nodes: Number of nodes.
		
		@type  num_edges: number
		@param num_edges: Number of edges.
	
		@type  directed: boolean
		@param directed: Wether the generated graph should be directed or not.
		"""
		generators.generate(self, num_nodes, num_edges, directed)


	def get_nodes(self):
		"""
		Return node list.

		@rtype:  list
		@return: Node list.
		"""
		return self.nodes.keys()


	def get_edges(self, node):
		"""
		Return all outgoing edges from given node.

		@type  node: node
		@param node: Node identifier

		@rtype:  list
		@return: List of nodes directly accessible from given node.
		"""
		return self.nodes[node]


	def has_node(self, node):
		"""
		Return whether the requested node exists.

		@type  node: node
		@param node: Node identifier

		@rtype:  boolean
		@return: Truth-value for node existence.
		"""
		return self.nodes.has_key(node)


	def add_nodes(self, nodelist):
		"""
		Add given nodes to the graph.
		
		@attention: While nodes can be of any type, it's strongly recommended to use only numbers and single-line strings as node identificators if you intend to use write().

		@type  nodelist: list
		@param nodelist: List of nodes to be added to the graph.
		"""
		for each in nodelist:
			self.nodes[each] = []


	def add_edge(self, u, v, wt=1):
		"""
		Add an edge (u,v) to the graph connecting nodes u and v.

		@attention: This function should not be used in directed graphs: use add_arrow() instead.

		@type  u: node
		@param u: One node.

		@type  v: node
		@param v: Other node.
		
		@type  wt: number
		@param wt: Edge weight.
		
		"""
		if (v not in self.nodes[u]):
			self.nodes[u].append(v)
			self.nodes[v].append(u)
			self.weights[(u, v)] = wt
			self.weights[(v, u)] = wt


	def add_arrow(self, u, v, wt=1):
		"""
		Add an arrow (u,v) to the directed graph connecting node u to node v.

		@type  u: node
		@param u: One node.

		@type  v: node
		@param v: Other node.

		@type  wt: number
		@param wt: Arrow weight.
		"""
		if (v not in self.nodes[u]):
			self.nodes[u].append(v)
			self.weights[(u, v)] = wt


	def del_edge(self, u, v):
		"""
		Remove an edge (u, v) from the graph.

		@attention: This function should not be used in directed graphs: use del_arrow() instead.

		@type  u: node
		@param u: One node.

		@type  v: node
		@param v: Other node.
		"""
		if (v in self.nodes[u]):
			self.nodes[u].remove(v)
			self.nodes[v].remove(u)
			del(self.weights[(u,v)])
			del(self.weights[(v,u)])


	def del_arrow(self, u, v):
		"""
		Remove an arrow (u, v) from the directed graph.

		@type  u: node
		@param u: One node.

		@type  v: node
		@param v: Other node.
		"""
		if (v in self.nodes[u]):
			self.nodes[u].remove(v)
			del(self.weights[(u,v)])


	def get_arrow_weight(self, u, v):
		"""
		Get the weight of an arrow.

		@type  u: node
		@param u: One node.

		@type  v: node
		@param v: Other node.
		
		@rtype:  number
		@return: Arrow weight
		"""
		return self.weights[(u, v)]


	def get_edge_weight(self, u, v):
		"""
		Get the weight of an arrow.

		@type  u: node
		@param u: One node.

		@type  v: node
		@param v: Other node.
		
		@rtype:  number
		@return: Edge weight
		"""
		return self.weights[(u, v)]


	def has_arrow(self, u, v):
		"""
		Return whether an arrow from node u to node v exists.

		@type  u: node
		@param u: One node.

		@type  v: node
		@param v: Other node.

		@rtype:  boolean
		@return: Truth-value for arrow existence.
		"""
		return self.weights.has_key((u,v))


	def has_edge(self, u, v):
		"""
		Return whether an edge between nodes u and v exists.

		@type  u: node
		@param u: One node.

		@type  v: node
		@param v: Other node.

		@rtype:  boolean
		@return: Truth-value for edge existence.
		"""
		return self.weights.has_key((u,v)) and self.weights.has_key((v,u))


	def add_graph(self, graph):
		"""
		Add other graph to the graph.
		
		@type  graph: graph
		@param graph: Graph
		"""
		self.add_nodes(graph.get_nodes())
		for each_node in graph.get_nodes():
			for each_arrow in graph.get_edges(each_node):
				self.add_arrow(each_node, each_arrow)


	def add_spanning_tree(self, st):
		"""
		Add a spanning tree to the graph.
		
		@type  st: dictionary
		@param st: Spanning tree.
		"""
		self.add_nodes(st.keys())
		for each in st:
			if (st[each]):
				self.add_arrow(st[each], each)


	def depth_first_search(self, root=None):
		"""
		Depht-first search.
		
		@type  root: node
		@param root: Optional root node (will explore only root's connected component)

		@rtype:  tuple
		@return:  tupple containing a dictionary and two lists:
			1. Generated spanning tree
			2. Graph's preordering
			3. Graph's postordering
		"""
		return searching.depth_first_search(self, root)


	def breadth_first_search(self, root=None):
		"""
		Breadth-first search.

		@type  root: node
		@param root: Optional root node (will explore only root's connected component)

		@rtype:  dictionary
		@return: Generated spanning tree
		"""
		return searching.breadth_first_search(self, root)


	def accessibility(self):
		"""
		Accessibility matrix (transitive closure).

		@rtype:  dictionary
		@return: Accessibility information for each node.
		"""
		return accessibility.accessibility(self)


	def mutual_accessibility(self):
		"""
		Mutual-accessibility matrix (strongly connected components).

		@rtype:  list
		@return: Mutual-accessibility information for each node.
		"""
		return accessibility.mutual_accessibility(self)


	def topological_sorting(self):
		"""
		Topological sorting.

		@attention: Topological sorting is meaningful only for directed acyclic graphs.

		@rtype:  list
		@return: Topological sorting for the graph.
		"""
		return sorting.topological_sorting(self)


	def connected_components(self):
		"""
		Connected components.

		@attention: Indentification of connected components is meaningful only for non-directed graphs.

		@rtype:  dictionary
		@return: Pairing that associates each node to its connected component.
		"""
		return accessibility.connected_components(self)


	def minimal_spanning_tree(self, root=None):
		"""
		Minimal spanning tree.

		@type  root: node
		@param root: Optional root node (will explore only root's connected component)

		@attention: Minimal spanning tree meaningful only for weighted graphs.

		@rtype:  list
		@return: Generated spanning tree.
		"""
		return minmax.minimal_spanning_tree(self, root)


	def shortest_path(self, source):
		"""
		Return the shortest path distance between source node and all other nodes using Dijkstra's algorithm.
		
		@attention: All weights must be nonnegative.

		@type  source: node
		@param source: Node from which to start the search.

		@rtype:  tuple
		@return: A tuple containing two dictionaries, each keyed by target nodes.
			1. Shortest path spanning tree (each key points to previous node in the shortest path transversal)
			2. Shortest distance from given source to each target node
		Inaccessible target nodes do not appear in either dictionary.
		"""
		return minmax.shortest_path(self, source)
	
	
	def cut_edges(self):
		"""
		Return the cut-edges of the given graph.
		
		@rtype:  list
		@return: List of cut-edges.
		"""
		return accessibility.cut_edges(self)


	def cut_nodes(self):
		"""
		Return the cut-nodes of the given graph.
		
		@rtype:  list
		@return: List of cut-nodes.
		"""
		return accessibility.cut_nodes(self)


# Hypergraph class

class hypergraph:
	"""
	Hypergraph class.
	
	@attention: This class is still experimental and incomplete (most functions are stubs).
	"""


	def __init__(self):
		"""
		Initialize a hypergraph.
		"""
		self.all_nodes = {}		# Ordinary nodes and hyperedges
		self.nodes = {}			# Ordinary nodes
		self.edges = {}			# Ordinary edges (between nodes and hyperedges)
		self.hyperedges = {} 	# Hyperedges
		self.weights = {}		# Hyperedge weight list


	def __str__(self):
		"""
		Return a string representing the graph when requested by str() (or print).

		@rtype:  string
		@return: String representing the graph.
		"""
		return "<hypergraph object " + str(self.get_nodes()) + " " + str(self.weights) + ">"


	def __len__(self):
		"""
		Return the size of the graph when requested by len().

		@rtype:  number
		@return: Size of the graph.
		"""
		return len(self.nodes)
	

	def read(self, string, fmt=None):
		"""
		Read a graph from a string. Nodes and arrows specified in the input will be added to the current graph.
		
		@type  string: string
		@param string: Input string specifying a graph.

		@type  fmt: string
		@param fmt: Input format. Possible formats are:
			1. 'xml' - XML (default)
		"""
		pass


	def write(self, fmt=None):
		"""
		Write the graph to a string. Depending of the output format, this string can be used by read() to rebuild the graph.
		
		@type  fmt: string
		@param fmt: Output format. Possible formats are:
			1. 'xml' - XML (default)
			2. 'dot' - DOT Language (for GraphViz)
			3. 'dotwt' - DOT Language with weight information

		@rtype:  string
		@return: String specifying the graph.
		"""
		pass
	
	
	def generate(self, num_nodes, num_edges, directed=False):
		"""
		Add nodes and random edges to the graph.
		
		@type  num_nodes: number
		@param num_nodes: Number of nodes.
		
		@type  num_edges: number
		@param num_edges: Number of edges.
	
		@type  directed: boolean
		@param directed: Wether the generated graph should be directed or not.
		"""
		pass


	def get_nodes(self, hyper=True):
		"""
		Return node list.
		
		@type  hyper: boolean
		@param hyper: Wether hyperedge-nodes should be returned in the list.

		@rtype:  list
		@return: Node list.
		"""
		if (hyper):
			return self.all_nodes.keys()
		else:
			return self.nodes.keys()


	def get_hyperedges(self):
		"""
		Return hyperedge list.
		
		@rtype:  list
		@return: Node list.
		"""
		return self.hyperedges.keys()


	def get_edges(self, node):
		"""
		Return all outgoing edges from given node.

		@type  node: node
		@param node: Node identifier

		@rtype:  list
		@return: List of nodes directly accessible from given node.
		"""
		if (node in self.nodes):
			return self.nodes[node]
		else:
			return self.hyperedges[node]


	def has_node(self, node):
		"""
		Return whether the requested node exists.

		@type  node: node
		@param node: Node identifier

		@rtype:  boolean
		@return: Truth-value for node existence.
		"""
		return self.all_nodes.has_key(node)


	def add_nodes(self, nodelist):
		"""
		Add given nodes to the graph.
		
		@attention: While nodes can be of any type, it's strongly recommended to use only numbers and single-line strings as node identificators if you intend to use write().

		@type  nodelist: list
		@param nodelist: List of nodes to be added to the graph.
		"""
		for each in nodelist:
			self.all_nodes[each] = []
			self.nodes[each] = []


	def add_hyperedges(self, nodelist):
		"""
		Add given hyperedges to the graph.
		
		@attention: Hyperedges are represented as nodes.

		@type  nodelist: list
		@param nodelist: List of nodes to be added to the graph.
		"""
		for each in nodelist:
			self.all_nodes[each] = []
			self.hyperedges[each] = []


	def add_edge(self, node, hyperedge):
		"""
		Add an edge (u,v) to the graph connecting given node and hyperedge.

		@attention: This function should not be used in directed graphs: use add_arrow() instead.

		@type  node: node
		@param node: Ordinary node.

		@type  hyperedge: node
		@param hyperedge: Hyperedge node.
		"""
		if (hyperedge not in self.nodes[node]):
			self.nodes[node].append(hyperedge)
			self.hyperedges[hyperedge].append(node)


	def del_edge(self, u, v):
		"""
		Remove an edge (u, v) from the graph.

		@attention: This function should not be used in directed graphs: use del_arrow() instead.

		@type  u: node
		@param u: One node.

		@type  v: node
		@param v: Other node.
		"""
		pass


	def get_edge_weight(self, u, v):
		"""
		Get the weight of an arrow.

		@type  u: node
		@param u: One node.

		@type  v: node
		@param v: Other node.
		
		@rtype:  number
		@return: Edge weight
		"""
		pass


	def has_edge(self, u, v):
		"""
		Return whether an edge between nodes u and v exists.

		@type  u: node
		@param u: One node.

		@type  v: node
		@param v: Other node.

		@rtype:  boolean
		@return: Truth-value for edge existence.
		"""
		pass


	def add_graph(self, graph):
		"""
		Add other graph to the graph.
		
		@type  graph: graph
		@param graph: Graph
		"""
		pass


	def depth_first_search(self, root=None):
		"""
		Depht-first search.
		
		@type  root: node
		@param root: Optional root node (will explore only root's connected component)

		@rtype:  tuple
		@return:  tupple containing a dictionary and two lists:
			1. Generated spanning tree
			2. Graph's preordering
			3. Graph's postordering
		"""
		st, pre, post = searching.depth_first_search(self, root)
		
		nodes = self.get_nodes(hyper=False)
		hyperedges = self.get_hyperedges()
		
		for each in st.keys():
			if (each in nodes):
				if (st[each] != None and st[each] in hyperedges):
					st[each] = st[st[each]]

		for each in st.keys():
			if (each in hyperedges):
				del st[each]
				del pre[pre.index(each)]
				del post[post.index(each)]
		
		return st, pre, post


	def breadth_first_search(self, root=None):
		"""
		Breadth-first search.

		@type  root: node
		@param root: Optional root node (will explore only root's connected component)

		@rtype:  dictionary
		@return: Generated spanning tree
		"""
		pass


	def accessibility(self):
		"""
		Accessibility matrix (transitive closure).

		@rtype:  dictionary
		@return: Accessibility information for each node.
		"""
		pass


	def mutual_accessibility(self):
		"""
		Mutual-accessibility matrix (strongly connected components).

		@rtype:  list
		@return: Mutual-accessibility information for each node.
		"""
		pass


	def topological_sorting(self):
		"""
		Topological sorting.

		@attention: Topological sorting is meaningful only for directed acyclic graphs.

		@rtype:  list
		@return: Topological sorting for the graph.
		"""
		pass


	def connected_components(self):
		"""
		Connected components.

		@attention: Indentification of connected components is meaningful only for non-directed graphs.

		@rtype:  dictionary
		@return: Pairing that associates each node to its connected component.
		"""
		pass


	def minimal_spanning_tree(self, root=None):
		"""
		Minimal spanning tree.

		@type  root: node
		@param root: Optional root node (will explore only root's connected component)

		@attention: Minimal spanning tree meaningful only for weighted graphs.

		@rtype:  list
		@return: Generated spanning tree.
		"""
		pass


	def shortest_path(self, source):
		"""
		Return the shortest path distance between source node and all other nodes using Dijkstra's algorithm.
		
		@attention: All weights must be nonnegative.

		@type  source: node
		@param source: Node from which to start the search.

		@rtype:  tuple
		@return: A tuple containing two dictionaries, each keyed by target nodes.
			1. Shortest path spanning tree (each key points to previous node in the shortest path transversal)
			2. Shortest distance from given source to each target node
		Inaccessible target nodes do not appear in either dictionary.
		"""
		pass
	
	
	def cut_edges(self):
		"""
		Return the cut-edges of the given graph.
		
		@rtype:  list
		@return: List of cut-edges.
		"""
		pass


	def cut_nodes(self):
		"""
		Return the cut-nodes of the given graph.
		
		@rtype:  list
		@return: List of cut-nodes.
		"""
		pass