import sys
import re
import operator

global citiesList
global zipsList
global statesList

citiesList = []

global zipCodeList
zipCodeList = []

global upperCitiesList
upperCitiesList = []


global commonCityNames 
commonCityNames = []

global latitude
latitude = []

global citySt
citySt = dict()

global commonCityNamesDict
commonCityNamesDict = dict()


def read_text_file(fileName):
	global citiesList
	global zipsList
	global statesList

	with open (fileName) as file_txt:
	
		if fileName == 'cities.txt':
			citiesList = file_txt.read().splitlines()
		if fileName == 'zips.txt':
			zipsList = file_txt.read().splitlines()
		if fileName == 'states.txt':
			statesList = file_txt.read().splitlines()



def CommonCityNames():

	read_text_file('states.txt')
	readFile = open('zipcodes.txt', 'r')

	for line in readFile:
		pieces = line.split('\t')

		#commonCityNamesDict
		#if pieces[4] in statesList:
			#commonCityNames.append(pieces[3])
		
		if pieces[4] in statesList:
			key = pieces[4]

			if key not in commonCityNamesDict:
				commonCityNamesDict[key] = []

			commonCityNamesDict[key].append(pieces[3])

	writeFile()

def writeFile():

	
	commonCityNamesFinal = []
	writeFile = open('CommonCityNames.txt', 'w')

	# Find the intersection of all values in the commonCityNamesDictionary
	cityIntersection = set.intersection(*(set(val) for val in commonCityNamesDict.values()))

	# PrintCommonCityNames has all of the unique cities for each state in statesList.
	printCommonCityNames = list(cityIntersection)
	printCommonCityNames.sort()
		
	for item in printCommonCityNames:
		
		writeFile.write(item)
		writeFile.write('\n')


def writeFile2():
	writeFile = open('LatLon.txt', 'w')
	
	counter = 0
	
	while(counter < len(latitude)):

		writeFile.write(latitude[counter])
		writeFile.write(" ")
		counter = counter + 1
		writeFile.write(latitude[counter])
		counter = counter + 1
		writeFile.write('\n')


def LatLon():
	
	read_text_file('zips.txt')
	readFile = open('zipcodes.txt', 'r')
	
	#zipsList

	for line in readFile:
		
		pieces = line.split('\t')
		if pieces[1] in zipsList:
			latitude.append(pieces[6])
			latitude.append(pieces[7])
			zipsList.remove(pieces[1])

	writeFile2()

def writeFile3():

	writeFile = open('CityStates.txt', 'w')
	
	for cityName in citiesList:
	
		tempList = []
		tempList2 = []
		tempList = citySt[cityName.upper()]
		tempList2 = list(set(tempList))
		tempList2.sort()
	
		for elements in tempList2:
			writeFile.write(elements)
			writeFile.write(' ')


		writeFile.write('\n')
		

def CityStates():

	read_text_file('cities.txt')
	readFile = open('zipcodes.txt', 'r')
	upperCitiesList = [element.upper() for element in citiesList]


	for line in readFile:
		pieces = line.split('\t')

		if pieces[3] in upperCitiesList:
			key = pieces[3]

			if key not in citySt:
				citySt[key] = []

			citySt[key].append(pieces[4])

	writeFile3()
		

CommonCityNames()
LatLon()
CityStates()


