"""
Created on February 12, 2017

@author: John Jackson
"""

import copy
import re
import unittest
from unittest import mock

from kojak.core.utilities import account_number as an

PATCH_RANDOM = 'kojak.core.utilities.account_number.random'


###############################################################################
# TEST AccountNumber
###############################################################################

class TestAccountNumber(unittest.TestCase):

    masker = an.AccountNumberMasker()

    kwargs = {
        'account_number': '373412345678900',
        'bank_display_name': 'BankOfGallifrey',
        'bank_name': 'DaBank',
        'cvv': '1234',
        'cvv_bad': '6666',
        'cvv_length': 7,
        'masker': masker,
        'routing_number': '22233345678',
        'use_bad_cvv': True,
    }

    # =========================================================================
    # METHOD - CONSTRUCTOR
    # =========================================================================

    def test_CONSTRUCTOR(self):

        x = an.AccountNumber('')
        self.assertEqual("AccountNumber: account_number='' bank_display_name='' bank_name='' cvv='' cvv_bad='' cvv_length=0 masker=None routing_number='' use_bad_cvv=False", str(x))
        self.assertEqual('', x.get_bank_display_name())
        self.assertEqual('', x.get_bank_name())
        self.assertEqual('', x.get_account_number())
        self.assertEqual('', x.get_cvv())
        self.assertEqual('', x.get_cvv_bad())
        self.assertEqual(0, x.get_cvv_length())
        self.assertEqual('', x.get_masked_number())
        self.assertIsNone(x.get_masker())
        self.assertEqual('', x.get_routing_number())

        x = an.AccountNumber('1')
        self.assertEqual("AccountNumber: account_number='1' bank_display_name='' bank_name='' cvv='1' cvv_bad='2' cvv_length=1 masker=None routing_number='' use_bad_cvv=False", str(x))
        self.assertEqual('1', x.get_account_number())
        self.assertEqual('1', x.get_cvv())
        self.assertEqual('2', x.get_cvv_bad())
        self.assertEqual(1, x.get_cvv_length())
        self.assertEqual('1', x.get_masked_number())

        x = an.AccountNumber('12')
        self.assertEqual("AccountNumber: account_number='12' bank_display_name='' bank_name='' cvv='12' cvv_bad='13' cvv_length=2 masker=None routing_number='' use_bad_cvv=False", str(x))

        x = an.AccountNumber('123')
        self.assertEqual("AccountNumber: account_number='123' bank_display_name='' bank_name='' cvv='123' cvv_bad='124' cvv_length=3 masker=None routing_number='' use_bad_cvv=False", str(x))

        x = an.AccountNumber('1234')
        self.assertEqual("AccountNumber: account_number='1234' bank_display_name='' bank_name='' cvv='234' cvv_bad='235' cvv_length=3 masker=None routing_number='' use_bad_cvv=False", str(x))

        x = an.AccountNumber('12345')
        self.assertEqual("AccountNumber: account_number='12345' bank_display_name='' bank_name='' cvv='345' cvv_bad='346' cvv_length=3 masker=None routing_number='' use_bad_cvv=False", str(x))

        x = an.AccountNumber('123456')
        self.assertEqual("AccountNumber: account_number='123456' bank_display_name='' bank_name='' cvv='456' cvv_bad='457' cvv_length=3 masker=None routing_number='' use_bad_cvv=False", str(x))

        x = an.AccountNumber('1234567')
        self.assertEqual("AccountNumber: account_number='1234567' bank_display_name='' bank_name='' cvv='567' cvv_bad='568' cvv_length=3 masker=None routing_number='' use_bad_cvv=False", str(x))

        x = an.AccountNumber('12345678')
        self.assertEqual("AccountNumber: account_number='12345678' bank_display_name='' bank_name='' cvv='678' cvv_bad='679' cvv_length=3 masker=None routing_number='' use_bad_cvv=False", str(x))

        x = an.AccountNumber('123456789')
        self.assertEqual("AccountNumber: account_number='123456789' bank_display_name='' bank_name='' cvv='789' cvv_bad='790' cvv_length=3 masker=None routing_number='' use_bad_cvv=False", str(x))

        x = an.AccountNumber('1234567890')
        self.assertEqual("AccountNumber: account_number='1234567890' bank_display_name='' bank_name='' cvv='890' cvv_bad='891' cvv_length=3 masker=None routing_number='' use_bad_cvv=False", str(x))

        x = an.AccountNumber(account_number='373412345678900')
        self.assertEqual("AccountNumber: account_number='373412345678900' bank_display_name='' bank_name='' cvv='900' cvv_bad='901' cvv_length=3 masker=None routing_number='' use_bad_cvv=False", str(x))

    def test_CONSTRUCTOR__bank_display_name(self):
        x = an.AccountNumber('', bank_display_name='Bank of Gallifrey')
        self.assertEqual("AccountNumber: account_number='' bank_display_name='Bank of Gallifrey' bank_name='' cvv='' cvv_bad='' cvv_length=0 masker=None routing_number='' use_bad_cvv=False", str(x))
        self.assertEqual('Bank of Gallifrey', x.get_bank_display_name())

    def test_CONSTRUCTOR__bank_name(self):
        x = an.AccountNumber('', bank_name='BankOfGallifrey')
        self.assertEqual("AccountNumber: account_number='' bank_display_name='' bank_name='BankOfGallifrey' cvv='' cvv_bad='' cvv_length=0 masker=None routing_number='' use_bad_cvv=False", str(x))
        self.assertEqual('BankOfGallifrey', x.get_bank_name())

    def test_CONSTRUCTOR__cvv(self):
        # Test that cvv_bad retains leading zero.
        x = an.AccountNumber('1234567890', cvv='01')
        self.assertEqual("AccountNumber: account_number='1234567890' bank_display_name='' bank_name='' cvv='01' cvv_bad='02' cvv_length=2 masker=None routing_number='' use_bad_cvv=False", str(x))
        self.assertEqual('01', x.get_cvv())
        self.assertEqual('02', x.get_cvv_bad())
        self.assertEqual(2, x.get_cvv_length())

        # Test that cvv_bad retains length not equal to default value.
        x = an.AccountNumber('1234567890', cvv='4567')
        self.assertEqual("AccountNumber: account_number='1234567890' bank_display_name='' bank_name='' cvv='4567' cvv_bad='4568' cvv_length=4 masker=None routing_number='' use_bad_cvv=False", str(x))
        self.assertEqual('4567', x.get_cvv())
        self.assertEqual('4568', x.get_cvv_bad())
        self.assertEqual(4, x.get_cvv_length())

        # Test that cvv_bad wraps to zero and retains proper length.
        x = an.AccountNumber('1234567890', cvv='9999', cvv_length=1)
        self.assertEqual("AccountNumber: account_number='1234567890' bank_display_name='' bank_name='' cvv='9999' cvv_bad='0000' cvv_length=4 masker=None routing_number='' use_bad_cvv=False", str(x))
        self.assertEqual('9999', x.get_cvv())
        self.assertEqual('0000', x.get_cvv_bad())
        self.assertEqual(4, x.get_cvv_length())

    def test_CONSTRUCTOR__cvv_bad(self):
        # Test that explicit cvv_bad overrides default.
        x = an.AccountNumber('1234567890', cvv='4567', cvv_bad='1111')
        self.assertEqual("AccountNumber: account_number='1234567890' bank_display_name='' bank_name='' cvv='4567' cvv_bad='1111' cvv_length=4 masker=None routing_number='' use_bad_cvv=False", str(x))
        self.assertEqual('4567', x.get_cvv())
        self.assertEqual('1111', x.get_cvv_bad())
        self.assertEqual(4, x.get_cvv_length())

    def test_CONSTRUCTOR__cvv_length(self):
        x = an.AccountNumber('1234567890', cvv_length=-1)
        self.assertEqual("AccountNumber: account_number='1234567890' bank_display_name='' bank_name='' cvv='890' cvv_bad='891' cvv_length=3 masker=None routing_number='' use_bad_cvv=False", str(x))
        self.assertEqual('890', x.get_cvv())
        self.assertEqual('891', x.get_cvv_bad())
        self.assertEqual(3, x.get_cvv_length())

        x = an.AccountNumber('1234567890', cvv_length=0)
        self.assertEqual("AccountNumber: account_number='1234567890' bank_display_name='' bank_name='' cvv='' cvv_bad='' cvv_length=0 masker=None routing_number='' use_bad_cvv=False", str(x))
        self.assertEqual('', x.get_cvv())
        self.assertEqual('', x.get_cvv_bad())
        self.assertEqual(0, x.get_cvv_length())

        x = an.AccountNumber('1234567890', cvv_length=1)
        self.assertEqual("AccountNumber: account_number='1234567890' bank_display_name='' bank_name='' cvv='0' cvv_bad='1' cvv_length=1 masker=None routing_number='' use_bad_cvv=False", str(x))
        self.assertEqual('0', x.get_cvv())
        self.assertEqual('1', x.get_cvv_bad())
        self.assertEqual(1, x.get_cvv_length())

        x = an.AccountNumber('1234567890', cvv_length=2)
        self.assertEqual("AccountNumber: account_number='1234567890' bank_display_name='' bank_name='' cvv='90' cvv_bad='91' cvv_length=2 masker=None routing_number='' use_bad_cvv=False", str(x))
        self.assertEqual('90', x.get_cvv())
        self.assertEqual('91', x.get_cvv_bad())
        self.assertEqual(2, x.get_cvv_length())

        x = an.AccountNumber('1234567890', cvv_length=3)
        self.assertEqual("AccountNumber: account_number='1234567890' bank_display_name='' bank_name='' cvv='890' cvv_bad='891' cvv_length=3 masker=None routing_number='' use_bad_cvv=False", str(x))
        self.assertEqual('890', x.get_cvv())
        self.assertEqual('891', x.get_cvv_bad())
        self.assertEqual(3, x.get_cvv_length())

        x = an.AccountNumber('1234567890', cvv_length=4)
        self.assertEqual("AccountNumber: account_number='1234567890' bank_display_name='' bank_name='' cvv='7890' cvv_bad='7891' cvv_length=4 masker=None routing_number='' use_bad_cvv=False", str(x))
        self.assertEqual('7890', x.get_cvv())
        self.assertEqual('7891', x.get_cvv_bad())
        self.assertEqual(4, x.get_cvv_length())

        x = an.AccountNumber('1234567890', cvv_length=5)
        self.assertEqual("AccountNumber: account_number='1234567890' bank_display_name='' bank_name='' cvv='67890' cvv_bad='67891' cvv_length=5 masker=None routing_number='' use_bad_cvv=False", str(x))
        self.assertEqual('67890', x.get_cvv())
        self.assertEqual('67891', x.get_cvv_bad())
        self.assertEqual(5, x.get_cvv_length())

    def test_CONSTRUCTOR__masker(self):
        masker = an.AccountNumberMasker()
        x = an.AccountNumber('1234567890', masker=masker)
        self.assertEqual("AccountNumber: account_number='1234567890' bank_display_name='' bank_name='' cvv='890' cvv_bad='891' cvv_length=3 masker=(AccountNumberMasker: first_m=4 last_n=4 mask_character='*') routing_number='' use_bad_cvv=False", str(x))
        self.assertEqual('1234**7890', x.get_masked_number())
        self.assertIs(masker, x.get_masker())

    def test_CONSTRUCTOR__routing_number(self):
        x = an.AccountNumber('1234567890', routing_number='22233345678')
        self.assertEqual("AccountNumber: account_number='1234567890' bank_display_name='' bank_name='' cvv='890' cvv_bad='891' cvv_length=3 masker=None routing_number='22233345678' use_bad_cvv=False", str(x))
        self.assertEqual('22233345678', x.get_routing_number())

        x = an.AccountNumber('1234567890', use_bad_cvv=True)
        self.assertEqual('891', x.get_cvv())
        self.assertEqual('891', x.get_cvv_bad())
        self.assertEqual(3, x.get_cvv_length())

        x = an.AccountNumber('1234567890', use_bad_cvv=False)
        self.assertEqual('890', x.get_cvv())
        self.assertEqual('891', x.get_cvv_bad())
        self.assertEqual(3, x.get_cvv_length())

    # =========================================================================
    # METHOD - __str__
    # =========================================================================

    def test___str__(self):
        x = an.AccountNumber(**self.kwargs)
        self.assertEqual(str(x), "AccountNumber: account_number='373412345678900' bank_display_name='BankOfGallifrey' bank_name='DaBank' cvv='1234' cvv_bad='6666' cvv_length=4 masker=(AccountNumberMasker: first_m=4 last_n=4 mask_character='*') routing_number='22233345678' use_bad_cvv=True")

    # =========================================================================
    # METHOD - __repr__
    # =========================================================================

    def test___repr__(self):
        x = an.AccountNumber(**self.kwargs)
        self.assertEqual(repr(x), "AccountNumber('373412345678900', 'BankOfGallifrey', 'DaBank', '1234', '6666', 4, AccountNumberMasker(4, 4, '*'), '22233345678', True)")

    # =========================================================================
    # METHOD - __eq__
    # =========================================================================

    def test___eq__(self):
        x = an.AccountNumber(**self.kwargs)

        # TEST EQUALITY
        x2 = an.AccountNumber(**self.kwargs)
        self.assertEqual(x, x2)

        temp_kwargs = copy.copy(self.kwargs)
        temp_kwargs['use_bad_cvv'] = True
        x2 = an.AccountNumber(**temp_kwargs)
        self.assertEqual(x, x2)

        # TEST INEQUALITY
        temp_kwargs = copy.copy(self.kwargs)
        temp_kwargs['account_number'] = '1234567890123456'
        x2 = an.AccountNumber(**temp_kwargs)
        self.assertNotEqual(x, x2)

        temp_kwargs = copy.copy(self.kwargs)
        temp_kwargs['bank_display_name'] = 'some other bank'
        x2 = an.AccountNumber(**temp_kwargs)
        self.assertNotEqual(x, x2)

        temp_kwargs = copy.copy(self.kwargs)
        temp_kwargs['bank_name'] = 'some other bank'
        x2 = an.AccountNumber(**temp_kwargs)
        self.assertNotEqual(x, x2)

        temp_kwargs = copy.copy(self.kwargs)
        temp_kwargs['cvv'] = '999'
        x2 = an.AccountNumber(**temp_kwargs)
        self.assertNotEqual(x, x2)

        temp_kwargs = copy.copy(self.kwargs)
        temp_kwargs['cvv_bad'] = '999'
        x2 = an.AccountNumber(**temp_kwargs)
        self.assertNotEqual(x, x2)

        temp_kwargs = copy.copy(self.kwargs)
        temp_kwargs['cvv_length'] = 3
        temp_kwargs['cvv'] = ''
        x2 = an.AccountNumber(**temp_kwargs)
        self.assertNotEqual(x, x2)

        temp_kwargs = copy.copy(self.kwargs)
        temp_kwargs['masker'] = an.AccountNumberMasker(6, 6)
        x2 = an.AccountNumber(**temp_kwargs)
        self.assertNotEqual(x, x2)

        temp_kwargs = copy.copy(self.kwargs)
        temp_kwargs['routing_number'] = '1234567890123456'
        x2 = an.AccountNumber(**temp_kwargs)
        self.assertNotEqual(x, x2)

    # =========================================================================
    # METHOD - copy
    # =========================================================================

    def test_copy(self):
        x = an.AccountNumber(**self.kwargs)
        x2 = x.copy()
        self.assertEqual(x, x2)

    # =========================================================================
    # METHOD - get_last_n
    # =========================================================================

    def test_get_last_n(self):
        x = an.AccountNumber('1234567890', use_bad_cvv=True)
        self.assertEqual('', x.get_last_n(-1))
        self.assertEqual('', x.get_last_n(0))
        self.assertEqual('0', x.get_last_n(1))
        self.assertEqual('90', x.get_last_n(2))
        self.assertEqual('890', x.get_last_n(3))
        self.assertEqual('7890', x.get_last_n(4))
        self.assertEqual('67890', x.get_last_n(5))
        self.assertEqual('567890', x.get_last_n(6))
        self.assertEqual('4567890', x.get_last_n(7))
        self.assertEqual('34567890', x.get_last_n(8))
        self.assertEqual('234567890', x.get_last_n(9))
        self.assertEqual('1234567890', x.get_last_n(10))
        self.assertEqual('1234567890', x.get_last_n(11))

    # =========================================================================
    # METHOD - _normalize_cvv
    # =========================================================================

    def test___normalize_cvv(self):

        self.assertEqual('003', an.AccountNumber._normalize_cvv('3', 3))
        self.assertEqual('123', an.AccountNumber._normalize_cvv('123', 3))
        self.assertEqual('345', an.AccountNumber._normalize_cvv('12345', 3))

    # =========================================================================
    # METHOD - set_account_number
    # =========================================================================

    def test_set_account_number(self):

        x = an.AccountNumber(
            '373412345678900',
            bank_display_name='BankOfGallifrey',
            bank_name='DaBank',
            cvv='1234',
            cvv_bad='6666',
            cvv_length=7,
            masker=an.AccountNumberMasker(),
            routing_number='22233345678',
            use_bad_cvv=True
            )
        self.assertEqual("AccountNumber: account_number='373412345678900' bank_display_name='BankOfGallifrey' bank_name='DaBank' cvv='1234' cvv_bad='6666' cvv_length=4 masker=(AccountNumberMasker: first_m=4 last_n=4 mask_character='*') routing_number='22233345678' use_bad_cvv=True", str(x))

        # Empty x, so empty cvv and cvv_bad
        acct_num2 = x.copy()
        acct_num2.set_account_number('')
        self.assertEqual("AccountNumber: account_number='' bank_display_name='BankOfGallifrey' bank_name='DaBank' cvv='' cvv_bad='' cvv_length=0 masker=(AccountNumberMasker: first_m=4 last_n=4 mask_character='*') routing_number='22233345678' use_bad_cvv=True", str(acct_num2))

        # Uses the internal cvv_length
        acct_num2 = x.copy()
        acct_num2.set_account_number('1')
        self.assertEqual("AccountNumber: account_number='1' bank_display_name='BankOfGallifrey' bank_name='DaBank' cvv='1' cvv_bad='2' cvv_length=1 masker=(AccountNumberMasker: first_m=4 last_n=4 mask_character='*') routing_number='22233345678' use_bad_cvv=True", str(acct_num2))

        acct_num2 = x.copy()
        acct_num2.set_account_number('1234567890123456')
        self.assertEqual("AccountNumber: account_number='1234567890123456' bank_display_name='BankOfGallifrey' bank_name='DaBank' cvv='3456' cvv_bad='3457' cvv_length=4 masker=(AccountNumberMasker: first_m=4 last_n=4 mask_character='*') routing_number='22233345678' use_bad_cvv=True", str(acct_num2))

    # =========================================================================
    # METHOD - set_cvv
    # =========================================================================

    def test_set_cvv(self):

        x = an.AccountNumber(
            '373412345678900',
            bank_display_name='BankOfGallifrey',
            bank_name='DaBank',
            cvv='5555',
            cvv_bad='6666',
            cvv_length=7,
            masker=an.AccountNumberMasker(),
            routing_number='22233345678',
            use_bad_cvv=True
            )
        self.assertEqual("AccountNumber: account_number='373412345678900' bank_display_name='BankOfGallifrey' bank_name='DaBank' cvv='5555' cvv_bad='6666' cvv_length=4 masker=(AccountNumberMasker: first_m=4 last_n=4 mask_character='*') routing_number='22233345678' use_bad_cvv=True", str(x))

        # Length of cvv == 0 and length of cvv_bad == 0
        acct_num2 = x.copy()
        acct_num2.set_cvv(cvv='')
        self.assertEqual("AccountNumber: account_number='373412345678900' bank_display_name='BankOfGallifrey' bank_name='DaBank' cvv='' cvv_bad='' cvv_length=0 masker=(AccountNumberMasker: first_m=4 last_n=4 mask_character='*') routing_number='22233345678' use_bad_cvv=True", str(acct_num2))

        # Length of cvv > 0 and length of cvv_bad == 0
        acct_num2 = x.copy()
        acct_num2.set_cvv(cvv='12345')
        self.assertEqual("AccountNumber: account_number='373412345678900' bank_display_name='BankOfGallifrey' bank_name='DaBank' cvv='12345' cvv_bad='12346' cvv_length=5 masker=(AccountNumberMasker: first_m=4 last_n=4 mask_character='*') routing_number='22233345678' use_bad_cvv=True", str(acct_num2))

        # Length of cvv == 0 and length of cvv_bad > 0
        acct_num2 = x.copy()
        acct_num2.set_cvv(cvv='', cvv_bad='345')
        self.assertEqual("AccountNumber: account_number='373412345678900' bank_display_name='BankOfGallifrey' bank_name='DaBank' cvv='' cvv_bad='345' cvv_length=0 masker=(AccountNumberMasker: first_m=4 last_n=4 mask_character='*') routing_number='22233345678' use_bad_cvv=True", str(acct_num2))

        # Length of cvv > 0 and length of cvv_bad > 0
        acct_num2 = x.copy()
        acct_num2.set_cvv(cvv='345678', cvv_bad='456789')
        self.assertEqual("AccountNumber: account_number='373412345678900' bank_display_name='BankOfGallifrey' bank_name='DaBank' cvv='345678' cvv_bad='456789' cvv_length=6 masker=(AccountNumberMasker: first_m=4 last_n=4 mask_character='*') routing_number='22233345678' use_bad_cvv=True", str(acct_num2))

        # Check wraparound
        acct_num2 = x.copy()
        acct_num2.set_cvv(cvv='9999')
        self.assertEqual("AccountNumber: account_number='373412345678900' bank_display_name='BankOfGallifrey' bank_name='DaBank' cvv='9999' cvv_bad='0000' cvv_length=4 masker=(AccountNumberMasker: first_m=4 last_n=4 mask_character='*') routing_number='22233345678' use_bad_cvv=True", str(acct_num2))

    # =========================================================================
    # METHOD - set_routing_number / get_routing_number
    # =========================================================================

    def test_set_routing_number(self):
        x = an.AccountNumber(
            '373412345678900',
            bank_display_name='BankOfGallifrey',
            bank_name='DaBank',
            cvv='5555',
            cvv_bad='6666',
            cvv_length=7,
            masker=an.AccountNumberMasker(),
            routing_number='22233345678',
            use_bad_cvv=True
            )
        self.assertEqual("AccountNumber: account_number='373412345678900' bank_display_name='BankOfGallifrey' bank_name='DaBank' cvv='5555' cvv_bad='6666' cvv_length=4 masker=(AccountNumberMasker: first_m=4 last_n=4 mask_character='*') routing_number='22233345678' use_bad_cvv=True", str(x))
        self.assertEqual('22233345678', x.get_routing_number())

        x.set_routing_number('555566789')
        self.assertEqual("AccountNumber: account_number='373412345678900' bank_display_name='BankOfGallifrey' bank_name='DaBank' cvv='5555' cvv_bad='6666' cvv_length=4 masker=(AccountNumberMasker: first_m=4 last_n=4 mask_character='*') routing_number='555566789' use_bad_cvv=True", str(x))
        self.assertEqual('555566789', x.get_routing_number())

    # =========================================================================
    # METHOD - use_bad_cvv
    # =========================================================================

    def test_use_bad_cvv(self):
        x = an.AccountNumber(
            '373412345678900',
            bank_display_name='BankOfGallifrey',
            bank_name='DaBank',
            cvv='5555',
            cvv_bad='6666',
            cvv_length=7,
            masker=an.AccountNumberMasker(),
            routing_number='22233345678',
            use_bad_cvv=False
            )
        self.assertEqual("AccountNumber: account_number='373412345678900' bank_display_name='BankOfGallifrey' bank_name='DaBank' cvv='5555' cvv_bad='6666' cvv_length=4 masker=(AccountNumberMasker: first_m=4 last_n=4 mask_character='*') routing_number='22233345678' use_bad_cvv=False", str(x))

        # Set False in constructor
        self.assertEqual('5555', x.get_cvv())

        x.use_bad_cvv(True)
        self.assertEqual('6666', x.get_cvv())

        x.use_bad_cvv(False)
        self.assertEqual('5555', x.get_cvv())


###############################################################################
# TEST AccountNumberLuhn
###############################################################################

class TestAccountNumberLuhn(unittest.TestCase):

    # =========================================================================
    # METHOD - CONSTRUCTOR
    # =========================================================================

    def test_CONSTRUCTOR(self):
        x = an.AccountNumberLuhn('373400000000000')
        self.assertEqual("AccountNumberLuhn: account_number='373400000000001' bank_display_name='' bank_name='' cvv='001' cvv_bad='002' cvv_length=3 masker=None routing_number='' use_bad_cvv=False", str(x))


###############################################################################
# TEST AccountNumberMasker
###############################################################################

class TestAccountNumberMasker(unittest.TestCase):

    # =========================================================================
    # METHOD - CONSTRUCTOR
    # =========================================================================

    def test_CONSTRUCTOR(self):

        x = an.AccountNumberMasker(6, 3, '#')
        self.assertEqual(x._first_m, 6)
        self.assertEqual(x._last_n, 3)
        self.assertEqual(x._mask_character, '#')

        x = an.AccountNumberMasker(-1, 3, '#')
        self.assertEqual(x._first_m, 0)
        self.assertEqual(x._last_n, 3)
        self.assertEqual(x._mask_character, '#')

        x = an.AccountNumberMasker(6, -1, '#')
        self.assertEqual(x._first_m, 6)
        self.assertEqual(x._last_n, 0)
        self.assertEqual(x._mask_character, '#')

        x = an.AccountNumberMasker(6, 3, '')
        self.assertEqual(x._first_m, 6)
        self.assertEqual(x._last_n, 3)
        self.assertEqual(x._mask_character, '*')

        x = an.AccountNumberMasker(6, 3, 'ABCD')
        self.assertEqual(x._first_m, 6)
        self.assertEqual(x._last_n, 3)
        self.assertEqual(x._mask_character, 'A')


    # =========================================================================
    # METHOD - __str__
    # =========================================================================

    def test___str__(self):
        x = an.AccountNumberMasker(6, 3, '#')
        self.assertEqual(str(x), "AccountNumberMasker: first_m=6 last_n=3 mask_character='#'")

    # =========================================================================
    # METHOD - __repr__
    # =========================================================================

    def test___repr__(self):
        x = an.AccountNumberMasker(6, 3, '#')
        self.assertEqual(repr(x), "AccountNumberMasker(6, 3, '#')")

    # =========================================================================
    # METHOD - __eq__
    # =========================================================================

    def test___eq__(self):
        x = an.AccountNumberMasker(6, 3, '#')

        # TEST EQUALITY
        x2 = an.AccountNumberMasker(6, 3, '#')
        self.assertEqual(x, x2)

        # TEST INEQUALITY
        x2 = an.AccountNumberMasker(4, 3, '#')
        self.assertNotEqual(x, x2)

        x2 = an.AccountNumberMasker(6, 4, '#')
        self.assertNotEqual(x, x2)

        x2 = an.AccountNumberMasker(6, 3, '*')
        self.assertNotEqual(x, x2)

    # =========================================================================
    # METHOD - mask_number
    # =========================================================================

    def test_mask_number(self):

        x = an.AccountNumberMasker()
        self.assertEqual("AccountNumberMasker: first_m=4 last_n=4 mask_character='*'", str(x))

        self.assertEqual('', x.mask_number(''))
        self.assertEqual('1', x.mask_number('1'))
        self.assertEqual('12', x.mask_number('12'))
        self.assertEqual('123', x.mask_number('123'))
        self.assertEqual('1234', x.mask_number('1234'))
        self.assertEqual('12345', x.mask_number('12345'))
        self.assertEqual('123456', x.mask_number('123456'))
        self.assertEqual('1234567', x.mask_number('1234567'))
        self.assertEqual('12345678', x.mask_number('12345678'))
        self.assertEqual('1234*6789', x.mask_number('123456789'))
        self.assertEqual('1234**7890', x.mask_number('1234567890'))
        self.assertEqual('1234***8901', x.mask_number('12345678901'))
        self.assertEqual('1234****9012', x.mask_number('123456789012'))
        self.assertEqual('1234*****0123', x.mask_number('1234567890123'))
        self.assertEqual('1234******1234', x.mask_number('12345678901234'))
        self.assertEqual('1234*******2345', x.mask_number('123456789012345'))
        self.assertEqual('1234********3456', x.mask_number('1234567890123456'))
        self.assertEqual('1234*********4567', x.mask_number('12345678901234567'))
        self.assertEqual('1234**********5678', x.mask_number('123456789012345678'))
        self.assertEqual('1234***********6789', x.mask_number('1234567890123456789'))
        self.assertEqual('1234************7890', x.mask_number('12345678901234567890'))

    def test_mask_number__first_m(self):
        x = an.AccountNumberMasker(first_m=-1)
        self.assertEqual("AccountNumberMasker: first_m=0 last_n=4 mask_character='*'", str(x))
        self.assertEqual('************3456', x.mask_number('1234567890123456'))

        x = an.AccountNumberMasker(first_m=0)
        self.assertEqual("AccountNumberMasker: first_m=0 last_n=4 mask_character='*'", str(x))
        self.assertEqual('************3456', x.mask_number('1234567890123456'))

        x = an.AccountNumberMasker(first_m=1)
        self.assertEqual("AccountNumberMasker: first_m=1 last_n=4 mask_character='*'", str(x))
        self.assertEqual('1***********3456', x.mask_number('1234567890123456'))

        x = an.AccountNumberMasker(first_m=5)
        self.assertEqual("AccountNumberMasker: first_m=5 last_n=4 mask_character='*'", str(x))
        self.assertEqual('12345*******3456', x.mask_number('1234567890123456'))

    def test_mask_number__last_n(self):
        x = an.AccountNumberMasker(last_n=-1)
        self.assertEqual("AccountNumberMasker: first_m=4 last_n=0 mask_character='*'", str(x))
        self.assertEqual('1234************', x.mask_number('1234567890123456'))

        x = an.AccountNumberMasker(last_n=0)
        self.assertEqual("AccountNumberMasker: first_m=4 last_n=0 mask_character='*'", str(x))
        self.assertEqual('1234************', x.mask_number('1234567890123456'))

        x = an.AccountNumberMasker(last_n=1)
        self.assertEqual("AccountNumberMasker: first_m=4 last_n=1 mask_character='*'", str(x))
        self.assertEqual('1234***********6', x.mask_number('1234567890123456'))

        x = an.AccountNumberMasker(last_n=5)
        self.assertEqual("AccountNumberMasker: first_m=4 last_n=5 mask_character='*'", str(x))
        self.assertEqual('1234*******23456', x.mask_number('1234567890123456'))

    def test_mask_number__mask_character(self):
        x = an.AccountNumberMasker(mask_character='0')
        self.assertEqual("AccountNumberMasker: first_m=4 last_n=4 mask_character='0'", str(x))
        self.assertEqual('1234000000003456', x.mask_number('1234567890123456'))

        x = an.AccountNumberMasker(mask_character='#')
        self.assertEqual("AccountNumberMasker: first_m=4 last_n=4 mask_character='#'", str(x))
        self.assertEqual('1234########3456', x.mask_number('1234567890123456'))

        x = an.AccountNumberMasker(mask_character='#ABC')
        self.assertEqual("AccountNumberMasker: first_m=4 last_n=4 mask_character='#'", str(x))
        self.assertEqual('1234########3456', x.mask_number('1234567890123456'))

        x = an.AccountNumberMasker(mask_character='')
        self.assertEqual("AccountNumberMasker: first_m=4 last_n=4 mask_character='*'", str(x))
        self.assertEqual('1234********3456', x.mask_number('1234567890123456'))


###############################################################################
# TEST AccountNumberGenerator
###############################################################################

class TestAccountNumberGenerator(unittest.TestCase):

    # Make a subclass that implements the abstract methods by passing control
    # to them.

    class MyAccountNumberGenerator(an.AccountNumberGenerator):

        def __init__(self):
            pass

        def get_new_number(self) -> an.AccountNumber:
            return super().get_new_number()

    # =========================================================================
    # METHOD - get_new_number
    # =========================================================================

    def test_get_new_number(self):

        x = self.MyAccountNumberGenerator()
        self.assertRaises(NotImplementedError, x.get_new_number)


###############################################################################
# TEST AccountNumberGeneratorFixed
###############################################################################

class TestAccountNumberGeneratorFixed(unittest.TestCase):

    account_numbers = (
        an.AccountNumber('1'),
        an.AccountNumber('2'),
        an.AccountNumber('3'),
        an.AccountNumber('4'),
    )

    # =========================================================================
    # METHOD - CONSTRUCTOR
    # =========================================================================

    def test_CONSTRUCTOR(self):

        x = an.AccountNumberGeneratorFixed(self.account_numbers)
        self.assertIs(x._numbers, self.account_numbers)
        self.assertEqual(x._next_number, 0)

        msg = 'You must provide at least one account number'
        self.assertRaisesRegex(
            AssertionError,
            '^' + re.escape(msg) + '$',
            an.AccountNumberGeneratorFixed, None
        )
        self.assertRaisesRegex(
            AssertionError,
            '^' + re.escape(msg) + '$',
            an.AccountNumberGeneratorFixed, tuple()
        )

    def test__str__(self):

        x = an.AccountNumberGeneratorFixed(tuple([self.account_numbers[0]]))
        msg = "AccountNumberGeneratorFixed: 1 number starting with '1'"
        self.assertEqual(str(x), msg)

        x = an.AccountNumberGeneratorFixed(self.account_numbers)
        msg = "AccountNumberGeneratorFixed: 4 numbers starting with '1'"
        self.assertEqual(str(x), msg)

    def test_get_new_number(self):

        x = an.AccountNumberGeneratorFixed(self.account_numbers)

        account_number = x.get_new_number()
        self.assertIs(account_number, self.account_numbers[0])

        account_number = x.get_new_number()
        self.assertIs(account_number, self.account_numbers[1])

        account_number = x.get_new_number()
        self.assertIs(account_number, self.account_numbers[2])

        account_number = x.get_new_number()
        self.assertIs(account_number, self.account_numbers[3])

        account_number = x.get_new_number()
        self.assertIs(account_number, self.account_numbers[0])


###############################################################################
# TEST AccountNumberGeneratorRandom
###############################################################################

class TestAccountNumberGeneratorRandom(unittest.TestCase):

    masker = an.AccountNumberMasker()
    prefixes = ('1', '22', '333')

    kwargs = {
        'length': 16,
        'bank_display_name': 'BDN',
        'bank_name': 'BN',
        'cvv_length': 3,
        'masker': masker,
        'routing_number': 'RN',
        'prefixes': prefixes,
    }

    # =========================================================================
    # METHOD - CONSTRUCTOR
    # =========================================================================

    def test_CONSTRUCTOR(self):

        x = an.AccountNumberGeneratorRandom(**self.kwargs)
        self.assertEqual(x._length, self.kwargs['length'])
        self.assertEqual(x._bank_display_name, self.kwargs['bank_display_name'])
        self.assertEqual(x._bank_name, self.kwargs['bank_name'])
        self.assertEqual(x._cvv_length, self.kwargs['cvv_length'])
        self.assertIs(x._masker, self.kwargs['masker'])
        self.assertEqual(x._routing_number, self.kwargs['routing_number'])
        self.assertIs(x._prefixes, self.kwargs['prefixes'])
        self.assertEqual(x._next_prefix, 0)

        temp_kwargs = copy.copy(self.kwargs)
        temp_kwargs['length'] = 0
        msg = 'You must provide a length > 0'
        self.assertRaisesRegex(
            AssertionError,
            '^' + re.escape(msg) + '$',
            an.AccountNumberGeneratorRandom, **temp_kwargs
        )

        temp_kwargs = copy.copy(self.kwargs)
        temp_kwargs['prefixes'] = tuple()
        msg = 'You must provide at least one prefix'
        self.assertRaisesRegex(
            AssertionError,
            '^' + re.escape(msg) + '$',
            an.AccountNumberGeneratorRandom, **temp_kwargs
        )

    def test__str__(self):

        temp_kwargs = copy.copy(self.kwargs)
        temp_kwargs['prefixes'] = tuple(self.prefixes[0])
        x = an.AccountNumberGeneratorRandom(**temp_kwargs)
        msg = "AccountNumberGeneratorRandom: 1 prefix starting with '1'"
        self.assertEqual(str(x), msg)

        x = an.AccountNumberGeneratorRandom(**self.kwargs)
        msg = "AccountNumberGeneratorRandom: 3 prefixes starting with '1'"
        self.assertEqual(str(x), msg)

    @mock.patch(PATCH_RANDOM)
    def test_get_new_number(self, mock_random):

        mock_random.randint.side_effect = [_ % 10 for _ in range(200)]

        x = an.AccountNumberGeneratorRandom(**self.kwargs)

        account_number = x.get_new_number()
        expected = an.AccountNumber('1012345678901234', 'BDN', 'BN', '234', '235', 3, self.masker, 'RN', False)
        self.assertEqual(account_number, expected)

        account_number = x.get_new_number()
        expected = an.AccountNumber('2256789012345678', 'BDN', 'BN', '678', '679', 3, self.masker, 'RN', False)
        self.assertEqual(account_number, expected)

        account_number = x.get_new_number()
        expected = an.AccountNumber('3339012345678901', 'BDN', 'BN', '901', '902', 3, self.masker, 'RN', False)
        self.assertEqual(account_number, expected)

        account_number = x.get_new_number()
        expected = an.AccountNumber('1234567890123456', 'BDN', 'BN', '456', '457', 3, self.masker, 'RN', False)
        self.assertEqual(account_number, expected)

    @mock.patch(PATCH_RANDOM)
    def test__get_next_number(self, mock_random):

        mock_random.randint.side_effect = [_ % 10 for _ in range(200)]

        x = an.AccountNumberGeneratorRandom(**self.kwargs)

        account_number = x._get_next_number()
        self.assertEqual(account_number, '1012345678901234')

        account_number = x._get_next_number()
        self.assertEqual(account_number, '2256789012345678')

        account_number = x._get_next_number()
        self.assertEqual(account_number, '3339012345678901')

        account_number = x._get_next_number()
        self.assertEqual(account_number, '1234567890123456')


###############################################################################
# TEST AccountNumberGeneratorRandomLuhn
###############################################################################

class TestAccountNumberGeneratorRandomLuhn(unittest.TestCase):

    masker = an.AccountNumberMasker()
    prefixes = ('1', '22', '333')

    kwargs = {
        'length': 16,
        'bank_display_name': 'BDN',
        'bank_name': 'BN',
        'cvv_length': 3,
        'masker': masker,
        'routing_number': 'RN',
        'prefixes': prefixes,
    }

    @mock.patch(PATCH_RANDOM)
    def test_get_new_number(self, mock_random):

        mock_random.randint.side_effect = [_ % 10 for _ in range(200)]

        x = an.AccountNumberGeneratorRandomLuhn(**self.kwargs)

        # In our 'extected' account numbers we use a '#' as a placeholder
        # for the Luhn checksum, which the constructor will replace with the
        # real checksum.

        account_number = x.get_new_number()
        expected = an.AccountNumberLuhn('101234567890123#', 'BDN', 'BN', '235', '236', 3, self.masker, 'RN', False)
        self.assertEqual(account_number, expected)

        account_number = x.get_new_number()
        expected = an.AccountNumberLuhn('225678901234567#', 'BDN', 'BN', '679', '680', 3, self.masker, 'RN', False)
        self.assertEqual(account_number, expected)

        account_number = x.get_new_number()
        expected = an.AccountNumberLuhn('333901234567890#', 'BDN', 'BN', '909', '910', 3, self.masker, 'RN', False)
        self.assertEqual(account_number, expected)

        account_number = x.get_new_number()
        expected = an.AccountNumberLuhn('123456789012345#', 'BDN', 'BN', '452', '453', 3, self.masker, 'RN', False)
        self.assertEqual(account_number, expected)
