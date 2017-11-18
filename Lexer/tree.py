import re

trackerString = ""


class tree:
    """
    Tree class, where a tree is a label
    with zero or more trees as children
    """

    def __init__(self, label, children=None):
        """
        Tree constructor
        """
        self.label = label
        self.children = children if children != None else []

    def __str__(self):
        """
        Translate to newick string
        """
        return self.strhelper() + ';'

    def strhelper(self):
        s = ""
        length = len(self.children)
        if length > 0:
            s += "("
            for x in range(0, length):
                s += self.children[x].strhelper()
                if x < length - 1:
                    s += ","
            s += ")"
        s += self.label
        return s

    def __repr__(self):
        return "Tree: " + str(self)

    def __len__(self):
        """
        Return number of nodes in tree
        """
        childLength = 0
        for child in self.children:
            childLength += len(child)
        return 1 + childLength
        # Instructional note: This is expected to be recursive.

    def isLeaf(self):
        """
        Return true/false indicating whether
        the tree is a leaf
        """
        return len(self.children) == 0


class ParserException(Exception):
    """
    Exception class for parse_newick
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


def lexer(g):
    s = ''
    lastchar = ''
    for l in re.sub("\s+", "", g):
        if l.isalnum():
            s += l
            lastchar = ''
        elif len(s) > 0:
            yield s
            s = ''
            # non alnum character was read, but an alphanum was previously read in
            yield l
            if l == ')':
                lastchar = l
        # non alnum character read, and one wasn't being built
        else:
            if lastchar == ')':
                yield lastchar
                lastchar = ''
            yield l
            if l == ')':
                lastchar = ')'
    if len(s) > 0:
        yield s
    yield '$'


# Parse_newick Should raise the following ParserException errors when appropriate:
# * Terminating semi-colon missing.
# * Expected label missing.
# * Missing command or ) where expected.
# (You may add others as you see fit.)
#
# Spacing should not matter: "(a,b)c;", and " ( a  ,  b ) c; " should result in idential
# trees.
def parse_newick(s):
    """
    Take a newick string and return the corresponding tree object.
    """
    global trackerString
    trackerString = s.replace(" ", "")
    G = lexer(s)
    try:
        return Tree(next(G), G)
    except ParserException as e:
        raise e


# Tree, S, ID, rule

def Tree(current, G):
    global trackerString
    t = ''
    if current == ';':
        raise ParserException("Can't start with ;")
    if current.isalnum():
        t = tree(RequireName(current, G))
    else:
        t = Subtree(current, G)
    try:
        end = next(G)
        if end == ';':
            if next(G) == '$':
                return t
        elif t.label == "" and end == '$':
            return t
        else:
            raise ParserException("Missing semi colon")
    except:
        raise ParserException("Bad end")


def Subtree(current, G):
    if current.isalnum():
        return tree(current)
    elif current == '(':
        return Internal(current, G)
    else:
        raise ParserException("Bad subtree start: " + current)


def Internal(current, G):
    trees = []
    if current == '(':
        trees = (BranchSet(next(G), G))
        return tree(Name(next(G), G), trees)
    else:
        raise ParserException("Bad Internal: " + current)


def BranchSet(current, G):
    trees = []
    trees.append(Branch(current, G))
    current = next(G)
    while current == ',':
        trees.append(Branch(next(G), G))
        current = next(G)
    return trees


def Branch(current, G):
    return Subtree(current, G)


def Name(current, G):
    if current.isalnum():
        return current
    return ''


def RequireName(current, G):
    if current.isalnum:
        return current
    raise ParserException("Can't have an empty name")

