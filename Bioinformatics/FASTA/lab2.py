
def checkTest(data_file):
    
    f = open(data_file, 'r')
    i = 0
    for i, line in enumerate(f):
        if i == 0:
            pregnantSubjects = line.split()
            pregnantSet = set(pregnantSubjects)
            i = i + 1
        if i == 1:
            nonPregnantSubjects = line.split()  
            nonPregnantSet = set(nonPregnantSubjects)
            i = i + 1    
        if i == 2:
            testingPositive = line.split()
            testingSet  = set(testingPositive )
        
    truePositives = len(pregnantSet.intersection(testingSet))
    falsePositives = len(nonPregnantSet.intersection(testingSet))
    trueNegatives = len(nonPregnantSet.difference(testingSet))
    falseNegatives = len(pregnantSet.difference(testingSet))
    sensitivity =  (truePositives / float(len(pregnantSet)))
    specificity =  (trueNegatives / float(len(nonPregnantSet)))

    listReturn = (truePositives, falsePositives, trueNegatives, falseNegatives, sensitivity, specificity)
    
    return listReturn
    
   
def readInFasta(input_fasta, output_fasta, col_width):
    
    idList = []
    restList = []    
    i = 0
    with open(input_fasta) as f:
        for line in f:
    
            if line.startswith('>'):
                me = ''.join(line)
                me = me.replace('\n','')
                idList.append(me)
               
                restList.append("5555")
                
            else:
                me2 = ''.join(line)
                me2 = me2.replace('\n','')
                restList.append(me2)
                
    

    count = 0
    sizeRestList = len(restList)
    
    while(count < sizeRestList):
        
        if(len(restList[count]) == 0):
            restList[count] = "\n"
        
        count = count + 1
        
            
    informationLine = idList
    restOfLines = restList
    stringMe = ''.join(restOfLines)
    finalList = stringMe.split("5555")
    finalList.pop(0)
    
    
    

 
    #writeFasta(informationLine, output_fasta, finalList, col_width)
    return(informationLine, finalList)
    

         
                
                
def writeFasta(informationLine, output_fasta, finalList, col_width):
    
    fileName = output_fasta
    f = open(fileName,'w')

    informationLine2 = ' '.join(informationLine)
    informationLine2 = informationLine2.split(">")
    informationLine2.remove('')
    iterator = len(informationLine2)
    count = 0
    count2 = 0
    
    while(count < iterator):
    
        line = ''.join(informationLine2[count])
        f.write(">")
        f.write(line);
        f.write("\n")        
        
        line = ''
        line = ''.join(finalList)
        lineChunked2 = []
        lineChunked2 = [line[i:i+col_width] for i in range(0, len(line), col_width)]   
        sizeFinalLine = len(lineChunked2)        
        
        while(count2 < sizeFinalLine):
            f.write(lineChunked2[count2])
            f.write("\n")
            count2 = count2 + 1      
        count2 = 0        
              
            
        count = count + 1
    
        
def reformatFasta(input_fasta,output_fasta,col_width=80):
      
    list1 = []
    list2 = []
    list1, list2 = readInFasta(input_fasta, output_fasta, col_width)

    writeFasta(list1, output_fasta, list2, col_width)
 

      
def spliceGenes(input_file,output_file,col_width=80):
    
    list1 = []
    list2 = []
    list3 = []
    list1, list2 = readInFasta(input_file, output_file, col_width)  
    
    
    stringList2 = ''.join(list2)
    stringSplitme = stringList2
    charsSEQ = list(stringSplitme)



    stringMe = ''.join(list1)
    stringMe2 = stringMe.split()
    stringMe2size = len(stringMe2)

    
    intRepresentation = []
    stringList = []

    
    for val in stringMe2:
        if val.isdigit() == False:
            stringList.append(val)
            
    stringhead = ''
    stringhead = stringList.pop(0)
    for val in stringList:
        stringhead = stringhead + " " + val
    
            
    for val in stringMe2:
        if val.isdigit():
            intRepresentation.append(int(val))
            

    index = 0
    for item in intRepresentation:
        if index % 2 != 0:
            intRepresentation[index] = intRepresentation[index] - 1
        index = index + 1
        
        
        

    index = 0
    valueToUse = 0
    sizeToRun = len(intRepresentation)
    sizeToRun = sizeToRun / 2
    i = 0
    counter = 0
    
    while(counter < sizeToRun):
        
        me = intRepresentation[i]
        me2 = intRepresentation[i+1]
        
        while(me <= me2):
            list3.append(charsSEQ[me])
            me = me + 1
            
        counter = counter + 1
        i = i + 2
        
        
        
    stringReturner = ''.join(list3)
    

    
    infLine = []
    resterLine = []
    infLine = stringReturner.split()
    resterLine = stringhead.split()
   
 
    writeFasta(resterLine, output_file, infLine, col_width)
 
 
   
            
 
    

       
    
    
  
    
    
    
    
   
