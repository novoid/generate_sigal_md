#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2019-12-15 16:02:52 vk>

import unittest
import generate_sigal_md
import logging

FORMAT = "%(levelname)-8s %(asctime)-15s %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

# Missing tests:
# - FIXXME: find code which is not tested yet (before 2017-11-11)
# - everything related to tagtrees


class TestMethods(unittest.TestCase):

    def setUp(self):
        pass

    
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
