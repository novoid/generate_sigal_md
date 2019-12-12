#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2019-12-12 23:19:58 vk>

# invoke tests using following command line:
# ~/src/vktag % PYTHONPATH="~/src/filetags:" tests/unit_tests.py --verbose

import unittest
import os
import generate_sigal_md
#import tempfile
import os.path
import logging

FORMAT = "%(levelname)-8s %(asctime)-15s %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

# Missing tests:
# - FIXXME: find code which is not tested yet (before 2017-11-11)
# - everything related to tagtrees


class TestMethods(unittest.TestCase):

    def setUp(self):
        pass

    def test_extract_filename_components(self):

        self.assertEqual(
            generate_sigal_md.extract_filename_components('2019-12-12T18.01.23 foo bar -- baz1 baz2 baz3.txt'),
            ('2019-12-12T18.01.23', 'foo bar', 'baz1 baz2 baz3', 'txt')
        )

        self.assertEqual(
            generate_sigal_md.extract_filename_components('2019-12-12T18.01 foo bar -- baz1 baz2 baz3.txt'),
            ('2019-12-12T18.01', 'foo bar', 'baz1 baz2 baz3', 'txt')
        )

        self.assertEqual(
            generate_sigal_md.extract_filename_components('2019-12-12 foo bar -- baz1 baz2 baz3.txt'),
            ('2019-12-12', 'foo bar', 'baz1 baz2 baz3', 'txt')
        )

        self.assertEqual(
            generate_sigal_md.extract_filename_components('2019-12-12T18.01.23 foo bar -- baz.txt'),
            ('2019-12-12T18.01.23', 'foo bar', 'baz', 'txt')
        )

        self.assertEqual(
            generate_sigal_md.extract_filename_components('2019-12-12T18.01 foo bar -- baz.txt'),
            ('2019-12-12T18.01', 'foo bar', 'baz', 'txt')
        )

        self.assertEqual(
            generate_sigal_md.extract_filename_components('2019-12-12 foo bar -- baz.txt'),
            ('2019-12-12', 'foo bar', 'baz', 'txt')
        )

        self.assertEqual(
            generate_sigal_md.extract_filename_components('2019-12-12T18.01.23 -- baz.txt'),
            ('2019-12-12T18.01.23', None, 'baz', 'txt')
        )

        self.assertEqual(
            generate_sigal_md.extract_filename_components('2019-12-12T18.01 -- baz.txt'),
            ('2019-12-12T18.01', None, 'baz', 'txt')
        )

        self.assertEqual(
            generate_sigal_md.extract_filename_components('2019-12-12 -- baz.txt'),
            ('2019-12-12', None, 'baz', 'txt')
        )

        self.assertEqual(
            generate_sigal_md.extract_filename_components('2019-12-12T18.01.23 foo bar.txt'),
            ('2019-12-12T18.01.23', 'foo bar', None, 'txt')
        )

        self.assertEqual(
            generate_sigal_md.extract_filename_components('2019-12-12T18.01 foo bar.txt'),
            ('2019-12-12T18.01', 'foo bar', None, 'txt')
        )

        self.assertEqual(
            generate_sigal_md.extract_filename_components('2019-12-12 foo bar.txt'),
            ('2019-12-12', 'foo bar', None, 'txt')
        )

        self.assertEqual(
            generate_sigal_md.extract_filename_components('2019-12-12T18.01.23.txt'),
            ('2019-12-12T18.01.23', None, None, 'txt')
        )

        self.assertEqual(
            generate_sigal_md.extract_filename_components('2019-12-12T18.01.txt'),
            ('2019-12-12T18.01', None, None, 'txt')
        )

        self.assertEqual(
            generate_sigal_md.extract_filename_components('2019-12-12.txt'),
            ('2019-12-12', None, None, 'txt')
        )


    def test_get_md(self):

        self.assertEqual(
            generate_sigal_md.get_md('2019-12-12T18.01.23.txt'),
            """Title: -

Tags: -
"""
        )

        self.assertEqual(
            generate_sigal_md.get_md('2019-12-12T18.01.23 foo bar -- baz1 baz2 baz3.txt'),
            """Title: foo bar

Tags: baz1 baz2 baz3
"""
        )

        self.assertEqual(
            generate_sigal_md.get_md('2019-12-12T18.01.23 -- baz.txt'),
            """Title: -

Tags: baz
"""
        )

        self.assertEqual(
            generate_sigal_md.get_md('2019-12-12T18.01.23 foo bar.txt'),
            """Title: foo bar

Tags: -
"""
        )


if __name__ == '__main__':
    unittest.main()
