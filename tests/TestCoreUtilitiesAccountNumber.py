"""
Created on February 12, 2017

@author: John Jackson
"""

import unittest
from kojak.core.utilities.AccountNumber import AccountNumber
from kojak.core.utilities.AccountNumberMasker import AccountNumberMasker


class TestCoreUtilitiesAccountNumber(unittest.TestCase):

    #####################################################################################################
    # METHOD - CONSTRUCTOR
    #####################################################################################################

    def test_method_constructor(self):

        acct_num = AccountNumber('')
        self.assertEqual("'' (cvv='' cvv_bad='' masked='' bank_name='' bank_display_name='' routing_number='')", str(acct_num))
        self.assertEqual('', acct_num.getBankDisplayName())
        self.assertEqual('', acct_num.getBankName())
        self.assertEqual('', acct_num.getClearTextNumber())
        self.assertEqual('', acct_num.getCVV())
        self.assertEqual('', acct_num.getCVVBad())
        self.assertEqual(0, acct_num.getCVVLength())
        self.assertEqual('', acct_num.getMaskedNumber())
        self.assertIsNone(acct_num.getMasker())
        self.assertEqual('', acct_num.getRoutingNumber())

        acct_num = AccountNumber('1')
        self.assertEqual("'1' (cvv='1' cvv_bad='2' masked='1' bank_name='' bank_display_name='' routing_number='')", str(acct_num))
        self.assertEqual('1', acct_num.getClearTextNumber())
        self.assertEqual('1', acct_num.getCVV())
        self.assertEqual('2', acct_num.getCVVBad())
        self.assertEqual(1, acct_num.getCVVLength())
        self.assertEqual('1', acct_num.getMaskedNumber())

        acct_num = AccountNumber('12')
        self.assertEqual("'12' (cvv='12' cvv_bad='13' masked='12' bank_name='' bank_display_name='' routing_number='')", str(acct_num))

        acct_num = AccountNumber('123')
        self.assertEqual("'123' (cvv='123' cvv_bad='124' masked='123' bank_name='' bank_display_name='' routing_number='')", str(acct_num))

        acct_num = AccountNumber('1234')
        self.assertEqual("'1234' (cvv='234' cvv_bad='235' masked='1234' bank_name='' bank_display_name='' routing_number='')", str(acct_num))

        acct_num = AccountNumber('12345')
        self.assertEqual("'12345' (cvv='345' cvv_bad='346' masked='12345' bank_name='' bank_display_name='' routing_number='')", str(acct_num))

        acct_num = AccountNumber('123456')
        self.assertEqual("'123456' (cvv='456' cvv_bad='457' masked='123456' bank_name='' bank_display_name='' routing_number='')", str(acct_num))

        acct_num = AccountNumber('1234567')
        self.assertEqual("'1234567' (cvv='567' cvv_bad='568' masked='1234567' bank_name='' bank_display_name='' routing_number='')", str(acct_num))

        acct_num = AccountNumber('12345678')
        self.assertEqual("'12345678' (cvv='678' cvv_bad='679' masked='12345678' bank_name='' bank_display_name='' routing_number='')", str(acct_num))

        acct_num = AccountNumber('123456789')
        self.assertEqual("'123456789' (cvv='789' cvv_bad='790' masked='123456789' bank_name='' bank_display_name='' routing_number='')", str(acct_num))

        acct_num = AccountNumber('1234567890')
        self.assertEqual("'1234567890' (cvv='890' cvv_bad='891' masked='1234567890' bank_name='' bank_display_name='' routing_number='')", str(acct_num))

        acct_num = AccountNumber(clear_text_account_number='373412345678900')
        self.assertEqual("'373412345678900' (cvv='900' cvv_bad='901' masked='373412345678900' bank_name='' bank_display_name='' routing_number='')", str(acct_num))

    def test_method_constructor_bank_display_name(self):
        acct_num = AccountNumber('', bank_display_name='foobar')
        self.assertEqual("'' (cvv='' cvv_bad='' masked='' bank_name='' bank_display_name='foobar' routing_number='')", str(acct_num))
        self.assertEqual('foobar', acct_num.getBankDisplayName())

    def test_method_constructor_bank_name(self):
        acct_num = AccountNumber('', bank_name='foobar')
        self.assertEqual("'' (cvv='' cvv_bad='' masked='' bank_name='foobar' bank_display_name='' routing_number='')", str(acct_num))
        self.assertEqual('foobar', acct_num.getBankName())

    def test_method_constructor_cvv(self):
        # Test that cvv_bad retains leading zero.
        acct_num = AccountNumber('1234567890', cvv='01')
        self.assertEqual("'1234567890' (cvv='01' cvv_bad='02' masked='1234567890' bank_name='' bank_display_name='' routing_number='')", str(acct_num))
        self.assertEqual('01', acct_num.getCVV())
        self.assertEqual('02', acct_num.getCVVBad())
        self.assertEqual(2, acct_num.getCVVLength())

        # Test that cvv_bad retains length not equal to default value.
        acct_num = AccountNumber('1234567890', cvv='4567')
        self.assertEqual("'1234567890' (cvv='4567' cvv_bad='4568' masked='1234567890' bank_name='' bank_display_name='' routing_number='')", str(acct_num))
        self.assertEqual('4567', acct_num.getCVV())
        self.assertEqual('4568', acct_num.getCVVBad())
        self.assertEqual(4, acct_num.getCVVLength())

        # Test that cvv_bad wraps to zero and retains proper length.
        acct_num = AccountNumber('1234567890', cvv='9999', cvv_length=1)
        self.assertEqual("'1234567890' (cvv='9999' cvv_bad='0000' masked='1234567890' bank_name='' bank_display_name='' routing_number='')", str(acct_num))
        self.assertEqual('9999', acct_num.getCVV())
        self.assertEqual('0000', acct_num.getCVVBad())
        self.assertEqual(4, acct_num.getCVVLength())

    def test_method_constructor_cvv_bad(self):
        # Test that explicit cvv_bad overrides default.
        acct_num = AccountNumber('1234567890', cvv='4567', cvv_bad='1111')
        self.assertEqual("'1234567890' (cvv='4567' cvv_bad='1111' masked='1234567890' bank_name='' bank_display_name='' routing_number='')", str(acct_num))
        self.assertEqual('4567', acct_num.getCVV())
        self.assertEqual('1111', acct_num.getCVVBad())
        self.assertEqual(4, acct_num.getCVVLength())

    def test_method_constructor_cvv_length(self):
        acct_num = AccountNumber('1234567890', cvv_length=-1)
        self.assertEqual("'1234567890' (cvv='890' cvv_bad='891' masked='1234567890' bank_name='' bank_display_name='' routing_number='')", str(acct_num))
        self.assertEqual('890', acct_num.getCVV())
        self.assertEqual('891', acct_num.getCVVBad())
        self.assertEqual(3, acct_num.getCVVLength())

        acct_num = AccountNumber('1234567890', cvv_length=0)
        self.assertEqual("'1234567890' (cvv='' cvv_bad='' masked='1234567890' bank_name='' bank_display_name='' routing_number='')", str(acct_num))
        self.assertEqual('', acct_num.getCVV())
        self.assertEqual('', acct_num.getCVVBad())
        self.assertEqual(0, acct_num.getCVVLength())

        acct_num = AccountNumber('1234567890', cvv_length=1)
        self.assertEqual("'1234567890' (cvv='0' cvv_bad='1' masked='1234567890' bank_name='' bank_display_name='' routing_number='')", str(acct_num))
        self.assertEqual('0', acct_num.getCVV())
        self.assertEqual('1', acct_num.getCVVBad())
        self.assertEqual(1, acct_num.getCVVLength())

        acct_num = AccountNumber('1234567890', cvv_length=2)
        self.assertEqual("'1234567890' (cvv='90' cvv_bad='91' masked='1234567890' bank_name='' bank_display_name='' routing_number='')", str(acct_num))
        self.assertEqual('90', acct_num.getCVV())
        self.assertEqual('91', acct_num.getCVVBad())
        self.assertEqual(2, acct_num.getCVVLength())

        acct_num = AccountNumber('1234567890', cvv_length=3)
        self.assertEqual("'1234567890' (cvv='890' cvv_bad='891' masked='1234567890' bank_name='' bank_display_name='' routing_number='')", str(acct_num))
        self.assertEqual('890', acct_num.getCVV())
        self.assertEqual('891', acct_num.getCVVBad())
        self.assertEqual(3, acct_num.getCVVLength())

        acct_num = AccountNumber('1234567890', cvv_length=4)
        self.assertEqual("'1234567890' (cvv='7890' cvv_bad='7891' masked='1234567890' bank_name='' bank_display_name='' routing_number='')", str(acct_num))
        self.assertEqual('7890', acct_num.getCVV())
        self.assertEqual('7891', acct_num.getCVVBad())
        self.assertEqual(4, acct_num.getCVVLength())

        acct_num = AccountNumber('1234567890', cvv_length=5)
        self.assertEqual("'1234567890' (cvv='67890' cvv_bad='67891' masked='1234567890' bank_name='' bank_display_name='' routing_number='')", str(acct_num))
        self.assertEqual('67890', acct_num.getCVV())
        self.assertEqual('67891', acct_num.getCVVBad())
        self.assertEqual(5, acct_num.getCVVLength())

    def test_method_constructor_masker(self):
        masker = AccountNumberMasker()
        acct_num = AccountNumber('1234567890', masker=masker)
        self.assertEqual("'1234567890' (cvv='890' cvv_bad='891' masked='1234**7890' bank_name='' bank_display_name='' routing_number='')", str(acct_num))
        self.assertEqual('1234**7890', acct_num.getMaskedNumber())
        self.assertIs(masker, acct_num.getMasker())

    def test_method_constructor_routing_number(self):
        acct_num = AccountNumber('1234567890', routing_number='22233345678')
        self.assertEqual("'1234567890' (cvv='890' cvv_bad='891' masked='1234567890' bank_name='' bank_display_name='' routing_number='22233345678')", str(acct_num))
        self.assertEqual('22233345678', acct_num.getRoutingNumber())

    def test_method_constructor_use_bad_cvv(self):
        acct_num = AccountNumber('1234567890', use_bad_cvv=True)
        self.assertEqual('891', acct_num.getCVV())
        self.assertEqual('891', acct_num.getCVVBad())
        self.assertEqual(3, acct_num.getCVVLength())

        acct_num = AccountNumber('1234567890', use_bad_cvv=False)
        self.assertEqual('890', acct_num.getCVV())
        self.assertEqual('891', acct_num.getCVVBad())
        self.assertEqual(3, acct_num.getCVVLength())

    #####################################################################################################
    # METHOD - copy
    #####################################################################################################

    def test_method_copy(self):
        acct_num = AccountNumber('373412345678900',
                                 bank_display_name='BankOfFoobar',
                                 bank_name='DaBank',
                                 cvv='1234',
                                 cvv_bad='6666',
                                 cvv_length=7,
                                 masker=AccountNumberMasker(),
                                 routing_number='22233345678',
                                 use_bad_cvv=True
                                 )
        self.assertEqual("'373412345678900' (cvv='1234' cvv_bad='6666' masked='3734*******8900' bank_name='DaBank' bank_display_name='BankOfFoobar' routing_number='22233345678')", str(acct_num))

        acct_num2 = acct_num.copy()
        self.assertEqual(str(acct_num), str(acct_num2))
        self.assertEqual(acct_num.getBankDisplayName(), acct_num.getBankDisplayName())
        self.assertEqual(acct_num.getBankName(), acct_num.getBankName())
        self.assertEqual(acct_num.getClearTextNumber(), acct_num.getClearTextNumber())
        self.assertEqual(acct_num.getCVV(), acct_num.getCVV())
        self.assertEqual(acct_num.getCVVBad(), acct_num.getCVVBad())
        self.assertEqual(acct_num.getCVVLength(), acct_num.getCVVLength())
        self.assertEqual(acct_num.getMaskedNumber(), acct_num.getMaskedNumber())
        self.assertIs(acct_num.getMasker(), acct_num.getMasker())
        self.assertEqual(acct_num.getRoutingNumber(), acct_num.getRoutingNumber())

    #####################################################################################################
    # METHOD - getLastN
    #####################################################################################################

    def test_method_getLastN(self):
        acct_num = AccountNumber('1234567890', use_bad_cvv=True)
        self.assertEqual('', acct_num.getLastN(-1))
        self.assertEqual('', acct_num.getLastN(0))
        self.assertEqual('0', acct_num.getLastN(1))
        self.assertEqual('90', acct_num.getLastN(2))
        self.assertEqual('890', acct_num.getLastN(3))
        self.assertEqual('7890', acct_num.getLastN(4))
        self.assertEqual('67890', acct_num.getLastN(5))
        self.assertEqual('567890', acct_num.getLastN(6))
        self.assertEqual('4567890', acct_num.getLastN(7))
        self.assertEqual('34567890', acct_num.getLastN(8))
        self.assertEqual('234567890', acct_num.getLastN(9))
        self.assertEqual('1234567890', acct_num.getLastN(10))
        self.assertEqual('1234567890', acct_num.getLastN(11))

    #####################################################################################################
    # METHOD - _normalizeCVV
    #####################################################################################################

    def test_method__normalizeCVV(self):

        self.assertEqual('003', AccountNumber._normalizeCVV('3', 3))
        self.assertEqual('123', AccountNumber._normalizeCVV('123', 3))
        self.assertEqual('345', AccountNumber._normalizeCVV('12345', 3))

    #####################################################################################################
    # METHOD - setClearTextNumber
    #####################################################################################################

    def test_method_setClearTextNumber(self):

        acct_num = AccountNumber('373412345678900',
                                 bank_display_name='BankOfFoobar',
                                 bank_name='DaBank',
                                 cvv='1234',
                                 cvv_bad='6666',
                                 cvv_length=7,
                                 masker=AccountNumberMasker(),
                                 routing_number='22233345678',
                                 use_bad_cvv=True
                                 )
        self.assertEqual("'373412345678900' (cvv='1234' cvv_bad='6666' masked='3734*******8900' bank_name='DaBank' bank_display_name='BankOfFoobar' routing_number='22233345678')", str(acct_num))

        # Empty acct_num, so empty cvv and cvv_bad
        acct_num2 = acct_num.copy()
        acct_num2.setClearTextNumber('')
        self.assertEqual("'' (cvv='' cvv_bad='' masked='' bank_name='DaBank' bank_display_name='BankOfFoobar' routing_number='22233345678')", str(acct_num2))

        # Uses the internal cvv_length
        acct_num2 = acct_num.copy()
        acct_num2.setClearTextNumber('1')
        self.assertEqual("'1' (cvv='1' cvv_bad='2' masked='1' bank_name='DaBank' bank_display_name='BankOfFoobar' routing_number='22233345678')", str(acct_num2))

        acct_num2 = acct_num.copy()
        acct_num2.setClearTextNumber('1234567890123456')
        self.assertEqual("'1234567890123456' (cvv='3456' cvv_bad='3457' masked='1234********3456' bank_name='DaBank' bank_display_name='BankOfFoobar' routing_number='22233345678')", str(acct_num2))

    #####################################################################################################
    # METHOD - setCVV
    #####################################################################################################

    def test_method_setCVV(self):

        acct_num = AccountNumber('373412345678900',
                                 bank_display_name='BankOfFoobar',
                                 bank_name='DaBank',
                                 cvv='5555',
                                 cvv_bad='6666',
                                 cvv_length=7,
                                 masker=AccountNumberMasker(),
                                 routing_number='22233345678',
                                 use_bad_cvv=True
                                 )
        self.assertEqual("'373412345678900' (cvv='5555' cvv_bad='6666' masked='3734*******8900' bank_name='DaBank' bank_display_name='BankOfFoobar' routing_number='22233345678')", str(acct_num))

        # Length of cvv == 0 and length of cvv_bad == 0
        acct_num2 = acct_num.copy()
        acct_num2.setCVV(cvv='')
        self.assertEqual("'373412345678900' (cvv='' cvv_bad='' masked='3734*******8900' bank_name='DaBank' bank_display_name='BankOfFoobar' routing_number='22233345678')", str(acct_num2))

        # Length of cvv > 0 and length of cvv_bad == 0
        acct_num2 = acct_num.copy()
        acct_num2.setCVV(cvv='12345')
        self.assertEqual("'373412345678900' (cvv='12345' cvv_bad='12346' masked='3734*******8900' bank_name='DaBank' bank_display_name='BankOfFoobar' routing_number='22233345678')", str(acct_num2))

        # Length of cvv == 0 and length of cvv_bad > 0
        acct_num2 = acct_num.copy()
        acct_num2.setCVV(cvv='', cvv_bad='345')
        self.assertEqual("'373412345678900' (cvv='' cvv_bad='345' masked='3734*******8900' bank_name='DaBank' bank_display_name='BankOfFoobar' routing_number='22233345678')", str(acct_num2))

        # Length of cvv > 0 and length of cvv_bad > 0
        acct_num2 = acct_num.copy()
        acct_num2.setCVV(cvv='345678', cvv_bad='456789')
        self.assertEqual("'373412345678900' (cvv='345678' cvv_bad='456789' masked='3734*******8900' bank_name='DaBank' bank_display_name='BankOfFoobar' routing_number='22233345678')", str(acct_num2))

        # Check wraparound
        acct_num2 = acct_num.copy()
        acct_num2.setCVV(cvv='9999')
        self.assertEqual("'373412345678900' (cvv='9999' cvv_bad='0000' masked='3734*******8900' bank_name='DaBank' bank_display_name='BankOfFoobar' routing_number='22233345678')", str(acct_num2))

    #####################################################################################################
    # METHOD - setRoutingNumber / getRoutingNumber
    #####################################################################################################

    def test_method_setRoutingNumber(self):
        acct_num = AccountNumber('373412345678900',
                                 bank_display_name='BankOfFoobar',
                                 bank_name='DaBank',
                                 cvv='5555',
                                 cvv_bad='6666',
                                 cvv_length=7,
                                 masker=AccountNumberMasker(),
                                 routing_number='22233345678',
                                 use_bad_cvv=True
                                 )
        self.assertEqual("'373412345678900' (cvv='5555' cvv_bad='6666' masked='3734*******8900' bank_name='DaBank' bank_display_name='BankOfFoobar' routing_number='22233345678')", str(acct_num))
        self.assertEqual('22233345678', acct_num.getRoutingNumber())

        acct_num.setRoutingNumber('555566789')
        self.assertEqual("'373412345678900' (cvv='5555' cvv_bad='6666' masked='3734*******8900' bank_name='DaBank' bank_display_name='BankOfFoobar' routing_number='555566789')", str(acct_num))
        self.assertEqual('555566789', acct_num.getRoutingNumber())

    #####################################################################################################
    # METHOD - useBadCVV
    #####################################################################################################

    def test_method_useBadCVV(self):
        acct_num = AccountNumber('373412345678900',
                                 bank_display_name='BankOfFoobar',
                                 bank_name='DaBank',
                                 cvv='5555',
                                 cvv_bad='6666',
                                 cvv_length=7,
                                 masker=AccountNumberMasker(),
                                 routing_number='22233345678',
                                 use_bad_cvv=False
                                 )
        self.assertEqual("'373412345678900' (cvv='5555' cvv_bad='6666' masked='3734*******8900' bank_name='DaBank' bank_display_name='BankOfFoobar' routing_number='22233345678')", str(acct_num))

        # Set False in constructor
        self.assertEqual('5555', acct_num.getCVV())

        acct_num.useBadCVV(True)
        self.assertEqual('6666', acct_num.getCVV())

        acct_num.useBadCVV(False)
        self.assertEqual('5555', acct_num.getCVV())
