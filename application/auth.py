import time
import random
import Luhn


# Ascii values range from 39 -> 127
# Ascii Digits				Sum Length
# 		1						3
# 		8						4
# 		79						5

# 79 Letters in the ward's name

#Serial Number will have the following parts
# 3 character ward name (all caps)										3
# DASH!!!!
# 5 digits the sum of ascii digits of ward name (A0, A1, A2, A3, A4)	5
# 2 digits to represent the number of characters (B0, B1)				2
# 2 digit month (plus 53) (C0, C1)										2
# 2 digit day (plus 53) (D0, D1)										2
# 2 digit year (plus 53) (E0, E1)										2
# 3 digit SUM of ascii 3 letter abbreviation (F0, F1, F2)				3
# 3 random digits (G0, G1, G2)											3
# Checksum (H0)															1

#sequence generated from random.org
# A0	0	13
# A1	1	19
# A2	2	10
# A3	3	12
# A4	4	5
# B0	5	8
# B1	6	4
# C0	7	6
# C1	8	11
# D0	9	0
# D1	10	9
# E0	11	7
# E1	12	16
# F0	13	17
# F1	14	18
# F2	15	3
# G0	16	2
# G1	17	14
# G2	18	15
# H0	19	1


class Auth:
	def __init__(self):
		self.SerialCode = ''
		self.mixerlist =   [13, 19, 10, 12, 5, 8, 4, 6, 11, 0, 9, 7, 16, 17, 18, 3, 2, 14, 15, 1]
		self.unmixerlist = [9, 19, 16, 15, 6, 4, 7, 11, 5, 10, 2, 8, 3, 0, 17, 18, 12, 13, 14, 1]

	def Encode(self, SerialCode = 'XXX-' + 'X' * 20, WardName = '', ExpMonth = 0, ExpDay = 0, ExpYear = 0):
		self.SerialCode = SerialCode
		self.WardName = WardName
		self.ExpMonth = ExpMonth
		self.ExpDay = ExpDay
		self.ExpYear = ExpYear
		print "Encoding"
		WardCode = self.WardName[:3].upper() + '-'
		Premixed = self.MakeSerialCode()
		Mixed = self.MakeMixed(Premixed)
		#unmixed = self.MakeUnmixed(Mixed)
		#print "PremixedSerial:", Premixed
		#print "   MixedSerial:", Mixed
		#print " UnmixedSerial:", unmixed
		self.SerialCode = WardCode + Mixed
		return self.SerialCode

	def IsValidWardName(self, WardName, Code):
		#I know the ward name is valid because:
		# 1) the prefix characters will be right
		if not WardName[:3].upper() == Code[:3]:
			print "Ward Prefix Wrong"
			return False
		# 2) The Sum will be correct
		if not self.MakeUnmixed(Code[4:])[:5] == self.SumAscii(WardName, 5):
			print "Ward Name Sum Wrong"
			return False
		# 3) The count will be correct
		if not self.MakeUnmixed(Code[4:])[5:7] == self.LengthWardName():
			print "Ward Name Length Wrong"
			return False
		#print "Ward Name is Valid"
		return True

	def IsValidDateData(self, Code, CurrentMMDDYY):
		UnmixedDate = self.RevertOffsetTriple(self.MakeUnmixed(Code[4:])[7:13])
		CurrentYYMMDD = CurrentMMDDYY[4:6] + CurrentMMDDYY[0:2] + CurrentMMDDYY[2:4]
		CodeYYMMDD = UnmixedDate[4:6] + UnmixedDate[0:2] + UnmixedDate[2:4]
		if CurrentYYMMDD > CodeYYMMDD:
			print "Not a valid Current Timestamp"
			print "Current:", CurrentYYMMDD
			print "Code:", CodeYYMMDD
			return False
		#print "Time is valid"
		return True

	def GetExpirationMMDDYY(self, Code):
		return self.RevertOffsetTriple(self.MakeUnmixed(Code[4:])[7:13])

	def IsValidChecksum(self, Code):
		LuhnHandle = Luhn.Luhn()
		if not LuhnHandle.Validate(int(self.MakeUnmixed(Code[4:]))):
			print "Not a valid checksum"
			return False
		#print "Checksum is valid"
		return True

	def IsValid(self, WardName = '', Code = 'XXX-' + 'X' * 20, CurrentMMDDYY = '072407'):
		#print "Decoding"
		self.WardName = WardName
		self.SerialCode = Code
		if not self.IsValidWardName(WardName, Code):
			print "not a valid ward name"
			return False
		if not self.IsValidDateData(Code, CurrentMMDDYY):
			print "Not within the correct date range"
			return False
		if not self.IsValidChecksum(Code):
			print "not a valid checksum"
			return False
		#print "TOTAL NUMBER IS VALID"
		return True

	def GetOffset(self, Number):
		return str(Number + 53).rjust(2, '0')

	def RevertOffsetTriple(self, Number):
		#print "PreviousNumber", Number
		return str(int(Number) - 535353).rjust(6, '0')

	def SumAscii(self, TheString, length):
		TheSum = 0
		for Letter in TheString:
			#print Letter.upper(), ord(Letter.upper())
			TheSum += ord(Letter)
		return str(TheSum).rjust(length, '0')

	def LengthWardName(self):
		return str(len(str(self.WardName))).rjust(2, '0')

	def GetMonth(self):
		return self.GetOffset(self.ExpMonth)

	def GetDay(self):
		return self.GetOffset(self.ExpDay)

	def GetYear(self):
		return self.GetOffset(self.ExpYear)

	def MakeSerialCode(self):
		UnmixedSerial = self.SumAscii(self.WardName, 5) + self.LengthWardName() + self.GetMonth() + self.GetDay() + 	\
							self.GetYear() + self.SumAscii(self.GetDayLetters(), 3) + self.GetRandom()
		LuhnHandle = Luhn.Luhn()
		UnmixedSerial = UnmixedSerial + str(LuhnHandle.Generate(int(UnmixedSerial)))
		return UnmixedSerial

	def MakeMixed(self, UnmixedValue):
		MixedValue = 'X' * 20
		for OldSlot in range(20):
			NewSlot = self.mixerlist[OldSlot]
			#print NewSlot
			MixedValue = MixedValue[:NewSlot] + UnmixedValue[OldSlot] + MixedValue[NewSlot + 1:]
			#print MixedValue
		return MixedValue

	def MakeUnmixed(self, MixedValue):
		UnmixedValue = 'X' * 20
		for OldSlot in range(20):
			NewSlot = self.unmixerlist[OldSlot]
			#print NewSlot
			UnmixedValue = UnmixedValue[:NewSlot] + MixedValue[OldSlot] + UnmixedValue[NewSlot + 1:]
			#print UnmixedValue
		return UnmixedValue

	def GetDayLetters(self):
		StringExp = str(self.ExpMonth).rjust(2, '0') + ' ' + str(self.ExpDay).rjust(2, '0') + ' ' + str(self.ExpYear).rjust(2, '0')
		TimeCode = time.strptime(StringExp, "%m %d %y")
		return time.strftime('%a', TimeCode).upper()

	def GetRandom(self):
		random.seed()
		MyRandom = random.randrange(1000)
		#print MyRandom
		return str(MyRandom).rjust(3, '0')

	def GetCode(self):
		return self.SerialCode

if __name__ == '__main__':
	print "Starting"
	AuthHandle = Auth()
	AuthHandle.Encode(WardName = 'Cherry Creek Ward', ExpMonth = 12, ExpDay = 31, ExpYear = 15)
	print AuthHandle.GetCode()
	NewAuthHandle = Auth()
	AuthHandle.IsValid(WardName = 'Greenfield Ward', Code = AuthHandle.GetCode(), CurrentMMDDYY = '082407')
