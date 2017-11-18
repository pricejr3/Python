# NOTE: 'N' represents the ambiguous base -- one whose content has not been 
# determined.  For purposes of compelmentation, the complement of 'N' is 'N'.
BASES = {'A', 'C', 'G', 'T', 'N', 'a', 'c', 'g', 't', 'n'}

# A dictionary computating base complements.  (e.g. COMPLMENT['A'] is 'T'.)
COMPLEMENT = {x:y for x,y in zip(['A', 'C', 'G', 'T', 'N', 'a', 'c', 'g', 't', 'n'],
                                 ['T', 'G', 'C', 'A', 'N', 't', 'g', 'c', 'a', 'N'])}


# An exception class to be thrown by your dnaSeq class.
class DNAError(Exception):
    def __init__(self, value = "Bad DNA string"):
        self.value = value

    def __str__(self):
        return str(self.value)


class dnaSeq:
    """Mutable DNA Sequence class."""

    # 1) Implement the constructor.  Should take one argument (other than self) and throw a ValueError if
    #    the value is not a string), or a DNAError (above) if the value is a string but contains bad 
    #    bases characters.  (That is, characters that are not in the BASES set.)  Otherwise, store the string
    #    is an attribute in whatever for you see fit.
    #    COMMENT: Since this is intended to be a mutable class, yo might want to consider holding
    #    the information in a mutable data strcture -- as opposed to one that you have to copy
    #    every time you want to change the object.
    def __init__(self, s):
        
        compare = isinstance(s, str)
        listCompare = set(s)
        isSubset = listCompare.issubset(BASES)
     
        if(compare == False):
            raise ValueError("Input is not a String")
        if(isSubset == False):
            raise DNAError("NOT DNA!!")
        
        self.list = []
        self.list.append(s)

    #---------------------------------
    # 2) Implement the __len__ function so that len(o) will return the length of sequence object o.
    def __len__(self):
        stringMe = ''.join(self.list)
        return len(stringMe)
        
        
    #---------------------------------
    # 3) Implement the __str__ function so that str(o) will return the the sequence as a string object.
    def __str__(self):
        stringMe = ''.join(self.list)
        return stringMe        
        

    def __repr__(self):
        stringMe = ''.join(self.list)
        return stringMe        
    
    #---------------------------------
    # 5) Implement the __getitem__ function so that we can use the index the operator on a dnaSeq -- 
    #    both single indexing and splicing.  An index should return a single-character string, 
    #    while a slice should return a dnaSeq object.
    #    NOTE: The Python specifications for __getitem__ require that:
    #          1) An illegal index type result in a TypeError being raised.
    #          2) An invalid index value results in a KeyError being raised.
    #    You may assume this for any other object, and implement this for dnaSeq.
    #    There are two legal index types: int and slice.  (The later being the class of the
    #    object __getitem__ gets for a call such as o[5:7].
    def __getitem__(self, i):
            string = ''.join(self.list)
            lister = []
            lister = string
            length = len(string)
            
            stringVal = str(i)
            stringVal = stringVal.replace("slice", "");
            stringVal = stringVal.replace("(", "");
            stringVal = stringVal.replace(")", "");
            stringVal = stringVal.replace("None", "");
            stringVal = stringVal.replace(",", "");
            listnew = stringVal.split()
            listLength = len(listnew)        
    
        
            
            
            if(isinstance(i, int)):
                if(i > length or i < 0):
                    raise TypeError("Index out of bounds")
                stringMe = string[i]
                return stringMe    
            
            if(isinstance(i, slice) and listLength == 2):
                         
        
                stringVal = str(i)
                stringVal = stringVal.replace("slice", "");
                stringVal = stringVal.replace("(", "");
                stringVal = stringVal.replace(")", "");
                stringVal = stringVal.replace("None", "");
                stringVal = stringVal.replace(",", "");
                listnew = stringVal.split()
                listLength = len(listnew)
                val1 = int(listnew[0])
                val2 = int(listnew[1])
            
        
                
                stringMe = string[val1:val2]
                return dnaSeq(stringMe)  
            
            if(isinstance(i, slice) and listLength == 3):
                stringVal = str(i)
                stringVal = stringVal.replace("slice", "");
                stringVal = stringVal.replace("(", "");
                stringVal = stringVal.replace(")", "");
                stringVal = stringVal.replace("None", "");
                stringVal = stringVal.replace(",", "");
                listnew = stringVal.split()
                listLength = len(listnew)
                val1 = int(listnew[0])
                val2 = int(listnew[1])
                val3 = int(listnew[2])
        
                
                stringMe = string[val1:val2:val3]
                return dnaSeq(stringMe)       
        
       
        
        

    #---------------------------------
    # 6) Implement the __setitem__ function so we can use index-assignment (e.g. o[5] = 'A' or O[5:7] = 'AC').
    #    Should throw the same sorts of errors as __getitem__.  Additionally, it should throw a ValueError
    #    if the value is not either a dnaSeq object or a string.
    #    (If value is a string, throw a DNAErro if it contains any non-base characters.)
    def __setitem__(self, i, value):
        string = ''.join(self.list)
        listMe = list(string)
        stringVal = str(i)
        stringVal = stringVal.replace("slice", "");
        stringVal = stringVal.replace("(", "");
        stringVal = stringVal.replace(")", "");
        stringVal = stringVal.replace("None", "");
        stringVal = stringVal.replace(",", "");
        listnew = stringVal.split()
        listLength = len(listnew)         
    
        if(isinstance(i, int)):
            listMe[i] = value
            string2 = ''.join(listMe)
            self.list = listMe
            
        if(isinstance(i, dnaSeq)):
            listMe[i] = value
            string2 = ''.join(listMe)
            self.list = listMe   
            
        if(isinstance(i, slice) and listLength == 2):
                     
    
            stringVal = str(i)
            stringVal = stringVal.replace("slice", "");
            stringVal = stringVal.replace("(", "");
            stringVal = stringVal.replace(")", "");
            stringVal = stringVal.replace("None", "");
            stringVal = stringVal.replace(",", "");
            listnew = stringVal.split()
            listLength = len(listnew)
            val1 = int(listnew[0])
            val2 = int(listnew[1])
    
            listMe[i] = value
            string2 = ''.join(listMe)

            self.list[i] = listMe       
            
           
     
 
    #---------------------------------
    # 7) Impelement the __add__ function to enable + to concatenate sequences.
    #    Throw a ValueError if object other is not of class dnaSeq
    #    Make sure it produces a deep copy.
    def __add__(self, other):
        
        compare = isinstance(other, dnaSeq)
                     
        if(compare == False):
            raise ValueError("Not of class dnaSeq")
                
        stringOne = ''.join(self.list)
        stringTwo = ''.join(other.list)
        stringConcat = stringOne + stringTwo
                
        return dnaSeq(stringConcat)
        

    #---------------------------------
    # 8) Implement the necessary method for the "in" operator to to allow operations such as:
    #     s in o (where s is a string or dnaSeq, o is a dnaSeq, and this returns true if either
    #     o contains s as a subsequence.
    #     Raise a ValueError if the query sequence is neither a string nor a dnaSeq.
    def __contains__(self, query):
        compare = isinstance(query, str)
        compare2 = isinstance(query, dnaSeq)
                   
        if(compare == False and compare2 == False):
            raise ValueError("Not a string, nor a dnaSeq")        
        o = ''.join(self.list)
        seto = set(o)
        
        
        s = str(query)
        sets = set(s)
       
        
        if(sets.issubset(seto)):
            return True
        return False


    #---------------------------------
    # 9) Make the class iterable -- allowing it to be used by for statements and comprehenstions.
    #     e.g. Once this is implemented, this should work: [print(i) for i in o], where o is a dnaSeq
    #     object.  
    #     See project specifications for instructions on how to do this. 
    def __iter__(self):
        pass


    
    #---------------------------------------------------------
    # Object methods: Mutators
    
    #---------------------------------
    # 11) In-place complement the sequence.  (No return value.)
    def complement(self):
        stringMe = ''.join(self.list)
        complementedString = ''
        for values in stringMe:
            complementedString = complementedString + COMPLEMENT[values]
        self.list.remove(stringMe)
        self.list.append(complementedString)

    #---------------------------------
    # 12) method reverse(self): Reverse the order of the sequence in-place.
    def reverse(self):
        stringMe = ''.join(self.list)
        reversed = stringMe[::-1]
        self.list.remove(stringMe)
        self.list.append(reversed)

    #---------------------------------
    # 13) method reverse_complement(self): Reverse-complements the sequence in-place.  
    def reverse_complement(self):
        self.reverse()
        self.complement()
        



