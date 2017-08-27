#!/usr/bin/env python
#
#  Read and work with OLS Caritas 2014-2015 directory
#
import os
import sys
import re
from datetime import datetime
import argparse
import logging

logging.basicConfig(format="%(message)s")
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

from openpyxl import load_workbook
from openpyxl.utils import coordinate_to_tuple

import django
django.setup()
from clients import models

# Constants
CURRENT_SHEET = 'New Data'
NEW_ID_COL = 'New ID #'
NOTES_COL = 'Notes'
AGE7_COL = '#7 age'

# Globals
dry_run = False

#######################################################################
# Classes
#######################################################################

class Person(object):
    def __init__(self, last_name=None, first_name=None,
        name=None, dob=None, gender=None, household=None):
        if name:
            last_name, first_name = name.split(',', 1)
        self.last_name = last_name
        self.first_name = first_name
        if dob:
            self.dob = dob.date()
        else:
            self.dob = None
        if gender:
            self.gender = gender
        else:
            self.gender = ''
        self.household = household
        self._id = None
        self._obj = None

    def __repr__(self):
        if self.dob:
            return "<{} {} ({}) b.{}>".format(self.first_name, self.last_name,
                    self.gender, self.dob.strftime("%b %d, %Y"))
        else:
            return "<{} {} ({})>".format(self.first_name, self.last_name, self.gender)

    def __unicode__(self):
        return self.first_name + " " + self.last_name

    @property
    def obj(self):
        """
        Return the corresponding model object from the database.
        If there's no database id, a new object will added to the database;
        otherwise, the existing item is fetched.
        """
        if not self._obj:
            if self._id is not None:
                self._obj = models.Person.objects.filter(pk=self._id)[0]
            else:
                self._obj = models.Person(firstname=self.first_name,
                        lastname=self.last_name, dob=self.dob,
                        gender=self.gender, household=self.household.obj)
                if not dry_run:
                    self._obj.save()
                    self._id = self._obj.id
        return self._obj

    def store(self):
        self.obj.save()


class Client(object):
    def __init__(self, person=None, newId=None, reg_notes="", notes=""):
        self.person = person
        self.reg_notes = reg_notes if reg_notes else ""
        self.notes = notes if notes else ""
        self.newId = str(newId) if newId else None
        self._id = None
        self._obj = None

    def __repr__(self):
        return "<client #{} - {}>".format(self.newId, str(self.person))

    def __unicode__(self):
        return "client {}: {}".format(self.newId, str(self.client))

    @property
    def obj(self):
        """
        Return the corresponding model object from the database.
        If there's no database id, a new object will added to the database;
        otherwise, the existing item is fetched.
        """
        if not self._obj:
            if self._id is not None:
                self._obj = models.Client.objects.filter(pk=self._id)[0]
            else:
                self._obj = models.Client(person=self.person.obj,
                        newId=self.newId, notes=self.notes)
                if not dry_run:
                    self._obj.save()
                    self._id = self._obj.id
        return self._obj

    def store(self):
        self.obj.save()

class Household(object):
    def __init__(self, address=None, city=None, client=None, members=None):
        self.address = address
        self.city = city
        if members:
            self.members = members
        else:
            self.members = []
        for member in self.members:
            member.household = self
        self.client = client
        if client:
            client.household = self
        self._id = None
        self._obj = None

    def __repr__(self):
        return "<{} household @ {}, {}>".format(str(self.client), self.address, self.city)

    def __unicode__(self):
        return str(self.client) + " household"

    @property
    def obj(self):
        """
        Return the corresponding model object from the database.
        If there's no database id, a new object will added to the database;
        otherwise, the existing item is fetched.
        """
        if not self._obj:
            if self._id is not None:
                self._obj = models.Household.objects.filter(pk=self._id)[0]
            else:
                self._obj = models.Household(address=self.address,
                        city=self.city)
                if not dry_run:
                    self._obj.save()
                    self._id = self._obj.id
        return self._obj

    def store(self):
        self.obj.save()


#######################################################################
# Main code
#######################################################################

def load_spreadsheet(infile, dryrun=False):
    """Load the client data from the specified spreadsheet.
    If dryrun is True, don't update the django database.
    """
    wb = load_workbook(infile)
    log.info("Opened '{}'".format(infile))

    sheet_names = wb.get_sheet_names()
    log.debug("Found {} sheets:".format(len(sheet_names)))
    for name in sheet_names:
        log.debug("- '{}'".format(name))

    ws = wb[CURRENT_SHEET]
    log.debug("Loaded '{}' sheet".format(CURRENT_SHEET))

    log.debug("Rows: {} - {}\tColumns: {} - {}".format(
        ws.min_row, ws.max_row, ws.min_column, ws.max_column))

    # Check that expected columns exist
    col_names =  [c[0].value for c in ws.iter_cols(min_row=1, max_row=1)]
    for idx, name in enumerate(col_names):
        log.debug("column {:2d}: '{}'".format(idx+1, name))
    assert NEW_ID_COL in col_names
    # assert NOTES_COL in col_names
    assert AGE7_COL in col_names
    newid_idx = col_names.index(NEW_ID_COL) + 1
    idNotes_idx = newid_idx + 1
    distNotes_idx = col_names.index(AGE7_COL) + 2

    # Load client data, row by row
    for row in ws.iter_rows(min_row=2):
        last_name, first_name, gender, dob = [c.value for c in row[:4]]
        address, city = [c.value for c in row[4:6]]

        if not (first_name and last_name):
            break
        household = Household(address=address, city=city)
        household.store()

        person = Person(last_name=last_name, first_name=first_name,
                gender=gender, dob=dob, household=household)
        person.store()
        log.debug("Loaded client {}".format(person))

        newId = row[newid_idx].value
        idNotes = row[idNotes_idx].value
        distNotes = row[distNotes_idx].value
        client = Client(person=person, newId=newId, notes=distNotes, reg_notes=idNotes)
        client.store()


def reset_database():
    Person.objects.all().delete()
    Client.objects.all().delete()
    Household.objects.all().delete()
    Visit.objects.all().delete()

def parse_args(args):
    """
    Parse the commandline options.
    A namespace object is returned.
    """
    parser = argparse.ArgumentParser(
            "Load food pantry data from Rebecca's Excel spreadsheet")
    parser.add_argument("--infile", "-i",
            help="An Excel spreadsheet with client data")
    parser.add_argument("--reset", action='store_true',
            help="An Excel spreadsheet with client data")
    parser.add_argument("--dry-run", dest="dryrun", action="store_true",
            help="Process the spreadsheet, but don't populate the database.")
    opt = parser.parse_args()
    return opt

def main(args):
    opt = parse_args(args)

    if opt.reset:
        reset_database

    load_spreadsheet(opt.infile)


if __name__ == '__main__':
    import pdb
    try:
        main(sys.argv[1:])
    except Exception:
        # pdb.post_mortem()
        raise
