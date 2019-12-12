#!/usr/bin/env python3
# -*- coding: utf-8 -*-
PROG_VERSION = "Time-stamp: <2019-12-12 17:46:58 vk>"

# TODO:
# - fix parts marked with «FIXXME»


# ===================================================================== ##
#  You might not want to modify anything below this line if you do not  ##
#  know, what you are doing :-)                                         ##
# ===================================================================== ##

from importlib import import_module

def save_import(library):
    try:
        globals()[library] = import_module(library)
    except ImportError:
        print("Could not find Python module \"" + library +
              "\".\nPlease install it, e.g., with \"sudo pip install " + library + "\".")
        sys.exit(2)

import re
import sys
import os
import argparse   # for handling command line arguments
import logging

PROG_VERSION_DATE = PROG_VERSION[13:23]

DESCRIPTION = "This tool extracts meta-data from file names matching the file name convention\n\
from https://karl-voit.at/managing-digital-photographs/. This meta-data is then written to\n\
mark-down files suitable for the web image album tool \"sigal\" in the same directory.\n\
\n\
"

EPILOG = u"\n\
:copyright: (c) by Karl Voit <tools@Karl-Voit.at>\n\
:license: GPL v3 or any later version\n\
:URL: -\n\
:bugreports: via github or <tools@Karl-Voit.at>\n\
:version: " + PROG_VERSION_DATE + "\n·\n"

FILENAME_TAG_SEPARATOR = ' -- '
BETWEEN_TAG_SEPARATOR = ' '

TIMESTAMP_PATTERN = '(?P<datestamp(\d{4,4})-([01]\d)-([0123]\d))[- _T][012]\d\.[012345]\d\.[012345]\d'
FILEDESCRIPTION_PATTERN = '.+?'
FILETAGS_PATTERN = FILENAME_TAG_SEPARATOR.rstrip() + '([ ](?P<filetags>.+))+'
EXTENSION_PATTERN = '\.(?P<extension>\w+)'
FILENAME_PATTERN_REGEX = re.compile('^(?P<timestamp>' + TIMESTAMP_PATTERN + ')[ -_]?' +
                                    '(?P<description>' + FILEDESCRIPTION_PATTERN + ')?' +
                                    '(' + FILETAGS_PATTERN + ')?' +
                                    EXTENSION_PATTERN + '$')

parser = argparse.ArgumentParser(prog=sys.argv[0],
                                 # keep line breaks in EPILOG and such
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=EPILOG,
                                 description=DESCRIPTION)

parser.add_argument(dest="DIR", metavar='DIR', nargs=1, help='Directory that contains the image files to parse')

parser.add_argument("-v", "--verbose",
                    dest="verbose", action="store_true",
                    help="Enable verbose mode")

parser.add_argument("-q", "--quiet",
                    dest="quiet", action="store_true",
                    help="Enable quiet mode")

parser.add_argument("--version",
                    dest="version", action="store_true",
                    help="Display version and exit")

options = parser.parse_args()


def handle_logging():
    """Log handling and configuration"""

    if options.verbose:
        FORMAT = "%(levelname)-8s %(asctime)-15s %(message)s"
        logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    elif options.quiet:
        FORMAT = "%(levelname)-8s %(message)s"
        logging.basicConfig(level=logging.ERROR, format=FORMAT)
    else:
        FORMAT = "%(levelname)-8s %(message)s"
        logging.basicConfig(level=logging.INFO, format=FORMAT)


def error_exit(errorcode, text):
    """exits with return value of errorcode and prints to stderr"""

    sys.stdout.flush()
    logging.error(text)

    sys.exit(errorcode)

def extract_filename_components(filename):

    components = re.match(FILENAME_PATTERN_REGEX, filename)
    if components:
        return components.group('timestamp'), \
            components.group('description'), \
            components.group('filetags'), \
            components.group('extension')
    else:
        return False, False, False, False


def handle_file(filename):
    """
    @param filename: string containing one file name
    @param return: FIXXME
    """

    logging.debug("handle_file(\"" + filename + "\") …  " + '★' * 20)

    if os.path.isdir(DIR):
        error_exit(1, "Skipping directory \"%s\" because this tool only renames file names." % DIR)

def successful_exit():
    logging.debug("successfully finished.")
    sys.stdout.flush()
    sys.exit(0)

def get_md(directory, filename):
    #logging.debug('processing file:  [' + current_file + ']')
    time_stamp, file_description, filetags, extension = extract_filename_components(filename)
    if time_stamp and file_description:
        logging.debug('file  [' + filename + '] has meta-data. Generating md file ...')
        md = "Title: " + file_description + "\n\n"
        # part of sigal output anyway: outputhandle.write("From: " + time_stamp + "\n\n")
        if filetags:
            md += "Tags: " + filetags + "\n"
        return md
    else:
        return None

def main():
    """Main function"""

    if options.version:
        print(os.path.basename(sys.argv[0]) + " version " + PROG_VERSION_DATE)
        sys.exit(0)

    handle_logging()

    if options.verbose and options.quiet:
        error_exit(1, "Options \"--verbose\" and \"--quiet\" found. " +
                   "This does not make any sense, you silly fool :-)")

    directory = options.DIR[0]
    logging.debug('received directory parameter:  [' + directory + ']')
    if not os.path.isdir(directory):
        error_exit(1, "Skipping directory \"%s\" because this tool only renames file names." % directory)
    directory = os.path.abspath(directory)
    logging.debug('processing absolute directory: [' + directory + ']')

    all_files = []
    for (dirpath, dirnames, filenames) in os.walk(directory):
        all_files.extend(filenames)
        break
    logging.debug('found a total of %i files in directory' % len(all_files))

    matching_files = []
    for current_file in all_files:
        metadata = get_md(directory, filename)
        if metadata:
            md_filename = os.path.join(directory, os.path.splitext(filename)[0] + '.md')
            with open(md_filename, 'w') as outputhandle:
                outputhandle.write(metadata)
        else:
            logging.debug('file  [' + current_file + '] has no meta-data. Skipping.')

    successful_exit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:

        logging.info("Received KeyboardInterrupt")

# END OF FILE #################################################################

# end
