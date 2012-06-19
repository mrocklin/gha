Language Plot
=============

This directory holds code to produce a graph of languges common on github.com.

This code takes the 
[timeline database](https://github.com/blog/1112-data-at-github) of
interactions on github and produces a graph described in the 
[DOT language](http://en.wikipedia.org/wiki/DOT_language)
which can then be compiled with neato into a pdf. 

Size of nodes are relative to their popularity on github 

Edges between nodes are a measure of how many people on github own repositories
in each of these languages. Because many people who use MatLab also use Fortran
these nodes are close together. Communities related to web, lisp, numerics,
.NET, etc... are evident in the graph.

Aesthetics
----------

It is difficult to visualize a graph that conveys information well and is
aesthetically pleasing. A number of arbitrary choices were made regarding node
size, edge length, transparency, color, etc.... Care has been taken so that
these choices are well separated out from the practical part of the code.
Experimentation in these aspects is encouraged. 

To Run
------
The following code should produce a pdf file

    python go.py

Author
------
[Matthew Rocklin](http://matthewrocklin.com/)
