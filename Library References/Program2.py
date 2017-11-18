
# Opens up the data file for Step 3.
f = open('Step3Data.txt', 'r')

# Initializes a dictionary to store key and values.
dictionary = {}

# Used for the loop below.
count = 0


# Enumerate through each line in the file
# and do necessary steps.
for i, line in enumerate(f):


        # If on the "first line" for each entry
        # it will detemine if the print type is
        # a book, journal, or conference paper.
        # This is used 
        if i == count:
                items = line.split()
                printType = items[0]
                
    
        # If the printType is found to be a book:
        if printType == "Book":   
              
                # Acquire key and keyvalue.
                if i == count+1:
                        items = line.split()
                        key = items[0]
                        keyValue = items[1]
                        
                # Acquire author information.
                if i == count + 2:
                        nameInfo = line.split(' ', 1)[1]
                        nameInfo = line.split(' ', 1)[1]          
                        multipleAuthors = nameInfo.count(',')
                                          
                        # If there are not multiple authors
                        # split into one string.
                        if multipleAuthors == 0:
                                
                                # String holds first author's last name
                                # followed by a comma and then their first name
                                # followed by the rest of the authors.                                
                                firstAuthor = line.split(",", 1)[0]
                                a = ''.join(firstAuthor)
                                b = a.split(" ")
                                nameInfo = b[2] + ", " + b[1] 
                        
                        # If there are multiple authors
                        # split into a few strings.
                        if multipleAuthors > 0:
                                             
                                firstAuthor = line.split(",", 1)[0]
                                firstAuthor2 = firstAuthor.split("Author:", 1)[1]
                                # The rest of the authors are placed into this
                                # string.
                                restAuthors = line.split(firstAuthor2, 1)[1] 
                                
                                a = ''.join(firstAuthor2)
                                b = a.split(" ")                     
                                                   
                                # String holds first author's last name
                                # followed by a comma and then their first name
                                # followed by the rest of the authors.
                                nameInfo = b[2] + ", " + b[1]  + restAuthors                        
                   
                # Acquire title information.
                if i ==  count + 3:
                        titleInfo = line.split(' ', 1)[1]
                       
                 # Acquire publisher information.
                if i ==  count + 4:
                        pubInfo = line.split(' ', 1)[1]
                      
                #  Acquire date information.
                if i ==  count + 5:
                        dateInfo = line.split(' ', 1)[1]
                        
                        
                        # Creation of the string to hold the string value to be
                        # paired with the key
                        display = keyValue + "        " + nameInfo + ", " + titleInfo + ", " + pubInfo + ", " + dateInfo + "." 
                        display2 = display.replace("\n", "")
                        
                        # Add the string and the key to the dictionary.
                        dictionary.update({keyValue: display2})
                        
                        # Add 6 to the count because book entries
                        # have a length of 6 (this will take us to 
                        # the next print item).
                        count = count + 6
                        
                continue
        
        
        # If the printType is found to be a conference:
        if printType == "Conference":   
                   
                # Acquire key and keyvalue.
                if i == count+1:
                        items = line.split()
                        key = items[0]
                        keyValue = items[1]
                               
               # Acquire author information, the same
               # way as last time.
                if i == count + 2:
                        nameInfo = line.split(' ', 1)[1]
                        
                        # if there are commas, means more than 1 autho
                        multipleAuthors = nameInfo.count(',')
                        
                        if multipleAuthors == 0:
                                # String holds first author's last name
                                # followed by a comma and then their first name
                                # followed by the rest of the authors.                                
                                firstAuthor = line.split(",", 1)[0]
                                a = ''.join(firstAuthor)
                                b = a.split(" ")
                                nameInfo = b[2] + ", " + b[1] 
                               
                        if multipleAuthors > 0:
                                firstAuthor = line.split(",", 1)[0]
                                firstAuthor2 = firstAuthor.split("Author:", 1)[1]
                                restAuthors = line.split(firstAuthor2, 1)[1]
                                a = ''.join(firstAuthor2)
                                b = a.split(" ")
                                nameInfo = b[2] + ", " + b[1]  + restAuthors
                                
                # Acquire title information.    
                if i ==  count + 3:
                        titleInfo = line.split(' ', 1)[1]
                
                # Acquire conference information.
                if i ==  count + 4:
                        conferenceInfo = line.split(' ', 1)[1]
                          
                # Acquire date information. 
                if i ==  count + 5:
                        dateInfo = line.split(' ', 1)[1]
                        dateInfo = dateInfo.replace('.', '')
                      
                            
                # Acquire location information.  
                if i ==  count + 6:
                        locationInfo = line.split(' ', 1)[1]                
                             
                # Acquire page information.
                if i ==  count + 7:
                        pageInfo = line.split(' ', 1)[1] 
                        pageInfo = pageInfo.replace(' ', '')
                                                
                                         
                        
                        
                                  
                        # Properly format the string
                        display = keyValue + "       " + nameInfo + ", " + titleInfo + ", " + conferenceInfo + ", " + locationInfo + ", " + dateInfo + ", " + pageInfo + "."
                        display2 = display.replace("\n", "")
                        
                        # Place the string and keyValue into the dictionary.
                        dictionary.update({keyValue: display2})
                               
                               
                        # Add 8 to the count because conference entries
                        # have a length of 8 (this will take us to 
                        # the next print item).                                       
                        count = count + 8
                        continue   
                
                

        # If the printType is found to be a journal:
        if printType == "Journal":
                if i == count+1:
                        items = line.split()
                        key = items[0]
                        keyValue = items[1]
                              
                # Acquire author information, as before.
                if i == count + 2:
                        nameInfo = line.split(' ', 1)[1]
                        multipleAuthors = nameInfo.count(',')
                        
                        if multipleAuthors == 0:
                                # String holds first author's last name
                                # followed by a comma and then their first name
                                # followed by the rest of the authors.                                
                                firstAuthor = line.split(",", 1)[0]
                                a = ''.join(firstAuthor)
                                b = a.split(" ")
                                nameInfo = b[2] + ", " + b[1] 
                               
                        if multipleAuthors > 0:
                                firstAuthor = line.split(",", 1)[0]
                                firstAuthor2 = firstAuthor.split("Author:", 1)[1]
                                restAuthors = line.split(firstAuthor2, 1)[1]
                                a = ''.join(firstAuthor2)
                                b = a.split(" ")
                                nameInfo = b[2] + ", " + b[1]  + restAuthors
                                  
                # Acquire title information.
                if i ==  count + 3:
                        titleInfo = line.split(' ', 1)[1]
                                      
                # Acquire journal information.
                if i ==  count + 4:
                        journalInfo = line.split(' ', 1)[1]
                                       
                # Acquire publisher information.
                if i ==  count + 5:
                        pubInfo = line.split(' ', 1)[1] 
                     
                      
                                       
                # Acquire date information.
                if i ==  count + 6:
                        dateInfo = line.split(' ', 1)[1]  
                        dateInfo = dateInfo.replace(' ', '')
                                       
                # Acquire volume information.
                if i ==  count + 7:
                        volumeInfo = line.split(' ', 1)[1]             
                                     
                # Acquire number information.
                if i ==  count + 8:
                        numberInfo = line.split(' ', 1)[1]
                        
               
                        # Format the string to place in dictionary.
                        display = keyValue + "       " + nameInfo + ", " + titleInfo + ", " + journalInfo + ", " + pubInfo + ":" + volumeInfo + "(" + numberInfo + ")" + ", " + dateInfo + "."
                        display2 = display.replace("\n", "")
                        
                        # Add the keyvalue and the string to the dictionary.
                        dictionary.update({keyValue: display2})
                                       
                        # Add 9 to count since journal 
                        # entries have a length of 9 lines.
                        count = count + 9
                        continue                
                
     
            
# Ask user for values to test:
while True:
        print ("Please enter a key:")
        keyValue = input()
        print(dictionary[keyValue])