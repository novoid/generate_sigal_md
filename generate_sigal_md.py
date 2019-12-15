#!/usr/bin/env python3
# -*- coding: utf-8 -*-
PROG_VERSION = "Time-stamp: <2019-12-15 16:03:45 vk>"

# TODO:
# - fix parts marked with «FIXXME»


# ===================================================================== ##
#  You might not want to modify anything below this line if you do not  ##
#  know, what you are doing :-)                                         ##
# ===================================================================== ##

from importlib import import_module
from filetagslib import filenameconvention

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


def successful_exit():
    logging.debug("successfully finished.")
    sys.stdout.flush()
    sys.exit(0)


def get_md(filename):
    """
    Derive meta-data (date- or time-stamp, title) from a file name.

    @param filename: string containing the file name
    @param return: string with the formatted meta-data
    """
    # logging.debug('processing file:  [' + current_file + ']')
    components = re.match(filenameconvention.FILENAME_PATTERN_REGEX, filename)
    datetimestamp = components.group('datetimestamp')
    description = components.group('description')
    filetags = components.group('filetags')
    extension = components.group('extension')

    if datetimestamp:
        logging.debug('file  [' + filename + '] has meta-data. Generating md file ...')
        if description:
            md = "Title: " + description + "\n\n"
        else:
            md = "Title: -\n\n"
        # part of sigal output anyway: outputhandle.write("From: " + time_stamp + "\n\n")
        if filetags:
            md += "Tags: " + filetags + "\n"
        else:
            md += "Tags: -\n"
        return md
    else:
        return None


def handle_file(directory, filename):
    """
    Handles one file: retrieving the meta-data string and writing to the meta-data file if meta-data were retrieved.

    @param directory: string containing the directory of the file
    @param filename: string containing the file name
    @param return: None
    """

    logging.debug("handle_file(\"" + filename + "\") …  " + '★' * 20)
    abs_filename = os.path.join(directory, filename)

    if os.path.isdir(abs_filename):
        logging.warning("Skipping directory \"%s\" because this tool only renames file names." % directory)
        return

    metadata = get_md(filename)
    if metadata:
        md_filename = os.path.join(directory, os.path.splitext(filename)[0] + '.md')
        with open(md_filename, 'w') as outputhandle:
            outputhandle.write(metadata)
    else:
        logging.debug('file  [' + filename + '] has no meta-data. Skipping.')


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
    # logging.debug('files: ' + str(all_files))

    for current_file in all_files:
        handle_file(directory, current_file)

    successful_exit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:

        logging.info("Received KeyboardInterrupt")

# END OF FILE #################################################################

# end
