"""
Created on February 12, 2017

@author: John Jackson
"""

from abc import ABC, abstractmethod
from typing import cast, Optional, Tuple
import random

from kojak.core.test_logger import TestLogger
from kojak.core.utilities.string_library import plural
from kojak.core.utilities.luhn_algorithm import set_checksum


###############################################################################
# AccountNumber
###############################################################################


class AccountNumber:
    """
    This class represents a credit-card or bank account number and associated
    numbers, such as card verification value and routing number.

    Creates a new AccountNumber with the given values.  The method assigns
    the value of <b>cvv</b> plus one as the bad CVV.

    :param account_number: The account number to set.
    :param bank_display_name: An optional bank name to appear in your test
        log files.
    :param bank_name: An optional bank name that you might include
        in service requests.
    :param cvv: An optional card verification value; if you omit this
        parameter, the cvv is set to the last three digits of the
        account number.
    :param cvv_bad: The CVV to use when ``use_bad_cvv=True``; if you omit
        this parameter, the bad cvv is set to the value of cvv+1, wrapped
        to zero if necessary.
    :param cvv_length: An optional value specifying the length of the card
        verification value. If you also specify cvv then cvv_length
        is ignored.
    :param masker: An optional Masker that knows how to match the masked
        card number values that appear in your test log files.
    :param routing_number: An optional routing number to set.
    :param use_bad_cvv: If set to True, ``get_cvv()`` returns a bad CVV.
    """

    ###########################################################################
    # CONSTANTS - PUBLIC
    ###########################################################################

    # Defines the default length of the Card Verification Value, in digits.
    DEFAULT_CVV_LENGTH: int = 3

    ###########################################################################
    # METHODS
    ###########################################################################

    # =========================================================================
    # CONSTRUCTOR
    # =========================================================================

    def __init__(
            self, account_number: str,
            bank_display_name: Optional[str] = None,
            bank_name: Optional[str] = None,
            cvv: Optional[str] = None,
            cvv_bad: Optional[str] = None,
            cvv_length: int = -1,
            masker: Optional['AccountNumberMasker'] = None,
            routing_number: Optional[str] = None,
            use_bad_cvv: bool = False):

        # Holds the name of the bank associated with this account number;
        # this name is appropriate for logging in log files.
        self._bank_display_name: str = bank_display_name or ''

        # Holds the name of the bank associated with this account number; this
        # name is appropriate for identifying the bank in service requests.
        self._bank_name: str = bank_name or ''

        # Holds the account number.
        self._account_number: str = account_number or ''

        # Holds the card validation value associated with this account number.
        self._cvv: str = cvv or ''

        # Holds an incorrect card validation value associated with this
        # account number.
        self._cvv_bad: str = cvv_bad or ''

        # Holds the length of the card validation value associated with this
        # account number.
        self._cvv_length: int = len(self._cvv) if len(self._cvv) > 0\
            else cvv_length if cvv_length >= 0\
            else self.DEFAULT_CVV_LENGTH\
            if len(self._account_number) > self.DEFAULT_CVV_LENGTH \
            else len(self._account_number)

        # Holds the AccountNumberMasker that knows how to mask the account
        # number.  For PCI compliance you must mask account numbers that appear
        #  in log files and this masker knows how to mimic what appears in your
        #  test log files.
        self._masker: AccountNumberMasker = masker

        # Holds the routing number; this applies to bank accounts rather than
        # card accounts.
        self._routing_number: str = routing_number or ''

        # Determines whether method ``get_cvv()`` should return good or bad
        # card verification values.
        self._use_bad_cvv: bool = use_bad_cvv

        # Calculate a cvv if no cvv was given explicitly.
        if len(self._cvv) == 0:
            if self._cvv_length <= 0:
                pass
            elif len(self._account_number) <= self._cvv_length:
                self._cvv = self._account_number
            else:
                start = len(self._account_number)-self._cvv_length
                self._cvv = self._account_number[start:]

        # Set the final value of _cvv, _cvv_length, and _cvv_bad.
        self.set_cvv(self._cvv, self._cvv_bad)

    # =========================================================================
    # __str__
    # =========================================================================

    def __str__(self):
        return (
            "{}: account_number='{}' "
            "bank_display_name='{}' bank_name='{}' "
            "cvv='{}' cvv_bad='{}' cvv_length={} "
            "masker={} routing_number='{}' use_bad_cvv={}".format(
                type(self).__name__, self._account_number,
                self._bank_display_name, self._bank_name,
                self._cvv, self._cvv_bad, self._cvv_length,
                '(' + str(self._masker) + ')' if self._masker else None,
                self._routing_number,
                self._use_bad_cvv))

    # =========================================================================
    # __repr__
    # =========================================================================

    def __repr__(self):
        return (
            "{}('{}', '{}', '{}', '{}', '{}', {}, {}, '{}', {})".format(
                type(self).__name__, self._account_number,
                self._bank_display_name, self._bank_name, self._cvv,
                self._cvv_bad, self._cvv_length,
                repr(self._masker), self._routing_number, self._use_bad_cvv))

    # =========================================================================
    # __eq__
    # =========================================================================

    def __eq__(self, other):
        if not isinstance(other, AccountNumber):
            return NotImplemented

        other = cast(AccountNumber, other)
        return \
            self._account_number == other._account_number \
            and self._bank_display_name == other._bank_display_name \
            and self._bank_name == other._bank_name \
            and self._cvv == other._cvv \
            and self._cvv_bad == other._cvv_bad \
            and self._cvv_length == other._cvv_length \
            and self._masker == other._masker \
            and self._routing_number == other._routing_number

    # =========================================================================
    # copy
    # =========================================================================

    def copy(self) -> 'AccountNumber':
        """
        Creates a copy of this AccountNumber.
        """

        return AccountNumber(
            account_number=self._account_number,
            bank_display_name=self._bank_display_name,
            bank_name=self._bank_name,
            cvv=self._cvv,
            cvv_bad=self._cvv_bad,
            cvv_length=self._cvv_length,
            masker=self._masker,
            routing_number=self._routing_number,
            use_bad_cvv=self._use_bad_cvv
        )

    # =========================================================================
    # get_account_number
    # =========================================================================

    def get_account_number(self) -> str:
        """
        Returns the account number.
        """

        return self._account_number

    # =========================================================================
    # get_bank_display_name
    # =========================================================================

    def get_bank_display_name(self) -> str:
        """
        Returns the name of the bank associated with this account number;
        this name should be appropriate for logging in log files.
        """

        return self._bank_display_name

    # =========================================================================
    # get_bank_name
    # =========================================================================

    def get_bank_name(self) -> str:
        """
        Returns the name of the bank associated with this account number; this
        name should be appropriate for identifying the bank in service
        requests.
        """

        return self._bank_name

    # =========================================================================
    # get_cvv
    # =========================================================================

    def get_cvv(self) -> str:
        """
        Returns the card validation value associated with this account number.
        However, if you have previously called ``use_bad_cvv`` with True
        then the method returns an incorrect card validation value.
        By default, the CVV value is set to the last three digits of the
        account number.
        """

        return self._cvv_bad if self._use_bad_cvv else self._cvv

    # =========================================================================
    # get_cvv_bad
    # =========================================================================

    def get_cvv_bad(self) -> str:
        """
        Returns an incorrect card validation value associated with this
        account number.
        """

        return self._cvv_bad

    # =========================================================================
    # get_cvv_length
    # =========================================================================

    def get_cvv_length(self) -> int:
        """
        Returns the length of the card validation value associated with this
        account number.
        """

        return self._cvv_length

    # =========================================================================
    # get_last_n
    # =========================================================================

    def get_last_n(self, n: int) -> str:
        """
        Returns the last N digits of the account number.

        :param n: The number of digits to return.
        :return: A string containing the last N digits of the account number.
        """

        n = 0 if n < 0 else n
        return self._account_number \
            if len(self._account_number) < n \
            else self._account_number[
                 len(self._account_number) - n:]

    # =========================================================================
    # get_masked_number
    # =========================================================================

    def get_masked_number(self) -> str:
        """
        Returns the account number masked according to the rules of this
        AccountNumber's masker. If this AccountNumber has no masker, the
        method returns the account number.
        """

        return self._account_number \
            if self._masker is None \
            else self._masker.mask_number(self._account_number)

    # =========================================================================
    # get_masker
    # =========================================================================

    def get_masker(self) -> 'AccountNumberMasker':
        """
        Returns the AccountNumberMasker associated with this AccountNumber.
        For PCI compliance you must mask account numbers that appear in log
        files and this masker knows how to mimic what appears in your test
        log files.
        """

        return self._masker

    # =========================================================================
    # get_routing_number
    # =========================================================================

    def get_routing_number(self) -> str:
        """
        Returns the routing number.
        """

        return self._routing_number

    # =========================================================================
    # _normalize_cvv
    # =========================================================================

    @staticmethod
    def _normalize_cvv(cvv: str, length: int) -> str:
        """
        Returns the given CVV normalized to the given length. If the length
        of the given CVV < **length**, then zeroes are prepended to make it the
        given **length**. If the length of the given CVV > **length** then the
        given cvv is truncated to the last **length** characters of the
        given **cvv**.

        :param cvv: The CVV to normalize.
        :param length: The desired length of the normalized CVV.
        :return: The normalized CVV.
        """

        if len(cvv) < length:
            # Zerofill to the correct length.
            return ('0' * (length - len(cvv))) + cvv
        elif len(cvv) > length:
            # Handles case where '999', for example, increments to '1000'
            return cvv[len(cvv) - length:]
        else:
            return cvv

    # =========================================================================
    # set_account_number
    # =========================================================================

    def set_account_number(self, account_number: str) -> None:
        """
        Sets the account number and calls ``set_cvv()`` with the last N digits
        of the account number where N is the cvv length established at the
        AccountNumber's construction.
        """

        self._account_number = account_number
        cvv: str = account_number \
            if len(account_number) <= self._cvv_length\
            else account_number[
                 len(account_number)-self._cvv_length:]
        self.set_cvv(cvv)

    # =========================================================================
    # set_cvv
    # =========================================================================

    def set_cvv(self, cvv: str, cvv_bad: str = '') -> None:
        """
        Sets the card validation value associated with this account number as
        well as the incorrect card validation value. The incorrect CVV is set
        to the value of the correct CVV plus 1 (wrapping to zero if necessary.)
        However, if you specify a null, blank, or non-numeric CVV then the
        incorrect CVV is set to null.

        :param cvv: The CVV value to set.
        :param cvv_bad: The bad CVV value to set, or the empty string to set
            the default CVV value, which is the CVV value plus one, wrapped
            to zero if necessary.
        """

        cvv_length: int = len(cvv)
        cvv_bad_length: int = len(cvv_bad)
        if cvv_length > 0 and cvv_bad_length == 0:
            cvv = self._normalize_cvv(cvv, cvv_length)
            try:
                # cvv_bad = cvv + 1
                cvv_bad = self._normalize_cvv(str(int(cvv) + 1), cvv_length)
            except ValueError:
                TestLogger().warn(
                    "Exception encountered trying to create the bad CVV "
                    "for '%s'".format(cvv))

        self._cvv = cvv
        self._cvv_bad = cvv_bad
        self._cvv_length = cvv_length

    # =========================================================================
    # set_routing_number
    # =========================================================================

    def set_routing_number(self, routing_number: str) -> None:
        """
        Sets the routing number.
        :param routing_number: The routing number to set.
        """

        self._routing_number = routing_number

    # =========================================================================
    # use_bad_cvv
    # =========================================================================

    def use_bad_cvv(self, use_bad_cvv: bool) -> None:
        """
        Sets whether ``get_cvv()`` returns the correct or an incorrect card
        verification value.  This condition is set False by default.

        :param use_bad_cvv: The condition to set; true instructs ``get_cvv()``
        to return a bad CVV value.
        """

        self._use_bad_cvv = use_bad_cvv


###############################################################################
# AccountNumberLuhn
###############################################################################


class AccountNumberLuhn(AccountNumber):
    """
    This class represents a credit-card or bank account number and associated
    numbers, such as card verification value and routing number, where the
    account number must pass the LUHN check.

    Creates a new AccountNumberLuhn with the given values.  The method assigns
    the value of <b>cvv</b> plus one as the bad CVV.

    :param account_number: The account number to set. You must supply all
        digits including a stand-in for the LUHN checksum; the constructor
        will recalculate the checksum.
    :param bank_display_name: An optional bank name to appear in your test
        log files.
    :param bank_name: An optional bank name that you might include
        in service requests.
    :param cvv: An optional card verification value; if you omit this
        parameter, the cvv is set to the last three digits of the
        account number.
    :param cvv_bad: The CVV to use when ``use_bad_cvv=True``; if you omit
        this parameter, the bad cvv is set to the value of cvv+1, wrapped
        to zero if necessary.
    :param cvv_length: An optional value specifying the length of the card
        verification value. If you also specify cvv then cvv_length
        is ignored.
    :param masker: An optional Masker that knows how to match the masked
        card number values that appear in your test log files.
    :param routing_number: An optional routing number to set.
    :param use_bad_cvv: If set to True, ``get_cvv()`` returns a bad CVV.
    """

    ###########################################################################
    # METHODS
    ###########################################################################

    # =========================================================================
    # CONSTRUCTOR
    # =========================================================================

    def __init__(
            self, account_number: str,
            bank_display_name: Optional[str] = None,
            bank_name: Optional[str] = None,
            cvv: Optional[str] = None,
            cvv_bad: Optional[str] = None,
            cvv_length: int = -1,
            masker: Optional['AccountNumberMasker'] = None,
            routing_number: Optional[str] = None,
            use_bad_cvv: bool = False):
        super().__init__(
            set_checksum(account_number), bank_display_name, bank_name,
            cvv, cvv_bad, cvv_length, masker, routing_number, use_bad_cvv)


###############################################################################
# AccountNumberMasker
###############################################################################


class AccountNumberMasker:
    """
    This class contains specific instructions on how to mask an account number.
    For PCI compliance, you need to mask account numbers that appear in log
    files. You create a subclass to provide specific instructions on how the
    AccountNumber class should generate masked account numbers that match your
    log files so that your log files can be verified.
    """

    ###########################################################################
    # METHODS
    ###########################################################################

    # =========================================================================
    # CONSTRUCTOR
    # =========================================================================

    def __init__(self, first_m: int=4, last_n: int=4, mask_character: str='*'):
        """
        Creates a new AccountNumberMasker that leaves the specified first M
        and last N digits clear.

        :param first_m: The count of leading digits to leave in clear text;
            the default is 4.
        :param last_n: The count of trailing digits to leave in clear text;
            the default is 4.
        :param mask_character: The character to use for masking the middle
            digits; the default is '*'.
        """

        self._first_m: int = first_m if first_m >= 0 else 0
        self._last_n: int = last_n if last_n >= 0 else 0
        self._mask_character: str = mask_character\
            if len(mask_character) == 1\
            else '*' if len(mask_character) == 0\
            else mask_character[0]

    # =========================================================================
    # __str__
    # =========================================================================

    def __str__(self):
        return (
            "{}: first_m={} last_n={} mask_character='{}'".format(
                type(self).__name__, self._first_m, self._last_n,
                self._mask_character
            ))

    # =========================================================================
    # __repr__
    # =========================================================================

    def __repr__(self):
        return (
            "{}({}, {}, '{}')".format(
                type(self).__name__, self._first_m, self._last_n,
                self._mask_character
            ))

    # =========================================================================
    # __eq__
    # =========================================================================

    def __eq__(self, other):
        if not isinstance(other, AccountNumberMasker):
            return NotImplemented

        other = cast(AccountNumberMasker, other)
        return self._first_m == other._first_m \
            and self._last_n == other._last_n \
            and self._mask_character == other._mask_character

    # =========================================================================
    # mask_number
    # =========================================================================

    def mask_number(self, number: str) -> str:
        """
        Returns a masked version of the specified number according to the
        criteria provided in the constructor. If the number is null or its
        length is <= **firstM+lastN** then the number is returned as-is.

        If your log files mask numbers using this straight-forward technique
        then your subclass can use this method to mask your numbers.

        :param number: The number to mask.
        :return: The masked number.
        """

        if len(number) <= self._first_m + self._last_n:
            return number

        mask_length: int = len(number) - self._first_m - self._last_n
        return number[:self._first_m]\
            + (self._mask_character * mask_length)\
            + number[len(number)-self._last_n:]


###############################################################################
# AccountNumberGenerator
###############################################################################


class AccountNumberGenerator(ABC):
    """
    This base class generates a random AccountNumber using rules
    that a subclass provides.
    """

    ###########################################################################
    # METHODS
    ###########################################################################

    # =========================================================================
    # get_new_number
    # =========================================================================

    @abstractmethod
    def get_new_number(self) -> AccountNumber:
        """
        Returns an account number based on the rules of the subclass.
        """

        raise NotImplementedError()


###############################################################################
# AccountNumberGeneratorFixed
###############################################################################


class AccountNumberGeneratorFixed(AccountNumberGenerator):
    """
    This class returns an AccountNumber, round robin, from a fixed list
    of account numbers.

    :param numbers: The list of account numbers to draw from.
    """

    ###########################################################################
    # METHODS
    ###########################################################################

    # =========================================================================
    # CONSTRUCTOR
    # =========================================================================

    def __init__(self, numbers: Tuple[AccountNumber, ...]):

        assert numbers, 'You must provide at least one account number'

        self._numbers = numbers

        # Each time the class returns a number, the class selects the next
        # number from the list of numbers using round-robin selection. This
        # variable keeps track of the next number to select.
        self._next_number: int = 0

    # =========================================================================
    # __str__
    # =========================================================================

    def __str__(self):
        """
        Returns a description of this account number generator.
        """

        entries = plural(len(self._numbers), '', 'number', 'numbers')
        return "{}: {} starting with '{}'".format(
            type(self).__name__, entries,
            self._numbers[0].get_account_number())

    # =========================================================================
    # get_new_number
    # =========================================================================

    def get_new_number(self) -> Optional[AccountNumber]:
        """
        Returns the next number in the round-robin sequence.
        Will return None if the pool happens to be empty.
        """

        if self._numbers:
            number = self._numbers[self._next_number]
            self._next_number += 1
            if self._next_number >= len(self._numbers):
                self._next_number = 0
            return number

        return None


###############################################################################
# AccountNumberGeneratorRandom
###############################################################################


class AccountNumberGeneratorRandom(AccountNumberGenerator):
    """
    This class generates a random AccountNumber.

    :param length: The final length of the account number.
    :param bank_display_name: Specifies the name of the bank associated
        with this account number; this name is appropriate for logging
        in log files.
    :param bank_name: Specifies name of the bank associated with this
        account number; this name is appropriate for identifying the bank
        in service requests.
    :param cvv_length: The length of the CVV.
    :param masker: Specifies the AccountNumberMasker that knows how to mask
        the account number. For PCI compliance you must mask account
        numbers that appear in log files and this masker knows how
        to mimic what appears in your test log files.
    :param routing_number: Specifies the routing number.
    :param prefixes: A tuple of prefixes that start account numbers.
    """

    ###########################################################################
    # METHODS
    ###########################################################################

    # =========================================================================
    # CONSTRUCTOR
    # =========================================================================

    def __init__(
            self, length: int,
            bank_display_name: Optional[str],
            bank_name: Optional[str],
            cvv_length: int,
            masker: Optional[AccountNumberMasker],
            routing_number: Optional[str],
            prefixes: Tuple[str, ...],
    ):

        assert length > 0, 'You must provide a length > 0'
        assert prefixes, 'You must provide at least one prefix'

        self._length: int = length
        self._bank_display_name: str = bank_display_name
        self._bank_name: str = bank_name
        self._cvv_length: int = cvv_length
        self._masker: AccountNumberMasker = masker
        self._routing_number: str = routing_number
        self._prefixes: Tuple[str, ...] = prefixes

        # Each time the class returns a number, the class selects the next
        # prefix from the list of prefixes using round-robin selection. This
        # variable keeps track of the next prefix to select.
        self._next_prefix: int = 0

    # =========================================================================
    # __str__
    # =========================================================================

    def __str__(self):
        """
        Returns a description of this account number generator.
        """

        entries = plural(len(self._prefixes), '', 'prefix', 'prefixes')
        return "{}: {} starting with '{}'".format(
            type(self).__name__, entries, self._prefixes[0])

    # =========================================================================
    # get_new_number
    # =========================================================================

    def get_new_number(self) -> AccountNumber:
        """
        Returns a random account number.
        """

        return AccountNumber(
            account_number=self._get_next_number(),
            bank_display_name=self._bank_display_name,
            bank_name=self._bank_name,
            cvv_length=self._cvv_length,
            masker=self._masker,
            routing_number=self._routing_number)

    # =========================================================================
    # _get_next_number
    # =========================================================================

    def _get_next_number(self) -> str:
        """
        Returns the next account number in the sequence.
        """

        account_number = self._prefixes[self._next_prefix]
        self._next_prefix += 1
        if self._next_prefix >= len(self._prefixes):
            self._next_prefix = 0
        # Append random digits until we are at the required length.
        while len(account_number) < self._length:
            account_number += str(random.randint(0, 9))
        return account_number


###############################################################################
# AccountNumberGeneratorRandomLuhn
###############################################################################


class AccountNumberGeneratorRandomLuhn(AccountNumberGeneratorRandom):
    """
    This class generates a random Luhn AccountNumber.

    :param length: The final length of the account number.
    :param bank_display_name: Specifies the name of the bank associated
        with this account number; this name is appropriate for logging
        in log files.
    :param bank_name: Specifies name of the bank associated with this
        account number; this name is appropriate for identifying the bank
        in service requests.
    :param cvv_length: The length of the CVV.
    :param masker: Specifies the AccountNumberMasker that knows how to mask
        the account number. For PCI compliance you must mask account
        numbers that appear in log files and this masker knows how
        to mimic what appears in your test log files.
    :param routing_number: Specifies the routing number.
    :param prefixes: A tuple of prefixes that start account numbers.
    """

    ###########################################################################
    # METHODS
    ###########################################################################

    # =========================================================================
    # CONSTRUCTOR
    # =========================================================================

    def __init__(
            self, length: int,
            bank_display_name: Optional[str],
            bank_name: Optional[str],
            cvv_length: int,
            masker: Optional[AccountNumberMasker],
            routing_number: Optional[str],
            prefixes: Tuple[str, ...],
    ):
        super().__init__(
            length, bank_display_name, bank_name, cvv_length, masker,
            routing_number, prefixes)

    # =========================================================================
    # get_new_number
    # =========================================================================

    def get_new_number(self) -> AccountNumberLuhn:
        """
        Returns a random Luhn account number.
        """

        return AccountNumberLuhn(
            account_number=self._get_next_number(),
            bank_display_name=self._bank_display_name,
            bank_name=self._bank_name,
            cvv_length=self._cvv_length,
            masker=self._masker,
            routing_number=self._routing_number)
