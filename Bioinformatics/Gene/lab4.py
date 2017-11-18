import sys
sys.path.append("../lib/")
from dnaSeq import dnaSeq


def extractGenes(gtf_file, fa_file, output):
   
    
    holdingValues = {}
    keyList = []
    S = []
    keyMapperDict = {}
    holder = []
    
    
    with open(gtf_file) as gtffile:
         
        for line in gtffile:
            
            pieces = line.split()
            typeHeader = pieces[11]
            typeHeader = typeHeader[1:]
            typeHeader = typeHeader[:-2]
            keyList.append(typeHeader)
            holder =  keyMapperDict.get(typeHeader, [])
            holder.append(pieces[4])
            holder.append(pieces[3])
            holdingValues[typeHeader] = holder
            keyMapperDict [typeHeader] = holder    

    with open(fa_file) as fp:
        info = fp.readline().rstrip()
        seq = ""
        while True:
            line = fp.readline()
            if not line or line[0] == ">":
                s = dnaSeq(seq)
                s.info = info
                S.append(s)
                if not line:
                    break
                info = line.rstrip()
                seq = ""
            else:
                seq += line.rstrip()
                
   
            
    ############################
    # Turn the keys into a list.
    oneKeyList = list(set(keyList))  

    
    # The number of times to iterate through the list
    iterateList = len(oneKeyList)


        

  
    with open(output, "w") as writeFA:
        

        for x in range(0, iterateList):
            
            # Map out a new list that holds them as ints, not strings
            integerList = list(map(int,holdingValues[(oneKeyList[x])]))
            integerListSorted = sorted(integerList)
            
    
            # Get the lowest and highest values to see which sequence to place.
            lowerValue =  integerListSorted[0]
            higherValue =  integerListSorted[-1]
            

            # The value to subtract them by.
            subtractBy = lowerValue
            subtractBy = lowerValue
     
    
            # The new list.
            newList = [x - subtractBy for x in integerList]
            newList = sorted(newList)
          
            
             # Counter for the iteration beow
            lengthIteration2 = len(newList)
            
            
            writeFA.write( ">" + str(oneKeyList[x]))
            writeFA.write(" ")
            
            P = 0
            
            while P < lengthIteration2:
                
                if (P % 2 == 0 and P+1 != lengthIteration2):
                    writeFA.write(str(newList[P]))
                    writeFA.write(" ")                    
                if (P % 2 == 1 and P+1 != lengthIteration2):
                    writeFA.write(str(newList[P]+1))
                    writeFA.write(" ")     
                if (P % 2 == 0  and P+1 == lengthIteration2):
                    writeFA.write(str(newList[P]))            
                if (P % 2 == 1 and P+1 == lengthIteration2):
                    writeFA.write(str(newList[P]+1))
                                
                # Increment the counter
                P = P + 1
                
            
            writeFA.write('\n')
        
        
            # Actually make the new sequence.
            newSeq = seq[lowerValue-1:higherValue]
        
            # Actually write the new sequence.
            #writeFA.write(newSeq)
            
            count2 = 0
            col_width = 60
            line = ''.join(newSeq)
            n = col_width
            lineChunked2 = [line[i:i+n] for i in range(0, len(line), n)]            
        
            sizeFinalLine = len(lineChunked2)        
            
            while(count2 < sizeFinalLine):
                writeFA.write(lineChunked2[count2])
                writeFA.write("\n")
                count2 = count2 + 1      
                      


