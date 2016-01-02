# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import csv


class CSVMembershipReader(object):
    def __init__(self, filename="Greenfield Ward member directory.csv"):
        self.filename = filename
        self.MembershipHandle = None
        self.Household = None

    def __iter__(self):
        self.MembershipHandle = csv.reader(open(self.filename))
        return self

    def next(self):
        self.Household = self.MembershipHandle.next()
        if self.Household[0] == 'familyname':
            self.Household = self.MembershipHandle.next()
        return self.Household
