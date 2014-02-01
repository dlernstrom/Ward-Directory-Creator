import os
import smtplib
import time
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from PDFTools import PDFTools
from Configuration import Configuration
from CSVMembershipParser import CSVMembershipParser

from rtree import index
from Coordinate import Coordinate
from Dwellings import Dwellings
from Maps import Map, Maps
from Directory import Directory
from DirectoryPages.Listings import get_listing_pages
from DirectoryPages.MapsPages import get_maps_pages, get_maps_lookup_pages
from DirectoryPages.Prefix import get_directory_prefix_pages
from DirectoryPages.Suffix import get_directory_suffix_pages

ConfigFilename = "WardDirectoryCreator.cfg"
ConfigDefaults = {
    "unit.unitname":			"Your Ward Name Here",
    "unit.unit_type":			"Ward",
    "unit.stakename":			"Your Stake Name Here",
    "quote.usequote":			"1",
    "quote.quotecontent":		"As children of the Lord\nwe should strive every day to rise to a higher level of personal righteousness in all of our actions.",
    "quote.quoteauthor":		"President James E. Faust",
    "block.displaysac":			"1",
    "block.sacstart":			"09:00 AM", # 70 mins
    "block.displayss":			"1",
    "block.ssstart":			"10:20 AM", # 40 mins
    "block.display_pr_rs":		"1",
    "block.pr_rs_start":		"11:10 AM", # 50 mins
    "bldg.phone":				"(XXX) XXX-XXXX",
    "bldg.addy1":				"Address Line 1",
    "bldg.addy2":				"City, State ZIP CODE"
}

class Application:
    def __init__(self,
                 parent,
                 DEBUG = 0):

        self.ConfigHandle = Configuration(ConfigFilename, ConfigDefaults)
        self.ConfigDefaults = ConfigDefaults

        self.DEBUG = DEBUG

        self.GetMembershipList()

    def GetConfigValue(self, DictionaryField):
        return self.ConfigHandle.GetValueByKey(DictionaryField)

    def SetConfigValue(self, DictionaryField, value):
        self.ConfigHandle.SetValueByKey(DictionaryField, value)
        if DictionaryField == 'file.member_csv_location':
            self.GetMembershipList()
            self.SetLists()
        if DictionaryField == 'file.nonmember_csv_location':
            self.GetMembershipList()
            self.SetLists()

    def build_directory(self):
        self.GetMembershipList()
        self.annotate_images()
        #return # return here if only mapping houses
        for household in self.MembershipList:
            household.set_map_index(self.homes.find_map_index_for_household(household))
        directoryCollection = Directory()
        configData = self.ConfigHandle.GetConfigData()
        directoryCollection.pages['prefix'] = get_directory_prefix_pages(dictionaryData = configData,
                                                                         debug = self.DEBUG)
        directoryCollection.pages['directory'] = get_listing_pages(configData = configData,
                                                                   membershipList = self.MembershipList,
                                                                   debug = self.DEBUG)
        directoryCollection.pages['maps'] = get_maps_pages(configData = configData,
                                                           maps = self.ourMaps,
                                                           membershipList = self.MembershipList,
                                                           debug = self.DEBUG)
        directoryCollection.pages['mapsLookup'] = get_maps_lookup_pages(configData = configData,
                                                                        dwellingsHandle = self.homes,
                                                                        membershipList = self.MembershipList,
                                                                        debug = self.DEBUG)
        directoryCollection.pages['suffix'] = get_directory_suffix_pages(dictionaryData = configData,
                                                                         debug = self.DEBUG)
        return directoryCollection

    def InitiatePDF(self, OutputFolder, Full, Booklet, Single2Double):
        directoryCollection = self.build_directory()
        #return # return here if only mapping houses

        if OutputFolder == None or OutputFolder == 'None':
            OutputFolder = ''
        else:
            OutputFolder = OutputFolder + os.sep
        tm = time.strftime("%Y_%m_%d_%H_%M")

        PDFToolHandle = PDFTools(self.DEBUG)
        if Full:
            filename = OutputFolder + 'PhotoDirectory_%s.pdf' % tm
            PDFToolHandle.generate_doc(filename, 'full', directoryCollection.get_pages_for_binding('full'))
        if Booklet:
            front = OutputFolder + 'PhotoDirectory_%s_FRONT.pdf' % tm
            back = OutputFolder + 'PhotoDirectory_%s_BACK.pdf' % tm
            PDFToolHandle.generate_doc(front, 'front', directoryCollection.get_pages_for_binding('booklet'))
            PDFToolHandle.generate_doc(back, 'back', directoryCollection.get_pages_for_binding('booklet'))
        if Single2Double:
            bookletprinted = OutputFolder + 'PhotoDirectory_%s_Single2Double.pdf' % tm
            PDFToolHandle.generate_doc(bookletprinted, 'special', directoryCollection.get_pages_for_binding('booklet'))

    def create_sortable_index(self):
        self.homes = Dwellings()
        self.idx = index.Index()
        counter = 0
        for entry in self.homes.dwellingList:
            left = float(entry.Longitude)
            bottom = float(entry.Latitude)
            right = float(entry.Longitude)
            top = float(entry.Latitude)
            self.idx.insert(counter, (left, bottom, right, top), obj=counter)
            counter += 1

    def annotate_images(self):
        self.create_sortable_index()
        # furthest north person is at 41.9706778
        # furthest south person is at ?
        # furthest west person is at -111.8081775
        # furthest east person is at -111.7705975
        self.ourMaps = Maps([Map(1, Coordinate(41.9720, -111.8117775), Coordinate(41.9720, -111.7669975), 'large', 'portrait', 'east', 16, "Cherry Creek Ward", [Coordinate(41.9702841,-111.8060452), Coordinate(41.9523412,-111.8081775)]),
                             Map(2, Coordinate(41.9366, -111.806247), Coordinate(41.9366, -111.7958776), 'small', 'landscape', 'east', 17, "Inset 1", [Coordinate(41.9359261,-111.7964), Coordinate(41.934148,-111.79725)]),
                             Map(3, Coordinate(41.9313799, -111.80875), Coordinate(41.9313799, -111.79955), 'small', 'landscape', 'east', 18, "Inset 2", [Coordinate(41.9306082,-111.800404), Coordinate(41.9292656,-111.8011141)])])
        currentPosition = (-112, 45, -112, 45) # must be left, bottom, right, top
        done = False
        counter = 1
        overrides = {7: (41.9646525, -111.776777),
                     8: (41.9656381, -111.7788342),
                     9: (41.9639087, -111.7753051),
                     11: (41.9594132, -111.7796387),
                     15: (41.95687, -111.783775),
                     16: (41.9537827, -111.7820407), # claudia beeney
                     17: (41.9557139, -111.7872486), # allen, craig
                     20: (41.9527252, -111.7854261), # Stallard
                     22: (41.950471, -111.7819565), # ernstrom
                     23: (41.9523412, -111.788422), # dutro
                     25: (41.94972, -111.7850972), # floyd griff
                     36: (41.9414439, -111.787962),
                     38: (41.9408163, -111.7813266),
                     39: (41.940414, -111.787455),
                     40: (41.9397178, -111.7944185),
                     41: (41.9392206, -111.7881929),
                     42: (41.938246, -111.780649),
                     44: (41.9373516, -111.7860991),
                     48: (41.931241, -111.7823051),
                     75: (41.934126, -111.80055),
                     77: (41.934931, -111.8010959),
                     78: (41.935188, -111.800637),
                     88: (41.935462, -111.799187),
                     90: (41.935051, -111.799856),
                     100: (41.9349648, -111.802612),
                     102: (41.9354462, -111.8032709),
                     104: (41.9348859, -111.8029934),
                     106: (41.9346405, -111.8037181),
                     110: (41.9337922, -111.8050698),
                     112: (41.9330397, -111.804966),
                     123: (41.9285393, -111.8003886),
                     127: (41.9269528, -111.8026337),
                     132: (41.9280942, -111.8031176),
                     140: (41.9278887, -111.8052702),
                     141: (41.9278835, -111.8045496),
                     142: (41.928216, -111.8053694),
                     149: (41.9290114, -111.8011141),
                     151: (41.9296263, -111.803214),
                     157: (41.9285052, -111.8059139),
                     160: (41.9270505, -111.8059784),
                     161: (41.9270027, -111.8073113),
                     163: (41.9270032, -111.8081775),
                     179: (41.928289, -111.807166),
                     192: (41.9291407, -111.8053663),
                     203: (41.9532703, -111.8029656),
                     }
        while done == False:
            if counter in overrides.keys():
                currentPosition = [overrides[counter][1], overrides[counter][0], overrides[counter][1], overrides[counter][0]] # must be left, bottom, right, top
            nearest = list(self.idx.nearest(coordinates = currentPosition,
                                            num_results=1,
                                            objects=True))
            if len(nearest) == 0:
                done = True
                continue
            print counter
            nearest = nearest[0]
            d = self.homes.dwellingList[nearest.object]
            d.save_map_index(counter)
            #print "Nearest ID", nearest.id
            print "Nearest Object", d
            print "XXX: (%s, %s)," % (d.Latitude, d.Longitude)
            currentPosition = [d.Longitude, d.Latitude, d.Longitude, d.Latitude] # must be left, bottom, right, top
            self.idx.delete(nearest.id, currentPosition)
            self.ourMaps.annotate_coordinate(counter, Coordinate(d.Latitude, d.Longitude))
            print "*" * 30
            counter += 1
        self.homes.order_dwelling_list()
        self.ourMaps.save()

    def isValidCSV(self):
        return self.ValidCSV

    def GetMembershipList(self):
        self.ValidCSV = False
        self.MembershipList = []
        if self.GetConfigValue('file.member_csv_location') == None or not self.GetConfigValue('file.member_csv_location')[-4:] == '.csv':
            raise Exception("Not a valid membership list")
        if self.GetConfigValue('file.nonmember_csv_location') == None or not self.GetConfigValue('file.nonmember_csv_location')[-4:] == '.csv':
            raise Exception("Not a valid nonmembership list")
        membershipHandle = CSVMembershipParser(self.GetConfigValue('file.member_csv_location'))
        for Household in membershipHandle.next():
            self.MembershipList.append(Household)
        membershipHandle = CSVMembershipParser(self.GetConfigValue('file.nonmember_csv_location'))
        for Household in membershipHandle.next():
            self.MembershipList.append(Household)
        if len(self.MembershipList) > 0:
            self.ValidCSV = True
        self.MembershipList = sorted(self.MembershipList, key=lambda h: h.coupleName)

    def GetNeededImageList(self):
        return map(lambda Member: Member.expectedPhotoName, self.MembershipList)

    def GetFamilyOfDuplicateAddressList(self):
        AddressesSeen = []
        AddressesAlreadyDuped = []
        ReportMsg = ''
        for Family in self.MembershipList:
            if not Family.familyAddress in AddressesAlreadyDuped and Family.familyAddress in AddressesSeen:
                ReportMsg += 'Address Already found\n'
                ReportMsg += 'Address: ' + Family.familyAddress + '\n'
                for Name in self.MembershipList:
                    if Name.familyAddress == Family.familyAddress:
                        ReportMsg += 'Family: ' + Name.coupleName + '\n'
                ReportMsg += '\n'
                AddressesAlreadyDuped.append(Family.familyAddress)
            AddressesSeen.append(Family.familyAddress)
        Report = "\nFamilies with duplicate addresses\n" + ReportMsg
        return Report

    def GetMissingHouseholds(self):
        ImagesDirectory = self.GetConfigValue('file.imagesdirectory')
        MissingImages = []
        for Family in self.MembershipList:
            if not os.path.exists(ImagesDirectory + os.sep + Family.expectedPhotoName):
                MissingImages.append(Family.coupleName)
        return MissingImages

    def GetMissingImages(self):
        ImagesDirectory = self.GetConfigValue('file.imagesdirectory')
        MissingImages = []
        for Family in self.MembershipList:
            if not os.path.exists(ImagesDirectory + os.sep + Family.expectedPhotoName):
                MissingImages.append(Family.expectedPhotoName)
        return MissingImages

    def GetReportMsg(self):
        MissingList = self.GetMissingHouseholds()
        message = "The following " + str(len(MissingList)) + " households are missing pictures\n\n"
        for Name in MissingList:
            message += Name + '\n'
        message += self.GetFamilyOfDuplicateAddressList()
        return message

    def GetImagesReportMsg(self):
        MissingList = self.GetMissingImages()
        message = "The following " + str(len(MissingList)) + " images are missing\n\n"
        for Name in MissingList:
            message += Name + '\n'
        return message

    def GetMissingMsgEmails(self):
        return self.GetConfigValue('email.recipients').split(',')

    def GetMemberEmails(self):
        emailList = []
        for family in self.MembershipList:
            emailList.extend(family.get_emails_as_list())
        return emailList

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
        if NameType == 'HoH':
            self.NameList_HoH = []
            for family in self.MembershipList:
                self.NameList_HoH.append(family.head_of_household.fullName)
        elif NameType == 'Parent':
            self.NameList_Parent = []
            for family in self.MembershipList:
                for parent in family.parents:
                    self.NameList_Parent.append(parent.fullName)

    def GetPhoneNumber(self, searchName):
        for household in self.MembershipList:
            for member in household.family:
                if member.fullName == searchName:
                    if len(member.phone.phoneFormatted):
                        return member.phone.phoneFormatted
                    else:
                        return household.familyPhone.phoneFormatted

    def SendEmails(self):
        if not self.GetConfigValue('email.smtp') == None:
            SMTP_SERVER = self.GetConfigValue('email.smtp')
            SMTP_User = self.GetConfigValue('email.username')
            SMTP_Pass = self.GetConfigValue('email.pass')
            session = smtplib.SMTP(SMTP_SERVER)
            if not SMTP_User == None and not SMTP_Pass == None:
                session.login(user = SMTP_User, password = SMTP_Pass)
            msg = MIMEMultipart()
            msg['From'] = 'Ward Directory Creator <david@ernstrom.net>'
            msg['Subject'] = 'Missing Persons Email'
            msg.attach(MIMEText(self.GetReportMsg()))
            for ToAddy in self.GetMissingMsgEmails():
                print ToAddy
                msg['To'] = ToAddy
                smtpresult = session.sendmail(from_addr = 'Ward Directory Creator <david@ernstrom.net>',
                                              to_addrs = ToAddy,
                                              msg = msg.as_string())
            session.close()

    def MakeMissingFile(self):
        Handle = open(CSV_LOCATION + "Needed.txt", 'w')
        Handle.write(self.GetMissingMsg())
        Handle.close()

    def GetSuperfluousImageList(self, LiveFolder):
        if LiveFolder == None:
            return []
        IgnoreList = ['Thumbs.db', 'Missing.jpg']
        NeededList = self.GetNeededImageList()
        ExtraImages = []
        for root, dirs, files in os.walk(LiveFolder):
            for fileName in files:
                if not fileName in IgnoreList and not fileName.lower() in map(lambda x: x.lower(), NeededList):
                    ExtraImages.append(fileName)
        return ExtraImages

    def MoveSuperflousImages(self, LiveFolder, ArchiveFolder):
        for Image in self.GetSuperfluousImageList(LiveFolder):
            try:
                os.rename(LiveFolder + os.sep + Image, ArchiveFolder + os.sep + Image)
            except WindowsError:
                os.mkdir(ArchiveFolder)
                os.rename(LiveFolder + os.sep + Image, ArchiveFolder + os.sep + Image)
            print Image, "moved to archive"
