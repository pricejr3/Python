
import random


def isDNASeq(s):
    """Determine whether the string s is a legitimate DNA sequence
    (definied by having only A, C, G, and T characters)."""
    
    boolValue = True
    i = 0
    while i < len(s):
        id = s[i]
        if id != "A" and id != "C" and id != "G" and id != "T":
            boolValue = False
        i = i + 1    
        
    return boolValue

def randSeq(n):
    """Return a random DNA sequence of length n."""
    
    dnaStrings = "ATGC"
    returnString = ""
    
    i = 0
    while i < n:
        string = random.choice(dnaStrings) 
        returnString = returnString + string
        i = i + 1
    
    return returnString
    

def countBases(s):
    """Count the number of bases in O(n) time."""
    dictionary = {}
    aCount = s.count('A')
    cCount = s.count('C')
    gCount = s.count('G')
    tCount = s.count('T')
    dictionary.update({'A': aCount})
    dictionary.update({'C': cCount})
    dictionary.update({'G': gCount})
    dictionary.update({'T': tCount})
    
    return dictionary

def mean(S):
    """Return the mean value of a list of numbers"""
    
    return sum(S) / len(S)

def verifyRandSeq(n,T):
    """Perform a Monte Carlo simulation to determine whether 
    RandSeq is selecting bases in uniform manner"""
    
    fracA = 0.0
    fracC = 0.0
    fracG = 0.0
    fracT = 0.0
    
    i = 0
    while i < T:   
        
        tempString = randSeq(n)
        
        fracA = fracA + tempString.count('A')
        fracC = fracC + tempString.count('C')
        fracG = fracG + tempString.count('G')
        fracT = fracT + tempString.count('T')        
        
        i = i + 1
    

    divideMe = n * T
    list = [fracA/divideMe, fracC/divideMe, fracG/divideMe, fracT/divideMe]
    
    return list
        

