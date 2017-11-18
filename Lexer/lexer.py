import re
import sys


class LexerError(Exception):
    """
    Exception to be thrown when the lexer encounters a bad token.
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg)


class Token:
    """
    A class for storing token information.
    The variable instances for a token object are:
    * t_class: The token class.
    * name: The name of the token.
    * pattern: The specific pattern of the token
    * line: The line containing the token
    * line_num: The line number (numbered from 1)
    * col: The column number (numbered from 0)
    """

    def __init__(self, t_class, name, pattern, line, line_num, col):
        """
        Constructor
        """
        self.t_class = t_class
        self.name = name
        self.pattern = pattern
        self.line = line
        self.line_num = int(line_num)
        self.col = int(col)

    def __str__(self):
        """
        Defines behavior of the str function on the Token class.
        Prints as a tupple all information except self.line.
        """
        return str((self.t_class, self.name, self.pattern, self.line_num, self.col))

    def __repr__(self):
        """
        Defines the behaviour of the repr() function
        on the Token class.
        """
        return "Token: " + str(self)

    def __eq__(self, other):
        """
        Defines behaviour of the == operator on the Token class
        """
        return self.t_class == other.t_class and self.name == other.name and \
               self.pattern == other.pattern and self.line == other.line and \
               self.line_num == other.line_num and self.col == other.col


def lexer(source_file, token_file):
    """
    Input:
    * source_file: file containing the content to be tokenized
    * token_file: token file (see assignment specifications for format)
    Output:
    * A generator that will iteratively return token objects corresponding to the tokens
      of source_file, throwing a LexerError if it hits a bad token.
    """
	
    token_reader = open(token_file)
    tokens = []

    for line in token_reader:
        parts = line.split()
        token_def = [parts[0], parts[1], parts[2]]
        tokens.append(token_def)
  
    line_num = 1
    col_num = 0
    source_scanner = open(source_file)
    for line in source_scanner:
        col_num = 0
        line = line.rstrip()
        lineToEdit = line
     
	 
        while len(lineToEdit.strip()) > 0:
            if lineToEdit.find("#"):
                lineToEdit = lineToEdit.split("#")[0]
            found_match = False
            for token in tokens:
                # try to match tokens
                if re.match(token[2], lineToEdit.lstrip()):
                    match_obj = re.search(token[2], lineToEdit)
                    yield Token(token[0], token[1], match_obj.group(1).rstrip(), line, line_num,
                                col_num + match_obj.start(1))
                    lineToEdit = lineToEdit[match_obj.end(1):]
                    col_num += match_obj.end(1)
                    found_match = True
                    break
            if not found_match:
                while re.match("\s", lineToEdit):
                    lineToEdit = lineToEdit[1:]
                    col_num += 1
                msg = "Bad token (line " + str(line_num) + ", column " + str(col_num) + "): " + lineToEdit
                raise LexerError(msg)
        line_num += 1
