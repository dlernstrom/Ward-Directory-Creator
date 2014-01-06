class Luhn:
	'''
	#################
	## Luhn.py
	##
	## This class exposes the functionality of:
	## 1) generating a Luhn Algorithm Valid Checksum
	## 2) Validating a number against the Luhn Algorithm
	'''

	def __init__(self):
		''' It is a lot faster if we create a lookup table
		for each double, reduce, and sum operation for use later
		'''
		self.Lookup = (0,2,4,6,8,1,3,5,7,9)

	def __LookupValue__(self, Number, Position):
		'''Position is the Zero-based index from the right side'''
		if Position % 2:
			#print "LOOKUP:",Position, self.Lookup[Number]
			return self.Lookup[Number]
		else:
			#print "LOOKUP:",Position, Number
			return Number

	def __FindDifference__(self, InputNumber):
		''' Tests the number and returns a value to set '''
		sum = 0
		NumberLength = len(str(InputNumber))
		#print "NumberLength", NumberLength
		for Position in range(NumberLength):
			DigitPicked = int(str(InputNumber)[NumberLength - 1 - Position])
			sum += self.__LookupValue__(DigitPicked, Position)
		#This returns what the last number should be to go Luhner
		#print sum
		return (10 - (sum % 10)) % 10


	def Generate(self, InputNumber):
		''' Accepts an input number to be luhnified'''
		return self.__FindDifference__(InputNumber * 10)

	def Validate(self, InputNumber):
		''' Accepts an input number to be validated'''
		CalculatedChecksum = self.__FindDifference__(InputNumber / 10 * 10)
		GivenChecksum = InputNumber % 10
		if CalculatedChecksum - GivenChecksum == 0:
			return True
		else:
			return False

if __name__ == '__main__':
	MyLuhn = Luhn()
	TestValue = 510510510510510# (A test MasterCard number), should be 0
	CheckSum = MyLuhn.Generate(TestValue)
	print "Checksum for ",TestValue, " is ", CheckSum
	NewValue = TestValue * 10 + CheckSum
	print "NewValue:", NewValue
	print "Testing Luhnified number", NewValue, "==", MyLuhn.Validate(NewValue)
	for Counter in range(100,111):
		print "----------------------------------"
		print "Number:", Counter
		CheckSum = MyLuhn.Generate(Counter)
		print "Checksum for " + str(Counter) + "_ is ", CheckSum, " = ", Counter * 10 + CheckSum
		NewNumber = Counter * 10 + CheckSum
		print "Is ", NewNumber, " a valid Luhn?", MyLuhn.Validate(NewNumber)