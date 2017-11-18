import sys
import argparse
from MLparser import *

class SemanticError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

def compiler(source = "test0.txt", tokens = "tokens.txt", output = "out.asm"):
    t, syms = parser(source, tokens)
    compile_c(t, syms, output).compile()

class compile_c():
    def __init__(self, t, syms, output):
        self.t = t
        self.dic = syms
        self.output = output
        self.index = 0
    def compile(self):
        text = ""
        data = ""
        #try:
        data = self.generate_data_segment()
        text = self.program(self.t)
        #except ParserError:
        f = open(self.output, "w")
        f.write("\n".join(["\n".join(data), "\n".join(text)]))
        f.close()    

    def generate_data_segment(self):
        statements = [".data"]
        statements += ["_boolt: .asciiz \"True\"", "_boolf: .asciiz \"False\""]
        for k in self.dic:
            if k == "_strings":
                for cs in self.dic[k]: #list of all strings that it will be assigned
                    statements.append("_" + str(self.index) + ": .asciiz " + cs)
                    self.index += 1
            else:
                statements.append(k + ": .word 0") #initialize one word (4 bytes) to 0
        return statements
    
    def program(self, t):
        s = [".text"] #first child is begin
        s += self.statement_list(t.children[1]) #second child is whole program
        s += ["li $v0, 10", "syscall"] #third child is end
        return s

    def statement_list(self, t):
        s = []
        for child in t.children:
            s += self.statement(child) #1 or more children, all statements
        return s

    def statement(self, t):
        if t.children[0].label == "ASSIGNMENT":
            return self.assign(t.children[0]) #statement only has one child, assign, read or write
        elif t.children[0].label == "DECLARATION":
            self.dic[t.children[0].children[0].label.pattern]["declared"] = True
            return []
        elif t.children[0].label == "WRITE": #TODO handle string and bool
            s = []
            for child in t.children[1].children: #rest of the children are expressions to be printed
                r, ty = self.expression(child)
                s += r
                if ty == "int":
                    s += ["move $a0, $v0", "li $v0, 1", "syscall"] #first syscall prints int, second prints newline as character
                elif ty == "bool":
                    s += ["beqz $v0, _" + str(self.index), "la $a0, _boolt", "b _" + str(self.index + 1)] #jump to false if false
                    s += ["_" + str(self.index) + ":", "la $a0, _boolf"] #load false
                    s += ["_" + str(self.index + 1) + ":", "li $v0, 4", "syscall"] #print
                    self.index += 2
                elif ty == "string": #treat $v0 as address of string
                    s += ["move $a0, $v0", "li $v0, 4", "syscall"]
                s += ["li $a0, 10", "li $v0, 11", "syscall"] #newline printing        
            return s
        elif t.children[0].label == "READ":
            s = []
            for child in t.children[1].children: #rest of the children are ids to be read
                if self.dic[child.label.pattern]["type"] != "int":
                    raise SemanticError("Semantic error, trying to read non int type")
                s += ["li $v0, 5", "syscall", "sw $v0, " + child.label.pattern]
                self.dic[child.label.pattern] = { "init": True, "type": "int" } #can only read int
            return s
        else:
            raise SemanticError("Semantic error, " + str(t.children[0].label) + " not defined")

    def assign(self, t):
        s, ty = self.expression(t.children[1]) #evaluate right side of assignment first, stored in $v0 (return value)
        s += ["sw $v0, " + t.children[0].label.pattern] #this gets the variable address in $t0
        vname = t.children[0].label.pattern
        if self.dic[vname]["type"] != ty:
            raise SemanticError("type mismatch in assignment")
        self.dic[vname] = { "type": ty, "init": True }
        return s

    def expression(self, t): #needs to return a type
        s = []
        ty = ""
        if isinstance(t.label, Token) or t.label in {'NOT', 'UNARY'}:
            s, ty = self.primary(t)
            return s, ty
        else:
            s1, ty1 = self.expression(t.children[0]) #will return in $v0
            s += s1
            s += ["addi $sp, $sp, -4", "sw $v0, 0($sp)"]  
            s2, ty2 = self.expression(t.children[1]) #will return in $v0
            s += s2
            s += ["lw $t0, 0($sp)", "addi $sp, $sp, 4"]
            if t.label == "EQUAL":
                self.raise_exception(ty1, "int")
                self.raise_exception(ty2, "int")
                s += ["seq $v0, $t0, $v0"]
                return s, "bool"
            elif t.label == "NOTEQUAL":
                self.raise_exception(ty1, "int")
                self.raise_exception(ty2, "int")
                s += ["sne $v0, $t0, $v0"]
                return s, "bool"
            elif t.label == "LESSTHAN":
                self.raise_exception(ty1, "int")
                self.raise_exception(ty2, "int")
                s += ["slt $v0, $t0, $v0"]
                return s, "bool"
            elif t.label == "LESSTHANEQUAL":
                self.raise_exception(ty1, "int")
                self.raise_exception(ty2, "int")
                s += ["sle $v0, $t0, $v0"]
                return s, "bool"
            elif t.label == "GREATERTHAN":
                self.raise_exception(ty1, "int")
                self.raise_exception(ty2, "int")
                s += ["sgt $v0, $t0, $v0"]
                return s, "bool"
            elif t.label == "GREATERTHANEQUAL":
                self.raise_exception(ty1, "int")
                self.raise_exception(ty2, "int")
                s += ["sge $v0, $t0, $v0"]
                return s, "bool"
            elif t.label == "PLUS":
                self.raise_exception(ty1, "int")
                self.raise_exception(ty2, "int") #then make sure whatever primary returns is an int
                s += ["add $v0, $t0, $v0"]
                return s, "int"
            elif t.label == "MINUS":
                self.raise_exception(ty1, "int")
                self.raise_exception(ty2, "int") #then make sure whatever primary returns is an int
                s += ["sub $v0, $t0, $v0"]
                return s, "int"
            elif t.label == "MULTIPLY":
                self.raise_exception(ty1, "int")
                self.raise_exception(ty2, "int") #then make sure whatever primary returns is an int
                s += ["mult $t0, $v0", "mflo $v0"]
                return s, "int"
            elif t.label == "DIVIDE":
                self.raise_exception(ty1, "int")
                self.raise_exception(ty2, "int") #then make sure whatever primary returns is an int
                s += ["div $t0, $v0", "mflo $v0"]
                return s, "int"
            elif t.label == "MOD":
                self.raise_exception(ty1, "int")
                self.raise_exception(ty2, "int") #then make sure whatever primary returns is an int
                s += ["rem $v0, $t0, $v0"]
                return s, "int"
            elif t.label == "OR":
                self.raise_exception(ty1, "bool")
                self.raise_exception(ty2, "bool")
                s += ["or $v0, $t0, $v0"] #we know $t0 is preserved, compare it against primary in $v0
                return s, "bool"
            elif t.label == "AND":
                self.raise_exception(ty1, "bool")
                self.raise_exception(ty2, "bool")
                s += ["and $v0, $t0, $v0"] #we know $t0 is preserved, compare it against primary in $v0
                return s, "bool"
            else:
                raise SemanticError("Semantic error unknown: \"" + str(item.name) + "\"")
    
    def primary(self, t):
        if t.label == "INTLIT": #int
            s = ["li $v0, " + str(t.label.pattern)]
            return s, "int"
        elif t.label == "STRINGLIT":
            return ["la $v0, _" + str(self.dic["_strings"].index(t.label.pattern))], "string"
        elif t.label == "BOOLT":
            s = ["li $v0, 1"]
            return s, "bool"
        elif t.label == "BOOLF":
            s = ["li $v0, 0"]
            return s, "bool"
        elif t.label == "EXPRESSION": #paranthesis
            s, ty = self.expression(t.children[0])
            return s, ty
        elif t.label == "ID":
            s = ["lw $v0, " + str(t.label.pattern)]
            return s, self.dic[t.label.pattern]["type"]
        elif t.label == "UNARY":
            s, ty = self.primary(t.children[0])
            s += ["sub $v0, $0, $v0"]
            return s, ty
        elif t.label == "NOT":
            s, ty = self.primary(t.children[0])
            s += ["xor $v0, 1"]
            return s, ty
        else:
            raise SemanticError("Semantic error, " + t.label + " not defined")

    def raise_exception(self, expected, ty):
        if isinstance(expected, tree):
            if len(expected.children) != ty:
                raise SemanticError("non arithmetic expressions after RELOP at: \"" + str(length) + "\"")
        if ty != expected:
            raise SemanticError("semantic error, expect type \"" + expected + "\" but got \"" + ty + "\"")
        
if __name__ == "__main__":  # Only true if program invoked from the command line

    # Use the argparse library to parse the commandline arguments
    arg_parser = argparse.ArgumentParser(description = "Group5 micro-language compiler")
    arg_parser.add_argument('-t', type = str, dest = 'token_file', help = "Token file", default = 'tokens.txt')
    arg_parser.add_argument('source_file', type = str, help = "Source-code file", default = 'test.1.1.ml')
    arg_parser.add_argument('output_file', type = str, help = 'output file name')

    args = arg_parser.parse_args()

    # Call the compiler function
    compiler(args.source_file, args.token_file, args.output_file)
