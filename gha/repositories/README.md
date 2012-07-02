Repositories Plot
=================

This directory holds code to produce a graph of the major projects on GitHub.

This code takes the 
[timeline database](https://github.com/blog/1112-data-at-github) of
interactions on github and produces a graph described in the 
[DOT language](http://en.wikipedia.org/wiki/DOT_language)
which can then be compiled with neato into a pdf. 

Size of nodes are relative to their fork counts on github 

Edges between nodes are a measure of how many people on github own
forks of each pair of repositories. I.e. because many people who own numpy also own scipy these nodes are close in the graph. 

Aesthetics
----------

This graph has a large number of nodes, a very large number of edges and is of small diameter (i.e. it is a standard small world graph). 
As a result a naive visualization of this graph produces a "hairball plot"
where a large number of large edges dominate the visual field and prevent 
insight from showing itself. 

To solve this problem we use work from 

<a href=http://thevcl.com/papers/1175%20final.pdf>
"Centrality Based Visualization of Small World Graphs"
by 
F. van Ham and M. Wattenberg</a>

Which removes edges with high 
<a href=http://en.wikipedia.org/wiki/Betweenness_centrality>
betweenness centrality</a>. The reasoning here is that these edges span
different communities and can be removed without losing the community
structure which is often the insight that is desired from such a visualization. 

The code in this directory currently produces a minimum spanning tree (minimum
in the sense of total edge betweenness) and produces a dot file from this
graph. Future work is to add in more edges to fill in the graph but not destroy
the clairty of information. 

It is difficult to visualize a graph that conveys information well and is
aesthetically pleasing. A number of arbitrary choices were made regarding node
size, edge length, transparency, color, etc.... Care has been taken so that
these choices are well separated out from the practical part of the code.
Experimentation in these aspects is encouraged. 

Dependencies
------------

This directory uses algorithms found in 
<a href=http://en.wikipedia.org/wiki/NetworkX>NetworkX</a> 
a common library for network analysis in Python.

Author
------
[Matthew Rocklin](http://matthewrocklin.com/)
