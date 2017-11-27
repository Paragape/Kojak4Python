"""
Created on February 10, 2017

@author: John Jackson
"""

import re
import unittest

from kojak.core.exceptions import AbortException
from kojak.core.exceptions import HardException
from kojak.core.exceptions import SoftException


###############################################################################
# TEST AbortException
###############################################################################

class TestAbortException(unittest.TestCase):

    # =========================================================================
    # METHOD - CONSTRUCTOR
    # =========================================================================

    def test_CONSTRUCTOR(self):

        def raise_exception(message: str):
            raise AbortException(message)

        msg = 'AbortException: message'
        self.assertRaisesRegex(
            AbortException,
            '^' + re.escape(msg) + '$',
            raise_exception, 'message')


###############################################################################
# TEST HardException
###############################################################################

class TestHardException(unittest.TestCase):

    # =========================================================================
    # METHOD - CONSTRUCTOR
    # =========================================================================

    def test_CONSTRUCTOR(self):

        def raise_exception(message: str):
            raise HardException(message)

        msg = 'HardException: message'
        self.assertRaisesRegex(
            HardException,
            '^' + re.escape(msg) + '$',
            raise_exception, 'message')


###############################################################################
# TEST SoftException
###############################################################################

class TestSoftException(unittest.TestCase):

    # =========================================================================
    # METHOD - CONSTRUCTOR
    # =========================================================================

    def test_CONSTRUCTOR(self):

        def raise_exception(message: str):
            raise SoftException(message)

        msg = 'SoftException: message'
        self.assertRaisesRegex(
            SoftException,
            '^' + re.escape(msg) + '$',
            raise_exception, 'message')
