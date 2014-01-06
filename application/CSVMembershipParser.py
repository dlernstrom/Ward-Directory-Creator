import CSVMembershipReader

class NoPersonError(Exception):
    """ Exception raised when there isn't really a person at this location."""
    
class Phone:
    def __init__(self, phoneCSV):
        phoneStripped = phoneCSV.replace(' ', '').replace('(', '').replace(')', '')\
            .replace('-', '').replace('.', '')
        if len(phoneStripped) == 0:
            self.phoneFormatted = ''
            return
        if phoneStripped[0] == '1':
            phoneStripped = phoneStripped[1:]
        if len(phoneStripped) == 7:
            phoneStripped = '435' + phoneStripped
        self.phoneFormatted = '(%s) %s-%s' % (phoneStripped[:3],
                                              phoneStripped[3:6],
                                              phoneStripped[6:])
    def __str__(self):
        return self.phoneFormatted

class EmailAddress:
    def __init__(self, emailAddress, name):
        emailAddress = emailAddress.split(' ')[0].split(',')[0].split('\r')[0].split('\n')[0]
        self.emailAddress = emailAddress
        if not len(emailAddress):
            self.emailFormatted = ''
        else:
            name = '%s %s' % (name.split(',')[1].strip(),
                              name.split(',')[0].strip().upper())
            self.emailFormatted = '%s <%s>' % (name, emailAddress)

class FamilyMember:
    """ a family member. """
    def __init__(self, familyCSV, startEntry, isParent = False):
        self.isParent = isParent
        familySurname = familyCSV[0]
        try:
            self.nameCSV = familyCSV[startEntry]
        except IndexError:
            raise NoPersonError("No Person")
        self.fullName = familyCSV[startEntry]
        if self.nameCSV == '':
            raise NoPersonError("No person")
        # remove family surname from this member's name
        self.nameCSV = self.nameCSV.replace(familySurname + ', ', '')
        # move remaining individual surname to end
        if len(self.nameCSV.split(',')) > 1:
            self.nameCSV = '%s %s' % (self.nameCSV.split(',')[1].strip(),
                                      self.nameCSV.split(',')[0].strip().upper())
        self.phone = Phone(familyCSV[startEntry + 1])
        self.email = EmailAddress(familyCSV[startEntry + 2], self.fullName)
    def __str__(self):
        return self.nameCSV

class Family:
    """ a container of one or more family members """
    def __init__(self, familyCSV):
        self.surname = familyCSV[0]
        self.coupleName = familyCSV[1]
        self.familyPhone = Phone(familyCSV[2])
        self.familyEmail = EmailAddress(familyCSV[3], self.coupleName)
        self.familyAddress = familyCSV[4].replace(' PO', '\nP.O.')\
            .replace(' p.o.', '\nP.o.')\
            .replace(' P.O.', '\nP.O.')\
            .replace(' Rich', '\nRich')\
            .replace(' RIch', '\nRich')\
            .replace(' Cove', '\nCove')
        self.family = []
        self.family.append(FamilyMember(familyCSV, 5, isParent = True))
        self.head_of_household = self.family[0]
        self.parents = [self.head_of_household]
        self.expectedPhotoName = self.head_of_household.fullName.replace(',', '').replace(' ', '') + '.jpg'
        try:
            self.family.append(FamilyMember(familyCSV, 8, isParent = True))
            self.parents.append(self.family[-1])
        except NoPersonError:
            pass
        try:
            nextValue = 11
            while True:
                self.family.append(FamilyMember(familyCSV, nextValue))
                nextValue += 3
        except NoPersonError:
            pass
    def get_emails_as_list(self):
        emails = []
        if len(self.familyEmail.emailFormatted):
            emails.append(self.familyEmail.emailFormatted)
        for member in self.family:
            if len(member.email.emailFormatted):
                emails.append(member.email.emailFormatted)
        return emails

class CSVMembershipParser:
    def __init__(self, filename = "Greenfield Ward member directory.csv"):
        self.filename = filename
        self.MembershipHandle = CSVMembershipReader.CSVMembershipReader(self.filename)

    def next(self):
        try:
            for familyData in self.MembershipHandle:
                if familyData[0] == 'Family Name':
                    continue
                yield Family(familyData)
        except IOError:
            return

if __name__ == '__main__':
    CSV_LOCATION = 'C:\\Documents and Settings\\Administrator\\Desktop\\Directory\\'
    Handle = CSVMembershipParser(CSV_LOCATION + "Greenfield Ward member directory.csv")
    for Family in Handle.next():
        print Family