import PDFTools
import CSVMembershipParser
from Email import mail
import os
import Configuration
import string
import time

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
		#self.DEBUG = 1

		self.GetMembershipList()

	def GetConfigValue(self, DictionaryField):
		return self.ConfigHandle.GetValueByKey(DictionaryField)

	def SetConfigValue(self, DictionaryField, value):
		self.ConfigHandle.SetValueByKey(DictionaryField, value)
		if DictionaryField == 'file.csvlocation':
			self.GetMembershipList()
			self.SetLists()

	def StructureBlockData(self):
		#Here, I need to return a list of lists about the current block data
		BlockData = []
		format = '%I:%M %p'
		if self.GetConfigValue('block.displaysac'):
			BlockData.append([time.strptime(self.GetConfigValue('block.sacstart'), format),
							  "Sacrament Meeting"])
		if self.GetConfigValue('block.displayss'):
			BlockData.append([time.strptime(self.GetConfigValue('block.ssstart'), format),
							  "Sunday School"])
		if self.GetConfigValue('block.display_pr_rs'):
			BlockData.append([time.strptime(self.GetConfigValue('block.pr_rs_start'), format),
							  "Priesthood / Relief Society"])
		if self.DEBUG:
			print BlockData
		BlockData.sort()
		for Mtg in BlockData:
			Mtg[0] = time.strftime(format, Mtg[0])
			if Mtg[0][0] == '0':
				Mtg[0] = Mtg[0][1:]
		if self.DEBUG:
			print BlockData
		return BlockData

	def GetQuoteData(self):
		QuoteData = ['','']
		if self.GetConfigValue('quote.usequote') == '1':
			QuoteData = [self.GetConfigValue('quote.quotecontent'),
						 self.GetConfigValue('quote.quoteauthor')]
		return QuoteData

	def InitiatePDF(self, ImageDirectory, OutputFolder, Full, Booklet):
		PDFToolHandle = PDFTools.PDFTools(self.DEBUG,
										  ImageDirectory,
										  OutputFolder,
										  Full,
										  Booklet,
										  DictionaryData = self.ConfigHandle.GetConfigData(),
										  BlockData = self.StructureBlockData(),
										  QuoteData = self.GetQuoteData(),
										  FullVersionString = self.GetFullVersion()
										  )

		#Here I start adding flowables
		PDFToolHandle.AddDirectoryPrefixData()
		NumberOfMembers = 0
		NumberOfHouseholds = 0
		self.GetMembershipList()
		for Household in self.MembershipList:
			NumberOfHouseholds += 1
			NumberOfMembers += len(Household[1][0]) + len(Household[1][1])
			PDFToolHandle.AddFamily(Household)
			if self.DEBUG:
				print str(NumberOfHouseholds), Household[0]
				print '------------------------------------------'
		PDFToolHandle.AddFooter(str(NumberOfHouseholds) + ' Total Families')
		PDFToolHandle.AddFooter(str(NumberOfMembers) + ' Total Individuals')
		PDFToolHandle.AddDirectorySuffixData()
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
			print "Not a valid membership list"
			return
		MembershipHandle = CSVMembershipParser.CSVMembershipParser(self.GetConfigValue('file.csvlocation'))
		for Household in MembershipHandle.next():
			self.MembershipList.append(Household)
		if len(self.MembershipList) > 0:
			self.ValidCSV = True

	def GetNeededImageList(self):
		return map(lambda Member: Member[3], self.MembershipList)

	def GetMissingList(self, ImagesDirectory):
		MissingImages = []
		for Family in self.MembershipList:
			if not os.path.exists(ImagesDirectory + os.sep + Family[3]):
				MissingImages.append(Family[4])
		return MissingImages

	def GetMissingMsg(self, ImagesDirectory):
		MissingList = self.GetMissingList(ImagesDirectory)
		message = "The following " + str(len(MissingList)) + " people are missing pictures\n\n"
		for Name in MissingList:
			message += Name + '\n'
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

	def GetSuperfluousImageList(self, LiveFolder):
		IgnoreList = ['-001.jpg', '-002.jpg', 'blank.jpg',
					  '-003.jpg', 'Thumbs.db', 'Missing.jpg']
		NeededList = self.GetNeededImageList()
		ExtraImages = []
		for root, dirs, files in os.walk(LiveFolder):
			for file in files:
				if not file in IgnoreList and not string.lower(file) in map(lambda x: string.lower(x), NeededList):
					ExtraImages.append(file)
		return ExtraImages

	def MoveSuperflousImages(self, LiveFolder, ArchiveFolder):
		for Image in self.GetSuperfluousImageList(LiveFolder):
			try:
				os.rename(LiveFolder + os.sep + Image, ArchiveFolder + os.sep + Image)
			except WindowsError:
				os.mkdir(ArchiveFolder)
				os.rename(LiveFolder + os.sep + Image, ArchiveFolder + os.sep + Image)
			print Image, "moved to archive"
