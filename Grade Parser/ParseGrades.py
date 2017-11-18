

# Read in the file: studentGrades.txt.
readFile = open('studentGrades.txt', 'r')

# Hardcoded values for the respective weights.
quizWeight = 0.20
homeworkWeight = 0.30
examWeight = 0.50

# Initialize values that are used in calculations
finalAverage = 0
wholeGrade = "To Fill In"

# Initialize the list which is used to 
# hold the final values.
list = []


# Read in each piece, one-by-one, from the 
# file that was read in and place them in
# temporary lists.
for line in readFile:

    # Read piece by piece by splitting in each line.
    pieces = line.split()
    
    # Store each split value into its 
    # own respective list element.
    name = pieces[0]
    quiz1 = float(pieces[1])
    quiz2 = float(pieces[2])
    quiz3 = float(pieces[3])
    homework1 = float(pieces[4])
    homework2 = float(pieces[5])
    homework3 = float(pieces[6])
    homework4 = float(pieces[7])
    homework5 = float(pieces[8])
    exam1 = float(pieces[9])
    exam2 = float(pieces[10])
    
    
    # Calculation of the weighted scores for
    # Quizzes, Tests and Homeworks.
    weightedQuizScore = (quiz1 + quiz2 + quiz3) / 3.0
    weightedQuizScore = weightedQuizScore * quizWeight
    weightedHomeworkScore = (homework1 + homework2 + homework3 + homework4 + homework5) / 5.0
    weightedHomeworkScore = weightedHomeworkScore * homeworkWeight
    weightedExamScore = (exam1 + exam2) / 2.0
    weightedExamScore = weightedExamScore * examWeight
    
    # Final average is found by adding all the weighted scores.
    finalAverage = weightedExamScore + weightedHomeworkScore + weightedQuizScore
    
    # Check to see what the whole letter grade will be
    # by comparing the average to standard scores.
    if finalAverage >= 90.0:
        wholeGrade = "A"
    elif finalAverage >= 80.0 and finalAverage < 90.0:
        wholeGrade = "B"
    elif finalAverage >= 70.0 and finalAverage < 80.0:
        wholeGrade = "C"    
    elif finalAverage >= 60.0 and finalAverage < 70.0:
        wholeGrade = "D"    
    elif finalAverage < 60.0:
        wholeGrade = "F"    
       
  
    # Adds each Name, finalAverage and wholeGrade to the list below:
    
    # Right justifies the name in a field of 20 characters.
    list.append(name.rjust(20, ' '))
    
    # Formats the finalAverage by only allowing one decimal place.
    list.append("%.1f" % finalAverage)
    list.append(wholeGrade)
    list.append("\t")
   

# Variables used in greeting below.   
x = 0
greeting = "studentOutputFile.txt"
space = " "


# Writing to the file below by opening
# a new textFile.
writeFile = open('studentOutputFile.txt','w')

# Write the greeting, and three spaces (for better text format).
writeFile.write("%s\n " % greeting)
writeFile.write("%s\n " % space)
writeFile.write("%s\n " % space)
writeFile.write("%s\n " % space)


# Iterate through each item in list and write it to the file.
for item in list:
    
    # Write the item.
    writeFile.write("%s " % item)
    x+=1
    
    # If x is equal to 4, then we tab.
    if x == 4:
        writeFile.write("%s\n " % item)
        
        # Set x to 0 again, until it is time to tab again.
        x = 0
            
# Close the file.
writeFile.close()

    