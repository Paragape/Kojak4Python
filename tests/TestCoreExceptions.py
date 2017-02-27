"""
Created on February 10, 2017

@author: John Jackson
"""

import unittest
from kojak.core.Exceptions import AbortException
from kojak.core.Exceptions import HardException
from kojak.core.Exceptions import SoftException


class TestCoreExceptions(unittest.TestCase):

    ####################################################################################################
    # CLASS - AbortException
    ####################################################################################################

    def test_class_AbortException(self):

        def raiseAbortException(message: str):
            raise AbortException(message)

        self.assertRaisesRegex(AbortException, "^AbortException: foobar$", raiseAbortException, "foobar")

    ####################################################################################################
    # CLASS - HardException
    ####################################################################################################

    def test_class_HardException(self):

        def raiseHardException(message: str):
            raise HardException(message)

        self.assertRaisesRegex(HardException, "^HardException: foobar$", raiseHardException, "foobar")

    ####################################################################################################
    # CLASS - SoftException
    ####################################################################################################

    def test_class_SoftException(self):

        def raiseSoftException(message: str):
            raise SoftException(message)

        self.assertRaisesRegex(SoftException, "^SoftException: foobar$", raiseSoftException, "foobar")
