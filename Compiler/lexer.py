
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
        return str(self.name)

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
        if other.__class__ == type(""):
            return self.name == other
        return self.t_class == other.t_class and self.name == other.name and \
               self.pattern == other.pattern and self.line == other.line and \
               self.line_num == other.line_num and self.col == other.col


def lexer(source_file, token_file = "tokens.txt"):
    """
    Input:
    * source_file: file containing the content to be tokenized
    * token_file: token file (see assignment specifications for format)
    Output:
    * A generator that will iteratively return token objects corresponding to the tokens
      of source_file, throwing a LexerError if it hits a bad token.
    """
    # move this outside of the other file open so that this file can be closed while the other is open
    # Read in token defs and store them in 2d list.
    # Each token definition contains its CLASS, NAME, and REGEX, defined at the top of the file.
    with open(token_file) as tFile:
        tokenDefs = []
        for line in tFile:
            tokenDef = []
            for word in line.split():
                tokenDef.append(word)
            tokenDefs.append(tokenDef)

    # Read in source code.
    # sourceCodeLines = sFile.readlines() would be bad, since it reads in entire file without
    # verifying file length (then large files crash program)
    with open(source_file) as sFile:
        lineNum = 0
        for line in sFile:
            lineNum += 1

            # create a copy of line so that the correct column can be found after lineCopy is modified
            # Whitespace on the left is irrelevant
            lineCopy = line.lstrip()

            # Token wants the original line with no whitespace on the right.
            # Created variable so .rstrip() doesn't have to be called every time we create a Token
            rStrippedLine = line.rstrip()

            # Create variable so we can make fewer function calls
            lineLength = len(line)

            # This while loop goes through each possible token and tries to find a match.
            # If one is found, a Token is created, lineCopy is edited, and i is set to 0.
            # i gets set to zero so that the first token def is used in the next search.
            # lineCopy is edited so that the first char that hasn't been matched yet is at the start of the string.
            # If lineCopy is empty or the first character is '#', we are finished with this line.
            # We know that we won't have any spaces before a comment because we keep stripping on the left.
            i = 0
            while lineCopy != "" and lineCopy[0] != "#":
                column = lineLength - len(lineCopy)
                definition = tokenDefs[i]
                result = re.search("^" + definition[REGEX], lineCopy)
                if result:
                    token = Token(definition[CLASS], definition[NAME], result.group(1), rStrippedLine, lineNum, column)

                    # delete what re.search found and strip whitespace, shortening string to search,
                    # only the first occurance (third parameter)
                    lineCopy = lineCopy.replace(result.group(1), "", 1).lstrip()
                    yield token
                    i = 0
                else:
                    i += 1
                    # If we've made it here and we've run out of tokens to try, there is a problem.
                    # Also, note that we will never be here when lineCopy is empty or starts with a #.
                    if i >= len(tokenDefs):
                        raise LexerError("bad token line# " + str(lineNum) + " column " + str(column) + " line \"" + lineCopy.strip() + "\"" )
