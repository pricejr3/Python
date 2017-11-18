
class tree(object):
    """
    Tree class, where a tree is a label
    with zero or more trees as children
    """

    def __init__(self, label, children = None):
        """
        Tree constructor
        """
        self.label = label
        self.children = children if children != None else []

    def __str__(self):
        """
        Translate to newick string
        """
        return self.strHelper(self.label, self.children) + ";"

    def __repr__(self):
        return "Tree: " + str(self)

    def __len__(self):
        """
        Return number of nodes in teee
        """
        if self.isLeaf():
            return 1
        return 1 + sum([len(child) for child in self.children])

    def isLeaf(self):
        """
        Return true/false indicating whether
        the tree is a leaf
        """
        return len(self.children) == 0

    def strHelper(self, label, children):
        output = ""
        if len(children) > 0:
            output = "(" + ",".join([self.strHelper(str(child.label), child.children) for child in children]) + ")"
        return output + str(label)



class ParserException(Exception):
    """
    Exception class for parse_newick
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


import re
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
    s = re.sub("\s+", "", s) #remove all whitespace.
    ret = process(s) #returns array [tree, {remaining string}]
    if ret[1] != ";": #the only thing left in the string after all is parsed should be just ";"
        raise ParserException("Bad tree")
    return ret[0] #tree
    

#returns a list of two elements, the first element is the tree formed by the call
#and the second element is the string left to parse.
#s[1:] is s with the first character removed. we do this to chop off a character after processing it
#s[0] points to the character we are currently processing.
def process(s):
    if len(s) == 0: #only happens when processing empty string
        raise ParserException("Bad tree")
    if s[0] == "(": #nested tree
        #emulate do while loop by recursing once then going into the loop
        ret_vals = process(s[1:])
        children = [ret_vals[0]]
        s = ret_vals[1]
        if len(s) == 0: #"(a,b" causes s to be empty here
            raise ParserException("Bad tree")
        while s[0] == ",": #handles multiple children in nested tree
            ret_vals = process(s[1:]) #return new s and children
            children.append(ret_vals[0])
            s = ret_vals[1] #get new string to process with recursive part removed
        if s[0] != ")":
            raise ParserException("No matching paren")
        s = s[1:] #remove )
        result = re.search("^\w+", s)
        if not result:
            raise ParserException("No label")
        label = result.group(0)
        s = s[len(label):] #remove label from string
        return [tree(label, children), s]
    #down here means we only have a label to process and return
    result = re.search("^\w+", s) #find label
    if not result:
        raise ParserException("No label")
    label = result.group(0)
    s = s[len(label):] #remove label from string
    return [tree(label, []), s] #return new tree with label and no children

