def size(matrix):
	return matrix.size

		

class bandMatrix:
	def __init__(self, s):
		self.size = s
		self.width = s
		self.length = s
		self.array = [0] * 900


	
	def get(matrix, index1, index2):

		inBounds = False

		if(index1 < 0 or index2 < 0):
			raise ValueError("Invalid position!")

		if((index1 == 0 and index2 == 0) or (index1 == 0 and index2 == 1)):
		
			inBounds = True

		one = 0
		two = 1
		three = 2

		i = 1
		x = size(matrix) - 1

		while i < x:
			if((index1 == i and index2 == one) or (index1 == i and index2 == two) or (index1 == i and index2 == three)):
			
				inBounds = True
				break
			one = one + 1
			two = two + 1
			three = three + 1
			i = i + 1


		if((index1 == x and index2 == x-1) or (index1 == x and index2 == x)):
		
			inBounds = True

		if(inBounds == False):
			raise ValueError("Invalid position!")

		if(inBounds == True):
			theValue = matrix.array[(2 * index1) + index2]

		return theValue

	def set(matrix, index1, index2, value):
	


		inBounds = False

		if(index1 < 0 or index2 < 0):
			raise ValueError("Invalid position!")

		if((index1 == 0 and index2 == 0) or (index1 == 0 and index2 == 1)):
			inBounds = True

		one = 0
		two = 1
		three = 2

		i = 1
		x = size(matrix) - 1

		while i < x:

			if((index1 == i and index2 == one) or (index1 == i and index2 == two) or (index1 == i and index2 == three)):
				inBounds = True
				break
			one = one + 1
			two = two + 1
			three = three + 1
			i = i + 1

		
		if((index1 == x and index2 == x - 1) or (index1 == x and index2 == x)):
			inBounds = True

		if(inBounds == False):
			raise ValueError("Invalid position!")

		if(inBounds == True):
		
			idx = ((2 * index1)) + index2

			matrix.array[idx] = value

		

	def __add__(self, other):

		if self.size != other.size:
			raise ValueError("Arrays of different size!")


		if self.size == other.size:
			newMat = bandMatrix(self.size)

		
		i = 0
		x = ((self.size - 2) * 3) + 4
		while i < x:

			
			val1 = self.array[i]
			val2 = other.array[i]

			newMat.array[i] = val1 + val2
		
			i = i + 1

		return newMat
		


	
	
        
        