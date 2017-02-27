"""
Created on February 21, 2017

@author: John Jackson
"""

import unittest
from kojak.core.utilities.AccountNumberMasker import AccountNumberMasker


class TestCoreUtilitiesAccountNumberMasker(unittest.TestCase):

    #####################################################################################################
    # METHOD - maskNumber
    #####################################################################################################

    def test_method_maskNumber(self):

        masker = AccountNumberMasker()
        self.assertEqual('Mask: 4-*-4', str(masker))

        self.assertEqual('', masker.maskNumber(''))
        self.assertEqual('1', masker.maskNumber('1'))
        self.assertEqual('12', masker.maskNumber('12'))
        self.assertEqual('123', masker.maskNumber('123'))
        self.assertEqual('1234', masker.maskNumber('1234'))
        self.assertEqual('12345', masker.maskNumber('12345'))
        self.assertEqual('123456', masker.maskNumber('123456'))
        self.assertEqual('1234567', masker.maskNumber('1234567'))
        self.assertEqual('12345678', masker.maskNumber('12345678'))
        self.assertEqual('1234*6789', masker.maskNumber('123456789'))
        self.assertEqual('1234**7890', masker.maskNumber('1234567890'))
        self.assertEqual('1234***8901', masker.maskNumber('12345678901'))
        self.assertEqual('1234****9012', masker.maskNumber('123456789012'))
        self.assertEqual('1234*****0123', masker.maskNumber('1234567890123'))
        self.assertEqual('1234******1234', masker.maskNumber('12345678901234'))
        self.assertEqual('1234*******2345', masker.maskNumber('123456789012345'))
        self.assertEqual('1234********3456', masker.maskNumber('1234567890123456'))
        self.assertEqual('1234*********4567', masker.maskNumber('12345678901234567'))
        self.assertEqual('1234**********5678', masker.maskNumber('123456789012345678'))
        self.assertEqual('1234***********6789', masker.maskNumber('1234567890123456789'))
        self.assertEqual('1234************7890', masker.maskNumber('12345678901234567890'))

    def test_method_maskNumber_first_m(self):
        masker = AccountNumberMasker(first_m=-1)
        self.assertEqual('Mask: 0-*-4', str(masker))
        self.assertEqual('************3456', masker.maskNumber('1234567890123456'))

        masker = AccountNumberMasker(first_m=0)
        self.assertEqual('Mask: 0-*-4', str(masker))
        self.assertEqual('************3456', masker.maskNumber('1234567890123456'))

        masker = AccountNumberMasker(first_m=1)
        self.assertEqual('Mask: 1-*-4', str(masker))
        self.assertEqual('1***********3456', masker.maskNumber('1234567890123456'))

        masker = AccountNumberMasker(first_m=5)
        self.assertEqual('Mask: 5-*-4', str(masker))
        self.assertEqual('12345*******3456', masker.maskNumber('1234567890123456'))

    def test_method_maskNumber_last_n(self):
        masker = AccountNumberMasker(last_n=-1)
        self.assertEqual('Mask: 4-*-0', str(masker))
        self.assertEqual('1234************', masker.maskNumber('1234567890123456'))

        masker = AccountNumberMasker(last_n=0)
        self.assertEqual('Mask: 4-*-0', str(masker))
        self.assertEqual('1234************', masker.maskNumber('1234567890123456'))

        masker = AccountNumberMasker(last_n=1)
        self.assertEqual('Mask: 4-*-1', str(masker))
        self.assertEqual('1234***********6', masker.maskNumber('1234567890123456'))

        masker = AccountNumberMasker(last_n=5)
        self.assertEqual('Mask: 4-*-5', str(masker))
        self.assertEqual('1234*******23456', masker.maskNumber('1234567890123456'))

    def test_method_maskNumber_mask_character(self):
        masker = AccountNumberMasker(mask_character='0')
        self.assertEqual('Mask: 4-0-4', str(masker))
        self.assertEqual('1234000000003456', masker.maskNumber('1234567890123456'))

        masker = AccountNumberMasker(mask_character='#')
        self.assertEqual('Mask: 4-#-4', str(masker))
        self.assertEqual('1234########3456', masker.maskNumber('1234567890123456'))

        masker = AccountNumberMasker(mask_character='#ABC')
        self.assertEqual('Mask: 4-#-4', str(masker))
        self.assertEqual('1234########3456', masker.maskNumber('1234567890123456'))

        masker = AccountNumberMasker(mask_character='')
        self.assertEqual('Mask: 4-*-4', str(masker))
        self.assertEqual('1234********3456', masker.maskNumber('1234567890123456'))
