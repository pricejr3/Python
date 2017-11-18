"""

Parser for the Micro-language.
Grammar:
   <program> -> begin <statement_list> end
   <statement_list> -> <statement>; { <statement; }
   <statement> -> <assign> | read( <id_list> ) | write( <expr_list> )
   <assign> -> <ident> := <exp1>
   <id_list> -> <ident> {, <ident>}
   <expr_list> -> <exp1> {, <exp1}
   <exp1> -> term1 { or term1 }
   <term1> -> fact1 { and fact1 }
   <R> -> rel_op exp2 | lambda
   <exp2> -> term2 { + term2 | - term2 }
   <term2> -> fact2 { * fact2 | / fact2 }
   <fact2> -> ident | INTLIT | BOOLLIT | (exp1)
   <ident> -> ID
   <arith_op> -> + | - | * | \
   <bool_op> -> and | or | not
   <rel_op> -> = | != | < | <= | > | >=
"""
from lexer import *
from tree import *

st = { }

def id_list(current, L):
    t = tree('ID_LIST')
    current, child = ident(current, L)
    t.children.append(child)
    while current.name == 'COMMA':
        current, child = ident(next(L), L) #consume comma
        t.children.append(child)
    return current, t

def expr_list(current, L):
    t = tree('EXPR_LIST')
    current, child = exp1(current, L)
    t.children.append(child)
    while current.name == 'COMMA':
        current, child = exp1(next(L), L) #consume comma
        t.children.append(child)
    return current, t

def program(current, L):
    t = tree('PROGRAM')
    if current.name != 'BEGIN':
        raise ParserError("Parser error: Missing BEGIN at line " + str(current.line_num) + " " + str(current.col) + " got \"" + str(current) + "\"")
    current, child = statement_list(next(L), L) #consume BEGIN
    t.children = [tree("BEGIN"), child]
    if current.name != 'END':
        raise ParserError("Parser error: Expecting END, got " + current.name + " at line " + str(current.line_num) + " " + str(current.col))
    t.children.append(tree("END"))
    return current, t

def statement_list(current, L):
    t = tree('STATEMENT_LIST')
    current, child = statement(current, L)
    count = 1
    t.children.append(child)
    if current.name != 'SEMICOLON':
        raise ParserError("Parser error: Missing semicolon at line " + str(current.line_num) + " " + str(current.col))
    current = next(L) #consume semicolon
    while current.name in {'ID', 'READ', 'WRITE', 'INT', 'BOOL', 'STRING'}:
        current, child = statement(current, L)
        count += 1
        t.children.append(child)
        if current.name != 'SEMICOLON':
            raise ParserError("Parser error: Missing semicolon at line " + str(current.line_num) + " " + str(current.col))
        current = next(L) #consume semicolon
    return current, t

def statement(current, L):
    t = tree('STATEMENT')
    if current.name == 'ID':
        current, child = assign(current, L)
        t.children.append(child)
        return current, t
    if current.name == 'READ':
        current = next(L) #consume READ
        if current.name != 'LPAREN':
            raise ParserError("Parser error: Missing LPAREN at line " + str(current.line_num) + " " + str(current.col))
        current, child = id_list(next(L), L) #consume LPAREN
        t.children = [tree("READ"), child]
        if current.name != 'RPAREN':
            raise ParserError("Parser error: Missing RPAREN at line " + str(current.line_num) + " " + str(current.col))
        return next(L), t #consume LPAREN
    if current.name == 'WRITE':
        current = next(L) #consume WRITE
        if current.name != 'LPAREN':
            raise ParserError("Parser error: Missing LPAREN at line " + str(current.line_num) + " " + str(current.col))
        current, child = expr_list(next(L), L) #consume LPAREN
        t.children = [tree("WRITE"), child]
        if current.name != 'RPAREN':
            raise ParserError("Parser error: Missing RPAREN at line " + str(current.line_num) + " " + str(current.col))
        return next(L), t #consume RPAREN
    if current.t_class == 'TYPE':
        current, child = declaration(current, L)
        t.children.append(tree('DECLARATION', [child]))
        return current, t
    raise ParserError("Parser error: Unexpected character at line " + str(current.line_num) + " " + str(current.col) + " " + str(current.name))

def declaration(current, L):
    typeid = current.pattern
    current, child = ident(next(L), L, typeid)
    return current, child

def exp1(current, L):
    current, child = term1(current, L)
    t = None
    while current.name == 'OR':
        current, temp = bool_op(current, L)
        current, child2 = term1(current, L)
        if t == None:
            t = temp
            t.children = [child, child2]
        else:
            temp.children = [t, child2]
            t = temp
    if t == None:
        t = child
    return current, t

def term1(current, L):
    current, child = fact1(current, L)
    t = None
    while current.name == 'AND':
        current, temp = bool_op(current, L)
        current, child2 = fact1(current, L)
        if t == None:
            t = temp
            t.children = [child, child2]
        else:
            temp.children = [t, child2]
            t = temp
    if t == None:
        t = child
    return current, t

def fact1(current, L):
    current, child = exp2(current, L)
    t = child    
    if current.t_class == 'RELOP':
        current, t = rel_op(current, L)
        current, child2 = exp2(current, L)
        t.children += [child, child2]
    return current, t

def exp2(current, L):
    current, child = term2(current, L)
    t = None
    while current.name in {'PLUS', 'MINUS'}:
        current, temp = arith_op(current, L)
        current, child2 = term2(current, L)
        if t == None:
            t = temp
            t.children = [child, child2]
        else:
            temp.children = [t, child2]
            t = temp
    if t == None:
        t = child
    return current, t

def term2(current, L):
    current, child = fact2(current, L)
    t = None 
    while current.name in {'MULTIPLY', 'DIVIDE'}:
        current, temp = arith_op(current, L)
        current, child2 = fact2(current, L)
        if t == None:
            t = temp
            t.children = [child, child2]
        else:
            temp.children = [t, child2]
            t = temp
    if t == None:
        t = child    
    return current, t

def fact2(current, L):
    #t = tree("PRIMARY") might want this
    #don't make a tree here so that the things here are leaves
    if current.name == 'LPAREN':
        current, child = exp1(next(L), L) #consume lparen
        if current.name != 'RPAREN':
            raise ParserError("Parser error: Missing right paran at line " + str(current.line_num) + " " + str(current.col))
        return next(L), child #consume rparen
    if current.name == 'ID':
        current, child = ident(current, L) #this consumes ID
        return current, child #consume nothing
    if current.name in {'BOOLT', 'BOOLF', 'INTLIT', 'STRINGLIT'}:
        if current.name == 'STRINGLIT':
            st['_strings'] += [current.pattern]
        return next(L), tree(current)
    if current.name == 'UNARY':
        t = tree("UNARY")
        current, child = fact2(next(L), L) #consume -, get what it is negating
        t.children += [child]
        return current, t
    if current.name == 'NOT':
        t = tree("NOT")
        current, child = fact2(next(L), L) #consume NOT, get what it is negating
        t.children += [child]
        return current, t
    raise ParserError("Parser error unknown primary: " + str(current))

def assign(current, L):
    t = tree('ASSIGNMENT')
    st[current.pattern]["init"] = True
    current, child1 = ident(current, L) #get first identifier
    if current.name != 'ASSIGNOP': #make sure equals op is after ident
        raise ParserError("Parser error: Unexpected token at line " + str(current.line_num) + " " + str(current.col))  
    current, child2 = exp1(next(L), L) #consume assignop and expression
    if st[child1.label.pattern]["type"] == "string":
        if isinstance(child1.label, Token):
            if child1.label.name == "STRINGLIT":
                st['_strings'].append(child2.label.pattern)
            
    #if lefttype is righttype: #type of assignment doesn't match type of storing variable
        #raise ParserError("Parser error: type of assignment value doesn't match type of storing variable at line " + str(current.line_num) + " " + str(current.col))
    t.children = [child1, child2]

    return current, t

def ident(current, L, typeid = None):
    if typeid != None: #typeid is sent in through declaration
        st[current.pattern] = { "type" : typeid, "init" : False, "index": 0, "max_index": 0, "lits": [] }
    if current.name != 'ID':
        raise ParserError("Parser error: Unexpected token at line " + str(current.line_num) + " " + str(current.col))
    return next(L), tree(current) #saving token instead of name so that we can access its data later

def arith_op(current, L):
    if current.t_class != 'ARITHOP': #handle plus and minus by checking class instead of name
        raise ParserError("Parser error: Unexpected token at line " + str(current.line_num) + " " + str(current.col))
    return next(L), tree(current.name)

def bool_op(current, L):
    if current.t_class != 'BOOLOP': #handle "and", "or", and "not" by checking class instead of name
        raise ParserError("Parser error: Unexpected token at line " + str(current.line_num) + " " + str(current.col))
    return next(L), tree(current.name)

def rel_op(current, L):
    if current.t_class != 'RELOP': #handle ==, !=, <, <=, >, >= by checking class instead of name
        raise ParserError("Parser error: Unexpected token at line " + str(current.line_num) + " " + str(current.col))
    return next(L), tree(current.name)


class ParserError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


#######################################
# Parsing code
def parser(source_file = "test.txt", token_file = "tokens.txt"):
    """
    source_file: A program written in the ML langauge.
    returns True if the code is syntactically correct.
    Throws a ParserError otherwise.
    """
    lex = lexer(source_file, token_file)
    tr = None
    st.clear() #it's a global variable so make sure it's cleared between calls
    st['_strings'] = []
    try:
        current, tr = program(next(lex), lex)
    except StopIteration:
        raise ParserError("Parser error: EOF reached when not expected")
    try:
        next(lex)
    except StopIteration:
        return tr, st
    raise ParserError("Parser error: Code after end statement")
