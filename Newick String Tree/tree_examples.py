import tree

"""
A set of sample trees.  Provided for help with testing.
"""

t1 = tree.tree("a")  # a;
t2 = tree.tree("b")  # b;
t3 = tree.tree("c")  # c;
t4 = tree.tree("d", [t1, t2, t3])  # (a,b,c)d;
t5 = tree.tree("e")  # e;
t6 = tree.tree("f")  # f;
t7 = tree.tree("g", [t5, t6])  # (e,f)g;
t8 = tree.tree("h", [t4, t7])  # ((a,b,c)d,(e,f)g)h;
