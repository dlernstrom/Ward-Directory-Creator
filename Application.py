import PDFTools
import CSVMembershipParser
from Email import mail
import os
import Configuration

__version__ = "$Rev$".split()[1]
VersionString = '1.0'
State = 'dev'
ConfigFilename = "WardDirectoryCreator.cfg"
ConfigDefaults = {
	"unit.unitname":			"Your Ward Name Here",
	"unit.unit_type":			"Ward",
	"unit.stakename":			"Your Stake Name Here",
	"quote.usequote":			"1",
	"quote.quotecontent":		"As children of the Lord\nwe should strive every day to rise to a higher level of personal rightousness in all of our actions.",
	"quote.quoteauthor":		"President James E. Faust",
	"block.displaysac":			"1",
	"block.sacstart":			"09:00 AM",
	"block.displayss":			"1",
	"block.ssstart":			"10:20 AM",
	"block.display_pr_rs":		"1",
	"block.pr_rs_start":		"11:10 AM"
	}

class Application:
	def __init__(self,
				 parent,
				 DEBUG = 0):

		self.ConfigHandle = Configuration.Configuration(ConfigFilename, ConfigDefaults)
		self.ConfigDefaults = ConfigDefaults

		self.DEBUG = DEBUG

		self.GetMembershipList()

	def GetConfigValue(self, DictionaryField):
		return self.ConfigHandle.GetValueByKey(DictionaryField)

	def SetConfigValue(self, DictionaryField, value):
		self.ConfigHandle.SetValueByKey(DictionaryField, value)
		if DictionaryField == 'file.csvlocation':
			self.GetMembershipList()
			self.SetLists()

	def InitiatePDF(self):
		PDFToolHandle = PDFTools.PDFTools(self.DEBUG,
										  self.DIRECTORY_IMAGES,
										  self.APPDATAFOLDER,
										  self.filename,
										  self.front,
										  self.back
										  )

		#Here I start adding flowables
		NumberOfMembers = 0
		NumberOfHouseholds = 0
		self.GetMembershipList()
		for Household in self.MembershipList:
			NumberOfHouseholds += 1
			NumberOfMembers += len(Household[1][0]) + len(Household[1][1])
			PDFToolHandle.AddFamily(Household)
			print str(NumberOfHouseholds), Household[0]
			print '------------------------------------------'
		PDFToolHandle.AddFooter(str(NumberOfHouseholds) + ' Total Families')
		PDFToolHandle.AddFooter(str(NumberOfMembers) + ' Total Individuals')
		PDFToolHandle.AddDirectoryWrapperImages()
		PDFToolHandle.GenerateWardPagination()
		PDFToolHandle.GeneratePDFDocs()

	def GetFullVersion(self):
		return VersionString + State + __version__

	def GetMajorVersion(self):
		return VersionString

	def isValidCSV(self):
		return self.ValidCSV

	def GetMembershipList(self):
		self.ValidCSV = False
		self.MembershipList = []
		if self.GetConfigValue('file.csvlocation') == None or not self.GetConfigValue('file.csvlocation')[-4:] == '.csv':
			print "Not valid"
			return
		MembershipHandle = CSVMembershipParser.CSVMembershipParser(self.GetConfigValue('file.csvlocation'))
		for Household in MembershipHandle.next():
			self.MembershipList.append(Household)
		if len(self.MembershipList) > 0:
			self.ValidCSV = True

	def GetNeededImageList(self):
		return map(lambda Member: Member[3], self.MembershipList)

	def GetMissingList(self):
		MissingImages = []
		for Family in self.MembershipList:
			if not os.path.exists(self.DIRECTORY_IMAGES + Family[3]):
				MissingImages.append(Family[4])
		return MissingImages

	def GetMissingMsg(self):
		message = "The following " + str(len(self.GetMissingList())) + " people are missing pictures\n\n"
		for Name in self.GetMissingList():
			message += Name + '\n'
		#print message
		return message

	def GetMemberEmails(self):
		EmailList = []
		for Family in self.MembershipList:
			# Family[1] is the name/email list
			# Family[0] is the surname
			#print Family[0]
			for MemberType in Family[1]:
				#print MemberType
				for Name in MemberType:
					if not Name.find('<') == -1:
						Result = '"' + Name[:Name.find('<')] + Family[0] + '"' + Name[Name.find('<') - 1:]
						EmailList.append(Result)
		return EmailList

	def SetLists(self):
		self.SetNameList(NameType = 'HoH')
		self.SetNameList(NameType = 'Parent')

	def GetNameList(self, NameType = 'HoH'):
		if NameType == 'HoH':
			return self.NameList_HoH
		elif NameType == 'Parent':
			return self.NameList_Parent
		else:
			print "I haven't implimented 'Family' type yet."

	def SetNameList(self, NameType = 'HoH'):
		#This will return a list of all HeadOfHousehold/Spouses in ward
		Name = []
		if NameType == 'HoH':
			for Family in self.MembershipList:
				Name.append((Family[0] + ', ' + Family[1][0][0].split('<')[0]).strip())
			self.NameList_HoH = Name
		elif NameType == 'Parent':
			for Family in self.MembershipList:
				for Result in Family[1][0]:
					Name.append((Family[0] + ', ' + Result.split('<')[0]).strip())
			self.NameList_Parent = Name

	def GetPhoneNumber(self, Name):
		for Family in self.MembershipList:
			for Result in Family[1][0]:
				if Name == (Family[0] + ', ' + Result.split('<')[0]).strip():
					return Family[2][1]

	def SendEmails(self):
		if self.SEND_EMAILS:
			for ToAddy in self.MISSING_PEOPLE_EMAILS:
				mail(self.SMTP_SERVER, 'David@Ernstrom.net', ToAddy, 'Missing Picture', self.GetMissingMsg())

	def MakeMissingFile(self):
		Handle = open(CSV_LOCATION + "Needed.txt", 'w')
		Handle.write(self.GetMissingMsg())
		Handle.close()

	def GetSuperfluousImageList(self):
		IgnoreList = ['000.jpg', '-000.jpg', '-001.jpg', '-002.jpg', 'blank.jpg',
					  '-003.jpg', '001.jpg', 'Thumbs.db', 'Missing.jpg']
		NeededList = self.GetNeededImageList()
		ExtraImages = []
		for root, dirs, files in os.walk(self.DIRECTORY_IMAGES):
			for file in files:
				if not file in IgnoreList and not file in NeededList:
					ExtraImages.append(file)
		return ExtraImages

	def MoveSuperflousImages(self, LiveFolder, ArchiveFolder):
		for Image in self.GetSuperfluousImageList():
			try:
				os.rename(LiveFolder + os.sep + Image, ArchiveFolder + os.sep + Image)
			except WindowsError:
				os.mkdir(ArchiveFolder)
				os.rename(LiveFolder + os.sep + Image, ArchiveFolder + os.sep + Image)
			print Image,"moved to archive"
