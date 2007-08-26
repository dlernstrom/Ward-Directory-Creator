import CSVMembershipReader

class CSVMembershipParser:
	def __init__(self, filename = "Greenfield Ward member directory.csv"):
		self.filename = filename
		self.MembershipHandle = CSVMembershipReader.CSVMembershipReader(self.filename)

	def next(self):
		try:
			for FamilyData in self.MembershipHandle:
				self.CurrentFamily = FamilyData
				yield [self.GetSurname(),
					   [self.GetParentNames(), self.GetChildrenNames()],
					   [self.GetAddy1(), self.GetPhoneNumber()],
					   self.GetFileName(),
					   self.GetFamilySalutation()
					   ]
		except IOError:
			return

	def GetSurname(self):
		return self.CurrentFamily[0].split(',')[0]

	def GetParentCount(self):
		if self.CurrentFamily[0].find(' and ') == -1:
			return 1
		else:
			return 2

	def GetFamilyNames(self):
		return self.CurrentFamily[6:]

	def GetParentNames(self):
		if self.GetParentCount() == 1:
			return [self.GetFamilyNames()[0]]
		else:
			return self.GetFamilyNames()[0:2]

	def GetChildrenNames(self):
		if self.GetParentCount() == 1:
			return self.GetFamilyNames()[1:]
		else:
			return self.GetFamilyNames()[2:]

	def GetAddy1(self):
		return self.CurrentFamily[2]

	def GetPhoneNumber(self):
		return self.CurrentFamily[1]

	def GetFileName(self):
		FileName = (self.GetSurname() + self.GetParentNames()[0].split()[0])
		return FileName.replace(' ','').replace('\'', '').replace('.', '') + '.jpg'

	def GetFamilySalutation(self):
		return self.CurrentFamily[0]

if __name__ == '__main__':
	CSV_LOCATION = 'C:\\Documents and Settings\\Administrator\\Desktop\\Directory\\'
	Handle = CSVMembershipParser(CSV_LOCATION + "Greenfield Ward member directory.csv")
	for Family in Handle.next():
		print Family