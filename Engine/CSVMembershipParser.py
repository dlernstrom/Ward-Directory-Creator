# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from . import CSVMembershipReader


class NoPersonError(Exception):
    """ Exception raised when there isn't really a person at this location."""


class Phone(object):
    def __init__(self, phoneCSV):
        phone_stripped = phoneCSV.replace(' ', '').replace('(', '') \
            .replace(')', '') \
            .replace('-', '').replace('.', '')
        if len(phone_stripped) == 0:
            self.phone_formatted = ''
            return
        if phone_stripped[0] == '1':
            phone_stripped = phone_stripped[1:]
        if len(phone_stripped) == 7:
            phone_stripped = '435' + phone_stripped
        self.phone_formatted = '(%s) %s-%s' % (phone_stripped[:3],
                                               phone_stripped[3:6],
                                               phone_stripped[6:])
    def __str__(self):
        return self.phone_formatted


class EmailAddress(object):
    def __init__(self, email_addy, name):
        email_addy = email_addy.split(' ')[0].split(',')[0] \
            .split('\r')[0].split('\n')[0]
        self.email_addy = email_addy
        if not len(email_addy):
            self.email_formatted = ''
        else:
            name = '%s %s' % (name.split(',')[1].strip(),
                              name.split(',')[0].strip().upper())
            self.email_formatted = '%s <%s>' % (name, email_addy)


class FamilyMember(object):
    def __init__(self, familyCSV, startEntry, is_parent=False):
        self.is_parent = is_parent
        fam_surname = familyCSV[0]
        try:
            self.nameCSV = familyCSV[startEntry]
        except IndexError:
            raise NoPersonError("No Person")
        self.fullName = familyCSV[startEntry]
        if self.nameCSV == '':
            raise NoPersonError("No person")
        # remove family surname from this member's name
        self.nameCSV = self.nameCSV.replace(fam_surname + ', ', '')
        # move remaining individual surname to end
        if len(self.nameCSV.split(',')) > 1:
            self.nameCSV = '%s %s' % (
                self.nameCSV.split(',')[1].strip(),
                self.nameCSV.split(',')[0].strip().upper())
        self.phone = Phone(familyCSV[startEntry + 1])
        self.email = EmailAddress(familyCSV[startEntry + 2], self.fullName)
    def __str__(self):
        return self.nameCSV


class Family(object):
    """a container of one or more family members"""
    mapIndexString = ''
    def __init__(self, familyCSV, isMember):
        self.isMember = isMember
        self.surname = familyCSV[0]
        self.coupleName = familyCSV[1]
        self.familyPhone = Phone(familyCSV[2])
        self.familyEmail = EmailAddress(familyCSV[3], self.coupleName)
        self.familyAddress = familyCSV[4].replace(' PO', '\nP.O.')\
            .replace(' p.o.', '\nP.o.')\
            .replace(' P.O.', '\nP.O.')\
            .replace(' Rich', '\nRich')\
            .replace(' RIch', '\nRich')\
            .replace(' Cove', '\nCove').strip()
        self.family = []
        self.family.append(FamilyMember(familyCSV, 5, is_parent=True))
        self.head_of_household = self.family[0]
        self.parents = [self.head_of_household]
        self.expectedPhotoName = self.head_of_household.fullName \
            .replace(',', '').replace(' ', '') + '.jpg'
        try:
            self.family.append(FamilyMember(familyCSV, 8, is_parent=True))
            self.parents.append(self.family[-1])
        except NoPersonError:
            pass
        try:
            next_val = 11
            while True:
                self.family.append(FamilyMember(familyCSV, next_val))
                next_val += 3
        except NoPersonError:
            pass

    def __unicode__(self):
        return self.coupleName

    def get_emails_as_list(self):
        emails = []
        if len(self.familyEmail.email_formatted):
            emails.append(self.familyEmail.email_formatted)
        for member in self.family:
            if len(member.email.email_formatted):
                emails.append(member.email.email_formatted)
        return emails

    def set_map_index(self, index):
        if index != None:
            self.mapIndexString = 'Map Index: %s' % index

    def __repr__(self):
        return self.coupleName


class CSVMembershipParser(object):
    def __init__(self, filename):
        self.filename = filename
        self.MembershipHandle = CSVMembershipReader.CSVMembershipReader(
            self.filename)

    def next(self):
        is_member = True
        if 'non' in self.filename:
            is_member = False
        try:
            for familyData in self.MembershipHandle:
                if familyData[0] == 'Family Name':
                    continue
                yield Family(familyData, isMember=is_member)
        except IOError:
            return
