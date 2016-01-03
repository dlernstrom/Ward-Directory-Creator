# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from rtree import index

from .constants import CONFIG_DEFAULTS
from .Coordinate import Coordinate
from .CSVMembershipParser import CSVMembershipParser
from .Directory import Directory
from .DirectoryPages.Listings import get_listing_pages
from .DirectoryPages.MapsPages import get_maps_pages, get_maps_lookup_pages
from .DirectoryPages.Prefix import get_directory_prefix_pages
from .DirectoryPages.Suffix import get_directory_suffix_pages
from .Dwellings import Dwellings
from .INI_Configuration import INIMixin
from .Maps import Map, Maps
from .PDFTools import PDFTools


class Application(INIMixin):
    def __init__(self, DEBUG=0, *args, **kwargs):
        kwargs['ini_defaults'] = CONFIG_DEFAULTS
        super(Application, self).__init__(*args, **kwargs)
        self.homes = None
        self.NameList_Parent = None
        self.NameList_HoH = None
        self.ourMaps = None
        self.idx = None

        self.DEBUG = DEBUG
        self.ValidCSV = False
        if self.file_member_csv_location:
            self.GetMembershipList()
            self.SetLists()

    def build_directory(self):
        self.GetMembershipList()
        self.annotate_images()
        for household in self.MembershipList:
            household.set_map_index(
                self.homes.find_map_index_for_household(household))
        directory_build = Directory()
        directory_build.pages['prefix'] = get_directory_prefix_pages(
            self, debug=self.DEBUG)
        directory_build.pages['directory'] = get_listing_pages(
            self, membership_list=self.MembershipList,
            debug=self.DEBUG)
        directory_build.pages['maps'] = get_maps_pages(self.ourMaps)
        directory_build.pages['mapsLookup'] = get_maps_lookup_pages(
            self, dwellingsHandle=self.homes,
            membership_list=self.MembershipList)
        directory_build.pages['suffix'] = get_directory_suffix_pages(
            self, debug=self.DEBUG)
        return directory_build

    def InitiatePDF(self, OutputFolder, Full, Booklet, Single2Double):
        directory_build = self.build_directory()

        if OutputFolder is None or OutputFolder == 'None':
            OutputFolder = ''
        curr_time = time.strftime("%Y_%m_%d_%H_%M")

        pdf_tool_handle = PDFTools(self.DEBUG)
        if Full:
            filename = os.path.join(OutputFolder,
                                    'PhotoDirectory_%s.pdf' % curr_time)
            pdf_tool_handle.generate_doc(
                filename, 'full',
                directory_build.get_pages_for_binding('full'))
        if Booklet:
            front = os.path.join(OutputFolder,
                                 'PhotoDirectory_%s_FRONT.pdf' % curr_time)
            back = os.path.join(OutputFolder,
                                'PhotoDirectory_%s_BACK.pdf' % curr_time)
            pdf_tool_handle.generate_doc(
                front, 'front',
                directory_build.get_pages_for_binding('booklet'))
            pdf_tool_handle.generate_doc(
                back, 'back',
                directory_build.get_pages_for_binding('booklet'))
        if Single2Double:
            fname = 'PhotoDirectory_%s_Single2Double.pdf' % curr_time
            bookletprinted = os.path.join(OutputFolder, fname)
            pdf_tool_handle.generate_doc(
                bookletprinted, 'special',
                directory_build.get_pages_for_binding('booklet'))

    def create_sortable_index(self):
        self.homes = Dwellings(self.file_dwellings_csv_location)
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
        self.ourMaps = Maps([
            Map(self.cache_dir, 1, Coordinate(41.9720, -111.8117775),
                Coordinate(41.9720, -111.7669975), 'large', 'portrait', 'east',
                16, "Cherry Creek Ward",
                [Coordinate(41.9702841, -111.8060452),
                 Coordinate(41.9523412, -111.8081775)]),
            Map(self.cache_dir, 2, Coordinate(41.9385, -111.808),
                Coordinate(41.9385, -111.7963776), 'large', 'portrait', 'east',
                17, "Inset 1",
                [Coordinate(41.9359261, -111.7964),
                 Coordinate(41.934148, -111.79725)]),
        ])
        # must be left, bottom, right, top
        current_pos = (-112, 45, -112, 45)
        done = False
        counter = 1
        dwelling = None
        while done is False:
            if dwelling != None:
                if dwelling.NextDwellingOverride != '':
                    # must be left, bottom, right, top
                    current_pos = [dwelling.NextDwellingOverride[1],
                                   dwelling.NextDwellingOverride[0],
                                   dwelling.NextDwellingOverride[1],
                                   dwelling.NextDwellingOverride[0]]
            nearest = list(self.idx.nearest(coordinates=current_pos,
                                            num_results=1,
                                            objects=True))
            if len(nearest) == 0:
                done = True
                continue
            print counter
            nearest = nearest[0]
            dwelling = self.homes.dwellingList[nearest.object]
            dwelling.save_map_index(counter)
            # print "Nearest ID", nearest.id
            print "Nearest Object", dwelling
            print "XXX: (%s, %s)," % (dwelling.Latitude, dwelling.Longitude)
            # must be left, bottom, right, top
            current_pos = [dwelling.Longitude,
                           dwelling.Latitude,
                           dwelling.Longitude,
                           dwelling.Latitude]
            self.idx.delete(nearest.id, current_pos)
            self.ourMaps.annotate_coordinate(counter,
                                             Coordinate(dwelling.Latitude,
                                                        dwelling.Longitude))
            print "*" * 30
            counter += 1
        self.homes.order_dwelling_list()
        self.ourMaps.save()

    def isValidCSV(self):
        return self.ValidCSV

    def GetMembershipList(self):
        self.ValidCSV = False
        self.MembershipList = []
        self.MembershipList.extend(self.member_list)
        self.MembershipList.extend(self.nonmember_list)
        if len(self.MembershipList) > 0:
            self.ValidCSV = True
        self.MembershipList = sorted(self.MembershipList,
                                     key=lambda h: h.coupleName)

    @property
    def member_list(self):
        if self.file_member_csv_location == '' or \
                self.file_member_csv_location[-4:] != '.csv':
            raise Exception("Not a valid membership list")
        memb_list = []
        membership_handle = CSVMembershipParser(self.file_member_csv_location)
        for household in membership_handle.next():
            memb_list.append(household)
        return memb_list

    @property
    def nonmember_list(self):
        if self.file_nonmember_csv_location == '' or \
                self.file_nonmember_csv_location[-4:] != '.csv':
            return []
        membership_handle = CSVMembershipParser(
            self.file_nonmember_csv_location)
        nonmem_list = []
        for household in membership_handle.next():
            nonmem_list.append(household)
        return nonmem_list

    def GetNeededImageList(self):
        return [member.expectedPhotoName for member in self.member_list]

    def GetFamilyOfDuplicateAddressList(self):
        addresses_seen = []
        addresses_already_duped = []
        msg = ''
        for family in self.MembershipList:
            if family.familyAddress not in addresses_already_duped and \
                    family.familyAddress in addresses_seen:
                msg += 'Address Already found\n'
                msg += 'Address: ' + family.familyAddress + '\n'
                for name in self.MembershipList:
                    if name.familyAddress == family.familyAddress:
                        msg += 'Family: ' + name.coupleName + '\n'
                msg += '\n'
                addresses_already_duped.append(family.familyAddress)
            addresses_seen.append(family.familyAddress)
        report = "\nFamilies with duplicate addresses\n" + msg
        return report

    def GetMissingHouseholds(self):
        images_dir = self.file_images_directory
        missing_images = []
        for family in self.member_list:
            if not os.path.exists(os.path.join(images_dir,
                                               family.expectedPhotoName)):
                missing_images.append(family.coupleName)
        return missing_images

    def GetMissingImages(self):
        images_dir = self.file_images_directory
        missing_images = []
        for family in self.member_list:
            if not os.path.exists(os.path.join(images_dir,
                                               family.expectedPhotoName)):
                missing_images.append(family.expectedPhotoName)
        return missing_images

    def GetReportMsg(self):
        missing_list = self.GetMissingHouseholds()
        message = "%d households are missing pictures\n\n" % len(missing_list)
        for name in missing_list:
            message += name + '\n'
        message += self.GetFamilyOfDuplicateAddressList()
        return message

    def GetImagesReportMsg(self):
        missing_list = self.GetMissingImages()
        message = "The following %d images are missing\n\n" % len(missing_list)
        for name in missing_list:
            message += name + '\n'
        return message

    def GetMissingMsgEmails(self):
        return self.email_recipients.split(',')

    def GetMemberEmails(self):
        email_list = []
        for family in self.MembershipList:
            email_list.extend(family.get_emails_as_list())
        return email_list

    def SetLists(self):
        self.SetNameList(NameType='HoH')
        self.SetNameList(NameType='Parent')

    def GetNameList(self, NameType='HoH'):
        if NameType == 'HoH':
            return self.NameList_HoH
        elif NameType == 'Parent':
            return self.NameList_Parent
        else:
            print "I haven't implimented 'Family' type yet."

    def SetNameList(self, NameType='HoH'):
        # This will return a list of all HeadOfHousehold/Spouses in ward
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
                    if len(member.phone.phone_formatted):
                        return member.phone.phone_formatted
                    else:
                        return household.familyPhone.phone_formatted

    def SendEmails(self):
        if self.email_smtp != '':
            session = smtplib.SMTP(self.email_smtp)
            if self.email_username != '' and self.email_pass != '':
                session.login(user=self.email_username,
                              password=self.email_pass)
            msg = MIMEMultipart()
            msg['From'] = 'Ward Directory Creator <david@ernstrom.net>'
            msg['Subject'] = 'Missing Persons Email'
            msg.attach(MIMEText(self.GetReportMsg()))
            for to_addy in self.GetMissingMsgEmails():
                print to_addy
                msg['To'] = to_addy
                frm = 'Ward Directory Creator <david@ernstrom.net>'
                session.sendmail(from_addr=frm,
                                 to_addrs=to_addy,
                                 msg=msg.as_string())
            session.close()

    def get_extra_images(self, live_folder):
        if live_folder is None:
            return []
        ignore_list = ['Thumbs.db', 'Missing.jpg']
        needed_list = self.GetNeededImageList()
        extra_images = []
        for root, dirs, files in os.walk(live_folder):
            for fname in files:
                if fname not in ignore_list and \
                        fname.lower() not in [x.lower() for x in needed_list]:
                    extra_images.append(fname)
        return extra_images

    def move_extra_images(self, live_folder, archive_folder):
        if not os.path.exists(archive_folder):
            os.mkdir(archive_folder)
        for img in self.get_extra_images(live_folder):
            os.rename(os.path.join(live_folder, img),
                      os.path.join(archive_folder, img))
            print img, "moved to archive"
