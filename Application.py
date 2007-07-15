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
	"block.displaySac":			"0",
	"block.sacstart":			"",#9:00 AM",
	"block.displayss":			"0",
	"block.ssstart":			"",#10:20 AM",
	"block.display_pr_rs":		"0",
	"block.pr_rs_start":		""#11:10 AM"
	}


class Application:
	def __init__(self,
				 parent,
				 filename,
				 front,
				 back,
				 APPDATAFOLDER = 'Ward Directory',
				 DIRECTORY_IMAGES = 'C:\\Documents and Settings\\Administrator\\Desktop\\Directory\\WardPictures\\',
				 MOVED_OUT = 'C:\\Documents and Settings\\Administrator\\Desktop\\Directory\\ImageArchive\\',
				 CSV_LOCATION = 'C:\\Documents and Settings\\Administrator\\Desktop\\Directory\\',
				 SEND_EMAILS = 0,
				 SMTP_SERVER = None,
				 MISSING_PEOPLE_EMAILS = ['david.ernstrom@usa.dupont.com'],
				 DEBUG = 0):
		self.ConfigHandle = Configuration.Configuration(ConfigFilename, ConfigDefaults)
		self.filename = filename
		self.front = front
		self.back = back
		self.APPDATAFOLDER = APPDATAFOLDER
		self.DIRECTORY_IMAGES = DIRECTORY_IMAGES
		self.MOVED_OUT = MOVED_OUT
		self.CSV_LOCATION = CSV_LOCATION
		self.SEND_EMAILS = SEND_EMAILS
		self.SMTP_SERVER = SMTP_SERVER
		self.MISSING_PEOPLE_EMAILS = MISSING_PEOPLE_EMAILS
		self.DEBUG = DEBUG

		self.MembershipList = []

	def GetConfigValue(self, DictionaryField):
		return self.ConfigHandle.GetValueByKey(DictionaryField)

	def SetConfigValue(self, DictionaryField, value):
		self.ConfigHandle.SetValueByKey(DictionaryField, value)

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

	def GetMembershipList(self):
		self.MembershipList = []
		MembershipHandle = CSVMembershipParser.CSVMembershipParser(self.CSV_LOCATION + "Greenfield Ward member directory.csv")
		for Household in MembershipHandle.next():
			self.MembershipList.append(Household)

	def GetNeededImageList(self):
		self.GetMembershipList()
		return map(lambda Member: Member[3], self.MembershipList)

	def GetMissingList(self):
		self.GetMembershipList()
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
		self.GetMembershipList()
		EmailList = []
		for Family in self.MembershipList:
			# Family[1] is the name/email list
			# Family[0] is the surname
			#print Family[0]
			for MemberType in Family[1]:
				#print MemberType
				for Name in MemberType:
					if not Name.find('<') == -1:
						Result = '"' + Name[:Name.find('<')] + Family[0] + '" ' + Name[Name.find('<') - 1:]
						EmailList.append(Result)
		return EmailList

	def GetNamePhoneList(self):
		#This will return a list of all HeadOfHousehold/Spouses in ward
		self.GetMembershipList()
		Name_Phone = []
		for Family in self.MembershipList:
			for Name in Family[1][0]:
				Name_Phone.append([Family[0] + ', ' + Name.split('<')[0], Name.split('<')[0] + Family[0], Family[2][1]])
		return Name_Phone

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

	def MoveSuperflousImages(self):
		for Image in self.GetSuperfluousImageList():
			try:
				os.rename(self.DIRECTORY_IMAGES + Image, self.MOVED_OUT + Image)
			except WindowsError:
				os.mkdir(self.MOVED_OUT)
				os.rename(self.DIRECTORY_IMAGES + Image, self.MOVED_OUT + Image)
			print Image,"moved to archive"
