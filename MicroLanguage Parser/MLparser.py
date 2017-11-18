"""

Parser for the Micro-language.
Grammar:
   <program> -> begin <statement_list> end
   <statement_list> -> <statement>; { <statement; }
   <statement> -> <assign> | read( <id_list> ) | write( <expr_list> )
   <assign> -> <ident> := <expression>
   <id_list> -> <ident> {, <ident>}
   <expr_list> -> <expression> {, <expression>}
   <expression> -> <primary> {<arith_op> <primary>}
   <primary> -> (<expression>) | <ident> | INTLITERAL
   <ident> -> ID
   <arith_op> -> + | -
"""
from lexer import *
from tree import *

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
    current, child = expression(current, L)
    t.children.append(child)
    while current.name == 'COMMA':
        current, child = expression(next(L), L) #consume comma
        t.children.append(child)
    return current, t

def program(current, L):
    t = tree('PROGRAM')
    if current.name != 'BEGIN':
        raise ParserError("Missing BEGIN at line " + str(current.line_num) + " " + str(current.col))
    current, child = statement_list(next(L), L) #consume BEGIN
    t.children.append(child)
    if current.name != 'END':
        raise ParserError("Expecting END, got " + current.name + " at line " + str(current.line_num) + " " + str(current.col))
    return current, t

def statement_list(current, L):
    t = tree('STATEMENT_LIST')
    current, child = statement(current, L)
    t.children.append(child)
    if current.name != 'SEMICOLON':
        raise ParserError("Missing semicolon at line " + str(current.line_num) + " " + str(current.col))
    current = next(L) #consume semicolon
    while current.name in {'ID', 'READ', 'WRITE'}:
        current, child = statement(current, L)
        t.children.append(child)
        if current.name != 'SEMICOLON':
            raise ParserError("Missing semicolon at line " + str(current.line_num) + " " + str(current.col))
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
            raise ParserError("Missing LPAREN at line " + str(current.line_num) + " " + str(current.col))
        current, child = id_list(next(L), L) #consume LPAREN
        t.children.append(child)
        if current.name != 'RPAREN':
            raise ParserError("Missing RPAREN at line " + str(current.line_num) + " " + str(current.col))
        return next(L), t #consume LPAREN
    if current.name == 'WRITE':
        current = next(L) #consume WRITE
        if current.name != 'LPAREN':
            raise ParserError("Missing LPAREN at line " + str(current.line_num) + " " + str(current.col))
        current, child = expr_list(next(L), L) #consume LPAREN
        t.children.append(child)
        if current.name != 'RPAREN':
            raise ParserError("Missing RPAREN at line " + str(current.line_num) + " " + str(current.col))
        return next(L), t #consume LPAREN
    #TODO add read and write
    raise ParserError("Unexpected character at line " + str(current.line_num) + " " + str(current.col))


def expression(current, L):
    t = tree('EXPRESSION')
    current, child = primary(current, L)
    t.children.append(child)
    while current.t_class == 'ARITHOP':
        current, child = arith_op(current, L)
        t.children.append(child)
        if not (current.name in {'LPAREN', 'ID', 'INTLIT'}):
            raise ParserError("Unexpected character at line " + str(current.line_num) + " " + str(current.col))
        current, child = primary(current, L)
        t.children.append(child)
    return current, t


def primary(current, L):
    t = tree('PRIMARY')
    if current.name == 'LPAREN':
        #consume lparen
        current, child = expression(next(L), L) #consume expression
        t.children.append(child)
        if current.name != 'RPAREN':
            raise ParserError("Missing right paran at line " + str(current.line_num) + " " + str(current.col))
        return next(L), t #consume rparen
    if current.name == 'ID':
        current, child = ident(current, L) #this consumes ID
        t.children.append(child)
        return current, t #consume nothing
    if current.name == 'INTLIT':
        t.children.append([tree(current.name, [tree(current.pattern)])])
        return next(L), t #consume INTLIT
    raise ParserError("Unexpected character at line " + str(current.line_num) + " " + str(current.col))


def assign(current, L):
    t = tree('ASSIGN')
    current, child1 = ident(current, L) #get first identifier
    if current.name != 'ASSIGNOP': #make sure equals op is after ident
        raise ParserError("Unexpected token at line " + str(current.line_num) + " " + str(current.col))
    current, child2 = expression(next(L), L) #consume assignop and expression
    t.children.append([tree(current.name, [child1, child2])])
    return current, t

def ident(current, L):
    t = tree('IDENT')
    if current.name != 'ID':
        raise ParserError("Unexpected token at line " + str(current.line_num) + " " + str(current.col))
    t.children.append([tree(current.name, [tree(current.pattern)])]) #save identifier
    return next(L), t

def arith_op(current, L):
    t = tree('ARITH_OP')
    if current.t_class != 'ARITHOP': #handle plus and minus by checking class instead of name
        raise ParserError("Unexpected token at line " + str(current.line_num) + " " + str(current.col))
    t.children.append([tree(current.name)])
    return next(L), t



class ParserError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


#######################################
# Parsing code
def parser(source_file, token_file):
    """
    source_file: A program written in the ML langauge.
    returns True if the code is syntactically correct.
    Throws a ParserError otherwise.
    """
    lex = lexer(source_file, token_file)
    t = None
    try:
        t = program(next(lex), lex)
    except StopIteration:
        raise ParserError("EOF reached when not expected")
    try:
        next(lex)
    except StopIteration:
        return True
    raise ParserError("Code after end statement")
