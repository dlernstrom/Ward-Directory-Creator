import PDFTools
import CSVMembershipParser
from Email import mail
import os

class Application:
	def __init__(self,
				 parent,
				 filename,
				 front,
				 back,
				 APPDATAFOLDER = 'Ward Directory',
				 DIRECTORY_IMAGES = 'C:\\Documents and Settings\\Administrator\\Desktop\\Directory\\WardPictures\\',
				 MOVED_OUT = 'C:\\Documents and Settings\\Administrator\\Desktop\\Directory\\MovedOut\\',
				 CSV_LOCATION = 'C:\\Documents and Settings\\Administrator\\Desktop\\Directory\\',
				 SEND_EMAILS = 0,
				 SMTP_SERVER = None,
				 MISSING_PEOPLE_EMAILS = ['david.ernstrom@usa.dupont.com'],
				 DEBUG = 0):
		self.DIRECTORY_IMAGES = DIRECTORY_IMAGES
		self.MOVED_OUT = MOVED_OUT
		self.CSV_LOCATION = CSV_LOCATION
		self.SEND_EMAILS = SEND_EMAILS
		self.SMTP_SERVER = SMTP_SERVER
		self.MISSING_PEOPLE_EMAILS = MISSING_PEOPLE_EMAILS
		self.MembershipList = []

		self.MoveSuperflousImages()
		return

		PDFToolHandle = PDFTools.PDFTools(DEBUG,
										  DIRECTORY_IMAGES,
										  APPDATAFOLDER,
										  filename,
										  front,
										  back
										  )

		#Here I start adding flowables
		NumberOfMembers = 0
		NumberOfHouseholds = 0
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

	def GetMembershipList(self):
		self.MembershipList = []
		MembershipHandle = CSVMembershipParser.CSVMembershipParser(self.CSV_LOCATION + "Greenfield Ward member directory.csv")
		for Household in MembershipHandle.next():
			self.MembershipList.append(Household)

	def GetNeededImageList(self):
		self.GetMembershipList()
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
