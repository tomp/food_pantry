#!/usr/bin/env python
#
#  Read and work with OLS Caritas 2014-2015 directory
#
import os
import sys
import re
import argparse
import logging

logging.basicConfig(format="%(message)s")
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

from openpyxl import load_workbook

import django
django.setup()
from clients.models import Person, Client, Household, Visit

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
