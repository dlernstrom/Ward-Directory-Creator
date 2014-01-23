import csv

class Dwelling:
    index = None
    def __init__(self, dwellingDict):
        ['Longitude','Latitude','Street','City','State','Zip']
        keys = dwellingDict.keys()
        for key in keys:
            setattr(self, key, dwellingDict[key])
        self.Longitude = float(self.Longitude)
        self.Latitude = float(self.Latitude)
        self.dwellingDict = dwellingDict
        self.addressForCompare = '%s\n%s, %s %s' % (self.Street.replace(',', ''), self.City, self.State, self.Zip)

    def __repr__(self):
        return '%s\n%s, %s %s' % (self.Street, self.City, self.State, self.Zip)

    def save_index(self, index):
        self.index = index

class Dwellings:
    dwellingList = []
    def __init__(self):
        self.dwellingsFname = 'C:\\Users\\dlernstrom\\Desktop\\DirectoryCherryCreek\\Cherry_Creek_Dwellings.csv'
        self.read_from_file()

    """
    def __del__(self):
        self.write_to_file()
    """

    def read_from_file(self):
        reader = csv.DictReader(open(self.dwellingsFname))
        try:
            while True:
                self.add_dwelling_if_unique(Dwelling(reader.next()))
        except StopIteration:
            pass

    def add_dwelling_if_unique(self, d):
        for currDwelling in self.dwellingList:
            if str(currDwelling) == str(d):
                print "Dwelling already exists!"
                print currDwelling
                return
        self.dwellingList.append(d)

    def write_to_file(self):
        writer = csv.DictWriter(open(self.dwellingsFname, 'wb'), ["Longitude","Latitude","Street","City","State","Zip"])
        writer.writeheader()
        for d in self.dwellingList:
            writer.writerow(d.dwellingDict)

    def find_map_index_for_household(self, household):
        for d in self.dwellingList:
            #print "Comparing H:\n[%s] to D:\n[%s]" % (household.familyAddress, d.addressForCompare)
            if household.familyAddress == d.addressForCompare:
                return d.index
        return None