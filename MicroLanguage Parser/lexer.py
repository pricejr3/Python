
import re

# Constants
CLASS = 0
NAME = 1
REGEX = 2


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

    with open(token_file) as tFile:
        tokenDefs = []
        for line in tFile:
            tokenDef = []
            for word in line.split():
                tokenDef.append(word)
            tokenDefs.append(tokenDef)


    with open(source_file) as sFile:
        lineNum = 0
        for line in sFile:
            lineNum += 1

  
            lineCopy = line.lstrip()

            rStrippedLine = line.rstrip()

            lineLength = len(line)

            i = 0
            while lineCopy != "" and lineCopy[0] != "#":
                column = lineLength - len(lineCopy)
                definition = tokenDefs[i]
                result = re.search("^" + definition[REGEX], lineCopy)
                if result:
                    token = Token(definition[CLASS], definition[NAME], result.group(1), rStrippedLine, lineNum, column)


                    lineCopy = lineCopy.replace(result.group(1), "", 1).lstrip()
                    yield token
                    i = 0
                else:
                    i += 1
             
                    if i >= len(tokenDefs):
                        raise LexerError("bad token line " + str(lineNum) + " column " + str(column))
